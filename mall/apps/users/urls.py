from django.contrib import admin
from django.urls import path, re_path
from users import views

urlpatterns = [
    path('registry/', views.Registry.as_view(), name="users.registry"),
    re_path(r'usernames/(?P<username>\w+)/count/$', views.CheckUsername.as_view(), name="users.checkuser"),
    re_path(r'mobiles/(?P<mobile>\d+)/count/$', views.CheckMobile.as_view(), name="users.mobile"),
]
