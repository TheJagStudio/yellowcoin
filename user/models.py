from django.db import models
from django.contrib.auth.models import User


class UserAccount(models.Model):
    id = models.AutoField(primary_key=True)
    Account_Code = models.CharField(max_length=10)
    Account_Name = models.CharField(max_length=50)
    Account_Type = models.CharField(max_length=10)
    Card_Type = models.CharField(max_length=10)
    Card_Number = models.CharField(max_length=10)
    Partnership = models.CharField(max_length=100, default="YellowCoin")
    Remarks = models.CharField(max_length=10)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
