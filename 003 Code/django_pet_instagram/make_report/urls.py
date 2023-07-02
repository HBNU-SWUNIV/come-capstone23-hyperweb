from django.urls import include,path
from . import views
from .views import Report2
urlpatterns = [
    path('', views.index),
    path('report_page/', views.ReportView.as_view(), name='ReportViewSet'),
    path('save_image/', views.save_image, name='save_image'),
    path('report2', Report2.as_view()),
    path('report_to_post', views.report_to_post, name='report_post'),
]