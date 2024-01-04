from django.urls import path,re_path
from . import views

app_name = 'property'

urlpatterns = [
    path('list/', views.property_list, name='property_list'),
    re_path(r'^create-property/$', views.create_property, name='create_property'),
    re_path(r'^property-info/(?P<pk>.*)/$', views.property_info, name='property_info'),
    re_path(r'^edit-property/(?P<pk>.*)/$', views.edit_property, name='edit_property'),
    re_path(r'^delete-property/(?P<pk>.*)/$', views.delete_property, name='delete_property'),
    re_path(r'^assign-property/(?P<unit_id>.*)/$', views.assign_property_tenant, name='assign_property_tenant'),
]