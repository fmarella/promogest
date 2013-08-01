#!/usr/bin/python
#-*- coding: utf-8 -*-
#
# Janas
#
# Copyright (C) 2009 by Promotux Informatica - http://www.promotux.it/
# Author: Francesco Meloni <francesco@promotux.it>

import os, signal
import locale
import gettext
from werkzeug import Request, SharedDataMiddleware, ClosingIterator

#from werkzeug.routing import Map, Rule, NotFound, RequestRedirect
from werkzeug.utils import escape
from werkzeug.utils import SharedDataMiddleware
from werkzeug.debug import DebuggedApplication
from werkzeug.exceptions import HTTPException, NotFound
from wsgiref.simple_server import make_server
from core.Environment import *
from core import views

#comandi Localizzazione
# pybabel extract -F ngs_mappingfile.ini ./ -o ngsresine.pot
# pybabel init -i ngsresine.pot -l en -d ./lang/
# pybabel compile -d ./lang/



class Janas(object):

    def __init__(self):
        local.application = self
        #self.database_engine = engine
        #self.dispatch = SharedDataMiddleware(self.dispatch, {
            #'/static':  STATIC_PATH
        #})
    #def init_database(self):
        #meta
        ##metadata.create_all(self.database_engine)
    def dispatch(self, environ, start_response):
        local.application = self
        request = Request(environ)
        local.url_adapter = adapter = url_map.bind_to_environ(environ)
        try:
            endpoint, values = adapter.match()
            handler = getattr(views, endpoint)
            response = handler(request, **values)
        except NotFound, e:
            response = views.not_found(request)
            response.status_code = 404
        except HTTPException, e:
            response = e
        return ClosingIterator(response(environ, start_response),
                               [local_manager.cleanup])

    def __call__(self, environ, start_response):
        return self.dispatch(environ, start_response)
