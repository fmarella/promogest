#!/usr/bin/python
#-*- coding: utf-8 -*-
#
#PromoWeb
#
# Copyright (C) 2009 by Promotux Informatica - http://www.promotux.it
# Author: Francesco Meloni <francesco@promotux.it>

import os, signal
import locale
import gettext
from werkzeug import Request, SharedDataMiddleware, ClosingIterator
from core.lib.page import Page
from werkzeug.utils import escape
from werkzeug.utils import SharedDataMiddleware
from werkzeug.debug import DebuggedApplication
from werkzeug.exceptions import HTTPException, NotFound
from wsgiref.simple_server import make_server
from core.Environment import *
from core.pages import views
from core.lib.utils import *

class Janas(object):

    def __init__(self):
        local.application = self
        self.importModulesFromDir(modules_dir="core/pages/modules")
        self.dispatch = SharedDataMiddleware(self.dispatch, {
            '/templates/': STATIC_PATH,
            '/feed': STATIC_PATH_FEED,
        })


    def importModulesFromDir(self, modules_dir=None):
        """
        Check the modules directory and automatically try to load all available modules
        """
        Environment.modulesList=[]
        modules_folders = [folder for folder in os.listdir(modules_dir) \
                        if (os.path.isdir(os.path.join(modules_dir, folder)) \
                        and os.path.isfile(os.path.join(modules_dir, folder, 'module.py')))]
        for m_str in modules_folders:
            #if hasattr(Environment.conf,m_str):
                #exec "mod_enable = hasattr(Environment.conf.%s,'mod_enable')" %m_str
                #if mod_enable:
                    #exec "mod_enableyes = getattr(Environment.conf.%s,'mod_enable','yes')" %m_str
                    #if mod_enableyes=="yes":
            stringa = "%s.%s.module" % (modules_dir.replace("/", "."), m_str)
            m= __import__(stringa, globals(), locals(), ["m"], -1)
            Environment.modulesList.append(str(m.MODULES_NAME))
            for class_name in m.MODULES_FOR_EXPORT:
                exec 'module = m.'+ class_name
                self.modules[class_name] = {
                                    'module': module(),
                                    'type': module.VIEW_TYPE[0],
                                    'module_dir': "%s" % (m_str),
                                    'guiDir':m.GUI_DIR
}
        print "LISTA DEI MODULI CARICATI E FUNZIONANTI", repr(Environment.modulesList)
        #self.groupModulesByType()

    def dispatch(self, environ, start_response):
        local.application = self
        req = Request(environ)
        local.url_adapter = adapter = url_map.bind_to_environ(environ)
        try:
            endpoint, values = adapter.match()
            handler = getattr(views, endpoint)
            jinja_env.globals['req'] = req
            pathList = req.path.split('/')
            jinja_env.globals['path'] = pathList
            #print "req.path --->",  req.path
            #print "req.script_root --->", req.script_root
            #print "req.url --->", req.url
            #print "req.base_url --->", req.base_url
            #print "req.url_root --->", req.url_root
            #print "req.host_url --->", req.host_url
            #print "req.host --->", req.host_url
            #print "req.remote_addr --->", req.remote_addr
            #print "pathList --->", pathList
            response = handler(req, **values)
        except NotFound, e:
            response = self.not_found(req)
            response.status_code = 404
        except HTTPException, e:
            response = e
        return ClosingIterator(response(environ, start_response),
                               [local_manager.cleanup])

    def __call__(self, environ, start_response):
        return self.dispatch(environ, start_response)

    def not_found(self,req):
        pageData = {'file' : 'not_found',
    }
        return Page(req).render(pageData)
