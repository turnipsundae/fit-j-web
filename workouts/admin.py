from django.contrib import admin

from .models import Routine, Exercise, Comment, User, Follower

# Register your models here.

admin.site.register(Routine)
admin.site.register(Exercise)
admin.site.register(Comment)
admin.site.register(User)
admin.site.register(Follower)
