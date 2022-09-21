from unicodedata import name
from django.contrib import admin
from django.urls import path, include
from filesManager.views import FileDetailview, FileListview, Upload
from rest_framework.urlpatterns import format_suffix_patterns

app_name = 'fileManager'
urlpatterns = [
    path('admin/', admin.site.urls),
    path('<str:user>/files/', FileListview.as_view()),
    path('<str:user>/files/<uuid:pk>', FileDetailview.as_view()),
    path('upload/', Upload.as_view(), name='upload_file')
]
urlpatterns = format_suffix_patterns(urlpatterns)
