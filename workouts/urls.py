from django.conf.urls import url

from . import views

app_name = 'workouts'
urlpatterns = [
  # e.g. /workouts
  url(r'^$', views.index, name='index'),
  # e.g. /base
  url(r'^base/$', views.base, name='base'),
  # e.g. /workouts/2
  url(r'^(?P<routine_id>[0-9]+)/$', views.detail, name='detail'),
  # e.g. /workouts/2/results
  url(r'^(?P<routine_id>[0-9]+)/results/$', views.results, name='results'),
  # e.g. /workouts/2/likes
  url(r'^(?P<routine_id>[0-9]+)/likes/$', views.like, name='like'),
  # e.g. /workouts/add/routine
  url(r'^add/routine/$', views.add_routine, name='add_routine'),
  # e.g. /workouts/2/add/exercise
  url(r'^(?P<routine_id>[0-9]+)/add/exercise/$', views.add_exercise, name='add_exercise'),
  # e.g. /workouts/2/like
  url(r'^(?P<routine_id>[0-9]+)/like/$', views.like, name='like'),

]
