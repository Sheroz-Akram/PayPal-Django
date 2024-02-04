"""webapps2023 URL Configuration

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
from registor import views

urlpatterns = [
    path('admin/', admin.site.urls, name="admin"),
    path('', views.redirectToSignIn, name="Redirect"),
    path('SignIn', views.viewSignInPage, name="SignIn"),
    path('SignUp', views.viewSignUpPage, name="SignUp"),
    path('Home', views.viewHomePage, name="Home"),
    path('Logout', views.viewLogoutPage, name="Logout"),
    path('Transactions', views.viewTransactionsPage, name="Transactions"),
    path('Terms', views.viewTermsAndConditions, name="Terms"),
    path('Notifications', views.viewNotificationPage, name="Notifications"),
    path('conversion/<str:from_currency>/<str:to_currency>/<str:amount>/', views.conversionView),
] 
