from django.contrib import admin
from django.urls import path
from django.views.static import serve
from django.urls import  include, path, re_path

from real_estate import settings
from main import views as general_views

urlpatterns = [
    path('',include(('main.urls'),namespace='main')),
    path('admin/', admin.site.urls),
    path('app/accounts/', include('registration.backends.default.urls')),
    path('super-admin/main/',general_views.app,name='app'),
    
    path('super-admin/admin-user/',include(('admin_user.urls'),namespace='admin_user')),
    path('super-admin/property/',include(('property.urls'),namespace='property')),
    path('super-admin/tenant/',include(('tenant.urls'),namespace='tenant')),
    
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT})
]
