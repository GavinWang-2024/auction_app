from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create",views.createListing,name="create"),
    path("listing/<int:id>",views.listing,name="listing"),
    path("addWatchlist/<int:id>",views.addWatchlist,name="addWatchlist"),
    path("removeWatchlist/<int:id>",views.removeWatchlist,name="removeWatchlist"),
    path("addBid/<int:id>",views.addBid,name="addBid"),
    path("close/<int:id>",views.close,name="close"),
    path("addComment/<int:id>",views.addComment,name="addComment"),
    path("displayWatchlist",views.displayWatchlist,name="displayWatchlist"),
    path("displayCategories",views.displayCategories,name="displayCategories"),
]
