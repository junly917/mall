from django.shortcuts import render, HttpResponse, redirect
from django.views import View
from django.http import JsonResponse
from django_redis import get_redis_connection
from users.models import User
from mall.libs.captcha.captcha import captcha
import json


class GetImageCode(View):
    def get(self, request, image_code):
        print("UUID:", image_code)
        _, text, image = captcha.generate_captcha()
        redis_conn = get_redis_connection("validate")
        redis_conn.set("validate_{}".format(image_code), text, 60)
        return HttpResponse(image, content_type="image/png")


class Registry(View):
    def get(self, request):
        return render(request, 'register.html')

    def post(self, request):
        # 1. 获取前端的参数
        user = request.POST.get("user_name")
        cpwd = request.POST.get("cpwd")
        pwd = request.POST.get("pwd")
        phone = request.POST.get("phone")
        pic_code = request.POST.get("pic_code")
        msg_code = request.POST.get("msg_code")

        # 2. 验证相应的参数
        if not all([user, pwd, cpwd, phone, pic_code, msg_code]):
            return JsonResponse({"msg": "参数不能为空", "code": 1001})

        user_obj = User.objects.filter(username=user).first()
        if user_obj:
            return JsonResponse({"msg": "用户名己存在", "code": 1003})

        phone_obj = User.objects.filter(mobile=phone).first()
        if phone_obj:
            return HttpResponse(json.dumps({"msg": "手机号码己存在", "code": 1003}, ensure_ascii=False))

        redis_conn = get_redis_connection("validate")
        sms_code = redis_conn.get("sms_{}".format(phone)).decode("utf-8")
        if sms_code != msg_code:
            return HttpResponse(json.dumps({"msg": "短信认证码不正确", "code": 1003}, ensure_ascii=False))

        # 3. 写入数据库
        try:
            User.objects.create_user(username=user, password=pwd, mobile=phone)
        except Exception as e:
            return JsonResponse({"msg": "注册数据异常 {}".format(e)})

        # 4. 返回前端
        return HttpResponse(json.dumps({"msg": "注册成功.", "code": 200}, ensure_ascii=False))


class CheckUsername(View):
    def get(self, request, username):
        res = User.objects.filter(username=username).count()
        if res:
            return JsonResponse({"errmsg": "用户名己存在", "code": 1000, "count": res})
        return JsonResponse({"errmsg": None, "code": 0})


class CheckMobile(View):
    def get(self, request, mobile):
        res = User.objects.filter(mobile=mobile).count()
        if res:
            return HttpResponse(json.dumps({"errmsg": "手机号码己存在", "count": res, "code": 1000}, ensure_ascii=False))
        return JsonResponse({"errmsg": None, "code": 0})


