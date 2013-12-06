import os
import sys
import settings
import socket
import logging
logger = logging.getLogger(__name__)

def set_local():
    pass

def set_test():
    settings.DATABASES['default']['ENGINE'] = 'django.db.backends.sqlite3'
    settings.USE_TZ = True

#===============================================================================
# CONFIGURE environment
#===============================================================================
def configure(environment_type = None):
    if not environment_type:
        environment_type = os.environ.get('SERVER_ENVIRONMENT', 'LOCAL')

        for arg in sys.argv:
            if 'test' in arg or 'nose' in arg:
                environment_type = 'TEST'
                break
    settings.SERVER_ENVIRONMENT = environment_type.upper()
    if 'TEST' == settings.SERVER_ENVIRONMENT:
        set_test()
    else:
        set_local()

