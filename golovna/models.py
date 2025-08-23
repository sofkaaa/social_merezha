from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class UserProfile(models.Model):
    us = models.OneToOneField(User, on_delete= models.CASCADE)

    ava = models.ImageField(upload_to="ava/", blank=True, null=True)
    bio = models.TextField(blank=True, null= True)

    friends = models.ManyToManyField("self", blank=True)

    def __str__ (self):
        return self.us.username 

class Post(models.Model):
    content = models.TextField(blank=True)

    image = models.ImageField(upload_to='post/image/', blank=True, null= True)
    video = models.FileField(upload_to="post/video/", blank=True, null= True)
    link = models.URLField( blank=True, null=True)

    time = models.DateTimeField(auto_now_add=True)

    us = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_posts")

    like = models.ManyToManyField(User, blank=True, related_name="favorite_posts")
    favorite = models.ManyToManyField(User, blank=True, related_name="liked_posts" )

class Comment(models.Model):
    post = models.ForeignKey(Post , on_delete=models.CASCADE)
    content = models.TextField()
    time = models.DateField(auto_now_add=True)
    us = models.ForeignKey(User, on_delete=models.CASCADE)

    #Відповідь на чийсь комент.
    vid = models.ForeignKey("self", null = True, blank= True, on_delete=models.CASCADE)

    def is_reply(self):
        return self.vid is not None
    
class Event(models.Model):
    name = models.CharField(max_length=250)
    #Oпис
    bescription = models.TextField()
    data = models.DateTimeField()
    
    member = models.ManyToManyField(User,blank=True)

    def __str__(self):
        return self.name 


class Group(models.Model):
    name = models.CharField(max_length=250)
    bio = models.TextField(blank=True, null= True)

    time = models.DateField(auto_now_add=True)

    ava = models.ImageField(upload_to="group/ava/", blank=True, null=True)

    member = models.ManyToManyField(User,blank=True)

    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='owned_groups')

    def __str__(self):
        return self.name 
    
