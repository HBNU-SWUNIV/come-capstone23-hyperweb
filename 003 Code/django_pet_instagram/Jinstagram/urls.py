from django.contrib import admin
from django.urls import path, include
from .views import Sub
from content.views import Main, UploadFeed
from .settings import MEDIA_URL, MEDIA_ROOT
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('main/', Main.as_view()),
    path('content/', include('content.urls')),
    path('user/', include('user.urls')),
    path('make_report/',include('make_report.urls')),
    path('algorithm_api/', include('algorithm_api.urls'))
]

urlpatterns += static(MEDIA_URL, document_root=MEDIA_ROOT)
