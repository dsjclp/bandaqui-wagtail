from .base import *
import random
import string

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# DJANGO_SECRET_KEY *should* be specified in the environment. If it's not, generate an ephemeral key.
if 'DJANGO_SECRET_KEY' in os.environ:
    SECRET_KEY = os.environ['DJANGO_SECRET_KEY']
else:
    # Use if/else rather than a default value to avoid calculating this if we don't need it
    print("WARNING: DJANGO_SECRET_KEY not found in os.environ. Generating ephemeral SECRET_KEY.")
    SECRET_KEY = ''.join([random.SystemRandom().choice(string.printable) for i in range(50)])

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ['127.0.0.1', '.pythonanywhere.com', '.yarig.fr']

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

EMAIL_HOST = "SSL0.OVH.NET"
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = "contact@yarig.fr"
EMAIL_HOST_PASSWORD = "Jclp1999*"

ADMINS = [('dsjclp', 'dsjclp@gmail.com')]