from django.contrib import admin
from .models import Stuff, MyUser
# Register your models here.
admin.site.register(Stuff)
admin.site.register(MyUser)