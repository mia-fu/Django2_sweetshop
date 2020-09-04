from django.urls import path, re_path
from user.views import RegisterView1, ActiveView, ModifypwdView, ForgetPsd, ResetPsd, LoginView1, UserInfoView, UserOrderView, AddressView, \
    LogoutView

urlpatterns = [
    path('register1', RegisterView1.as_view(), name='register1'),  # 注册

    re_path('active/(?P<token>.*)$', ActiveView.as_view(), name='active'),  # 用户激活
    path('login1', LoginView1.as_view(), name='login1'),  # 登录1

    path('logout', LogoutView.as_view(), name='logout'),  # 注销登录

    path('forget', ForgetPsd.as_view(), name='forget'),  # 忘记密码
    re_path('reset/(?P<token>.*)$', ResetPsd.as_view(), name='reset'),  # 重置密码
    path('modify_pwd', ModifypwdView.as_view(), name='modify_pwd'),

    path('', UserInfoView.as_view(), name='user'),  # 用户中心-信息页
    path('order/<int:page>', UserOrderView.as_view(), name='order'),  # 用户中心-订单页
    path('address', AddressView.as_view(), name='address'),  # 用户中心-地址页
]
