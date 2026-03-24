from django.db import models
from django.contrib.auth.models import User #me
import uuid #me
from datetime import datetime #me

# Create your models here.

class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) #this is used to show 1 to many relationships
    id_user = models.IntegerField(primary_key=True, default=0)
    bio = models.TextField(blank=True) #Profile has a bio variable
    profileimg = models.ImageField(upload_to='profile_images', default='default_img_2.jpg') #it will upload to this folder
    location = models.CharField(max_length=100, blank=True, default='')

    # register this model
    def __str__(self):
        return self.user.username
    

class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.CharField(max_length=100)
    image=models.ImageField(upload_to='post_images')
    caption=models.TextField()
    created_at=models.DateTimeField(default=datetime.now)
    no_of_likes=models.IntegerField(default=0)

    def __str__(self):
        return self.user
    

class LikePost(models.Model):
    post_id = models.CharField(max_length=500)
    username = models.CharField(max_length=100)

    def __str__(self):
        return self.username

    
class Followers(models.Model):
    follower = models.CharField(max_length=100)
    user = models.CharField(max_length=100)

    def __str__(self):
        return self.user