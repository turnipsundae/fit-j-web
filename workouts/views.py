from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.db.models import F
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth import authenticate
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import login as auth_login
from django.contrib.auth.models import User 
from django.contrib.auth.decorators import login_required

from .models import Routine, Comment, Journal
import re

# Create your views here.
def base(request):
  return render(request, 'workouts/base.html')

def index(request):
  latest_routine_list = Routine.objects.order_by('-pub_date')[:10]
  context = {'routine_list': latest_routine_list}
  return render(request, 'workouts/index.html', context)

def login(request):
  if request.method == "POST":
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
      auth_login(request, user)
      return render(request, "workouts/index.html") 
    else:
      # return an 'invalid login' error message
      return render(request, "workouts/login.html", {
        "error_message" : "Username and password did not match",
        "username" : username,
        })
  else:
    return render(request, 'workouts/login.html')

def logout(request):
  auth_logout(request)
  return render(request, "workouts/logout.html")

def profile(request):
  if not request.user.is_authenticated:
    return HttpResponseRedirect(reverse('workouts:login'))
  else:
    return render(request, "workouts/profile.html") 

def sign_up(request):
  if request.method == "POST":
    first_name = request.POST['first_name']
    last_name = request.POST['last_name']
    email = request.POST['email']
    password = request.POST['password']

    # TODO validate fields

    user = User(first_name = first_name,
                last_name = last_name,
                email = email,
                username = email,
                password = password)
    user.save()
    return HttpResponse("New user successfully created!")
  else:
    return render(request, "workouts/sign_up.html")

@login_required(login_url="/workouts/login/")
def journal(request):
  journal = Journal.objects.filter(user=request.user)
  return render(request, "workouts/journal.html", {
    'journal' : journal,
    })

def results(request, routine_id):
  response = "You're looking at the results of routine %s."
  return HttpResponse(response % routine_id)

def like(request, routine_id):
  """
  routine = get_object_or_404(Routine, pk=routine_id)
  user_list = User.objects.all()
  if request.method == "POST":
    if "user_id" in request.POST:
      user_id = request.POST["user_id"]
      user = get_object_or_404(User, pk=user_id)
      user.user_routine_set.create(user=user, routine=routine)
    routine.likes = F('likes') + 1
    routine.save()
    return HttpResponseRedirect(reverse('workouts:detail', args=[routine_id]))
  else:
    return render(request, 'workouts/like.html', {
      'routine':routine,
      'list': user_list,
    })
  """
  return HttpResponse("Yiou liked this page")

def detail(request, routine_id):
  routine = get_object_or_404(Routine, pk=routine_id)
  if request.method == 'POST':
    routine.delete()
    return HttpResponseRedirect(reverse('workouts:index'))
  else:
    return render(request, 'workouts/detail.html', {
      'routine': routine,
    })

@login_required(login_url="/workouts/login/")
def add_to_journal(request, routine_id):
  routine = get_object_or_404(Routine, pk=routine_id)
  if request.method == 'POST':
    entry = Journal(user=request.user, routine=routine)
    entry.save()
    return HttpResponseRedirect(reverse('workouts:index'))
  else:
    return render(request, "workouts/add_to_journal.html", {
      'routine' : routine, 
      })

def parse_exercises(exercises):
	return exercises.split("\r\n")

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{6,20}$")
def valid_username(username):
    return username and USER_RE.match(username)

PASS_RE = re.compile(r"^.{6,20}$")
def valid_password(password):
    return password and PASS_RE.match(password)

EMAIL_RE  = re.compile(r'^[\S]+@[\S]+\.[\S]+$')
def valid_email(email):
    return not email or EMAIL_RE.match(email)

CONTENT_RE = re.compile(r'^[\S0-9]{2,}')
def valid_content_input(content):
  return content and CONTENT_RE.match(content)

def add_routine(request):
  if request.method == 'POST':
    error_exists = False
    routine_title = request.POST['routine_title']
    routine_text = request.POST['routine_text']
    params = dict(routine_title=routine_title,
                  routine_text=routine_text)
    # TODO validate inputs 
    if not valid_content_input(routine_title):
      error_exists = True
      params['error_title'] = "Please enter a title"
    if not valid_content_input(routine_text):
      error_exists = True
      params['error_text'] = "Please enter the details"
    if error_exists:
      return render(request, 'workouts/add_routine.html', params)
    r = Routine(routine_title=routine_title, routine_text=routine_text, 
                pub_date=timezone.now())
    r.save()
    return HttpResponseRedirect(reverse('workouts:index'))
  else:
    return render(request, 'workouts/add_routine.html')

def edit_routine(request, routine_id):
  routine = get_object_or_404(Routine, pk=routine_id)
  if request.method == 'POST':
    # TODO validate inputs 
    error_exists = False
    routine_title = request.POST['routine_title']
    routine_text = request.POST['routine_text']
    params = dict(routine_title=routine_title,
                  routine_text=routine_text)
    if not valid_content_input(routine_title):
      error_exists = True
      params['error_title'] = "Please enter a title"
    if not valid_content_input(routine_text):
      error_exists = True
      params['error_text'] = "Please enter the details"
    if error_exists:
      return render(request, 'workouts/edit_routine.html', params)
    routine.routine_title = routine_title
    routine.routine_text = routine_text
    routine.save()
    return HttpResponseRedirect(reverse('workouts:detail', args=[routine_id]))
  else:
    return render(request, "workouts/edit_routine.html", {
      'routine_title': routine.routine_title,
      'routine_text': routine.routine_text,
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
  """
  user = get_object_or_404(User, pk=user_id)
  if request.method == 'POST':
    user.delete()
    return HttpResponseRedirect(reverse('workouts:user'))
  else:
    comments = user.comment_set.all()
    output_list = []
    for comment in comments:
      for comment_routine in comment.comment_routine_set.all():
        output_list.append(comment_routine)
    return render(request, 'workouts/user_detail.html', {
    'user': user,
    'output_list': output_list,
  })
  """
  return HttpResponse("This is the user_detail page")


def follow_user(request, user_id):
  """
  user = get_object_or_404(User, pk=user_id)
  user_list = User.objects.all()
  currently_following = user.follower.values_list("user", flat=True)
  currently_following_all = user.follower.all()
  if request.method == 'POST':
    new_following_ids = request.POST.getlist('follow')
    # compare current following to new list
    # if current following is in new list, do nothing
    # if current following isn't part of new list, remove it
    # if any new list isn't in current following, add it 
    for current_user in currently_following_all:
      if str(current_user.id) not in new_following_ids:
        current_user.delete()

    for new_id in new_following_ids:
      if int(new_id) not in user.follower.values_list("id", flat=True):
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
  """
  return HttpResponse("This is the follow a new user page")

def add_user(request):
  """
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
  """
  return HttpResponse("This is the add user page")

def comment(request, routine_id):
  """
  routine = get_object_or_404(Routine, pk=routine_id)
  user_list = User.objects.all()
  if request.method == "POST":
    if "user_id" in request.POST and "comment" in request.POST:
      user_id = request.POST["user_id"]
      user = User.objects.filter(pk=user_id).get()
      comment_text = request.POST["comment"]
      comment = Comment(user=user, comment_text=comment_text, pub_date=timezone.now())
      comment.save()
      routine.comment_routine_set.create(routine=routine, comment=comment) 
    
    #return HttpResponseRedirect(reverse("workouts:detail", args=[routine_id]))
    return HttpResponseRedirect(reverse('workouts:detail', args=[routine_id]))
  else:
    return render(request, 'workouts/comment.html', {
      'routine': routine,
      'list': user_list,
    })
  """
  return HttpResponse("This is the comment page")
