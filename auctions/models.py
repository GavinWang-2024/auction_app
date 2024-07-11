from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Bid(models.Model):
    bid=models.IntegerField()
    user=models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True,related_name="userBid")

class Category(models.Model):
    categoryName=models.CharField(max_length=50)

    def __str__(self):
        return self.categoryName

class Listing(models.Model):
    title=models.CharField(max_length=30)
    imageUrl=models.CharField(max_length=1000)
    price=models.ForeignKey(Bid,on_delete=models.CASCADE,null=True,blank=True,related_name="bidPrice")
    owner=models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True,related_name="user")
    category=models.ForeignKey(Category,on_delete=models.CASCADE,null=True,blank=True,related_name="category")
    watchlist=models.ManyToManyField(User,null=True,blank=True,related_name="listingWatchlist")
    isActive=models.BooleanField(default=True)
    description=models.CharField(max_length=300)

    def __str__(self):
        return self.title

class Comment(models.Model):
    author=models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True,related_name="userComment")
    message=models.CharField(max_length=200)
    listing=models.ForeignKey(Listing,on_delete=models.CASCADE,blank=True,null=True,related_name="listingComment")
    
    def __str__(self):
        return f"{self.author} comment on {self.listing}"
    
