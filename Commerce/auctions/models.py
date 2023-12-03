from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Category(models.Model):
    name = models.CharField(max_length=100)


class auctions_listing(models.Model) :
    name = models.CharField(max_length=200)
    price = models.IntegerField(default=None)
    date = models.DateTimeField(auto_now_add=True)
    det = models.TextField(max_length=500, default=None)
    con = models.TextField(max_length=500, default=None)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=None)
    watchers = models.ManyToManyField(User, related_name="watched_auctions", blank=True)
    current = models.IntegerField(blank=True, null=True)
    winner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="auction_winner" ,blank=True, null=True)
    active = models.BooleanField(default= True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)



    class Meta:
        verbose_name= "Auctions_list"


class bids(models.Model) :
    auction = models.OneToOneField(auctions_listing, on_delete=models.CASCADE, primary_key=True)
    price = models.IntegerField(default=None, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    class Meta:
        verbose_name = "Bid"



class Comments(models.Model) :
    auct = models.ForeignKey(auctions_listing, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.CharField(max_length=500)

    class Meta:
        verbose_name_plural = "Comments"


class Image(models.Model):
    image = models.ImageField(upload_to='images/')
    auct = models.ForeignKey(auctions_listing, on_delete=models.CASCADE, default=None)
    uploaded_at = models.DateTimeField(auto_now_add=True)


class watch_list(models.Model) :
    auct = models.ForeignKey(auctions_listing, on_delete=models.CASCADE, default=None)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    added_time = models.DateTimeField(auto_now_add=True)


