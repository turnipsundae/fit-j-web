from django.conf.urls import url

from . import views

app_name = 'routines'
urlpatterns = [
  # e.g. /routines
  url(r'^$', views.index, name='index'),
]
