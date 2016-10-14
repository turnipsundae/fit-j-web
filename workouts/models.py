from django.db import models
from django.utils import timezone
from django.conf import settings

import datetime

# Create your models here.
class Routine(models.Model):
  routine_title = models.CharField(max_length=70)
  routine_text = models.TextField()
  pub_date = models.DateTimeField('date published')
  created_by = models.ForeignKey(settings.AUTH_USER_MODEL)
  likes = models.IntegerField(default=0)
  def __str__(self):
    return self.routine_title
  

class Exercise(models.Model):
  routine = models.ForeignKey(Routine, on_delete=models.CASCADE)
  exercise_text = models.CharField(max_length=200)
  pub_date = models.DateTimeField('date published')
  likes = models.IntegerField(default=0)
  def was_published_recently(self):
    return self.pub_date >= timezone.now() - datetime.timedelta(days=1)
  def __str__(self):
    return self.exercise_text


class Comment(models.Model):
  created_by = models.ForeignKey(settings.AUTH_USER_MODEL)
  routine = models.ForeignKey(Routine, on_delete=models.CASCADE)
  comment_text = models.CharField(max_length=200)
  pub_date = models.DateTimeField('date published')
  likes = models.IntegerField(default=0)
  def __str__(self):
    return self.comment_text


class Tag(models.Model):
  routine = models.ForeignKey(Routine, on_delete=models.CASCADE)
  tag_text = models.CharField(max_length=70)
  def __str__(self):
    return self.tag_text


class Comment_Routine(models.Model):
  routine = models.ForeignKey(Routine, on_delete=models.CASCADE)
  comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
  def __str__(self):
    return self.comment.comment_text


class Follower(models.Model):
  # user = models.ForeignKey(User, related_name="user")
  user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="user")
  follower = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="follower")
  create_date = models.DateTimeField('date created')
  def __str__(self):
    return self.user.username

class Journal(models.Model):
  user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
  routine = models.ForeignKey(Routine, on_delete=models.CASCADE)
  def __str__(self):
    return self.routine.routine_title
