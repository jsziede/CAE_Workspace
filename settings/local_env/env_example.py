"""
Local settings .env example file.

Move to 'env.py' and modify to provide local overrides.

Committed values should just be example or "expected default" values.
"""


# User Class Imports.
from settings.reusable_settings import *


# Static/Media file locations.
# Static refers to CSS, JavaScript, Images, etc provided by project. Media refers to any user-uploaded files.
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static/')
MEDIA_URL = '/static/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'static/media')
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
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'), # SQlite: File Location. MySQL: Database Name.
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
        'default-character-set': 'utf8',
    }
}


# Email settings.
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'    # For SMTP, use 'backends.smtp.EmailBackend'.
EMAIL_HOST = ''                             # Ip address for SMTP email server.
EMAIL_HOST_USER = ''                        # Name for SMTP user.
EMAIL_HOST_PASSWORD = ''                    # Password for SMTP user.
EMAIL_PORT = ''                             # Port for SMTP email server.
EMAIL_USE_TLS = True                        # Explicitly uses TLS for SMTP communication.
DEFAULT_FROM_EMAIL = 'webmaster@localhost'  # Default email address for standard emails.
SERVER_EMAIL = 'root@localhost'             # Default email address for admin error emails.


# Admins to send emails to on error (Only sends if debug = False).
ADMINS = []


# # HTTPS/Security Settings. Used in production.
# SECURE_SSL_HOST = ""
# SECURE_SSL_REDIRECT = True
# CSRF_COOKIE_SECURE = True
# SESSION_COOKIE_SECURE = True
#
# SECURE_HSTS_INCLUDE_SUBDOMAINS = True
# SECURE_HSTS_SECONDS =
# SECURE_BROWSER_XSS_FILTER = True
# X_FRAME_OPTIONS = "DENY"
# SECURE_CONTENT_TYPE_NOSNIFF = True
