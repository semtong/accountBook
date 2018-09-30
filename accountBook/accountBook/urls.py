"""accountBook URL Configuration

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

# for login
from django.contrib.auth import views as auth_views

# sign up
from account import views as account_views

# main view
from accountBookMain import views as home

urlpatterns = [
    path('admin/', admin.site.urls),

    # login form
    path('', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('signup/', account_views.sign_up, name='signup'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    path('home/', home.home, name='home')
]
