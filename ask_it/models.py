from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import math

# Create your models here.


class QuestionImage(models.Model):
    caption = models.TextField(blank = True, null = True)
    cover = models.ImageField(upload_to='images/')

    def __str__(self):
        return self.caption

class Ask_it(models.Model):
  question = models.CharField(max_length = 255)
  message = models.TextField(blank = True, null = True)
  author = models.ForeignKey(User, on_delete=models.CASCADE)
  image_caption = models.TextField(blank = True, null = True)
  image = models.ImageField(upload_to='images/', blank = True, null = True)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  upvotes = models.IntegerField(default = 1)
  cookies = models.IntegerField(default = 0)

  def __str__(self):
    return self.question

  def whenpublished(self):
    now = timezone.now()
      
    diff= now - self.created_at

    if diff.days == 0 and diff.seconds >= 0 and diff.seconds < 60:
      seconds= diff.seconds
      
      if seconds == 1:
        return str(seconds) +  " second ago"
      else:
        return str(seconds) + " seconds ago"
        
        
    if diff.days == 0 and diff.seconds >= 60 and diff.seconds < 3600:
      minutes= math.floor(diff.seconds/60)

      if minutes == 1:
        return str(minutes) + " minute ago"
      else:
        return str(minutes) + " minutes ago"


    if diff.days == 0 and diff.seconds >= 3600 and diff.seconds < 86400:
      hours= math.floor(diff.seconds/3600)

      if hours == 1:
        return str(hours) + " hour ago"
      else:
        return str(hours) + " hours ago"

    # 1 day to 30 days
    if diff.days >= 1 and diff.days < 30:
      days= diff.days
    
      if days == 1:
        return str(days) + " day ago"

      else:
        return str(days) + " days ago"

    if diff.days >= 30 and diff.days < 365:
      months= math.floor(diff.days/30)

      if months == 1:
        return str(months) + " month ago"
      else:
        return str(months) + " months ago"

    if diff.days >= 365:
      years= math.floor(diff.days/365)

      if years == 1:
        return str(years) + " year ago"
      else:
        return str(years) + " years ago"

class Reply(models.Model):
  author = models.ForeignKey(User, on_delete=models.CASCADE)
  parent = models.ForeignKey(Ask_it, on_delete=models.CASCADE)
  message = models.TextField()
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  upvotes = models.IntegerField(default = 1)
  cookies = models.IntegerField(default = 0)

  def __str__(self):
    return str(self.parent) + " " + self.message
  
  def whenpublished(self):
    now = timezone.now()
      
    diff= now - self.created_at

    if diff.days == 0 and diff.seconds >= 0 and diff.seconds < 60:
      seconds= diff.seconds
      
      if seconds == 1:
        return str(seconds) +  " second ago"
      else:
        return str(seconds) + " seconds ago"
        
        
    if diff.days == 0 and diff.seconds >= 60 and diff.seconds < 3600:
      minutes= math.floor(diff.seconds/60)

      if minutes == 1:
        return str(minutes) + " minute ago"
      else:
        return str(minutes) + " minutes ago"


    if diff.days == 0 and diff.seconds >= 3600 and diff.seconds < 86400:
      hours= math.floor(diff.seconds/3600)

      if hours == 1:
        return str(hours) + " hour ago"
      else:
        return str(hours) + " hours ago"

    # 1 day to 30 days
    if diff.days >= 1 and diff.days < 30:
      days= diff.days
    
      if days == 1:
        return str(days) + " day ago"

      else:
        return str(days) + " days ago"

    if diff.days >= 30 and diff.days < 365:
      months= math.floor(diff.days/30)

      if months == 1:
        return str(months) + " month ago"
      else:
        return str(months) + " months ago"

    if diff.days >= 365:
      years= math.floor(diff.days/365)

      if years == 1:
        return str(years) + " year ago"
      else:
        return str(years) + " years ago"

class Cookie_jar(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE)
  cookies = models.IntegerField(default = 10)

  def __str__(self):
    return str(self.user)

class Upvoted(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  upvoted_questions = models.ForeignKey(Ask_it,on_delete=models.CASCADE,blank=True,null=True)
  upvoted_reply =  models.ForeignKey(Reply,on_delete=models.CASCADE,blank=True,null=True)


  def __str__(self):
    return str(self.user)

