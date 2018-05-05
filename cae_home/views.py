"""
Views for CAE_Home App.
"""

from django.shortcuts import render


def index(request):
    """
    Home page for website.
    """
    return render(request, 'cae_home/index.html')
