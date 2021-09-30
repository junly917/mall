from django.http import JsonResponse, HttpResponseForbidden
from django.shortcuts import render, HttpResponse
from django.views import View
from mall.libs.captcha.captcha import captcha
from django_redis import get_redis_connection
import re
import random


class GetImageCode(View):
    def get(self, request, image_code):
        _, text, image = captcha.generate_captcha()
        redis_conn = get_redis_connection("validate")
        redis_conn.set("UUID_{}".format(image_code), text, 60)
        return HttpResponse(image, content_type="image/png")


# /sms_codes/' + this.mobile + '/?image_code=' + this.image_code + '&image_code_id=' + this.image_code_id
class GetMoblieCode(View):
    def get(self, request, mobile):
        image_code = request.GET.get("image_code")
        image_code_id = request.GET.get("image_code_id")
        redis_conn = get_redis_connection("validate")
        redis_pipeline = redis_conn.pipeline()
        query_redis_code = redis_conn.get("UUID_{}".format(image_code_id)).decode("utf-8")

        # 参数不为空
        if not all([mobile, image_code, image_code_id]):
            return JsonResponse({"errmsg": "参数不能为空.", "code": 4001})

        # 如果传过来的图片验和redis里面的验证码不符合
        if query_redis_code.lower() != image_code.lower():
            return JsonResponse({"errmsg": "验证码输入错误.", "code": 4001})

        # 检查手机号码
        if not re.match(r'1[3-9]\d{9}$', mobile):
            return JsonResponse({"errmsg": "手机号码不正确.", "code": 4001})

        # 生成短信验证码
        sms_code = "%06d" % random.randint(0, 999999)
        redis_pipeline.set("sms_{}".format(mobile), sms_code, 300)
        print("sms_code:", sms_code)

        # 防止生发短信
        redis_pipeline.set("sms_flag_{}".format(mobile), 1, 60)
        retry_send_sms = redis_conn.get("sms_flag_{}".format(mobile))
        if not retry_send_sms:
            return HttpResponse({"errmsg": "重复发送短信"}, status=400)
        redis_pipeline.execute()

        return JsonResponse({"msg": "生成验证码.", "code": 0})
