from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import UserAccount
from django.contrib.auth.models import User


@login_required
def adduser(request):
    current_user = request.user
    if current_user.is_superuser:
        if (request.method == 'POST'):
            Username = request.POST.get('Username')
            Password = request.POST.get('password')
            # create new user
            newDefualtUser = User.objects.create_user(Username, '', Password)
            newDefualtUser.save()
            Account_Code = request.POST.get('Account_Code')
            Account_Name = request.POST.get('Account_Name')
            Account_Type = request.POST.get('inputGroupSelect01')
            Card_Type = request.POST.get('flexRadioDefault1')
            Card_Number = request.POST.get('Card_Number')
            Partnership = request.POST.get('Partnership')
            Remarks = request.POST.get('Remarks')
            newUser = UserAccount(Account_Code=Account_Code, Account_Name=Account_Name, Account_Type=Account_Type,
                                  Card_Type=Card_Type, Card_Number=Card_Number, Partnership=Partnership, Remarks=Remarks, user=newDefualtUser)
            newUser.save()
            print(newUser)
        return render(request, 'create_user.html', {'current_user': current_user})


@login_required
def user_list(request):
    current_user = request.user
    if current_user.is_superuser:
        user_list = UserAccount.objects.all()
        return render(request, 'user_list.html', {'current_user': current_user, 'user_list': user_list})
