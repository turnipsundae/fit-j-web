from django.conf.urls import url

from . import views

app_name = 'workouts'
urlpatterns = [
  # e.g. /workouts
  url(r'^$', views.index, name='index'),
  # e.g. /workouts/login
  url(r'^login/$', views.login, name='login'),
  # e.g. /workouts/logout
  url(r'^logout/$', views.logout, name='logout'),
  # e.g. /workouts/sign_up
  url(r'^sign_up/$', views.sign_up, name='sign_up'),
  # e.g. /workouts/trending
  url(r'^trending/$', views.trending, name='trending'),
  # e.g. /workouts/profile
  url(r'^profile/$', views.profile, name='profile'),
  # e.g. /workouts/journal
  url(r'^journal/$', views.journal, name='journal'),
  # e.g. /workouts/user
  url(r'^user/$', views.user, name='user'),
  # e.g. /workouts/user/2
  url(r'^user/(?P<user_id>[0-9]+)/$', views.user_detail, name='user_detail'),
  # e.g. /workouts/user/2/follow
  url(r'^user/(?P<user_id>[0-9]+)/follow/$', views.follow_user, name='follow_user'),
  # e.g. /workouts/2
  url(r'^(?P<routine_id>[0-9]+)/$', views.detail, name='detail'),
  # e.g. /workouts/2/edit
  url(r'^(?P<routine_id>[0-9]+)/edit/$', views.edit_routine, name='edit_routine'),
  # e.g. /workouts/2/customize
  url(r'^(?P<routine_id>[0-9]+)/customize/$', views.customize_routine, name='customize_routine'),
  # e.g. /workouts/2/results
  url(r'^(?P<routine_id>[0-9]+)/results/$', views.results, name='results'),
  # e.g. /workouts/add/routine
  url(r'^add/routine/$', views.add_routine, name='add_routine'),
  # e.g. /workouts/2/add/exercise
  url(r'^(?P<routine_id>[0-9]+)/add/exercise/$', views.add_exercise, name='add_exercise'),
  # e.g. /workouts/sort_by_likes
  url(r'^sort_by_likes/$', views.sort_by_likes, name='sort_by_likes'),

]
