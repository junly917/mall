from django.urls import path, re_path
from . import views

urlpatterns = [
    re_path(r'^image_codes/(?P<image_code>.+)/$', views.GetImageCode.as_view(), name="users.getimagecode"),
    re_path(r'^sms_codes/(?P<mobile>.+)/$', views.GetMoblieCode.as_view(), name="users.getmobilcode"),
]