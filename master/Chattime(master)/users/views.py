from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages, auth




#유저 베이스 화면
from django.shortcuts import render, redirect


def base(request):
    return render(request, 'user/base.html')

@login_required
def dash(request):
    return render(request, 'master/dash.html')

def m_base(request):
    return render(request, 'master/base.html')

# 마스터 로그인
def userlogin(request):
    if request.method == "GET":
        loginForm = AuthenticationForm(request.GET)
        return render(request, 'user/login.html', {'loginForm':loginForm})
    if request.method == "POST":
        loginForm = AuthenticationForm(request, request.POST)
        if loginForm.is_valid():
            login(request, loginForm.get_user())
            return redirect('/base')
        else:
            messages.info(request,'다시 입력해주세요')
            return redirect('/login')

# 유저 로그아웃
@login_required
def userlogout(request):
    if request.method == "GET":
        auth.logout(request)
        messages.info(request, "Logged out successfully!")
        print("로그아웃되었습니다")
        return redirect('/')
