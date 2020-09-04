from django.contrib import admin
from django.core.cache import cache
from order.models import OrderInfo, OrderGoods


class BaseModelAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        """新增或更新表中的数据时调用"""
        super().save_model(request, obj, form, change)

        # 发出任务，让celery worker重新生成首页静态页
        from celery_tasks.tasks import generate_static_index_html
        generate_static_index_html.delay()

        # 清除首页的缓存数据
        cache.delete('index_page_data')

    def delete_model(self, request, obj):
        """删除表中的数据时调用"""
        super().delete_model(request, obj)
        # 发出任务，让celery worker重新生成首页静态页
        from celery_tasks.tasks import generate_static_index_html
        generate_static_index_html.delay()

        # 清除首页的缓存数据
        cache.delete('index_page_data')


class OrderInfoAdmin(BaseModelAdmin):
    pass


class OrderGoodsAdmin(admin.ModelAdmin):
    pass


admin.site.register(OrderInfo, OrderInfoAdmin)
admin.site.register(OrderGoods, OrderGoodsAdmin)
