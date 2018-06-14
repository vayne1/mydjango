from django.contrib import admin
from django.urls import path,re_path
from cmdb import views

urlpatterns = [

    path('host/',views.host),
    path('login/',views.login),
    path('', views.login),
    path('account_number/', views.account),
    re_path('host/detail-(?P<nid>\d+).html/',views.detail),

]