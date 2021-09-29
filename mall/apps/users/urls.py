from django.contrib import admin
from django.urls import path
from users import views

urlpatterns = [
    path('registry/', views.Registry.as_view(), name="users.registry")
]