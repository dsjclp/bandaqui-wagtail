from .base import *
import random
import string

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# Generate an ephemeral key.
SECRET_KEY = ''.join([random.SystemRandom().choice(string.printable) for i in range(50)])

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ['127.0.0.1', '.pythonanywhere.com', '.yarig.fr']

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

EMAIL_HOST = "SSL0.OVH.NET"
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = "contact@yarig.fr"
EMAIL_HOST_PASSWORD = "Jclp1999*"

#EMAIL_HOST = "smtp.gmail.com"
#EMAIL_USE_TLS = True
#EMAIL_PORT = 587
#EMAIL_HOST_USER = "dsjclp@gmail.com"
#EMAIL_HOST_PASSWORD = "dslp..."

ADMINS = [('dsjclp', 'dsjclp@gmail.com')]

SESSION_COOKIE_SECURE = True

CSRF_COOKIE_SECURE = True

SECURE_REFERRER_POLICY = 'origin'

SECURE_SSL_REDIRECT = True

SECURE_HSTS_SECONDS = 3600

SECURE_HSTS_INCLUDE_SUBDOMAINS = True

SECURE_HSTS_PRELOAD = True