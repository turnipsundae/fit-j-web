from django.shortcuts import render
from django.http import HttpResponse

from .models import Greeting


# Create your views here.
def index(request):
    return HttpResponse('Hello from Python!')
    # return render(request, 'index.html')


def db(request):

    greeting = Greeting()
    greeting.save()

    greetings = Greeting.objects.all()

    greetings_str = "\n".join([str(greeting.when) for greeting in greetings])
    return HttpResponse(greetings_str)
