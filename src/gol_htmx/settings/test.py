from .base import *  # noqa: F403; pylint: disable=wildcard-import,unused-wildcard-import
from .base import env

# GENERAL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
SECRET_KEY = env(
    "DJANGO_SECRET_KEY",
    default="&!+p9w2iuugw$ck6=v)5h%qog6e3=l=eoz*mai6_4)183d@-=4",
)

# DEBUGGING FOR TEMPLATES
# ------------------------------------------------------------------------------
TEMPLATES[0]["OPTIONS"]["debug"] = True  # noqa: F405
