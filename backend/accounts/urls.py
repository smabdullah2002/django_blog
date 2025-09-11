from django.urls import path
from .views import UserRegistrationView

urlpatterns=[
    path('register/', UserRegistrationView.as_view(), name='user_registration'),
]

#http://127.0.0.1:8000/accounts/register/