from django.contrib import admin
from django.urls import path,re_path
from testapp import views

urlpatterns = [

    # path('host/',views.host),
    # path('login/',views.login),
    # path('', views.login),
    # re_path('host/detail-(?P<nid>\d+).html/',views.detail),
    path('test_form/',views.test_form),
    path('ajax_form/',views.ajax_form),
    path('test_host/',views.test_host),


]