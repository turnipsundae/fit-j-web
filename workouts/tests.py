from django.test import TestCase
from django.utils import timezone
from django.db.models import F
from django.contrib.auth.models import User

from .models import Routine, Journal

import datetime

# Create your tests here.
class LikeMethodTests(TestCase):

  def setUp(self):
    u = User(first_name="John",
             last_name="Smith",
             email="jsmith@email.com",
             username="jsmith")
    u.save()
    r = Routine(routine_title="test", routine_text="test body", created_by=u)
    r.save()

  def test_like_increase_in_routine_equals_count_of_likes(self):
    """routine.likes should equal Like.filter.count"""
    u = User.objects.get(pk=1)
    r = Routine.objects.get(pk=1)

    # add 3 likes
    for x in range(0,3):
      u.like_set.create(routine=r)
      r.likes = F("likes") + 1
      r.save()

    # reload the object to show the DB update
    r = Routine.objects.get(pk=r.id)
    self.assertIs(r.likes, u.like_set.filter(routine=r).count())

    # subtract 3 likes
    for x in range(0,3):
      u.like_set.filter(routine=r)[0].delete()
      r.likes = F('likes') - 1
      r.save()

    # reload the object to show the DB update
    r = Routine.objects.filter(pk=r.id).get()
    self.assertIs(r.likes, u.like_set.filter(routine=r).count())

  def test_routine_complete_increase_equals_count_of_routine_results(self):
    """routine.completed_count should equal Results.filter.count"""
    u = User.objects.get(pk=1)
    r = Routine.objects.get(pk=1)
    je = u.journal_set.create(routine=r)

    # add 3 routine completions
    for x in range(0,3):
      je.results_set.create(results_text="Rx")
      je.completed_count = F('completed_count') + 1
      je.save()

    # reload the object to show the DB update
    je = Journal.objects.filter(user=u, routine=r).get()
    self.assertIs(je.completed_count, je.results_set.all().count())

    # subtract 3 likes
    for x in range(0,3):
      je.results_set.all()[0].delete()
      je.completed_count = F('completed_count') -1
      je.save()

    # reload the object to show the DB update
    je = Journal.objects.filter(user=u, routine=r).get()
    self.assertIs(je.completed_count, je.results_set.all().count())
