from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
  return HttpResponse("This is the index page for workouts.")

def results(request, routine_id):
  response = "You're looking at the results of routine %s."
  return HttpResponse(response % routine_id)

def like(request, routine_id):
  return HttpResponse("You're adding a +1 to routine %s." % routine_id)

def detail(request, routine_id):
  return HttpResponse("You're looking at the details for routine %s." % routine_id)
