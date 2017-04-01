from django.db import models

# Create your models here.
class Greeting(models.Model):
    when = models.DateTimeField('date created', auto_now_add=True)

class Workout(models.Model):
  """Workout represents one WOD. May contain duplicates."""
  __tablename__ = 'workouts'

  title = models.CharField(max_length=255)
  description = models.TextField()
  results_best = models.CharField(max_length=255, null=True)
  results_worst = models.CharField(max_length=255, null=True)
  results_avg = models.CharField(max_length=255, null=True)
  results_best_male = models.CharField(max_length=255, null=True)
  results_worst_male = models.CharField(max_length=255, null=True)
  results_avg_male = models.CharField(max_length=255, null=True)
  results_best_female = models.CharField(max_length=255, null=True)
  results_worst_female = models.CharField(max_length=255, null=True)
  results_avg_female = models.CharField(max_length=255, null=True)

  def __repr__(self):
    return "<Workout(title='%s', description='%s')>" % (self.title, self.description)

class User(models.Model):
  """Users that leave comments for the workout."""
  __tablename__ = 'users'

  username = models.CharField(max_length=255) 

  def __repr__(self):
    return "<User(username='%s')>" % (self.username)

class Comment(models.Model):
  """Comments for each workout."""
  __tablename__ = 'comments'

  text = models.TextField()
  workout = models.ForeignKey(Workout, null=True)
  user = models.ForeignKey(User, null=True)

  def __repr__(self):
    return "<Comment(text='%s')>" % (self.text)


class Result(models.Model):
  """Result of a user performing a workout"""
  __tablename__ = 'results'

  workout = models.ForeignKey(Workout, null=True)
  comment = models.ForeignKey(Comment, null=True)
  user = models.ForeignKey(User, null=True)
  gender = models.CharField(max_length=255, null=True)
  age = models.IntegerField(null=True)
  height = models.CharField(max_length=255, null=True)
  weight = models.IntegerField(null=True)
  result = models.CharField(max_length=255, null=True)
  score = models.IntegerField(null=True)
  units = models.CharField(max_length=255, null=True)
  mods = models.CharField(max_length=255, null=True)

  def __repr__(self):
    return "<Result('%s %s')>" % (self.result, self.units)
