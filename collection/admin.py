from django.contrib import admin
from .models import Collection, Pin, Comment

admin.site.register(Collection)
admin.site.register(Pin)
admin.site.register(Comment)