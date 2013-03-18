import os
import cherrypy
from os.path import join
from cherrypy.lib.static import serve_file
  
class Root(object):
    def __init__(self):
        current_path = os.path.dirname(os.path.abspath(__file__))
        self.public_html_path = join(current_path,'..', 'public_html') 
        
    def index(self):
        return serve_file(join(self.public_html_path, 'index.html'), 'r')
    
    index.exposed = True
