from django.contrib import admin
from .models import *

class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'content', 'password')

admin.site.register(Post, PostAdmin)
