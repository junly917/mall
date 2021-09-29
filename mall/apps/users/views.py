from django.shortcuts import render, HttpResponse, redirect
from django.views import View
from django.http import JsonResponse
from users.models import User
import sys
print(sys.path)
# print(User.objects.filte(id=1).values())


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
        print(user, pwd, cpwd, phone, pic_code, msg_code)

        # 2. 验证相应的参数
        if not all([user, pwd, cpwd, phone, pic_code, msg_code]):
            return JsonResponse({"msg": "参数不能为空", "code": 1001})

        user_obj = User.objects.filte(username=user).count()
        if user_obj:
            return JsonResponse({"msg": "用户名己存在", "code": 1003})

        phone_obj = User.objects.filte(phone=phone).count()
        if phone_obj:
            return JsonResponse({"msg": "手机号码己存在", "code": 1003})

        # 3. 写入数据库
        try:
            User.objects.create(username=user, password=pwd, phone=phone)
        except Exception as e:
            return JsonResponse({"msg": "注册数据异常 {}".format(e)})

        # 4. 返回前端
        return JsonResponse({"msg": "注册成功.", "code": 200})


class View(View):
     def get(self, request):
        pass



