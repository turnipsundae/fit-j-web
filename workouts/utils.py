import re

# TODO move regex to a utils file
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

TITLE_RE = re.compile(r'^[a-zA-Z0-9]([a-zA-Z0-9_\-\'\s]){0,69}$')
def valid_title(title):
  return title and TITLE_RE.match(title)

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

def get_page_num(start, results_per_page=10):
  return int(start / results_per_page) + 1

def get_routine_form_params(request):
  routine_title = request.POST['routine_title']
  routine_text = request.POST['routine_text']
  tag_list = request.POST['tag_list']
  return dict(routine_title=routine_title,routine_text=routine_text,
              tag_list=tag_list, created_by=request.user)

def valid_routine_form(request):
  """Checks routine form for routine_title, routine_text, and tag_list. Returns tuple of an error check and params. Does not check for post method."""
  params = get_routine_form_params(request)
  error_exists = False
  if not valid_title(params['routine_title']):
    error_exists = True
    params['error_title'] = "Enter a title under 70 characters long. Only letters and numbers allowed."
  if not valid_content_input(params['routine_text']):
    error_exists = True
    params['error_text'] = "Enter details under 1000 characters long."
  if not valid_tag_list(params['tag_list']):
    error_exists = True
    params['error_tag_list'] = "Tags should be at least 3 characters long using only letters and numbers. Separate tags with a space."
  return (error_exists, params)
