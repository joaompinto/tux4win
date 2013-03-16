#!/usr/bin/pyhon
# -*- coding: utf-8 -*- 

from cherrypy import wsgiserver
import wsgi

__author__ = "João Pinto"
__copyright__ = "Copyright 2013, João Pinto"
__credits__ = ["João Pinto"]
__license__ = "GPL-3"
__version__ = "1.0"
__maintainer__ = "João Pinto"
__email__ = "lamego.pinto@gmail.com"
__status__ = "Production"


server = wsgiserver.CherryPyWSGIServer(
            ('0.0.0.0', 8070), wsgi.application)
server.start()