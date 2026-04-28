"""
URL configuration for task_manager project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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

from tasks.api import api as tasks_api
from shop.api import api as shop_api
from movies.api import api as movies_api
from blog.api import api as blog_api
from monitoring.api import api as monitoring_api
from library.api import api as library_api
from education.api import api as education_api

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/tasks/', tasks_api.urls),
    path('api/shop/', shop_api.urls),
    path('api/movies/', movies_api.urls),
    path('api/blog/', blog_api.urls),
    path('api/monitoring/', monitoring_api.urls),
    path('api/library/', library_api.urls),
    path('api/education/', education_api.urls),
]
