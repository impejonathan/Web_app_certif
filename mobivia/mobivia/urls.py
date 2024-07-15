"""mobivia URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from Carter_cash import views

urlpatterns = [
    path('admin/', admin.site.urls), # pour le super user
    path('index', views.index , name='home'),
    # path('login', views.login_page, name='login'),
    path('', views.login_page, name='login'), # page d'arriver 

    path('signup', views.signup_page, name='signup'),
    path('logout/', views.logout_user, name='logout'),
    
    path('voiture/', views.voiture_page, name='voiture'),
    path('trouver_pneu/', views.trouver_pneu, name='trouver_pneu'),
    path('dimension/', views.dimension_page, name='dimension'),
    
    path('prediction/', views.prediction_view, name='prediction'),
    
    path('gpt/', views.chatbot_view, name='gpt'),
    
    path('variation/', views.variation_page, name='variation'),

    
]


handler404 = 'Carter_cash.views.handler404'
