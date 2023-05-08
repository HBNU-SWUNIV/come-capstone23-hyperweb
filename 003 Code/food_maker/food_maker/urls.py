"""
URL configuration for food_maker project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
# from django.contrib import admin
from django.urls import path
from . import views
# urlpatterns = [
#     path('admin/', admin.site.urls),
# ]


urlpatterns = [
    # path('create_dog/', views.create_dog, name='create_dog'),
    # path('text_display/', views.text_display, name='text_display'),
    path('optimize_diet/', views.run_diet_optimizer, name='optimize_diet'), 
    # 기존 경로들...
    path('javascript_test/', views.javascript_test, name='javascript_test'),

]
