from django.urls import path
from .views import UploadFeed, Profile, Main, UploadReply, ToggleLike, ToggleBookmark, GetMorePosts
from . import views
from algorithm_api.views import Food_view

urlpatterns = [
    path('reply', UploadReply.as_view()),
    path('like', ToggleLike.as_view()),
    path('bookmark', ToggleBookmark.as_view()),
    path('profile', Profile.as_view(), name="profile"),
    path('main', Main.as_view(), name='main'),
    path('submit_pet_info/', views.submit_pet_info, name='submit_pet_info'),
    path('submit_user_info/', views.submit_user_info, name='submit_user_info'),
    path('Food_view', Food_view.as_view()),
    path('upload_image/', views.upload_image, name='upload_image'),
    path('upload/', views.upload_post, name='upload_post'),
    path('logout/', views.user_logout, name='user_logout'),
    path('get_more_posts/', GetMorePosts.as_view(), name='get_more_posts'),
]

