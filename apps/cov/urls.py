from django.urls import path
from cov.views import get_time, CovView, TestView, get_c1_data, get_c2_data, get_r1_data, get_r2_data, get_l2_data, \
get_l1_data

urlpatterns = [
    path('test', TestView.as_view(), name='test'),  # 疫情页
    path('china', CovView.as_view(), name='china'),  # 疫情页
    path('time', get_time, name='time'),
    path('c1', get_c1_data, name='c1'),
    path('c2', get_c2_data, name='c2'),
    path('r1', get_r1_data, name='r1'),
    path('r2', get_r2_data, name='r2'),
    path('l2', get_l2_data, name='l2'),
    path('l1', get_l1_data, name='l1'),
]
