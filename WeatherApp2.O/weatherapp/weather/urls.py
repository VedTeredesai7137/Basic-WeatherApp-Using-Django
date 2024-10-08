from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='home'),  # Keep the same path
] + static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])

