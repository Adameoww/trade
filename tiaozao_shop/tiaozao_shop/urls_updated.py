from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from django.views.static import serve  # Function to handle uploaded files

from .settings import MEDIA_ROOT

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^', include('df_goods.urls', namespace='df_goods')),
    url(r'^user/', include('df_user.urls', namespace='df_user')),
    url(r'^cart/', include('df_cart.urls', namespace='df_cart')),
    url(r'^order/', include('df_order.urls', namespace='df_order')),
    url(r'^tinymce/', include('tinymce.urls')),  # Configuration for using the rich text editor
    url(r'^media/(?P<path>.*)$', serve, {"document_root": MEDIA_ROOT})  # Handle media file serving
]
