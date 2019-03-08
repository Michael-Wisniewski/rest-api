from django.contrib import admin
from django.urls import path, include
import os

urlpatterns = [
    path('admin/', admin.site.urls),
    path('v1/', include('api.urls')),
]

if os.getenv('PRODUCTION') == 'false':
    urlpatterns.append(path('api-auth/', include('rest_framework.urls',namespace='rest_framework')))