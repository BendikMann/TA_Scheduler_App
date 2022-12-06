"""djangoProject URL Configuration

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
from django.urls import path, include

import TA_Scheduler.views

urlpatterns = [
    path('admin/', admin.site.urls),

    # accounts
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/register/',
         TA_Scheduler.views.CreateAccount.as_view()),
    path('accounts/<int:pk>/update/',
         TA_Scheduler.views.UpdateAccount.as_view(template_name='account/update_account.html'),
         name='account-update'),
    # path('accounts/<int:pk>/view/',
    #      TA_Scheduler.views.ViewAccount.as_view(template_name='account/view_account.html'),
    #      name='account-view'),
    path('account/<int:pk>/delete/',
         TA_Scheduler.views.DeleteAccount.as_view(template_name='account/delete_account.html'),
         name='account-delete'),

    # address
    path('address/create/',
         TA_Scheduler.views.CreateAddress.as_view(template_name='address/create_address.html'),
         name='address-create'),
    path('address/<int:pk>/update/',
         TA_Scheduler.views.UpdateAddress.as_view(template_name='account/update_account.html'),
         name='address-update'),
    path('address/<int:pk>/view/',
         TA_Scheduler.views.ViewAddress.as_view(template_name='address/view_address.html'),
         name='address-view'),

    # homepage
    path('accounts/profile/', TA_Scheduler.views.HomeView.as_view(template_name='adminHomepage.html'),
         name='home-page'),

    path('', TA_Scheduler.views.HomeView.as_view(template_name='adminHomepage.html'),
         name='home-page'),

    path('accounts/<int:pk>/view/',
         TA_Scheduler.views.ViewAccount.as_view(template_name='account/view_account.html'),
         name='account-view')

    # course
    path('course/create/', TA_Scheduler.views.CreateCourse.as_view(template_name='course/create_course.html'),
         name='course-create'),
    path('course/<int:pk>/update/', TA_Scheduler.views.UpdateCourse.as_view(template_name='course/update_course.html'),
         name='course-update'),
    path('course/<int:pk>/view/', TA_Scheduler.views.ViewCourse.as_view(template_name='course/view_course.html'),
         name='course-view'),

]
