from django.shortcuts import render, redirect
from django.urls import reverse
from django.core.mail import send_mail
from user.models import User, Address
from django.core.paginator import Paginator
from goods.models import GoodsSKU
from django.views.generic import View
from django.http import HttpResponse, JsonResponse
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django_redis import get_redis_connection
from order.models import OrderInfo, OrderGoods
from utils.mixin import LoginRequiredMixin
from celery_tasks.tasks import send_register_active_email
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import SignatureExpired
import re
import logging

fh = logging.FileHandler("test.log", encoding="utf-8", mode="a")
formatter = logging.Formatter("%(asctime)s - %(name)s-%(levelname)s %(message)s")
fh.setFormatter(formatter)
LOG = logging.getLogger(__name__)


class RegisterView1(View):
    """注册视图类"""

    def get(self, request):
        """显示注册页面"""
        return render(request, 'register1.html')

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
            return render(request, 'register1.html', {'errmsg': '数据不完整'})

        # 进行正则匹配，校验邮箱
        if not re.match(r'^[a-z0-9][\w.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
            return render(request, 'register1.html', {'errmsg': '邮箱格式不正确'})

        # 校验两次输入密码是否一致
        if com_password != password:
            return render(request, 'register1.html', {'errmsg': '两次输入密码不一致'})

        # 判断用户是否同意使用协议
        if allow != 'on':
            return render(request, 'register1.html', {'errmsg': '请同意协议'})

        # 校验用户名是否重复
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            User.username = None

        if User.username:
            # 用户名已存在
            return render(request, 'login1.html', {'errmsg': '用户名已经存在'})

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

        # 返回应答，跳转到登录页
        return redirect(reverse('user:login1'))


class ForgetPsd(View):
    """用户密码重置"""

    def get(self, request):
        """显示重置密码页面"""
        return render(request, 'forgetpwd.html')

    def post(self, request):
        """发送密码重置邮件"""
        # 接收数据
        username = request.POST.get('user_name')
        email = request.POST.get('email')

        # LOG.info('reset username:' + username)
        # LOG.info('reset email:' + email)

        # LOG.info('username:' + str(username))
        user = User.objects.get(username=username)

        # 发送激活邮件，包含激活链接：http://127.0.0.1:8000/user/active/1
        # 激活链接中需要包含用户的身份信息（加密解密）

        # 加密用户的身份信息，生成激活token, 1小时过期
        serializer = Serializer(settings.SECRET_KEY, 3600)
        info = {'confirm': user.id}
        token = serializer.dumps(info)  # 返回bytes数据
        token = token.decode('utf8')

        subject = '姜饼小屋密码重置信息'
        message = ''
        sender = settings.EMAIL_FROM
        html_message = '<h1>亲爱的{0}, </h1>你收到这封邮件是因为你请求重置你在网站 ' \
                       '127.0.0.1:8000上的用户账户密码。请访问该页面并选择一个新密码：' \
                       '<a href="http://127.0.0.1:8000/user/reset/{1}">' \
                       'http://127.0.0.1:8000/user/reset/{2}</a>'.format(username, token, token)
        receiver = [email]

        # LOG.info('username:' + str(username))

        send_mail(subject, message, sender, receiver, html_message=html_message)
        # 数据校验

        # 检验用户名和邮箱是否正确

        # 发送邮件

        # 返回应答，跳转到重置页面
        return redirect(reverse('user:login1'))


class ResetPsd(View):
    """邮件密码重置"""

    def get(self, request, token):
        """进行用户激活"""
        # 进行解密，获取要激活的用户信息
        serializer = Serializer(settings.SECRET_KEY, 3600)
        try:
            info = serializer.loads(token)
            # LOG.info('info:' + str(info))
            # 获取待激活用户的id
            user_id = info['confirm']
            # LOG.info('user_id:' + str(user_id))

            # 根据id获取用户信息
            user = User.objects.get(id=user_id)

            # LOG.info('reset user:' + str(user))
            # LOG.info('reset user:' + str(user.password))

            # 组织上下文
            context = {'page': 'user',
                       "user_id": user.username
                       }

            # 跳转到修改密码页面
            return render(request, 'password_reset.html', context)

        except SignatureExpired as e:
            # 激活链接已经过期
            return HttpResponse('激活链接已失效')


class ModifypwdView(View):
    def post(self, request):
        username = request.POST.get('username')
        LOG.info('user_id:' + str(username))
        pwd1 = request.POST.get('pwd')
        pwd2 = request.POST.get('cpwd')
        # 如果两次密码不相等，返回错误信息

        # 如果密码一致
        user = User.objects.get(username=username)
        LOG.info('user.username:' + str(user.username))
        LOG.info('user.password:' + str(user.password))
        # 加密成密文
        user.set_password(pwd1)
        # save保存到数据库
        user.save()

        # 返回应答，跳转到登录页
        return redirect(reverse('user:login1'))


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
            return redirect(reverse('user:login1'))
        except SignatureExpired as e:
            # 激活链接已经过期
            return HttpResponse('激活链接已失效')


# /user/login
class LoginView1(View):
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
        # LOG.info('checked= ' + str(checked))

        # 使用模板
        return render(request, 'login1.html', {'username': username, 'checked': checked})

    def post(self, request):
        """登录校验"""
        # 接收数据
        username = request.POST.get('username')
        password = request.POST.get('pwd')

        # LOG.info('username:' + str(username))
        # LOG.info('password:' + str(password))

        # 校验数据
        if not all([username, password]):
            return render(request, 'login1.html', {'errmsg': '数据不完整'})

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
                # LOG.info('remember = ' + str(remember))

                if remember == 'on':
                    # 记住用户名
                    response.set_cookie('username', username, max_age=7 * 24 * 3600)
                else:
                    response.delete_cookie('username')

                # 返回response
                return response
            else:
                # 用户未激活
                return render(request, 'login1.html', {'errmsg': '账户未激活'})
        else:
            # 用户名或密码错误
            return render(request, 'login1.html', {'errmsg': '用户名或密码错误'})


# /user/logout
class LogoutView(View):
    """退出登录"""

    def get(self, request):
        """退出"""
        # 清除用户的session信息
        logout(request)

        # 退出后跳转到首页
        return redirect(reverse('goods:index'))


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

        # 获取用户的个人信息
        user = request.user
        address = Address.objects.get_default_address(user)

        # 获取用户的历史浏览记录
        # from redis import StrictRedis
        # sr = StrictRedis(host='127.0.0.1', port='6379', db=1)
        con = get_redis_connection('default')

        history_key = 'history_%d' % user.id

        # 获取用户最新浏览的5个商品的id
        sku_ids = con.lrange(history_key, 0, 4)

        # 遍历获取用户浏览的商品信息
        goods_li = []
        for id in sku_ids:
            goods = GoodsSKU.objects.get(id=id)
            goods_li.append(goods)

        LOG.info("goods_li = " + str(goods_li))

        # 组织上下文
        context = {'page': 'user',
                   'address': address,
                   'goods_li': goods_li
                   }

        # 除了你给模板文件传递的模板变量之外，django框架会把request.user也传给模板文件
        return render(request, 'user_center_info.html', context)


# /user/order
class UserOrderView(LoginRequiredMixin, View):
    """用户中心-订单页"""

    def get(self, request, page):
        """显示"""
        # page='order'
        # 获取用户的订单信息
        user = request.user
        orders = OrderInfo.objects.filter(user=user).order_by('-create_time')

        # 遍历获取订单商品的信息
        for order in orders:
            # 根据order_id查询订单商品信息
            order_skus = OrderGoods.objects.filter(order_id=order.order_id)

            # 遍历order_skus计算商品的小计
            for order_sku in order_skus:
                # 计算小计
                amount = order_sku.count * order_sku.price
                # 动态给order_sku增加属性amount， 保存订单商品的小计
                order_sku.amount = amount

            # 动态给order增加属性， 保存订单支付状态标题
            order.status_name = OrderInfo.ORDER_STATUS[order.order_status]
            # 动态给order增加属性， 保存订单商品的信息
            order.order_skus = order_skus

        # 进行分页
        paginator = Paginator(orders, 1)

        # 获取第page页的内容
        try:
            page = int(page)
        except Exception as e:
            page = 1

        if page > paginator.num_pages:
            page = 1

        # 获取第page页的Page实例对象
        order_page = paginator.page(page)

        # todoo：进行页码的控制，页面上最多显示5个页码
        # 1. 总页数小于5页，页面上显示所有页码
        # 2. 如果当前页是前3页，显示1-5页
        # 3. 如果当前页是后3页，显示后5页
        # 4. 其他情况，显示当前页的前2页，当前页，当前页的后2页
        num_pages = paginator.num_pages
        if num_pages < 5:
            pages = range(1, num_pages + 1)
        elif page <= 3:
            pages = range(1, 6)
        elif num_pages - page <= 2:
            pages = range(num_pages - 4, num_pages + 1)
        else:
            pages = range(page - 2, page + 3)

        # 组织上下文
        context = {'order_page': order_page,
                   'pages': pages,
                   'page': 'order'
                   }

        # 使用模板
        return render(request, 'user_center_order.html', context)


# /user/address
class AddressView(LoginRequiredMixin, View):
    """用户中心-地址页"""

    def get(self, request):
        """显示"""
        # 获取登录用户对应的User对象
        user = request.user

        # 使用模板
        address = Address.objects.get_default_address(user)

        return render(request, 'user_center_site.html', {'page': 'address', 'address': address})

    def post(self, request):
        """地址的添加"""
        # 接受数据
        receiver = request.POST.get('receiver')
        addr = request.POST.get('addr')
        zip_code = request.POST.get('zip_code')
        phone = request.POST.get('phone')

        # LOG.info("receiver" + str(receiver))
        # LOG.info("addr" + str(addr))
        # LOG.info("zip_code" + str(zip_code))

        # 校验数据
        if not all([receiver, addr, phone]):
            return render(request, 'user_center_site.html', {'errmsg': '数据不完整'})

        # 校验手机号
        if not re.match(r'1[3,4,5,7,8]\d{9}$', phone):
            return render(request, 'user_center_site.html', {'errmsg': '手机格式不正确'})

        if len(zip_code) != 6:
            return render(request, 'user_center_site.html', {'errmsg': '邮件编码错误'})

        # 业务处理：地址添加
        # 如果用户已存在默认地址，添加的地址不作为默认地址，否则作为默认收货地址
        # 获取登录用户对应的User对象
        user = request.user

        # try:
        #     address = Address.objects.get(user=user, is_default=True)
        # except Address.DoesNotExist:
        #     # 说明不存在默认的收获地址
        #     address = None

        address = Address.objects.get_default_address(user)

        if address:
            is_default = False
        else:
            is_default = True

        # 添加地址
        Address.objects.create(user=user,
                               receiver=receiver,
                               addr=addr,
                               zip_code=zip_code,
                               phone=phone,
                               is_default=is_default)
        # 返回应答，刷新地址页面
        return redirect(reverse('user:address'))
