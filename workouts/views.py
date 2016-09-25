from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.db.models import F
from django.urls import reverse
from django.utils import timezone

from .models import Routine, User

# Create your views here.
def base(request):
  return render(request, 'workouts/base.html')

def index(request):
  latest_routine_list = Routine.objects.order_by('-pub_date')[:10]
  context = {'routine_list': latest_routine_list}
  return render(request, 'workouts/index.html', context)

def results(request, routine_id):
  response = "You're looking at the results of routine %s."
  return HttpResponse(response % routine_id)

def like(request, routine_id):
  routine = get_object_or_404(Routine, pk=routine_id)
  user_list = User.objects.all()
  if request.method == "POST":
    if request.POST["user_id"]:
      user_id = request.POST["user_id"]
      user = get_object_or_404(User, pk=user_id)
      user.user_routine_set.create(user=user, routine=routine)
      print (user.user_routine_set.all())
    routine.likes = F('likes') + 1
    routine.save()
    return HttpResponseRedirect(reverse('workouts:detail', args=[routine_id]))
  else:
    return render(request, 'workouts/like.html', {
      'routine':routine,
      'list': user_list,
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

def sort_by_likes(request):
  highest_likes_routine_list = Routine.objects.order_by('-likes')[:10]
  context = {'routine_list': highest_likes_routine_list}
  return render(request, 'workouts/index.html', context)

def trending(request):
  trending_list = Routine.objects.order_by('-pub_date')[:10]
  context = {'routine_list': trending_list}
  return render(request, 'workouts/index.html', context)
  
def user(request):
  user_list = User.objects.all()
  context = {'list': user_list}
  return render(request, 'workouts/user.html', context)

def user_detail(request, user_id):
  user = get_object_or_404(User, pk=user_id)
  if request.method == 'POST':
    user.delete()
    return HttpResponseRedirect(reverse('workouts:user'))
  else:
    return render(request, 'workouts/user_detail.html', {
    'user': user,
  })


def follow_user(request, user_id):
  user = get_object_or_404(User, pk=user_id)
  user_list = User.objects.all()
  currently_following = user.follower.values_list("user", flat=True)
  #print (currently_following)
  currently_following_all = user.follower.all()
  if request.method == 'POST':
    new_following_ids = request.POST.getlist('follow')
    # compare current following to new list
    # if current following is in new list, do nothing
    # if current following isn't part of new list, remove it
    # if any new list isn't in current following, add it 
    for current_user in currently_following_all:
      if str(current_user.id) not in new_following_ids:
        #print ("delete" + str(current_user.id))
        current_user.delete()
    for new_id in new_following_ids:
      if int(new_id) not in user.follower.values_list("id", flat=True):
        #print ("add" + new_id)
        user.follower.create(user=get_object_or_404(User, pk=int(new_id)), 
                             follower=user,
                             create_date=timezone.now())
        
    return HttpResponseRedirect(reverse('workouts:user'))
  else:
    # TODO replace with Django forms
    return render(request, 'workouts/follow_user.html', {
      'list': user_list,
      'current_following': currently_following,
    })

def add_user(request):
  if request.method == 'GET':
    return render(request, 'workouts/add_user.html')
  elif request.method == 'POST' and request.POST['username']:
    username = request.POST['username']
    user = User(username=username, create_date=timezone.now())
    user.save()
    return HttpResponseRedirect(reverse('workouts:user'))
  else:
    return render(request, 'workouts/add_user.html', {
      'error_message': "You didn't enter a name",
    })
