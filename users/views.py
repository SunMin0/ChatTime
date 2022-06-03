import webbrowser
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib import messages, auth
import requests
from django.shortcuts import render
from config.settings import SOCIAL_OUTH_CONFIG
from users.forms import SignupForm, UpdateUserForm, UpdateProfileForm, Signup_manager
from .forms import CheckPasswordForm
from django.shortcuts import redirect
from .models import CustomUser



#유저 베이스 화면
def base(request):
    return render(request, 'user/base.html')

def manager_base(request):
    return render(request, 'user/manager_base.html')


#유저 회원가입
def signup(request):
    if request.method == "GET":
        signupForm = SignupForm(request.GET)
        return render(request, 'user/signup.html', {'signupForm': signupForm})
    elif request.method == "POST":
        signupForm = SignupForm(request.POST)
        if signupForm.is_valid():
            if request.POST["password1"] == request.POST["password2"]:
                signupForm.save()
            return redirect('/')
        else:
            messages.info(request, '올바르지 않습니다.')
            return redirect('/signup')



#관리자 회원가입
def signup2(request):
    if request.method == "GET":
        signupForm = Signup_manager(request.GET)
        return render(request, 'user/signup_manager.html', {'signupForm': signupForm})
    elif request.method == "POST":
        signupForm = Signup_manager(request.POST)
        if signupForm.is_valid():
            if request.POST["password1"] == request.POST["password2"]:
                signupForm.save()
            return redirect('/')
        else:
            messages.info(request, '올바르지 않습니다.')
            return redirect('/signup_manager')


# 유저 로그인
def userlogin(request):
    if request.method == "GET":
        loginForm = AuthenticationForm(request.GET)
        return render(request, 'user/login.html', {'loginForm':loginForm})
    if request.method == "POST":
        loginForm = AuthenticationForm(request, request.POST)
        if loginForm.is_valid():
            login(request, loginForm.get_user())
            return redirect('/index')
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






##유저 비번 변경
@login_required
def change_password(request):
    if request.method == "GET":
        password_change_form = PasswordChangeForm(request.user)
        return render(request, 'user/change_password.html',
                {'password_change_form':password_change_form})

    elif request.method == 'POST':
        password_change_form = PasswordChangeForm(request.user, request.POST)

        if password_change_form.is_valid():
            user = password_change_form.save()
            update_session_auth_hash(request, user)
            return redirect('/profile')
        else:
            messages.info(request, '올바르지 않습니다.')
            return redirect('/password')




##프로필 변경
@login_required
def edit_profile(request):
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = UpdateProfileForm(request.POST, request.FILES, instance=request.user)
        print(profile_form)
        print(user_form)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile is updated successfully')
            return redirect('/profile')
    else:
        user_form = UpdateUserForm(instance=request.user)
        profile_form = UpdateProfileForm(instance=request.user)
    return render(request, 'user/edit_profile.html', {'user_form': user_form, 'profile_form': profile_form})


#유저 계정탈퇴
@login_required
def delete_user(request):
    if request.method == 'POST':
        password_form = CheckPasswordForm(request.user, request.POST)

        if password_form.is_valid():
            request.user.delete()
            logout(request)
            messages.success(request, "회원탈퇴가 완료되었습니다.")
            return redirect('/')
    else:
        password_form = CheckPasswordForm(request.user)

    return render(request, 'user/delete_user.html', {'password_form': password_form})
#



#카카오 계정과 서비스 같이 로그아웃
@login_required
def kakao_logout(request):
    """
    카카오톡과 함께 로그아웃 처리
    """
    kakao_rest_api_key = SOCIAL_OUTH_CONFIG['KAKAO_REST_API_KEY']
    print(kakao_rest_api_key)
    logout_redirect_uri = SOCIAL_OUTH_CONFIG['KAKAO_LOGOUT_URI']
    state = "none"
    kakao_service_logout_url = "https://kauth.kakao.com/oauth/logout"
    return redirect(f"{kakao_service_logout_url}?client_id={kakao_rest_api_key}&logout_redirect_uri={logout_redirect_uri}&state={state}")
    messages.info(request, "Logged out successfully!")




#카카오 로그인,받아오는 정보는 nickname,아이디, 이메일

def kakao_api(request):
    # return redirect('https://kauth.kakao.com/oauth/authorize?client_id=2194250ffa8fc89dad74efcab697bb7c&redirect_uri=http://127.0.0.1:8000/oauth&response_type=code')
    # 문자열로 하면 안받아옴 client_id = redierct_uri 이거 둘다 중요한것임.
    CLIENT_ID = SOCIAL_OUTH_CONFIG["KAKAO_REST_API_KEY"]
    print(CLIENT_ID)
    REDIRECT_URL = SOCIAL_OUTH_CONFIG["KAKAO_REDIRECT_URI"]
    print(REDIRECT_URL)
    url = "https://kauth.kakao.com/oauth/authorize?client_id={0}&redirect_uri={1}&response_type=code".format(
            CLIENT_ID, REDIRECT_URL)
    print(url)
    return redirect(url)

def kakao_api1(request):
    CLIENT_ID = SOCIAL_OUTH_CONFIG["KAKAO_REST_API_KEY"]
    REDIRECT_URI = SOCIAL_OUTH_CONFIG["KAKAO_REDIRECT_URI"]
    print(request.GET.get('code'))  # 인가코드 받아오는 애
    headers = {"Content-Type": "application/x-www-form-urlencoded"}  # h를
    data = {"grant_type": 'authorization_code',
            'client_id': CLIENT_ID,
            'redirect_uri': REDIRECT_URI,
            'code': request.GET.get('code')}  # 인가코드

    res = requests.post('https://kauth.kakao.com/oauth/token', data=data, headers=headers)

    token_json = res.json()
    access_token = token_json.get("access_token")
    profile_request = requests.get("https://kapi.kakao.com/v2/user/me",
                                   headers={"Authorization": f"Bearer {access_token}"}, )
    profile_json = profile_request.json()
    print(profile_json)

    kakao_id = profile_json.get("id")
    print(kakao_id)

    email = profile_json['kakao_account']['email']
    print(email)
    u_nickname = profile_json['properties']['nickname']
    print(u_nickname)

    if CustomUser.objects.filter(username=kakao_id).exists():
        user = CustomUser.objects.get(username=kakao_id)
        login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        return redirect('/index')
    else:
        CustomUser(username=kakao_id, email=email, u_nickname=u_nickname, is_active=True, login_method = 'K').save()
        CustomUser.objects.filter(username=kakao_id).exists()
        user = CustomUser.objects.get(username=kakao_id)
        login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        return redirect('/index')




#네이버 로그인API

def naver_api(request):
    CLIENT_ID = SOCIAL_OUTH_CONFIG["NAVER_CLIENT_ID"]
    REDIRECT_URI = SOCIAL_OUTH_CONFIG["NAVER_REDIRECT_URI"]
    url = 'https://nid.naver.com/oauth2.0/authorize?response_type=code&client_id={0}&state=none&redirect_uri={1}'.format(CLIENT_ID, REDIRECT_URI)
    return redirect(url)



def naver_api1(request):
    CLIENT_ID = SOCIAL_OUTH_CONFIG["NAVER_CLIENT_ID"]
    SECRET_KEY = SOCIAL_OUTH_CONFIG["NAVER_SECRET_KEY"]
    REDIRECT_URI = SOCIAL_OUTH_CONFIG["NAVER_REDIRECT_URI"]
    print(request.GET.get('code'))  # 인가코드 받아오는 애
    headers = {"Content-Type": "application/x-www-form-urlencoded"}  # h를
    data = {"grant_type": 'authorization_code',
            'client_id': CLIENT_ID,
            'client_secret': SECRET_KEY,
            'redirect_uri': REDIRECT_URI,
            'code': request.GET.get('code')}  # 인가코드
    res = requests.post('https://nid.naver.com/oauth2.0/token', data=data)
    print('res : ', res)

    token_json = res.json()
    print('1:',token_json)
    access_token = token_json.get("access_token")
    print('2:',access_token)
    profile_request = requests.get("https://openapi.naver.com/v1/nid/me",
                                   headers={"Authorization": f"Bearer {access_token}"}, )
    print('3:',profile_request)
    profile_json = profile_request.json()
    print('4:',profile_json)

    #내가 필요한 회원 정보(데이터베이스에 넣을 것)
    naver_id = profile_json['response']['id']
    print(naver_id)
    email = profile_json['response']['email']
    print(email)
    u_nickname = profile_json['response']['name']
    print(u_nickname)
    u_sex = profile_json['response']['gender']
    print(u_sex)
    birth_year = profile_json['response']['birthyear']
    print(birth_year)

    if CustomUser.objects.filter(username=naver_id).exists():
        user = CustomUser.objects.get(username=naver_id)
        login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        return redirect('/index')
    else:
        CustomUser(username=naver_id, email=email, u_nickname=u_nickname, is_active=True, birth_year=birth_year, u_sex=u_sex, login_method = 'N').save()
        CustomUser.objects.filter(username=naver_id).exists()
        user = CustomUser.objects.get(username=naver_id)
        login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        return redirect('/index')

#네이버 로그아웃
@login_required
def naver_logout(request):
    url = 'http://nid.naver.com/nidlogin.logout'
    webbrowser.open(url)
    return redirect('/logout')




















# 이메일 인증



# def getEmail(request):
#     global recvEmail
#     recvEmail = request.POST.get('mail')
#     return render(request, 'users/getEmail.html')
#
# def sendEmail(request):
#     global pw, recvEmail
#     pw = "".join([random.choice(string.ascii_lowercase) for _ in range(10)])  # 소문자 10개 랜덤생성
#     recvEmail = request.POST.get('mail')
#     sendEmail = "kyeeah9@gmail.com"
#
#
#     password = "dPqlsdl55!"
#     smtpName = "smtp.gmail.com"  # smtp 서버 주소
#     smtpPort = 587  # smtp 포트 번호
#
#     text = '인증번호 : ' + pw
#     msg = MIMEText(text)  # MIMEText(text , _charset = "utf8")
#
#     msg['Subject'] = '이메일 인증'
#     msg['From'] = sendEmail
#     msg['To'] = recvEmail
#     print(msg.as_string())
#
#     s = smtplib.SMTP(smtpName, smtpPort)  # 메일 서버 연결
#     s.starttls()  # TLS 보안 처리
#     s.login(sendEmail, password)  # 로그인
#     s.sendmail(sendEmail, recvEmail, msg.as_string())  # 메일 전송, 문자열로 변환하여 보냅니다.
#     s.close()  # smtp 서버 연결을 종료합니다.
#
#     return redirect('/users/match')
