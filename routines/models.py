from django.db import models

# Create your models here.
class Greeting(models.Model):
    when = models.DateTimeField('date created', auto_now_add=True)

class Workout(Base):
  """Workout represents one WOD. May contain duplicates."""
  __tablename__ = 'workouts'

  title = models.CharField()
  description = models.TextField()
  results_best = models.CharField(null=True)
  results_worst = models.CharField(null=True)
  results_avg = models.CharField(null=True)
  results_best_male = models.CharField(null=True)
  results_worst_male = models.CharField(null=True)
  results_avg_male = models.CharField(null=True)
  results_best_female = models.CharField(null=True)
  results_worst_female = models.CharField(null=True)
  results_avg_female = models.CharField(null=True)

  def __repr__(self):
    return "<Workout(title='%s', description='%s')>" % (self.title, self.description)

class User(Base):
  """Users that leave comments for the workout."""
  __tablename__ = 'users'

  username = models.CharField() 

  def __repr__(self):
    return "<User(username='%s')>" % (self.username)

class Comment(Base):
  """Comments for each workout."""
  __tablename__ = 'comments'

  text = models.TextField()
  workout = models.ForeignKey(Workout, null=True)
  user = models.ForeignKey(User, null=True)

  def __repr__(self):
    return "<Comment(text='%s')>" % (self.text)


class Result(Base):
  """Result of a user performing a workout"""
  __tablename__ = 'results'

  workout = models.ForeignKey(Workout, null=True)
  comment = models.ForeignKey(Comment, null=True)
  user = models.ForeignKey(User, null=True)
  gender = models.CharField(null=True)
  age = models.IntegerField(null=True)
  height = models.CharField(null=True)
  weight = models.IntegerField(null=True)
  result = models.CharField(null=True)
  score = models.IntegerField(null=True)
  units = models.CharField(null=True)
  mods = models.CharField(null=True)

  def __repr__(self):
    return "<Result('%s %s')>" % (self.result, self.units)
