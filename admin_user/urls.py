from django.urls import path,re_path
from . import views

app_name = 'admin_user'

urlpatterns = [
    path('list/', views.admin_user_list, name='admin_user_list'),
    re_path(r'^create/$', views.create_admin_user, name='create_admin_user'),
    re_path(r'^info/(?P<pk>.*)/$', views.admin_user_info, name='admin_user_info'),
    re_path(r'^edit/(?P<pk>.*)/$', views.edit_admin_user, name='edit_admin_user'),
    re_path(r'^delete/(?P<pk>.*)/$', views.delete_admin_user, name='delete_admin_user'),
]