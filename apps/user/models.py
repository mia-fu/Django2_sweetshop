from django.db import models
from django.contrib.auth.models import AbstractUser
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from django.conf import settings
from db.base_model import BaseModel


class User(AbstractUser, BaseModel):
    def generate_active_token(self):
        """生成用户签名字符串"""
        serialize = Serializer(settings.SECRET_KEY, 3600)
        info = {'confirm': self.id}
        token = serialize.dumps(info)
        return token.decode()

    # 指定该类的数据库表单名字
    class Meta:
        db_table = 'ss_user'
        verbose_name = '用户'
        verbose_name_plural = verbose_name


# 模型管理器类
class AddressManage(models.Manager):
    """地址模型管理器类"""

    # 1. 改变原有查询的结果集：all()
    # 2. 封装方法：用户操作模型类对应的数据库表（增删改查）
    def get_default_address(self, user):
        # self.model:获取self对象所在的模型类
        try:
            address = self.get(user=user, is_default=True)
        except self.model.DoesNotExist:
            # 说明不存在默认的收获地址
            address = None

        return address


class Address(BaseModel):
    """地址模型类"""
    user = models.ForeignKey('User', verbose_name='所属账户', on_delete=models.CASCADE)
    receiver = models.CharField(max_length=20, verbose_name='收件人')
    addr = models.CharField(max_length=256, verbose_name='收件地址')
    zip_code = models.CharField(max_length=6, null=True, verbose_name='邮政编码')
    phone = models.CharField(max_length=11, verbose_name='联系电话')
    is_default = models.BooleanField(default=False, verbose_name='是否默认')

    # 自定义一个模型管理器对象
    objects = AddressManage()

    class Meta:
        db_table = 'ss_address'
        verbose_name = '用户'
        verbose_name_plural = verbose_name
