from website.settings.common import *
# print("BASE_DIR : ", BASE_DIR)

# SECRET_KEY = 'r4$tlly+kl=(vbt2eiwf*%4)4341z%e(&ua*c6)a7s$h3fvn0m'
SECRET_KEY = SECRET_KEY


print("SECRET_KEY : ", SECRET_KEY)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]
STATIC_URL = '/static/'



CSRF_COOKIE_SECURE = False
SESSION_COOKIE_SECURE = False
SECURE_SSL_REDIRECT = False
SECURE_CONTENT_TYPE_NOSNIFF = False
SECURE_BROWSER_XSS_FILTER = False