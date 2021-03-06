import os
import re
import cherrypy
from cherrypy import HTTPError
from os.path import join, basename
from cherrypy.lib.static import serve_file

"""
  This module provides the WSGI application core which is build on top
  of a CherryPy application.
"""

class Root(object):
    def __init__(self):
        current_path = os.path.dirname(os.path.abspath(__file__))
        self.public_html_path = join(current_path,'..', 'public_html')

    @cherrypy.expose
    def index(self, page=1):
        page_nr = int(page)
        fname = join(self.public_html_path, 'index.html.%d' % page_nr)
        return serve_file(fname)

    @cherrypy.expose
    def game(self, *args):
        if len(args) < 1:
            raise cherrypy.HTTPError(404)
        game_name = basename(args[0])
        print game_name
        if not re.match('^[0-9a-z.]+$', game_name):
            raise cherrypy.HTTPError(404)
        fname = join(self.public_html_path, 'products', '%s.html' % game_name)
        return serve_file(fname)



def _enable_base_staticapp(app):
    current_path = os.path.dirname(os.path.abspath(__file__))
    base_static = ('js', 'css')
    conf = {}
    for dir in base_static:
        conf['/'+dir] = {\
                'tools.staticdir.on': True
                ,'tools.staticdir.dir': os.path.join(current_path
                , '..', 'templates', dir)
                }
    conf['/thumbs'] =  {\
                'tools.staticdir.on': True
                ,'tools.staticdir.dir': os.path.join(current_path
                , '..', 'public_html', 'thumbs')
                }
    conf['/media'] =  {\
                'tools.staticdir.on': True
                ,'tools.staticdir.dir': os.path.join(current_path
                , '..', 'data', 'media')
                }
    app.merge(conf)

def _base_config():
    cherrypy.config.update({'tools.encode.on': True,
                            'tools.encode.encoding': 'utf-8'})

application = cherrypy.Application(Root(), script_name=None, config=None)
_base_config()
_enable_base_staticapp(application)
