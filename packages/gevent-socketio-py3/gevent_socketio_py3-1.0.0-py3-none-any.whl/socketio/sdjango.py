import logging

from socketio import socketio_manage
import django
from django.conf.urls import url
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

try:
    # Django versions >= 1.9
    from django.utils.module_loading import import_module
except ImportError:
    # Django versions < 1.9
    from django.utils.importlib import import_module


SOCKETIO_NS = {}


LOADING_SOCKETIO = False


def autodiscover():
    """
    Auto-discover INSTALLED_APPS sockets.py modules and fail silently when
    not present. NOTE: socketio_autodiscover was inspired/copied from
    django.contrib.admin autodiscover
    """
    global LOADING_SOCKETIO
    if LOADING_SOCKETIO:
        return
    LOADING_SOCKETIO = True

    import imp
    from django.conf import settings

    for app in settings.INSTALLED_APPS:

        try:
            app_path = import_module(app).__path__
        except AttributeError:
            continue

        try:
            imp.find_module('sockets', app_path)
        except ImportError:
            continue

        import_module("%s.sockets" % app)

    LOADING_SOCKETIO = False


class namespace(object):
    def __init__(self, name=''):
        self.name = name

    def __call__(self, handler):
        SOCKETIO_NS[self.name] = handler
        return handler


@csrf_exempt
def socketio(request):
    try:
        socketio_manage(request.environ, SOCKETIO_NS, request)
    except:
        logging.getLogger("socketio").error("Exception while handling socketio connection", exc_info=True)
    return HttpResponse("")


if django.VERSION >= (1, 8,):
    urls = [url(r'', socketio)]
else:
    from django.conf.urls import patterns
    urls = patterns("", (r'', socketio))
