from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.db.models import F
from django.urls import reverse
from django.utils import timezone

from .models import Routine

# Create your views here.
def base(request):
  return render(request, 'workouts/base.html')

def index(request):
  latest_routine_list = Routine.objects.order_by('-pub_date')[:10]
  context = {'latest_routine_list': latest_routine_list}
  return render(request, 'workouts/index.html', context)

def results(request, routine_id):
  response = "You're looking at the results of routine %s."
  return HttpResponse(response % routine_id)

def like(request, routine_id):
  routine = get_object_or_404(Routine, pk=routine_id)
  if request.method == "POST":
    routine.likes = F('likes') + 1
    routine.save()
    return HttpResponseRedirect(reverse('workouts:detail', args=[routine_id]))
  else:
    return render(request, 'workouts/like.html', {
      'routine':routine,
    })

def detail(request, routine_id):
  routine = get_object_or_404(Routine, pk=routine_id)
  if request.method == 'POST':
    print (request.content_type, request.content_params)
    routine.delete()
    return HttpResponseRedirect(reverse('workouts:index'))
  else:
    return render(request, 'workouts/detail.html', {
      'routine': routine,
    })

def parse_exercises(exercises):
	return exercises.split("\r\n")

def add_routine(request):
  if request.method == 'GET':
    return render(request, 'workouts/add_routine.html')
  elif request.method == 'POST' and request.POST['routine_text']:
    routine_text = request.POST['routine_text']
    r = Routine(routine_text=routine_text, pub_date=timezone.now())
    r.save()
    if request.POST['exercise_text']:
      exercises = parse_exercises(request.POST['exercise_text'])
      for exercise in exercises:
        r.exercise_set.create(exercise_text=exercise, pub_date=timezone.now())
    return HttpResponseRedirect(reverse('workouts:index'))
  else:
    return render(request, 'workouts/add_routine.html', {
      'error_message': "You didn't enter a name"
    })

def add_exercise(request, routine_id):
  if request.method == 'GET':
    return render(request, 'workouts/add_exercise.html')
  elif request.method == 'POST' and request.POST['exercise_text']:
    exercises = parse_exercises(request.POST['exercise_text'])
    r = get_object_or_404(Routine, pk=routine_id)
    for exercise in exercises:
      r.exercise_set.create(exercise_text=exercise, pub_date=timezone.now())
    return HttpResponseRedirect(reverse('workouts:detail', args=[routine_id]))
  else:
    return render(request, 'workouts/add_exercise.html', {
      'error_message': "You didn't enter a name"
    })
