from django.shortcuts import render, redirect
from django.urls import reverse
from django.core.mail import send_mail
from user.models import User, Address
from django.views.generic import View
from django.http import HttpResponse, JsonResponse
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.template import RequestContext

from utils.mixin import LoginRequiredMixin
from celery_tasks.tasks import send_register_active_email
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import SignatureExpired
import re
import logging

LOG = logging.getLogger(__name__)


# def register(request):
#     """显示注册页面"""
#     if request.method == 'GET':
#         # 显示注册页面
#         return render(request, 'register.html')
#     else:
#         # 进行注册处理
#         # 接收数据
#         user_name = request.POST.get('user_name')
#         password = request.POST.get("pwd")
#         email = request.POST.get("email")
#         com_password = request.POST.get('cpwd')
#         allow = request.POST.get("allow")
#
#         # 进行数据校验
#         if not all([user_name, password, email]):
#             # 数据不完整
#             return render(request, 'register.html', {'errmsg': '数据不完整'})
#
#         # 进行正则匹配，校验邮箱
#         if not re.match(r'^[a-z0-9][\w.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
#             return render(request, 'register.html', {'errmsg': '邮箱格式不正确'})
#
#         # 校验两次输入密码是否一致
#         if com_password != password:
#             return render(request, 'register.html', {'errmsg': '两次输入密码不一致'})
#
#         # 判断用户是否同意使用协议
#         if allow != 'on':
#             return render(request, 'register.html', {'errmsg': '请同意协议'})
#
#         # 校验用户名是否重复
#         try:
#             user = User.objects.get(username=user_name)
#         except User.DoesNotExist:
#             # 用户名不存在
#             user = None
#
#         if user:
#             # 用户名已存在
#             return render(request, 'register.html', {'errmsg': '用户名已经存在'})
#
#         # 进行业务处理：进行用户注册
#         user = User.objects.create_user(user_name, password, email)
#         user.is_active = 0
#         user.save()
#
#         # 返回应答，跳转到首页
#         return redirect(reverse('goods:index'))
#         # return render(request, 'index.html')
#
#
# def register_handle(request):
#     """进行注册的处理"""
#     # 接收数据
#     username = request.POST.get('user_name')
#     password = request.POST.get("pwd")
#     email = request.POST.get("email")
#     com_password = request.POST.get('cpwd')
#     allow = request.POST.get("allow")
#
#     # 进行数据校验
#     if not all([username, password, email]):
#         # 数据不完整
#         return render(request, 'register.html', {'errmsg': '数据不完整'})
#
#     # 进行正则匹配，校验邮箱
#     if not re.match(r'^[a-z0-9][\w.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
#         return render(request, 'register.html', {'errmsg': '邮箱格式不正确'})
#
#     # 校验两次输入密码是否一致
#     if com_password != password:
#         return render(request, 'register.html', {'errmsg': '两次输入密码不一致'})
#
#     # 判断用户是否同意使用协议
#     if allow != 'on':
#         return render(request, 'register.html', {'errmsg': '请同意协议'})
#
#     # 校验用户名是否重复
#     try:
#         user = User.objects.get(username=username)
#     except User.DoesNotExits:
#         # 用户名不存在
#         user = None
#
#     if user:
#         # 用户名已存在
#         return render(request, 'register.html', {'errmsg': '用户名已经存在'})
#
#     # 进行业务处理：进行用户注册
#     user = User.objects.create_user(username, password, email)
#     user.is_active = 0
#     user.save()
#
#     # 返回应答，跳转到首页
#     return redirect(reverse('goods:index'))
#     # return render(request, 'index.html')


class RegisterView(View):
    """注册视图类"""

    def get(self, request):
        """显示注册页面"""
        return render(request, 'register.html')

    def post(self, request):
        """进行注册处理"""
        # 接收数据
        username = request.POST.get('user_name')
        password = request.POST.get("pwd")
        email = request.POST.get("email")
        com_password = request.POST.get('cpwd')
        allow = request.POST.get("allow")

        # LOG.info('username:' + username)
        # LOG.info('password:' + password)
        # LOG.info('email:' + email)

        # 进行数据校验
        if not all([username, password, com_password, email]):
            # 数据不完整
            return render(request, 'register.html', {'errmsg': '数据不完整'})

        # 进行正则匹配，校验邮箱
        if not re.match(r'^[a-z0-9][\w.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
            return render(request, 'register.html', {'errmsg': '邮箱格式不正确'})

        # 校验两次输入密码是否一致
        if com_password != password:
            return render(request, 'register.html', {'errmsg': '两次输入密码不一致'})

        # 判断用户是否同意使用协议
        if allow != 'on':
            return render(request, 'register.html', {'errmsg': '请同意协议'})

        # 校验用户名是否重复
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            User.username = None

        if User.username:
            # 用户名已存在
            return render(request, 'register.html', {'errmsg': '用户名已经存在'})

        # 进行业务处理：进行用户注册,django内置的用户认证系统
        user = User.objects.create_user(username=username, email=email, password=password)
        user.is_active = 0  # 禁止激活
        user.save()

        # 发送激活邮件，包含激活链接：http://127.0.0.1:8000/user/active/1
        # 激活链接中需要包含用户的身份信息（加密解密）

        # 加密用户的身份信息，生成激活token, 1小时过期
        serializer = Serializer(settings.SECRET_KEY, 3600)
        info = {'confirm': user.id}
        token = serializer.dumps(info)  # 返回bytes数据
        token = token.decode('utf8')

        # 异步发送邮件
        # 1. 将邮件放入任务队列
        send_register_active_email.delay(email, username, token)

        # 2. 启动任务处理者（注意：任务的发出者，中间人，任务处理者可以在同一台电脑上启用）
        # D:\sweetshop>celery -A celery_tasks.tasks worker --loglevel=info -P eventlet

        # 返回应答，跳转到首页
        return redirect(reverse('user:login'))


class ActiveView(View):
    """用户激活"""

    def get(self, request, token):
        """进行用户激活"""
        # 进行解密，获取要激活的用户信息
        serializer = Serializer(settings.SECRET_KEY, 3600)
        try:
            info = serializer.loads(token)
            # 获取待激活用户的id
            user_id = info['confirm']

            # 根据id获取用户信息
            user = User.objects.get(id=user_id)
            user.is_active = 1
            user.save()

            # 跳转到登录页面
            return redirect(reverse('user:login'))
        except SignatureExpired as e:
            # 激活链接已经过期
            return HttpResponse('激活链接已失效')


# /user/login
class LoginView(View):
    """登录"""

    def get(self, request):
        """显示登陆页面"""

        # 判断是否记住了用户名
        if 'username' in request.COOKIES:
            username = request.COOKIES.get('username')
            checked = 'checked'
        else:
            username = ''
            checked = ''

        # 使用模板
        return render(request, 'login.html', {'username': username, 'checked': checked})

    def post(self, request):
        """登录校验"""
        # 接收数据
        username = request.POST.get('username')
        password = request.POST.get('pwd')

        LOG.info('username:' + str(username))
        LOG.info('password:' + str(password))

        # 校验数据
        if not all([username, password]):
            return render(request, 'login.html', {'errmsg': '数据不完整'})

        # 业务处理
        user = authenticate(username=username, password=password)
        # LOG.info('user:' + str(user))
        if user is not None:
            # 用户名密码正确
            if user.is_active:
                # 用户已激活
                # 记录用户的登录状态
                login(request, user)

                # 获取登录后所要跳转到的地址
                # 默认跳转到首页
                next_url = request.GET.get('next', reverse('goods:index'))

                # 跳转到next_url
                response = redirect(next_url)  # HttpResponseRedirect

                # 判断是否需要记住用户名
                remember = request.POST.get('remember')

                if remember == 'on':
                    # 记住用户名
                    response.set_cookie('username', username, max_age=7 * 24 * 3600)
                else:
                    response.delete_cookie('username')

                # 返回response
                return response
            else:
                # 用户未激活
                return render(request, 'login.html', {'errmsg': '账户未激活'})
        else:
            # 用户名或密码错误
            return render(request, 'login.html', {'errmsg': '用户名或密码错误'})


class LogoutView(View):
    """退出登录"""
    def get(self, request):
        """退出"""

# /user
class UserInfoView(LoginRequiredMixin, View):
    """用户中心-信息页"""

    def get(self, request):
        """显示"""
        # page='user'
        # request.user
        # 如果用户未登录 -> AnonymousUser类的一个实例
        # 如果用户登录 -> User类的一个实例
        # request.user.is_authenticated 是属性
        # 除了你给模板文件传递的模板变量之外，django框架会把request.user也传给模板文件
        return render(request, 'user_center_info.html', {'page': 'user'})


# /user/order
class UserOrderView(LoginRequiredMixin, View):
    """用户中心-订单页"""
    def get(self, request):
        """显示"""
        # page='order'
        return render(request, 'user_center_order.html', {'page': 'order'})


# /user/address
class AddressView(LoginRequiredMixin, View):
    """用户中心-地址页"""

    def get(self, request):
        """显示"""
        # page='address'
        return render(request, 'user_center_site.html', {'page': 'address'})
