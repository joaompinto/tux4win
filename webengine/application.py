import os
import cherrypy
from os.path import join
from cherrypy.lib.static import serve_file

"""
  This module provides the WSGI application core which is build on top
  of a CherryPy application.
"""
  
class Root(object):
    def __init__(self):
        current_path = os.path.dirname(os.path.abspath(__file__))
        self.public_html_path = join(current_path,'..', 'public_html') 
        
    def index(self):
        return serve_file(join(self.public_html_path, 'index.html'))
    
    index.exposed = True

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
    app.merge(conf)
        
application = cherrypy.Application(Root(), script_name=None, config=None)
_enable_base_staticapp(application)

