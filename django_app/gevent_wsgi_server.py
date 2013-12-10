from gevent import monkey; monkey.patch_all()
import logging
log = logging.getLogger(__name__)

import os
import traceback
import sys
from gevent.pywsgi import WSGIServer

from django.core.handlers.wsgi import WSGIHandler
from django.core.signals import got_request_exception

os.environ['DJANGO_SETTINGS_MODULE'] = 'django_app.settings'

def exception_printer(sender, **kwargs):
    traceback.print_exc()
got_request_exception.connect(exception_printer)

PORT = 8600
if len(sys.argv) > 1:
    PORT = int(sys.argv[1])

print 'Serving on %d...' % PORT
WSGIServer(('', PORT), WSGIHandler(), backlog = 4096).serve_forever()
