from pathlib import Path

from .environment import env

BASE_DIR = Path(__file__).resolve().parent.parent


def rel(*path):
    return BASE_DIR.joinpath(*path)


DEBUG = env.bool("RECIPER_DEBUG", default=False)

INTERNAL_IPS = env.list("RECIPER_INTERNAL_IPS", default=[])

ALLOWED_HOSTS = env.list("RECIPER_ALLOWED_HOSTS", default=[])

SECRET_KEY = env.str("RECIPER_SECRET_KEY")

INSTALLED_APPS = [
                     # Django apps
                     "django.contrib.admin",
                     "django.contrib.auth",
                     "django.contrib.contenttypes",
                     "django.contrib.sessions",
                     "django.contrib.sites",
                     "django.contrib.messages",
                     "django.contrib.staticfiles",
                     # Third-party apps
                     "django_extensions",
                     "django_filters",
                     "drf_spectacular",
                     "rest_framework",
                     # First-party apps
                     "reciper.apps.common",
                     "reciper.apps.accounts",
                     "reciper.apps.recipes",
                     "reciper.apps.shopping",
                     "reciper.apps.tips",
                 ] + env.list("RECIPER_DEV_INSTALLED_APPS", default=[])

MIDDLEWARE = [
                 "django.middleware.security.SecurityMiddleware",
                 "django.contrib.sessions.middleware.SessionMiddleware",
                 "django.middleware.common.CommonMiddleware",
                 "django.middleware.csrf.CsrfViewMiddleware",
                 "django.contrib.auth.middleware.AuthenticationMiddleware",
                 "django.contrib.messages.middleware.MessageMiddleware",
                 "django.middleware.clickjacking.XFrameOptionsMiddleware",
             ] + env.list("RECIPER_DEV_MIDDLEWARE", default=[])

ROOT_URLCONF = "reciper.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [rel("templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ]
        },
    }
]

WSGI_APPLICATION = "reciper.wsgi.application"

DATABASES = {
    "default": env.db("RECIPER_DATABASE_URL"),
}

AUTH_USER_MODEL = "accounts.UserAccount"

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

SECURE_CONTENT_TYPE_NOSNIFF = env.bool("RECIPER_SECURE_CONTENT_TYPE_NOSNIFF", default=True)
SECURE_HSTS_SECONDS = env.int("RECIPER_SECURE_HSTS_SECONDS", default=31536000)  # 1 year

SESSION_COOKIE_HTTPONLY = env.bool("RECIPER_SESSION_COOKIE_HTTPONLY", default=True)
SESSION_COOKIE_SECURE = env.bool("RECIPER_SESSION_COOKIE_SECURE", default=True)
SESSION_COOKIE_NAME = "s"

CSRF_COOKIE_SECURE = env.bool("RECIPER_CSRF_COOKIE_SECURE", default=True)
CSRF_COOKIE_NAME = "c"

X_FRAME_OPTIONS = env.str("RECIPER_X_FRAME_OPTIONS", default="SAMEORIGIN")

LANGUAGE_CODE = "en-us"

TIME_ZONE = env.str("RECIPER_TIME_ZONE", default="UTC")

USE_I18N = True

USE_TZ = True

LOCALE_PATHS = [rel("..", "..", "api", "locale")]

STATIC_URL = env.str("RECIPER_STATIC_URL", default="/static/")
MEDIA_URL = env.str("RECIPER_MEDIA_URL", default="/media/")

# STATIC_FILES_DIRS = [rel("static_root")]
STATIC_ROOT = rel("static_root")

SITE_ID = env.int("RECIPER_SITE_ID", default=1)

USE_X_FORWARDED_HOST = True

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

APPEND_SLASH = False

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
