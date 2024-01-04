from django.urls import path,re_path
from . import views

app_name = 'tenant'

urlpatterns = [
    path('list/', views.tenant_list, name='tenant_list'),
    re_path(r'^create-tenant/$', views.create_tenant, name='create_tenant'),
    re_path(r'^tenant-info/(?P<pk>.*)/$', views.tenant_info, name='tenant_info'),
    re_path(r'^edit-tenant/(?P<pk>.*)/$', views.edit_tenant, name='edit_tenant'),
    re_path(r'^delete-tenant/(?P<pk>.*)/$', views.delete_tenant, name='delete_tenant'),
]