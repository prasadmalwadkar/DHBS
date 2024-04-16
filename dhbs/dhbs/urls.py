"""dhbs URL Configuration

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

from django.urls import path, re_path, include
from django.contrib import admin

from django.urls import path
# from insights import views
from booking import views


urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    # path('patients/<int:patient_id>/', views.patient_detail, name='patient-detail'),
    path('',views.home,name='home'),
    path('manager_view/',views.manager_view,name='manager_view'),
    path('user_view',views.user_view,name="user_view"),
    path('user_details/<int:pk>',views.user_details,name="user_details"),
    path('analysis/<int:pk>',views.analysis,name = "analysis"),
    path('add/',views.add,name = "add"),
    path('delete/',views.delete,name = "delete"),
    path('update/',views.update,name = "update"),
    #path('manager_graphs/',views.manager_graphs,name="manager_graphs")





]