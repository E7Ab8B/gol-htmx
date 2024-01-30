from .base import *  # noqa: F403; pylint: disable=wildcard-import,unused-wildcard-import
from .base import env

# GENERAL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#debug
DEBUG = True
# https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
SECRET_KEY = env("DJANGO_SECRET_KEY", default="&q0a9*#lfis8l+pf2uab*f+h*dt!!3+enxmpu4ff$@8stkyyuw")  # pyright: ignore
# https://docs.djangoproject.com/en/dev/ref/settings/#allowed-hosts
ALLOWED_HOSTS = ["localhost", "0.0.0.0", "127.0.0.1"]  # noqa: S104
