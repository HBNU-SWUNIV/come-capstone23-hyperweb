from django.urls import include,path
from . import views
from .views import Report2
urlpatterns = [
    path('report2', Report2.as_view()),
    path('report_to_post', views.report_to_post, name='report_post'),
]