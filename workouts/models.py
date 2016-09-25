from django.db import models
from django.utils import timezone

import datetime

# Create your models here.
class Routine(models.Model):
  routine_text = models.CharField(max_length=200)
  pub_date = models.DateTimeField('date published')
  likes = models.IntegerField(default=0)
  def __str__(self):
    return self.routine_text
  

class Exercise(models.Model):
  routine = models.ForeignKey(Routine, on_delete=models.CASCADE)
  exercise_text = models.CharField(max_length=200)
  pub_date = models.DateTimeField('date published')
  likes = models.IntegerField(default=0)
  def was_published_recently(self):
    return self.pub_date >= timezone.now() - datetime.timedelta(days=1)
  def __str__(self):
    return self.exercise_text


class User(models.Model):
  username = models.CharField(max_length=50)
  create_date = models.DateTimeField('date created')
  #followers = models.ForeignKey("self", null=True, blank=True, default=None)
  def count_followers(self):
    return Follower.objects.filter(user=self.id).count()
  def __str__(self):
    return self.username

class Comment(models.Model):
  #routine = models.ForeignKey(Routine, on_delete=models.CASCADE)
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  comment_text = models.CharField(max_length=200)
  pub_date = models.DateTimeField('date published')
  likes = models.IntegerField(default=0)
  def __str__(self):
    return self.comment_text


class Comment_Routine(models.Model):
  routine = models.ForeignKey(Routine, on_delete=models.CASCADE)
  comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
  def __str__(self):
    return self.comment.comment_text


class Follower(models.Model):
  user = models.ForeignKey(User, related_name="user")
  follower = models.ForeignKey(User, related_name="follower")
  create_date = models.DateTimeField('date created')
  def __str__(self):
    return self.user.username

class User_Routine(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  routine = models.ForeignKey(Routine, on_delete=models.CASCADE)
  def __str__(self):
    return self.routine.routine_text
