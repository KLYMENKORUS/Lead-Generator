from django.urls import path
from .views import *

app_name = 'users'

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('sign-up/', UserSignUpView.as_view(), name='signup'),
    path('update/<pk>/', UserUpdateView.as_view(), name='update'),
]