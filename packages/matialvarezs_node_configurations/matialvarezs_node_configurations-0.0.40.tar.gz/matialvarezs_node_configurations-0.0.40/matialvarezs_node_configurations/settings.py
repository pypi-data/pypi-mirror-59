from django.conf import settings
from django.utils.translation import ugettext as _
import os


DEBUG = getattr(settings, 'DEBUG')
BASE_DIR = getattr(settings, 'BASE_DIR')
STRING_SINGLE = getattr(settings, 'STRING_SINGLE')
STRING_SHORT = getattr(settings, 'STRING_SHORT')
STRING_MEDIUM = getattr(settings, 'STRING_MEDIUM')
STRING_NORMAL = getattr(settings, 'STRING_NORMAL')
STRING_LONG = getattr(settings, 'STRING_LONG')
STRING_DOUBLE = getattr(settings, 'STRING_DOUBLE')
HOST = getattr(settings, 'HOST')
SUBDOMAINS = getattr(settings, 'SUBDOMAINS')
PROTOCOL = getattr(settings, 'PROTOCOL')
HOSTNAME = getattr(settings, 'HOSTNAME')
WEBSITE_URL = getattr(settings, 'WEBSITE_URL')
STATIC_URL = getattr(settings, 'STATIC_URL')
STATIC_ROOT = getattr(settings, 'STATIC_ROOT')
MEDIA_URL = getattr(settings, 'MEDIA_URL')
MEDIA_ROOT = getattr(settings, 'MEDIA_ROOT')
ADMINS = getattr(settings, 'ADMINS', [])

APP = 'MATIALVAREZS_NODE_CONFIGURATIONS_'

VARIABLE = getattr(settings, APP + 'VARIABLE', None)


NETWORK_INTERFACE = getattr(settings,APP+'NETWORK_INTERFACE',None)
NODE_TYPE = getattr(settings,APP+'NODE_TYPE',None)
MASTER_VAL_STATUS = getattr(settings,APP+'MASTER_VAL_STATUS',None)
KEEP_RUNNING_MASTER_VAL = getattr(settings,APP+'KEEP_RUNNING_MASTER_VAL',None)
CURRENT_IRRIGATION_SECTOR = getattr(settings,APP+'CURRENT_IRRIGATION_SECTOR',None)


app = 'NETWORK_'

EDR_NODE_PROTOCOL = getattr(settings, app + 'EDR_NODE_PROTOCOL',None)
EDR_NODE_API_PORT = getattr(settings, app + 'EDR_NODE_API_PORT',None)