from django.urls import include,path
from . import views

urlpatterns = [
    path('', views.index),
    path('report_page/', views.ReportView.as_view(), name='ReportViewSet'),
    path('save_image/', views.save_image, name='save_image'),
]