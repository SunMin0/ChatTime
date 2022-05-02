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
from django.urls import path
import chat.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path("chat", chat.views.f_chat),
    path("chats", chat.views.f_chats),
    path("find", chat.views.f_find),
    path("more", chat.views.f_more),
    path("profile", chat.views.f_profile),
    path("index", chat.views.f_index),
    path("", chat.views.f_index),
]
