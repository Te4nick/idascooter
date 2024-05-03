"""
URL configuration for idascooter project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from scooter_control.views import ScooterViewSet

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='docs'),
    path(
        "api/v1/scooter/",
        ScooterViewSet.as_view(
            {
                "get": "get_scooter",
            }
        ),
        name="get_scooter",
    ),
    path(
        "api/v1/scooter/all",
        ScooterViewSet.as_view(
            {
                "get": "get_scooters_list",
            }
        ),
        name="get_scooters_list",
    ),
    path(
        "api/v1/passenger/",
        ScooterViewSet.as_view(
            {
                "post": "post_passenger",
            }
        ),
        name="post_passenger",
    ),
    path(
        "api/v1/scooter/occupy/",
        ScooterViewSet.as_view(
            {
                "post": "post_occupy_scooter",
            }
        ),
        name="occupy_scooter",
    ),
    path(
        "api/v1/scooter/vacant/",
        ScooterViewSet.as_view(
            {
                "post": "post_vacant_scooter",
            }
        ),
        name="vacant_scooter",
    ),
    path(
        "api/v1/scooter/broken/",
        ScooterViewSet.as_view(
            {
                "get": "get_scooter_broken",
                "post": "post_broken_scooter"
            }
        ),
        name="scooter_broken",
    ),
    path(
        "api/v1/log/",
        ScooterViewSet.as_view(
            {
                "get": "get_log_file",
            }
        ),
        name="get_log_file",
    ),
    path(
        "api/v1/log/status/",
        ScooterViewSet.as_view(
            {
                "get": "get_log_file_status",
            }
        ),
        name="get_log_file_status",
    ),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
