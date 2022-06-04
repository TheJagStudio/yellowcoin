from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import UserAccount
from django.contrib.auth.models import User
from accounts.models import stack


@login_required
def adduser(request):
    current_user = request.user
    user_account = UserAccount.objects.filter(user=current_user).first()
    allAccountTypes = ["Master One", "Master Two", "Master Three", "Master Four",
                       "Master Five", "Master Six", "Master Seven", "Broker", "Tele Master", "User"]
    accountTypes = []
    x = 0
    for accounts in allAccountTypes:
        if accounts == user_account.Account_Type or x == 1:
            if x == 1:
                accountTypes.append(accounts)
            x = 1
    print(accountTypes)
    if user_account.Account_Type != "User":
        if (request.method == 'POST'):
            Username = request.POST.get('Username')
            Password = request.POST.get('Password')
            print(Username, Password)
            # create new user
            newDefualtUser = User.objects.create_user(Username, '', Password)
            newDefualtUser.save()
            Account_Code = request.POST.get('Account_Code')
            Account_Name = request.POST.get('Account_Name')
            Account_Type = request.POST.get('inputGroupSelect01')
            Partnership = request.POST.get('Partnership')
            Remarks = request.POST.get('Remarks')
            newUser = UserAccount(Account_Code=Account_Code, Account_Name=Account_Name,
                                  Account_Type=Account_Type, Partnership=Partnership, Remarks=Remarks, creator=current_user.username, user=newDefualtUser)
            newUser.save()
            print(newUser)
        return render(request, 'create_user.html', {'current_user': current_user, "accountTypes": accountTypes})


@login_required
def user_list(request):
    current_user = request.user
    user_account = UserAccount.objects.filter(user=current_user).first()
    if user_account.Account_Type != "User":
        user_list = UserAccount.objects.filter(
            creator=current_user.username).all()
        return render(request, 'user_list.html', {'current_user': current_user, 'user_list': user_list})
