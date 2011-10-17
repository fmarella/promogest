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


from promoCMS import Environment
from promoCMS.utils import Response, Request , RedirectResponse
from werkzeug.utils import *
import shutil
import os
from promoCMS.utils import *
from pages import *
from promoCMS.session import Session
from promoCMS.page import Page
#import cgi
import os
import Image
from unipath.path import *


# Ensure that the fckeditor.py is included in your classpath
#from pages.fckeditor.fckeditor import FCKeditor

class File(object):
    """
    Remember that this function is like a home_tpl.py
    """
    def __init__(self, req, level=None):
        self.req = req
        self.path = req.environ['PATH_INFO'].split('/')
        self.correctPath=['siteAdmin', "file"]
#        self.mark = "USR"
        userEnvDir= prepareUserEnv(self.req)
        self.pth = Path(userEnvDir[:-6])


    def fileList(self):

        if self.req.args.get("upload")=="1":
            f = self.req.files['imageArticle']
            name =f.filename
            data = f.read()
            fileObj = open( userEnvDir+"/"+name ,"wb")
            fileObj.write(data)
            fileObj.close()
            #resizeImgThumbnailGeneric(req=selfReq, name=name)
            redirectUrl = self.path[2]+'/'+self.path[3]+"/Add"
            return Page(self.req).redirect(redirectUrl)
        fileList = os.listdir(userEnvDir)

        pageData = {'file' : 'file',
                    'pth':self.pth,
                    'fileList' : fileList,
                    }
        return Page(self.req).render(pageData)

    def genericUpdate(self,req, level=None):
        f = req.files['imageArticle']
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

