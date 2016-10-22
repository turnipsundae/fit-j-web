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
