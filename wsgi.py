#!/usr/bin/pyhon
# -*- coding: utf-8 -*- 

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

cherrypy.config.update({'environment': 'embedded'})

from webengine.application import Root

application = cherrypy.Application(Root(), script_name=None, config=None)