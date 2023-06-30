from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('lead_generator.urls', namespace='lead_generator')),
    path('users/', include('users.urls', namespace='users')),
]
