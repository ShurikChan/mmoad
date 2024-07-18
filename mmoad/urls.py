"""
URL configuration for mmoad project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path, include
from adboard.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('adcreate/', AdvertisementCreate.as_view()),
    path('', IndexView.as_view()),
    path('accounts/', include('allauth.urls')),
    path('adlist/', AdvertisementView.as_view()),
    path('addetail/<int:pk>', AdvertisementDetail.as_view()),
    path('adedit/<int:pk>', AdvertisementUpdate.as_view(), name='adedit'), 
    path('accounts/profile/', ProfileView.as_view()),
    path('do_response/<int:pk>/', DoResponse.as_view(), name='do_response'),
    path('adresponses/<int:pk>', AdResponsesView.as_view(), name='responseslist'),
    path('addelete/<int:pk>', AdvertisementDelete.as_view(), name='addelete'),
    path('adresponses/<int:pk>/delete', AdResponseDelete.as_view(), name='responsedelete'),
    path('confirm/', ConfirmUser.as_view(), name='confirm_user'),
    path('adresponses/<int:pk>/accept', AcceptResponse.as_view(), name='accept_response'),
]
