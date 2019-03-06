"""
CAE Workspace Middleware.
"""

import pytz

from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.utils import timezone

from cae_home import models


class SetTimezoneMiddleware(object):
    """
    Allows views to auto-convert from UTC to user's timezone.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request, *args, **kwargs):
        # Attempt to set timezone for user in all views.
        tzname = None
        if request.user.is_authenticated:
            tzname = request.user.profile.user_timezone
        if tzname:
            timezone.activate(pytz.timezone(tzname))
        else:
            timezone.deactivate()

        # Resume view call as normal.
        response = self.get_response(request)
        return response


class GetProjectDetailMiddleware(object):
    """
    Passes project detail information to all views.

    Note: To function properly, all views must use "TemplateResponse" instead of "Render"
          Views should also provide an object dictionary even in the event that they pass no data (such as an index).
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request, *args, **kwargs):
        response = self.get_response(request)
        return response

    def process_template_response(self, request, response):
        # Get site domain.
        response.context_data['domain'] = get_current_site(request)

        # Get installed project/app details.
        response.context_data['imported_projects'] = settings.INSTALLED_APP_DETAILS

        return response


class GetUserSiteOptionsMiddleware(object):
    """
    Gets site theme for all views.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request, *args, **kwargs):
        #Resume view call as normal.
        response = self.get_response(request)
        return response

    def process_template_response(self, request, response):
        if request.user.is_authenticated:
            # User authenticated. Attempt to get user's model.
            response.context_data['site_theme'] = request.user.profile.site_theme
            response.context_data['desktop_font_size'] = request.user.profile.get_desktop_font_size()
            response.context_data['mobile_font_size'] = request.user.profile.get_mobile_font_size()
        else:
            # Default to "wmu" site theme.
            response.context_data['site_theme'] = models.SiteTheme.objects.get(name='wmu')
            response.context_data['desktop_font_size'] = 'base'
            response.context_data['mobile_font_size'] = 'base'

        return response
