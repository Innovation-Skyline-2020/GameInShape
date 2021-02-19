"""Web_App URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from . import views

urlpatterns = [
    path('', views.home),
    path('front_web_1.html', views.home),
    path('game_page.html', views.game_page),
    path('about_us.html', views.about_us),
    path('game_mortal.html', views.game_mortal),
    path('admin.html', admin.site.urls),
    path('game_car.html', views.game_car),
    path('start_setup_car', views.start_setup_car, name='start_setup_car'),
    path('start_game_car', views.start_game_car, name='start_game_car'),
    path('start_setup_mortal', views.start_setup_mortal, name='start_setup_mortal'),
    path('start_game_mortal', views.start_game_mortal, name='start_game_mortal'),

]
