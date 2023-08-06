from asyncio.windows_events import NULL
from tkinter import FIRST
from django.db import models
from django.core.validators import MaxValueValidator
from datetime import date

from datetime import datetime
from django.utils import timezone
# Create your models here.


class Security(models.Model):
    id = models.AutoField(primary_key=True)
    w_id = models.IntegerField(default=1)
    name = models.CharField(max_length=50)
    age = models.CharField(max_length=10)
    gender = models.CharField(max_length=10)
    mobile = models.BigIntegerField(
        validators=[MaxValueValidator(9999999999)])
    aadhar = models.BigIntegerField(
        validators=[MaxValueValidator(99999999999999)])
    entry_date = models.DateField(default=timezone.now())
    entry_time = models.TimeField(default=datetime.now().strftime('%H:%M:%S'))
    exit_time = models.TimeField(null=True)

    def __str__(self):
        return self.name


class Supervisor(models.Model):
    id = models.IntegerField(primary_key=True)
    w_id = models.IntegerField(default=1)
    name = models.CharField(max_length=50)
    age = models.CharField(max_length=10)
    gender = models.CharField(max_length=10)
    mobile = models.BigIntegerField(
        validators=[MaxValueValidator(9999999999)])
    aadhar = models.BigIntegerField(
        validators=[MaxValueValidator(99999999999999)])
    department = models.CharField(max_length=20, default='')
    entry_date = models.DateField(auto_now_add=True)
    entry_time = models.TimeField(default=datetime.now().strftime('%H:%M:%S'))
    exit_time = models.TimeField(null=True)
    status = models.CharField(max_length=10, default='Request')

    def __str__(self):
        return self.name
