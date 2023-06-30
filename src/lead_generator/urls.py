from django.urls import path
from .views import *

app_name = 'lead_generator'

urlpatterns = [
    path('', MainView.as_view(), name='lead_generator'),
    path('leads/', ListLeadsView.as_view(), name='leads')
]
