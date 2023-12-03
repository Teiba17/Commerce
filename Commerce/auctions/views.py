from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from .models import *
import os
from .forms import ImageForm
from django.contrib.auth.decorators import login_required


def index(request):
    # Get all active auctions and bids
    return render(request, "auctions/index.html",{
        "listing" : auctions_listing.objects.filter(active = True),
        "bids" : bids.objects.all()
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")



# Define a view for auction item page
@login_required
def item(request, auct_id) :

    # Get the auction and the logged in user
    auction = auctions_listing.objects.get(pk=auct_id)
    user = request.user

    # Check if the auction is on the user's watchlist
    on_watchlist = watch_list.objects.filter(user=user, auct=auction).exists()

    # Set owner and winner flags
    owner = False
    winner = False

    if request.method == "GET" :

        # Get the highest bid for the auction
        high = bids.objects.get(pk=auct_id)
        if high.price ==None :
            high.price = 0

        # Check if the logged in user is the owner or winner of the auction
        if  request.user == auction.owner :
            owner = True
        if auction.active == False and request.user == auction.winner :
            winner = True

        # Render the item page with auction details, comments, and flags
        return render(request, "auctions/item.html",{
            "auction" : auction,
            "comments" : Comments.objects.filter(auct = auction),
            'on_watchlist': on_watchlist,
            "current" : high.price,
            "T" : owner,
            "winner" : winner
        })

    else :
        # get and add the new bid
        bid = request.POST["bid"]
        add_bid = bids(pk = auct_id, price = int(bid), user = user)
        auction.current = int(bid)
        auction.winner = user
        auction.save()
        add_bid.save()

        # return to the item page
        return HttpResponseRedirect(reverse('item', args=[auct_id]))






@login_required
def add(request) :
    if request.method == 'POST':
        # get all the item's details and save it
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            name = request.POST['name']
            price = request.POST['price']
            det = request.POST["det"]
            con = request.POST["contact"]
            cata0 = request.POST["cata"]

            cata = Category.objects.get(id=cata0)

            auction1 = auctions_listing(name= name.capitalize() , price= float(price),
                                         det=det, con = con, category = cata, owner = request.user)
            auction1.save()
            # for now I set the bid for the item equal to the price
            add_bid = bids(auction = auction1, price=float(price), user = request.user )
            add_bid.save()

            image = form.cleaned_data['image']
            #rename the image
            image.name = str(auction1.id)
            p = Image(image = image, auct = auction1)
            p.save()

            # return to th active list page
            return HttpResponseRedirect(reverse("index"))
    else:
        #render the add page
        form = ImageForm()
        cata = Category.objects.all()
        return render(request, "auctions/add.html", {'form': form ,
            'cata' : cata
            })

@login_required
def watch (request):
    if request.method == 'GET':
        # render the watchlist page
        items =  watch_list.objects.filter(user = request.user)
        return render(request, "auctions/watch.html", {
            "items" : items
        })
@login_required
def add_watch(request, auct_id):
    # Get the auction and the logged in user
    auction = auctions_listing.objects.get(pk=auct_id)
    user = request.user

    if watch_list.objects.filter(user=user, auct=auction).exists():
        # Auction is already on user's watchlist, remove it
        watchlist_item = watch_list.objects.get(user=user, auct=auction)
        watchlist_item.delete()
    else:
        # Auction is not on user's watchlist, add it
        watchlist_item = watch_list(user=user, auct=auction)
        watchlist_item.save()
    return HttpResponseRedirect(reverse('item', args=[auct_id]))



def category(request) :
    # Get all the categories
    allc = Category.objects.all()
    if request.method == "POST" :
        # finding the auctions with the needed category
        cateid = request.POST["cate"]
        cate = Category.objects.get(pk = cateid)
        aucts = auctions_listing.objects.filter(category = cate)
        return render(request, "auctions/category.html", {
                    "aucts" : aucts ,
                    "allc" : allc ,
                })
    else :
         return render(request, "auctions/category.html", {
             "allc" : allc
         })




def add_cate(request) :
    # add a category
    if request.method == "POST" :
        cate_name = request.POST["name"]

        # check if it is alreay exists
        if Category.objects.filter(name = cate_name).exists() :
            return HttpResponse('<h1>Category already exists, go back and add new category</h1>')
        else:
            cate = Category(name = cate_name)
            cate.save()
            return HttpResponseRedirect(reverse("add"))



def add_com(request, auct_id) :
    # add comments
    if request.method == 'POST' :
        # Get the user and the auction
        user = request.user
        auction = auctions_listing.objects.get(pk = auct_id)
        tex1 = request.POST["com"]
        comment = Comments(auct = auction, user = user, text = tex1)
        comment.save()
        return HttpResponseRedirect(reverse('item', args=[auct_id]))



def close(request, auct_id) :
    #close the auction
    auction = auctions_listing.objects.get(pk = auct_id)
    bid = bids.objects.get(auction = auction)

    auction.winner = bid.user
    auction.active = False
    auction.save()
    return HttpResponseRedirect(reverse("index"))



def all(request) :
    # render all the auctions that the user owns
    auctions = auctions_listing.objects.filter(owner = request.user)
    return render(request, "auctions/my_auctions.html", {
        "auctions" : auctions })


