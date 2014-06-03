import os
import sys

path = '/home/insane/graphite_hosting'
if path not in sys.path:
    sys.path.append(path)
#sys.path.append('/home/insane')

os.environ['DJANGO_SETTINGS_MODULE'] = 'graphite_hosting.settings'
#os.environ.setdefault("DJANGO_SETTINGS_MODULE", "graphite_hosting.settings")
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
