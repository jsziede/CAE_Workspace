"""
Site-wide URL Configuration
"""

from django.conf.urls import include, url
from django.contrib import admin


urlpatterns = [
    # Admin views.
    url(r'^admin/', admin.site.urls),

    # CAE_Home app views.
    url(r'^', include('cae_home.urls')),
]
