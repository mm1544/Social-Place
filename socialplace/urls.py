from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('base.urls')),
    # url starting with 'api/' will be 'sent'/directed to file 'base/api/urls.py'
    path('api/', include('base.api.urls')),
]
