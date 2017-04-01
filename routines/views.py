from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.db.models import F
from django.urls import reverse

from .models import Workout, User, Comment, Result


# Create your views here.
def index(request):
    # params = {'workout_title': 'Fran',
    #           'workout_description': '21-15-9 Pull Ups Thrusters 95#', 
    #           'workout_results_best_male': '4:30', 
    #           'workout_results_avg_male': '5:30',
    #           'workout_results_worst_male': '7:30',
    #           'workout_results_best_female': '5:55',
    #           'workout_results_avg_female': '7:30',
    #           'workout_results_worst_female': '10:00'}
    workout = get_object_or_404(Workout, id=1)
    params = {'workout': workout}
    return render(request, 'routines/index_dynamic.html', params)
    # return render(request, 'index.html')


def db(request):

    greeting = Greeting()
    greeting.save()

    greetings = Greeting.objects.all()

    greetings_str = "\n".join([str(greeting.when) for greeting in greetings])
    return HttpResponse(greetings_str)
