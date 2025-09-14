from django.urls import path
from .views import UserRegistrationView, UserLoginView

urlpatterns=[
    path('register/', UserRegistrationView.as_view(), name='user_registration'),
    path('login/', UserLoginView.as_view(), name='user_login'),
]

#http://127.0.0.1:8000/accounts/register/
#http://127.0.0.1:8000/accounts/login/