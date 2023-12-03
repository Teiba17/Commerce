from django.urls import path

from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("<int:auct_id>", views.item, name="item"),
    path("add", views.add, name="add"),
    path("watch", views.watch, name="watch"),
    path("add_watch/<int:auct_id>", views.add_watch, name="AW"),
    path("category", views.category, name="cate"),
    path("add_category", views.add_cate, name="add_cate"),
    path("add-comment/<int:auct_id>", views.add_com, name="add_com"),
    path("close/<int:auct_id>", views.close, name="close"),
    path("all", views.all, name="all")
    ]