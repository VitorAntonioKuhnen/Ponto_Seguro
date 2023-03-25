from django.db import models
from accounts.models import User
from django.utils import timezone

class Token(models.Model):
    codToken = models.CharField(max_length=6)
    usuario = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    datGer = models.DateField(auto_now_add=True)
    horGer = models.TimeField(auto_now_add=True)