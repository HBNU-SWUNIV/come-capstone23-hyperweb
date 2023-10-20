from django.urls import include,path
from . import views
from .views import Report2
urlpatterns = [
    # path('', views.index),
    path('report_page/', views.ReportView2.as_view(), name='ReportViewSet2'),
    path('report_month_page/', views.ReportMonthView.as_view(), name='ReportMonthViewSet'),
    # path('save_image/', views.save_image, name='save_image'),
    path('report2', Report2.as_view()),
    path('report_to_post', views.report_to_post, name='report_post'),
    path('report_month/', views.report_month, name='report_month'),
]