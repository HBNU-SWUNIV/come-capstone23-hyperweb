from django.urls import path, include
from .views import Join1, Join2, Join3, Join4, Login, LogOut, UploadProfile, Add_dog
from . import views
urlpatterns = [
    path('add_dog', Add_dog.as_view()),
    path('join1', Join1.as_view()),
    path('join2', Join2.as_view(), name="join2"),
    path('join3', Join3.as_view()),
    path('join4', Join4.as_view()),
    path('login', Login.as_view(), name="login"),
    path('logout', LogOut.as_view()),
    path('profile/upload', UploadProfile.as_view()),
     path('check_email/', views.check_email, name='check_email'),
]

