from django.contrib.auth.models import AbstractBaseUser, AbstractUser
from django.db import models
from django import forms


class CustomUser(AbstractUser):
    """User model."""
    # username = None
    # email = models.CharField(max_length=50, unique=False)
    first_name = None
    last_name = None
    login_method = models.CharField(max_length=10, null=True, unique=False)
    # u_id = models.CharField(max_length=200, unique=True)  # user 아이디
    u_nickname = models.CharField(max_length=50, unique=False)  # user nickname
    birth_year = models.IntegerField(null=True, unique=False)
    SEX = (('F', '여자'), ('M', '남자'), ('U', '선택 안함'))
    u_sex = models.CharField(max_length=10, choices=SEX, null=True, unique=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_master = models.BooleanField(default=False)
    is_manager = models.BooleanField(default=False)
    # USERNAME_FIELD = 'u_id'
    # REQUIRED_FIELDS = []




# class UserProfile(models.Model):
# user = models.OneToOneField(User)
#
# verified_email = models.BooleanField(blank=True, default = False)
# company_name = models.CharField(max_length=100, blank=False)
#
# def __unicode__(self):
#     return self.user.username


