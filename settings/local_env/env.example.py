"""
Example .env file.
Copy as "env.py" and edit values.

Provided values are just an example and may not necessarily work as is.
"""


# User Class Imports.
from settings.reusable_settings import *


# Static/Media file locations.
# Static refers to CSS, JavaScript, Images, etc provided by project. Media refers to any user-uploaded files.
STATIC_URL = '/static/'
STATIC_ROOT = '/static/'
MEDIA_URL = '/static/media/'
MEDIA_ROOT = '/static/media'
STATICFILES_DIRS = (
    # Path to any additional, non-standard static directories.
)


# Allowed server hosts.
ALLOWED_HOSTS = [
    # List of domain names the project can serve. Helps prevent HTTP Host Header attacks.
]


# Database connection information.
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}
