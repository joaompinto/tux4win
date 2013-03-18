#!/usr/bin/pyhon
# -*- coding: utf-8 -*- 

import os
import sys
import cherrypy

__author__ = "João Pinto"
__copyright__ = "Copyright 2013, João Pinto"
__credits__ = ["João Pinto"]
__license__ = "GPL-3"
__version__ = "1.0"
__maintainer__ = "João Pinto"
__email__ = "lamego.pinto@gmail.com"
__status__ = "Production"

sys.stdout = sys.stderr

def _enable_base_static():
    current_path = os.path.dirname(os.path.abspath(__file__))    
    base_static = ('js', 'css')
    conf = {}
    for dir in base_static:
        conf['/'+dir] = {\
                'tools.staticdir.on': True
                ,'tools.staticdir.dir': os.path.join(current_path
                , 'templates', dir)
                }
    conf['media'] =  {\
                'tools.staticdir.on': True
                ,'tools.staticdir.dir': os.path.join(current_path
                , 'media')
                }
    cherrypy.config.update(conf)
    
cherrypy.config.update({'environment': 'embedded'})
_enable_base_static()

from webengine.application import Root

application = cherrypy.Application(Root(), script_name=None, config=None)