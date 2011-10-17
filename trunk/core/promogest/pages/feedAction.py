#-*- coding: utf-8 -*-
#
# Promogest - Janas
#
# Copyright (C) 2005 by Promotux Informatica - http://www.promotux.it/
# Author: Francesco Meloni  <francesco@promotux.it>
#

import datetime
import Image
from sqlalchemy import *
from sqlalchemy.orm import *
from core.dao.Feed import Feed
from core.lib.utils import *
from core import Environment
from core.pages import *
from core.lib.session import Session
from core.lib.page import Page
from core.lib.unipath.path import *
#from core.pages.common.rssgen import rssgen

def feed(req, subdomain=None, action=None):

    def feedList(req, subdomain=None, action=None):
        #rssgen(req) # creo il file dei feeds
        item = 0
        searchword = str(req.form.get('search'))
        defaultOffset = 0
        #try:
            #defaultOffsetIndex = int(self.req.args.get('pag'))-1
            #if defaultOffsetIndex == 0:
                #defaultOffset = 0
            #else:
                #defaultOffset = defaultOffsetIndex * Environment.params['defaultLimit']
        #except:
        defaultOffsetIndex = 0
        if searchword != "None":
            feeds = Feed().select(denominazionec = searchword,
                                        offset=defaultOffset)
            item = len(feed)
        else:
            feeds = Feed().select(offset=defaultOffset)

        pageData = {'file' : 'feedAction',
                    "subdomain": addSlash(subdomain),
                    'item': item,
                    'pag' : defaultOffsetIndex,
                    'feeds' : feeds,
                    #'pth':pth,
                    #'fileList' : fileList
    }
        return Page(req).render(pageData)

    def feedAdd(req, subdomain="", action=None):
        """Aggiunge una pagina a contenuto statico"""
        idrr = Session(req).getUserId()
        userEnvDir= prepareUserEnv(req)
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

    def feedDel(req, subdomain=None, action=None):
        """
        Cancella una news
        """
        feedId = req.args.get('feedId')
        feed = Feed(req=req).getRecord(id=feedId)
        feed.delete()
        redirectUrl=addSlash(subdomain)+'/siteAdmin/feedList'
        return Page(req).redirect(redirectUrl)

    def feedActive(req,subdomain=None, action=None):
        """
        Funzione che si occupa di gestire lo stato della news
        Attivo o disattivo
        """
        feedId = req.args.get('id')
        feed = Feed(req=req).getRecord(id=feedId)
        if feed.active==False:
            feed.active = True
            if not feed.insert_date:
                feed.insert_date = datetime.datetime.now()
        else:
            feed.active = False
        feed.persist()
        redirectUrl=addSlash(subdomain)+'/siteAdmin/feedList'
        return Page(req).redirect(redirectUrl)

    if action.upper() =="FEEDLIST": # sezione moduli
        return feedList(req,subdomain=subdomain, action=action)
    elif action.upper() == "FEEDDEL":
        return feedDel(req,subdomain=subdomain,action=action)
    elif action.upper() == "FEEDADD":
        return feedAdd(req,subdomain=subdomain,action=action)
    elif action.upper() == "FEEDACTIVE":
        return feedActive(req,subdomain=subdomain,action=action)
