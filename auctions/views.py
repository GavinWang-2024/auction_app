from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render,get_object_or_404
from django.urls import reverse

from .models import User,Listing,Bid,Comment,Category


def index(request):
    activeListings=Listing.objects.filter(isActive=True)
    allCategories=Category.objects.all()
    return render(request, "auctions/index.html",{
        "activeListings":activeListings,
        "categories":allCategories,
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

def createListing(request):
    if request.method=="GET":
        allCategories=Category.objects.all()
        return render(request,"auctions/create.html",{
            "allCategories":allCategories,
        })
    else:
        title=request.POST['title']
        description=request.POST['description']
        imageUrl=request.POST['imageurl']
        price=request.POST['price']
        category=request.POST['category']
        currentUser=request.user
        
        categoryData=Category.objects.get(categoryName=category)
        bid=Bid(bid=int(price),user=currentUser)
        bid.save()
        a=Listing(
            title=title,
            description=description,
            imageUrl=imageUrl,
            price=bid,
            category=categoryData,
            owner=currentUser,
        )
        a.save()
        return HttpResponseRedirect(reverse(index))

def listing(request,id):
    listingData=Listing.objects.get(pk=id)
    isListingInWatchlist=request.user in listingData.watchlist.all()
    allComments=Comment.objects.filter(listing=listingData)
    isOwner=request.user.username==listingData.owner.username
    return render(request,"auctions/listing.html",{
        "listingData":listingData,
        "isListingInWatchlist":isListingInWatchlist,
        "allComments":allComments,
        "isOwner":isOwner,
    })

def addWatchlist(request,id):
    listingData=Listing.objects.get(pk=id)
    currentUser=request.user
    listingData.watchlist.add(currentUser)
    return HttpResponseRedirect(reverse("listing",args=(id, )))

def removeWatchlist(request,id):
    listingData=Listing.objects.get(pk=id)
    currentUser=request.user
    listingData.watchlist.remove(currentUser)
    return HttpResponseRedirect(reverse("listing",args=(id, )))

def addBid(request,id):
    newBid=request.POST['newBid']
    listingData=Listing.objects.get(pk=id)
    isListingInWatchlist=request.user in listingData.watchlist.all()
    allComments=Comment.objects.filter(listing=listingData)
    isOwner=request.user.username==listingData.owner.username
    if int(newBid)>listingData.price.bid:
        updateBid=Bid(user=request.user,bid=int(newBid))
        updateBid.save()
        listingData.price=updateBid
        listingData.save()
        return render(request,"auctions/listing.html",{
            "listingData":listingData,   
            "message":"Bid was added successfully",
            "update":True,
            "isListingInWatchlist":isListingInWatchlist,
            "allComments":allComments,
            "isOwner":isOwner,
        })
    else:
        return render(request,"auctions/listing.html",{
            "listingData":listingData,   
            "message":"Failed",
            "update":False,
            "isListingInWatchlist":isListingInWatchlist,
            "allComments":allComments,
            "isOwner":isOwner,  
        })  

def close(request, id):
    listingData = Listing.objects.get(pk=id)
    listingData.isActive = False
    listingData.save()

    isListingInWatchlist = request.user in listingData.watchlist.all()
    allComments = Comment.objects.filter(listing=listingData)
    isOwner = request.user.username == listingData.owner.username
    isWinner = request.user.username == listingData.price.user.username

    return render(request, "auctions/listing.html", {
        "listingData": listingData,
        "isListingInWatchlist": isListingInWatchlist,
        "allComments": allComments,
        "isOwner": isOwner,
        "isWinner": isWinner,
        "update": True,
        "message": "Your auction has ended",
    })

def addComment(request,id):
    listingData=Listing.objects.get(pk=id)
    comment=request.POST['addComment']
    writer=request.user
    a=Comment(author=writer,message=comment,listing=listingData)
    a.save()
    return HttpResponseRedirect(reverse("listing",args=(id, )))

def displayWatchlist(request):
    currentUser=request.user
    listings=currentUser.listingWatchlist.all()
    return render(request,"auctions/watchlist.html",{
        "listings":listings
    })

def displayCategories(request):
    if request.method=="POST":
        categoryFromForm=request.POST['category']
        category=Category.objects.get(categoryName=categoryFromForm)
        activeListings=Listing.objects.filter(isActive=True,category=category)
        allCategories=Category.objects.all()
        return render(request,"auctions/index.html",{
            "activeListings":activeListings,
            "categories":allCategories,
        })