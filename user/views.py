from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.shortcuts import render, redirect
from django.contrib import messages


def base(request):
    return render(request, 'user/base.html')


def signup(request):
    if request.method == "GET":
        return render(request, 'user/signup.html')
    elif request.method == "POST":
        # form = UserForm(request.POST)
        # if form.is_valid():
        #     new_user = models.User.objects.create_user(**form.cleaned_data)
        #     login(request, new_user)
        return redirect("/")



def userlogin(request):
    if request.method == "GET":
        loginForm = AuthenticationForm()
        return render(request, 'users/login.html', {'loginForm':loginForm})
    elif request.method == "POST":
        loginForm = AuthenticationForm(request, request.POST)
        if loginForm.is_valid():
            login(request, loginForm.get_user())
            return redirect('/base')
        else:
            return redirect('/users/login')

def userlogout(request):
    logout(request)
    return redirect('/base')
#
# @login_required(login_url='/users/login')
# def change_password(request):
#     if request.method == "GET":
#         password_change_form = PasswordChangeForm(request.user)
#         return render(request, 'users/change_password.html',
#                 {'password_change_form':password_change_form})
#
#     elif request.method == 'POST':
#         password_change_form = PasswordChangeForm(request.user, request.POST)
#
#         if password_change_form.is_valid():
#             user = password_change_form.save()
#             update_session_auth_hash(request, user)
#             return redirect('/base')
#         else:
#             return redirect('/users/change_password')
#
# @login_required(login_url='/users/login')
# def userdelete(request):
#     if request.method == 'POST':
#         request.user.delete()
#         return redirect('/base')
#     return render(request, 'users/userdelete.html')



