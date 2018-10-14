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
from accountBookMain import views

urlpatterns = [
    path('admin/', admin.site.urls),

    # login form
    path('', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('signup/', account_views.sign_up, name='signup'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # save add user
    path('saveAccountUser/?P<store_id>\d+/<int:history>', views.save_account_user, name='saveAccountUser'),

    # add account user
    path('addAccountUser/<int:history>/', views.add_account_user, name="addAccountUser"),

    # look user list
    path('accountListUser/<int:history>/', views.account_user_list, name='accountListUser'),

    # history write
    path('write_history/<int:history_pk>/', views.write_history, name='write_history'),

    path('history_main/<int:history_pk>/', views.history_main, name='history_main'),

    path('make_account/', views.make_account, name='make_account'),

    path('home/', views.main_view, name='home')
]
