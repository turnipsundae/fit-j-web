from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.utils import timezone

from .models import Routine

# Create your views here.
def index(request):
  latest_routine_list = Routine.objects.order_by('-pub_date')[:10]
  context = {'latest_routine_list': latest_routine_list}
  return render(request, 'workouts/index.html', context)

def results(request, routine_id):
  response = "You're looking at the results of routine %s."
  return HttpResponse(response % routine_id)

def like(request, routine_id):
  return HttpResponse("You're adding a +1 to routine %s." % routine_id)

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

def add_routine(request):
  if request.method == 'GET':
    return render(request, 'workouts/add_routine.html')
  elif request.method == 'POST' and request.POST['add_routine']:
    add_routine = request.POST['add_routine']
    r = Routine(routine_text=add_routine, pub_date=timezone.now())
    r.save()
    return HttpResponseRedirect(reverse('workouts:index'))
  else:
    return render(request, 'workouts/add_routine.html', {
      'error_message': "You didn't enter a name"
    })

def add_exercise(request, routine_id):
  if request.method == 'GET':
    return render(request, 'workouts/add_exercise.html')
  elif request.method == 'POST' and request.POST['add_exercise']:
    add_exercise = request.POST['add_exercise']
    routine = get_object_or_404(Routine, pk=routine_id)
    routine.exercise_set.create(exercise_text=add_exercise, pub_date=timezone.now())
    return HttpResponseRedirect(reverse('workouts:detail', args=[routine_id]))
  else:
    return render(request, 'workouts/add_exercise.html', {
      'error_message': "You didn't enter a name"
    })
