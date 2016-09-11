from django.test import TestCase
from django.utils import timezone

from .models import Routine

import datetime

# Create your tests here.
class RoutineMethodTests(TestCase):

  def test_was_routine_text_empty(self):
    """
    is_text_empty() should return True for text that is empty
    """
    pass
