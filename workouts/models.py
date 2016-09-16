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



class Comment(models.Model):
  routine = models.ForeignKey(Routine, on_delete=models.CASCADE)
  comment_text = models.CharField(max_length=200)
  pub_date = models.DateTimeField('date published')
  likes = models.IntegerField(default=0)
  def __str__(self):
    return self.comment_text

class User(models.Model):
  username = models.CharField(max_length=50)
  create_date = models.DateTimeField('date created')
  followers = models.ForeignKey("self", null=True, blank=True, default=None)
  def __str__(self):
    return self.username
