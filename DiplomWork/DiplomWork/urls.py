from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

from SiberiaApp.views import user_login

urlpatterns = [
    path('admin/', admin.site.urls),
    path('rework/', include('SiberiaApp.urls')),
    path('', user_login, name='login'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)