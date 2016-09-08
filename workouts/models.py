from django.db import models
from django.utils import timezone

import datetime

# Create your models here.
class Exercise(models.Model):
  exercise_text = models.CharField(max_length=200)
  pub_date = models.DateTimeField('date published')
  likes = models.IntegerField(default=0)
  def was_published_recently(self):
    return self.pub_date >= timezone.now() - datetime.timedelta(days=1)
  def __str__(self):
    return self.exercise_text


class Routine(models.Model):
  routine_text = models.CharField(max_length=200)
  pub_date = models.DateTimeField('date published')
  likes = models.IntegerField(default=0)
  exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
  def __str__(self):
    return self.routine_text
  

class Comment(models.Model):
  exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
  comment_text = models.CharField(max_length=200)
  pub_date = models.DateTimeField('date published')
  likes = models.IntegerField(default=0)
  def __str__(self):
    self.comment_text
