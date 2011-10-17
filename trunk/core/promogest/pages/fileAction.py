#-*- coding: utf-8 -*-
#
# Promogest - Janas
#
# Copyright (C) 2005 by Promotux Informatica - http://www.promotux.it/
# Author: Francesco Meloni  <francesco@promotux.it>
#
import os
import datetime
import Image
from sqlalchemy import *
from sqlalchemy.orm import *
#from core.dao.Feed import Feed
from core.lib.utils import *
from core import Environment
from core.pages import *
from core.lib.session import Session
from core.lib.page import Page
from core.lib.unipath.path import *

#from core.pages.common.rssgen import rssgen


def fileList(req, subdomain=None, action=None):
    prepareUserEnv(req)
    ruolo = getRoleFromId(req)
    #nameuser = getUsernameFromId(req)
    if ruolo =="Admin":
        filedir = os.walk(Environment.CONFIGPATH+"/templates/media/")
    else:
        filedir = userEnvDir
    item = 0

    pageData = {'file' : 'fileAction',
                "subdomain": addSlash(subdomain),
                'item': item,
                'pag' : 0,
                'filedir' : filedir,
}
    return Page(req).render(pageData)

def fileAdd(req, subdomain="", action=None):
    """Aggiunge una pagina a contenuto statico"""
    idrr = Session(req).getUserId()
    userEnvDir = prepareUserEnv(req)
    if req.args.get('new') =="":
        # Add vuoto per cui non è un aggiornamento
        feed = Feed(req=req)
        pageData = {'file' : 'feedAction',
                    "subdomain": addSlash(subdomain),
                    'feed' : feed,
}
        return Page(req).render(pageData)
    elif req.args.get("upload"):
        imgid = req.args.get('upload')
        #prepareUserEnv(req)
        f = req.files['image']
        name = f.filename
        data = f.read()
        fileObj = open(userEnvDir+"/"+name ,"wb")
        fileObj.write(data)
        fileObj.close()
        im1 = Image.open(userEnvDir+"/"+name)
        #print "DFGDFHFHFHHF", im1
        im1.thumbnail ( (128,128), Image.ANTIALIAS )
        newname= 'moduleimg_'+ str(imgid)
        im1.save(Environment.CONFIGPATH+"/templates/module_img/"+newname+".jpg","JPEG",quality=85)
        dao = Modulo(req=req).getRecord(id=imgid)
        dao.imagepath = newname
        dao.persist()
        redirectUrl=addSlash(subdomain)+'siteAdmin/moduleAdd?edit='+str(imgid)
        return Page(req).redirect(redirectUrl)
    elif req.args.get("edit"):
        feed = Feed(req=req).getRecord(id =req.args.get("edit"))
        pageData = {'file' : 'feedAction',
                    "subdomain": addSlash(subdomain),
                    'feed' : feed,
}
        return Page(req).render(pageData)
    elif req.args.get('add') == ""\
                    and req.form.get('name')\
                    and req.form.get('url'):
        feed = Feed(req=req)
    elif req.args.get('update')\
                    and req.form.get('name') \
                    and req.form.get('url'):
        feed = Feed(req=req).getRecord(id =req.args.get("update"))
    if feed:
        feed.name = req.form.get('name')
        feed.url = req.form.get('url')
        feed.persist()
        redirectUrl=addSlash(subdomain)+'/siteAdmin/feedList'
        return Page(req).redirect(redirectUrl)

def fileDel(req, subdomain=None, action=None):
    """
    Cancella una news
    """
    feedId = req.args.get('feedId')
    feed = Feed(req=req).getRecord(id=feedId)
    feed.delete()
    redirectUrl=addSlash(subdomain)+'/siteAdmin/feedList'
    return Page(req).redirect(redirectUrl)
