from website.settings.common import *


SECRET_KEY = 'r4$tlly+kl=(vbt2eiwf*%4)4341z%e(&ua*c6)a7s$h3fvn0m'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

STATICFILES_DIRS = [
    os.path.normpath(os.path.join(BASE_DIR, 'static')),
]