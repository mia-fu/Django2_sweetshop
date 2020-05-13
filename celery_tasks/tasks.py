# 使用celery
from django.core.mail import send_mail
from django.conf import settings
from celery import Celery
import time

# 在任务处理者一端加这几句， django环境的初始化
# broker和worker在同一台机子上则需要加上本段代码
import os
import django

import logging

LOG = logging.getLogger(__name__)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sweetshop.settings')
django.setup()

# 创建一个使用Celery类的实例对象
app = Celery('celery_tasks.tasks', broker='redis://127.0.0.1:6379/0')


# 定义任务函数
@app.task
def send_register_active_email(to_email, username, token):
    """发送激活邮件"""
    # 组织邮件信息
    subject = '甜甜小舖欢迎信息'
    message = ''
    sender = settings.EMAIL_FROM
    html_message = '<h1>{0}, 欢迎您注册成为甜甜小舖的小主，</h1>请点击下方链接激活您的账户哦~<br>' \
                   '<a href="http://127.0.0.1:8000/user/active/{1}">' \
                   'http://127.0.0.1:8000/user/active/{2}</a>'.format(username, token, token)
    receiver = [to_email]

    LOG.info('username:' + str(username))

    send_mail(subject, message, sender, receiver, html_message=html_message)
    time.sleep(5)
