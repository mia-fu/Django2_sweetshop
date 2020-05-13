from django.contrib import admin
from django.core.cache import cache
from goods.models import GoodsType, GoodsSKU, Goods


admin.site.register(GoodsSKU)
admin.site.register(Goods)
admin.site.register(GoodsType)
