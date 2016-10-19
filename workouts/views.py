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

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{6,20}$")
def valid_username(username):
  return username and USER_RE.match(username)

NAME_RE = re.compile(r'^[a-zA-Z]+([a-zA-Z-\'\s])*$')
def valid_name(name):
  return name and NAME_RE.match(name)

PASS_RE = re.compile(r"^.{6,20}$")
def valid_password(password):
    return password and PASS_RE.match(password)

EMAIL_RE  = re.compile(r'^[\S]+@[\S]+\.[\S]+$')
def valid_email(email):
    return email or EMAIL_RE.match(email)

CONTENT_RE = re.compile(r'^.|\n{1,1000}$')
def valid_content_input(content):
  return content and CONTENT_RE.match(content)

TAG_LIST_RE = re.compile(r'^([a-zA-Z0-9]{3,70}\s*)*$')
def valid_tag_list(tag_list):
  # TODO does not check for None since emtpy string should be allowed.
  #      return tag_list and TAG_LIST_RE.match(tag_list) gets a false with ''
  return TAG_LIST_RE.match(tag_list)

DIGIT_RE = re.compile(r'^[0-9]+$')
def valid_digit(num):
  return num and DIGIT_RE.match(num)

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
    error_exists = False
    params = dict(first_name=first_name, last_name=last_name, email=email)

    if not valid_name(first_name) or not valid_name(last_name):
      error_exists = True
      params['error_name'] = "Enter a first and last name using only letters, apostrophes and hyphens"
    if not valid_email(email):
      error_exists = True
      params['error_email'] = "Please enter in the format example@domain.com"
    if not valid_password(password):
      error_exists = True
      params['error_password'] = "Minimum password length is 6 characters"
    if error_exists:
      return render(request, "workouts/sign_up.html", params)

    user = User(first_name = first_name,
                last_name = last_name,
                email = email,
                username = email,
                password = password)
    user.save()
    return HttpResponse("New user successfully created!")
  else:
    return render(request, "workouts/sign_up.html")

@login_required()
def journal(request):
  # TODO get_object_or_404?
  journal = Journal.objects.filter(user=request.user)
  journal_planned = journal.filter(completed_count=0)
  journal_completed = journal.filter(completed_count__gt=0)

  params = dict(journal=journal, journal_planned=journal_planned, 
                journal_completed=journal_completed)

  if request.method == 'POST':
    if 'entry_id' in request.POST:
      error_exists = False
      entry_id = request.POST['entry_id']
      if not valid_digit(entry_id):
        error_exists = True
        params['error_entry_id'] = "The journal entry did not match any records"
      if error_exists:
        return render(request, 'workouts/journal.html', params)

      entry_id = int(entry_id)
      entry = get_object_or_404(Journal, user=request.user, pk=entry_id)

      if 'mark_complete' in request.POST:
        entry.completed_count = F('completed_count') + 1
        entry.completed_on = timezone.now()
        entry.save()
      if 'remove_from_journal' in request.POST:
        entry.delete()

  return render(request, "workouts/journal.html", {
    'journal_planned' : journal_planned,
    'journal_completed' : journal_completed,
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
  return HttpResponse("You liked this page")

def detail(request, routine_id):
  routine = get_object_or_404(Routine, pk=routine_id)
  if request.method == 'POST':
    if "delete_routine" in request.POST:
      if request.user.is_authenticated:
        if request.user != routine.created_by:
          return render(request, 'workouts/detail.html', { 'routine': routine, 'error_delete':"you aren't the creator of this routine"})
        routine.delete()
        return HttpResponseRedirect(reverse('workouts:index'))
    if "comment" in request.POST:
      if request.user.is_authenticated:
        comment_text = request.POST["comment_text"]
        params = dict(routine=routine, comment_text=comment_text)
        if not valid_content_input(comment_text):
          params['error_text'] = "Please enter the details"
          return render(request, 'workouts/detail.html', params)
        routine.comment_set.create(created_by=request.user,
                                   comment_text=comment_text,
                                   pub_date=timezone.now())
        return HttpResponseRedirect(reverse('workouts:detail', args=[routine.id]))
    # redirect anonymous users to login
    return HttpResponseRedirect(reverse('workouts:login'))
  else:
    tag_list = " ".join(routine.tag_set.values_list('tag_text', flat=True))
    return render(request, 'workouts/detail.html', {
      'routine': routine,
      'tag_list': tag_list,
    })

@login_required()
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


@login_required()
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
                pub_date=timezone.now(), created_by=request.user)
    r.save()
    return HttpResponseRedirect(reverse('workouts:index'))
  else:
    return render(request, 'workouts/add_routine.html')

@login_required()
def edit_routine(request, routine_id):
  routine = get_object_or_404(Routine, pk=routine_id)
  if request.user != routine.created_by:
    return HttpResponse("You're not the owner of this routine")
  if request.method == 'POST':
    # TODO validate inputs 
    error_exists = False
    routine_title = request.POST['routine_title']
    routine_text = request.POST['routine_text']
    tag_list = request.POST['tag_list']
    params = dict(routine_title=routine_title,
                  routine_text=routine_text,
                  tag_list=tag_list)
    if not valid_content_input(routine_title):
      error_exists = True
      params['error_title'] = "Please enter a title"
    if not valid_content_input(routine_text):
      error_exists = True
      params['error_text'] = "Please enter the details"
    if not valid_tag_list(tag_list):
      error_exists = True
      params['error_tag_list'] = "Please only use letters and numbers. Use spaces to separate tags."
    if error_exists:
      return render(request, 'workouts/edit_routine.html', params)
    routine.routine_title = routine_title
    routine.routine_text = routine_text
    routine.save()
    routine.tag_set.all().delete()
    # TODO ensure no duplicate tags
    [routine.tag_set.create(tag_text=tag_text) for tag_text in tag_list.split()]
    return HttpResponseRedirect(reverse('workouts:detail', args=[routine_id]))
  else:
    tag_list = " ".join(routine.tag_set.values_list('tag_text', flat=True))
    return render(request, "workouts/edit_routine.html", {
      'routine_title': routine.routine_title,
      'routine_text': routine.routine_text,
      'tag_list': tag_list,
      })

@login_required()
def customize_routine(request, routine_id):
  # if request.method == 'post':
  routine = get_object_or_404(Routine, pk=routine_id)
  if request.method == 'POST':
    error_exists = False
    routine_title = request.POST['routine_title']
    routine_text = request.POST['routine_text']
    tag_list = request.POST['tag_list']
    params = dict(routine_title=routine_title,
                  routine_text=routine_text,
                  tag_list=tag_list)
    if not valid_content_input(routine_title):
      error_exists = True
      params['error_title'] = "Please enter a title"
    if not valid_content_input(routine_text):
      error_exists = True
      params['error_text'] = "Please enter the details"
    if not valid_tag_list(tag_list):
      error_exists = True
      params['error_tag_list'] = "Please only use letters and numbers. Use spaces to separate tags."
    if error_exists:
      return render(request, 'workouts/edit_routine.html', params)
    # create copy of routine
    customized_routine = Routine(routine_title=routine_title,
                                 routine_text=routine_text,
                                 pub_date=timezone.now(),
                                 created_by=request.user)
    customized_routine.save()
    # TODO ensure no duplicate tags
    [customized_routine.tag_set.create(tag_text=tag_text) for tag_text in tag_list.split()]
    request.user.journal_set.create(routine=customized_routine)
    return HttpResponseRedirect(reverse('workouts:journal'))
  else:
    tag_list = " ".join(routine.tag_set.values_list('tag_text', flat=True))
    return render(request, "workouts/customize_routine.html", {
      'routine_title': routine.routine_title,
      'routine_text': routine.routine_text,
      'tag_list': tag_list,
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

@login_required()
def comment(request, routine_id):
  routine = get_object_or_404(Routine, pk=routine_id)
  if request.method == "POST":
    comment_text = request.POST["comment_text"]
    params = dict(routine_id=routine.id, comment_text=comment_text)
    if not valid_content_input(comment_text):
      params['error_text'] = "Please enter the details"
      return render(request, 'workouts/detail.html', params)
    routine.comment_set.create(created_by=request.user,
                               comment_text=comment_text,
                               pub_date=timezone.now())
    return HttpResponseRedirect(reverse('workouts:detail', args=[routine.id]))
  return HttpResponse("This is the comment page")
