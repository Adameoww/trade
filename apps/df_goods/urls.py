from django.conf.urls import url, re_path
from django.views.static import serve
from tiaozao_shop import settings
from . import views

app_name = 'df_goods'

urlpatterns = [
    url('^$', views.index, name="index"),  # Homepage
    url('^index/$', views.index, name="index"),  # Homepage
    url('^list(\d+)_(\d+)_(\d+)/$', views.good_list, name="good_list"),  # Product listing page
    url('^detail/(\d+)/$', views.detail, name="detail"),  # Product detail page
    url('^content/(\d+)/(\d+)/$', views.content, name="content"),  # Product content
    url(r'^search/', views.ordinary_search, name="ordinary_search"),  # Full-text search
    re_path('^media/(?P<path>.*)/$', serve, {'document_root': settings.MEDIA_ROOT}),  # Media file serving
]
