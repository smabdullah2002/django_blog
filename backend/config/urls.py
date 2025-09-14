
from django.contrib import admin
from django.urls import path,include

from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView



urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls'), name='accounts'),
    path('otp/', include('otp.urls'), name='otp'),
]
