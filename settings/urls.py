"""
Site-wide URL Configuration.

Note: Urls will automatically be prefixed with "<url-prefix>/" as defined in allowed_apps.py.
"""

import logging
from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin


# Import logger.
logger = logging.getLogger(__name__)


urlpatterns = [
    # Admin views.
    url(r'^admin/', admin.site.urls),

    # CAE_Home app views.
    url(r'^', include('cae_home.urls')),
]


# Dynamically grab app urls for urlpatterns variable. Essentially the same logic as routing.py.
for project, project_settings in settings.INSTALLED_CAE_PROJECTS.items():
    url_prefix = project_settings['url-prefix']
    for app, app_name in project_settings['related_apps'].items():
        try:
            # Add app's urls to urlpatterns variable.
            urlpatterns.append(
                url(r'^{0}/'.format(url_prefix), include('{0}.urls'.format(app_name))),
            )
        except ImportError:
            logger.warn('No valid urls for {0}:{1}. Skipping app url import.'.format(project, app))

print('')
