from asyncio.windows_events import NULL
from tkinter import FIRST
from tracemalloc import start
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from datetime import date
from django.utils import timezone
# Create your models here.


class Users(models.Model):
    id = models.IntegerField(default=0)
    name = models.CharField(max_length=50)
    mobile = models.BigIntegerField(
        validators=[MaxValueValidator(9999999999)])
    email = models.EmailField(primary_key=True, max_length=50)
    password = models.CharField(max_length=50)
    gender = models.CharField(max_length=10)
    designation = models.CharField(max_length=20)
    department = models.CharField(max_length=50, null=True, default=NULL)
    add_date = models.DateField(default=timezone.now())

    def __str__(self):
        return self.name
    
    
class Departments(models.Model):
    id = models.AutoField(primary_key=True,validators=[MinValueValidator(100)])
    dept_name = models.CharField(max_length=50, unique=True)
    create_date = models.DateField(default=timezone.now())
