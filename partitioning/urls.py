"""
URL configuration for partitioning project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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

from user.views import create_activity, delete_activity, get_activity, update_activity

urlpatterns = [
    path("admin/", admin.site.urls),
    path("activity/create/", create_activity),
    path("activity/<int:activity_id>/", get_activity),
    path("activity/<int:activity_id>/update/", update_activity),
    path("activity/<int:activity_id>/delete/", delete_activity),
]
