from django.db import models
# Create your models here.

class Stuff(models.Model):
    name = models.CharField(max_length=20)
    def __str__(self):
        return self.name

class MyUser(models.Model):
    name = models.CharField(max_length=20)
    password = models.CharField(max_length=20)