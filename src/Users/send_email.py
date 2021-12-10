from random import Random
from django.core.mail import send_mail
from django.http import JsonResponse
from pattern.models import emailVerify

from src.settings import EMAIL_FROM


# 生成随机字符串
def random_str(random_length=8):
    str = ''
    # 生成字符串的可选字符串
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars) - 1
    random = Random()
    for i in range(random_length):
        str += chars[random.randint(0, length)]
    return str


def send_my_email(email):
    email_title = "邮箱验证"
    code = random_str(6)
    email_body = "  您使用此邮箱apex平台进行注册，验证码为 " + code + "\n若非本人注册，请忽略此邮件"
    emailVerify.objects.create(email=email, randomCode=code)
    send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
    return send_status
