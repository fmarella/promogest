# -*- coding: utf-8 -*-

#    Copyright (C) 2005, 2006, 2007 2008, 2009, 2010 by Promotux
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

import hashlib
import time
from promogest import Environment
from promogest.lib.webutils import *
from promogest.lib.page import Page
#from core.lib.MailHandler import SendMail
from promogest.dao.Province import Province
from promogest.dao.Regioni import Regioni
#from promogest.dao.Subdomain import Subdomain
#from core.dao.PersonaGiuridica import PersonaGiuridica_ as PersonaGiuridica
#from core.dao.User import User
#from core.dao.News import News
import Image,ImageDraw
from random import randint as rint
import ImageFont

def theme_setup(req,action=None, static=None, subdomain=None):
    ruolo = getRoleFromId(req)
    #nameuser = getUsernameFromId(req)
    #print "LLLLLLLLLLLLLLLLL" , req.form.get("theme")
    if req.form.get("theme"):
        tema = req.form.get("theme")
        if tema:
            Environment.conf.Project.template = tema
            Environment.conf.save()
        #redirectUrl = '/siteAdmin'
        #return Page(req).redirect(redirectUrl)
    if ruolo =="Admin":
        filedir = os.listdir(Environment.CONFIGPATH+"/templates/theme/")
    else:
        filedir = userEnvDir

    pageData = {'file' : 'theme_setup',
        "subdomain": addSlash(subdomain),
        'filedir' : filedir,
}
    return Page(req).render(pageData)


def subs_setup(req,action=None, static=None, subdomain=None):
    """ funzione di creazione di nuovi subdomain con abbinamento di temi"""
    subss = Subdomain().select(batchSize=None)
    print "SUUUUUUUUUUBSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS", subss
    pageData = {'file' : 'subs_setup',
                "subdomain": addSlash(subdomain),
                "subs":subss
}
    return Page(req).render(pageData)


def mainSetup(req,action=None, static=None, subdomain=None):
    parameters = Environment.conf._configDict
    #print dir(parameters)
    #print parameters._configDict
    #cd = parameters.sections()
    #for c in parameters:
        #print c , dir(c)
    pageData = {'file' : 'main_setup',
            "subdomain": addSlash(subdomain),
            'parameters' : parameters,
    }
    return Page(req).render(pageData)
