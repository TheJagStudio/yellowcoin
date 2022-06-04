from django.db import models
from django.contrib.auth.models import User
    
class stack(models.Model):
    stocks = models.JSONField()
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    