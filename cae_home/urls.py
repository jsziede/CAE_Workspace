"""
Urls for CAE_Home App.
"""

from django.conf.urls import url

from . import views


app_name = 'cae_home'
urlpatterns = [
    # Home page.
    url(r'^$', views.index, name='index')
]
