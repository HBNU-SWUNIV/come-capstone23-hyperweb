from django.urls import path
from .views import UploadFeed, Profile, Main, UploadReply, ToggleLike, ToggleBookmark
from . import views
from algorithm_api.views import Food_view

urlpatterns = [
    path('upload', UploadFeed.as_view()),
    path('reply', UploadReply.as_view()),
    path('like', ToggleLike.as_view()),
    path('bookmark', ToggleBookmark.as_view()),
    path('profile', Profile.as_view(), name="profile"),
    path('main', Main.as_view()),
    path('submit_pet_info/', views.submit_pet_info, name='submit_pet_info'),
    path('submit_user_info/', views.submit_user_info, name='submit_user_info'),
    path('post_api', views.post_api, name='post_api'),
    path('Food_view', Food_view.as_view())

]

