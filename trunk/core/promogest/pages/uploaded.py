#-*- coding: utf-8 -*-
#
# Promogest - Janas
#
# Copyright (C) 2005 by Promotux Informatica - http://www.promotux.it/
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


from core import Environment
from core.lib.utils import Response, Request , RedirectResponse
from werkzeug.utils import *
import shutil
import os
from core.pages import *

class Uploaded(object):
    """
    Remember that this function is like a home_tpl.py
    """
    def __init__(self, req, level=None):
        loader = TemplateLoader([Environment.templates_dir])
        self.path = req.environ['PATH_INFO'].split('/')
        self.tmpl = loader.load( self.path[1] + '/index.html')
        self.auth = Session().control(req)
        self.itemsStaticMenu = StaticMenuAction(req).index(req, embedded=True)
        self.rowsCompany= Login(req).index(req, embedded=True)


    def index(self, req, level=None):
        print 'uno'
        if req.args.get("ArticleImg")=="artimg":
            print 'due'
            self.articleImg(req, level=level)
        else:
            print 'tre'
            self.genericUpdate(req, level=level)



    def genericUpdate(self,req, level=None):
        f = req.files['uploaded_file']
        name =f.filename
        data = f.read()
        subdomainUrl = Environment.templates_dir + Environment.subdomain
        fileObj = open(subdomainUrl + "/filesUpdated/" + name ,"wb")
        fileObj.write(data)
        fileObj.close()
        #shutil.move('./'+ name,pathImg+ name)

        #rowsCompany= Login().index(req, embedded=True)
        stream = self.tmpl.generate(
                        auth = self.auth,
                        file='main',
                        path = self.path,
                        #itemsStaticMenu = itemsStaticMenu,
                        #rowsCompany = rowsCompany,
                        nameuser=getUsernamenFromId(req))
        #return Response(f.read(), mimetype=f.content_type)
        #return Response(stream.render('xhtml'))
        return RedirectResponse('./')

    def articleImg(self,req, level=None):
        f = req.files['imageArticle']
        name =f.filename
        data = f.read()
        subdomainUrl = Environment.templates_dir + Environment.subdomain
        fileObj = open(subdomainUrl + "/images/" + name ,"wb")
        fileObj.write(data)
        fileObj.close()
        stream = self.tmpl.generate(
                        auth = self.auth,
                        file='main',
                        path = self.path,
                        #itemsStaticMenu = itemsStaticMenu,
                        #rowsCompany = rowsCompany,
                        nameuser=getUsernamenFromId(req))
        #return Response(f.read(), mimetype=f.content_type)
        #return Response(stream.render('xhtml'))
        Article(req).index(req, level=level)

        #return RedirectResponse('../../')
