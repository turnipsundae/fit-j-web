from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.utils import timezone

from .models import Routine

# Create your views here.
def index(request):
  latest_routine_list = Routine.objects.order_by('-pub_date')[:5]
  context = {'latest_routine_list': latest_routine_list}
  return render(request, 'workouts/index.html', context)

def results(request, routine_id):
  response = "You're looking at the results of routine %s."
  return HttpResponse(response % routine_id)

def like(request, routine_id):
  return HttpResponse("You're adding a +1 to routine %s." % routine_id)

def detail(request, routine_id):
  routine = get_object_or_404(Routine, pk=routine_id)
  return render(request, 'workouts/detail.html', {'routine': routine})

def new_routine(request):
  try:
    new_routine = request.POST['new_routine']
  except (KeyError, Routine.DoesNotExist):
    return render(request, 'workouts/new_routine.html')
  else:
    r = Routine(routine_text=new_routine, pub_date=timezone.now())
    r.save()
    return HttpResponseRedirect(reverse('workouts:index'))
