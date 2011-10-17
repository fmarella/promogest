#-*- coding: utf-8 -*-
#
# Promogest - Janas
#
# Copyright (C) 2005 by Promotux Informatica - http://www.promotux.it/
# Author: Andrea Maccis <amaccis@promotux.it>
# Author: Francesco Meloni <francesco@promotux.it>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.

import sha, time, datetime

from core.pages import *
from core import Environment
from core.lib.utils import *
from core.lib.session import Session

class Error(object):


    def __init__(self, req):
        loader = TemplateLoader([Environment.templates_dir])
        self.path = req.environ['PATH_INFO'].split('/')
        self.tmpl = loader.load( self.path[1] + '/index.html')
        self.auth = Session().control(req)
#        self.itemsStaticMenu = StaticMenuAction(req).index(req, embedded=True)
        self.rowsCompany= Login(req).index(req, embedded=True)


    def index(self,req,level=None,error=None):
        stream = self.tmpl.generate(auth=self.auth,
                                    path=self.path,
                                    rowsFamily=rowFamilyAndCount(req),
#                                    itemsStaticMenu = self.itemsStaticMenu,
                                    error=error,
                                    file='error')

        resp = Response(stream.render('xhtml'))
        cookiename = self.path[1]+'id'
        if not req.cookies.has_key(cookiename):
            cookieval = sha.new(repr(time.time())).hexdigest()
            resp.set_cookie(cookiename, value=cookieval, path='/')
        return resp
