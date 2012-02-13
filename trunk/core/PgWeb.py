# -*- coding: utf-8 -*-

#    Copyright (C) 2005-2012 by Promotux
#                        di Francesco Meloni snc - http://www.promotux.it/

#    Author: Francesco Meloni  <francesco@promotux.it>

#    This file is part of Promogest.

#    Promogest is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 2 of the License, or
#    (at your option) any later version.

#    Promogest is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

#    You should have received a copy of the GNU General Public License
#    along with Promogest.  If not, see <http://www.gnu.org/licenses/>.

import os, signal
import locale
import gettext
from werkzeug import Request, SharedDataMiddleware, ClosingIterator
from werkzeug.utils import escape
from werkzeug import SharedDataMiddleware
from werkzeug.debug import DebuggedApplication
from werkzeug.exceptions import HTTPException, NotFound
from wsgiref.simple_server import make_server

from promogest import Environment
from promogest.lib.page import Page
from promogest.lib.webutils import url_map, jinja_env, setconf
from promogest.lib import routes

class Pg2_web(object):

    def __init__(self):
        Environment.local.application = self
        try:
            if not (os.path.exists("cache")):
                    os.mkdir("cache")
            if not (os.path.exists("session")):
                    os.mkdir("session")
        except:
            print "pazienza"

        #TODO: eventuale gestione modulare successiva come nel pg
        #self.importModulesFromDir(modules_dir="./promogest/pages/modules")
        #Aggiungo le directory di lavoro ...
        self.dispatch = SharedDataMiddleware(self.dispatch, {
            '/templates/': Environment.STATIC_PATH,
            '/feed': Environment.STATIC_PATH_FEED,
        })


    def importModulesFromDir(self, modules_dir):
        """Check the modules directory and automatically try to load
        all available modules

        """
        #global jinja_env
        Environment.modulesList=[Environment.tipo_pg]
        modules_folders = [folder for folder in os.listdir(modules_dir) \
                        if (os.path.isdir(os.path.join(modules_dir, folder)) \
                        and os.path.isfile(os.path.join(modules_dir, folder, 'module.py')))]
        Environment.modules_folders = modules_folders

        for m_str in modules_folders:
            if hasattr(Environment.conf,m_str) or setconf(m_str,"mod_enable", value="yes"):
                try:
                    exec "mod_enable = getattr(Environment.conf.%s,'mod_enable')" %m_str
                except:
                    mod_enable = setconf(m_str,"mod_enable", value="yes")
                if mod_enable:
                    try:
                        exec "mod_enableyes = getattr(Environment.conf.%s,'mod_enable','yes')" %m_str
                    except:
                        mod_enableyes="yes"
                    if mod_enableyes=="yes":
                        stringa= "%s.%s.module" % (modules_dir.replace("/", "."), m_str)
                        m= __import__(stringa, globals(), locals(), ["m"], -1)
                        Environment.modulesList.append(str(m.MODULES_NAME))
                        #if hasattr(m,"TEMPLATES"):
                            #HtmlHandler.templates_dir.append(m.TEMPLATES)
                        for class_name in m.MODULES_FOR_EXPORT:
                            exec 'module = m.'+ class_name
                            self.modules[class_name] = {
                                                'module': module(),
                                                'type': module.VIEW_TYPE[0],
                                                'module_dir': "%s" % (m_str),
                                                'guiDir':m.GUI_DIR}


    def dispatch(self, environ, start_response):
        """ Funzione importante per la gestione dello smistamento della request

        """
        Environment.local.application = self
        req = Request(environ)
        Environment.local.url_adapter = adapter = url_map.bind_to_environ(environ)
        try:
            endpoint, values = adapter.match()
            handler = getattr(routes, endpoint)
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
                               [Environment.local_manager.cleanup])

    def __call__(self, environ, start_response):
        return self.dispatch(environ, start_response)

    def not_found(self,req):
        pageData = {'file' : 'not_found'}
        return Page(req).render(pageData)
