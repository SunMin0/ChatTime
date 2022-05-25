"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
import cafe.views
import cart.views
import chat.views
import users.views
from django.conf import settings
from django.conf.urls.static import static
from config.settings import MEDIA_URL
from order.views import OrderList

urlpatterns = [
    #어드민
    path('admin/', admin.site.urls),
    #메인 페이지
    path("chat", chat.views.f_chat),
    path("chats", chat.views.f_chats),
    path("more", chat.views.f_more),
    path("profile", chat.views.f_profile),
    path("index", chat.views.f_index),

    #로그인, 회원가입 페이지
    path("", users.views.base),
    path("signup", users.views.signup),
    path("login", users.views.userlogin),
    path("logout", users.views.userlogout),
    path("password", users.views.change_password),
    path('update', users.views.edit_profile),
    path('delete', users.views.delete_user),
    # 소셜 로그인
    # 카카오 로그인, 로그아웃
    path('kakao', users.views.kakao_api),
    path('kakao_login', users.views.kakao_api1),
    path('kakao_logout', users.views.kakao_logout),
    # 네이버 로그인, 로그아웃
    path('naver', users.views.naver_api),
    path('naver_login', users.views.naver_api1),
    path('naver_logout', users.views.naver_logout),

    #cafe
    path("cafe", cafe.views.f_cafe),
    # path("cafe/detail", cafe.views.espresso),
    # path('cart', cafe.views.cart),

    #order
    path('order/', include('order.urls', namespace='order')),

    #매니져
    path('manager',OrderList.as_view()),

    #Menu 등록
    path('create_menu', cafe.views.create_product),
    path('espresso', cafe.views.product_in_espresso),
    path('bread', cafe.views.product_in_bread),
    path('juice', cafe.views.product_in_juice),
    path('tea', cafe.views.product_in_tea),
    path('detail_menu',cafe.views.product_detail),

    #cart(장바구니)
    path('cart/', include('cart.urls', namespace='cart')),
    # path('cart/add', cart.views.add),
    # path('cart/remove', cart.views.remove),
    # path('cart/detail', cart.views.detail),
    # path('cart/', include('cart.urls')),
    # path('naver_login', users.views.naver_api1),
    # path('naver_logout', users.views.naver_logout),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
#static 읽을 떄 media_root의 폴더도 읽어들인다.