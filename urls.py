"""LaboratoryManagementSystem URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from LMS import views
from django.conf.urls import url
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^$',views.login,name='login'),
    url(r'^login/$',views.loginVerify,name='loginVerify'),
    url(r'^index/$',views.index,name='index'),
    url(r'^register_show/$', views.inregister, name='show_register'),
    url(r'^register/$', views.register, name='register'),
    url(r'^allTask/$', views.allTask, name='allTask'),
    url(r'^acceptTask/$', views.acceptTask, name='acceptTask'),
    url(r'^abandonTask/$', views.abandonTask, name='abandonTask'),
    url(r'^myWork/$', views.myWork, name='myWork'),
    url(r'^upload_ajax/$', views.upload_ajax, name='upload_ajax'),
    url(r'^eachWork/$', views.eachWork, name='eachWork'),
    url(r'^getWorkId/$', views.getWorkId, name='getWorkId'),
    url(r'^editMyWork/$', views.editMyWork, name='editMyWork'),
    url(r'^getFileInfo/$', views.getFileInfo, name='getFileInfo'),
    url(r'^download_file/$', views.download_file, name='download_file'),

]
