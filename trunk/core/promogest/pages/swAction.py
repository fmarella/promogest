#-*- coding: utf-8 -*-
#
# Promogest - Janas
#
# Copyright (C) 2005 by Promotux Informatica - http://www.promotux.it/
# Author: Andrea Maccis <amaccis@promotux.it>
#

import datetime
from sqlalchemy import *
from sqlalchemy.orm import *
from core.dao.Software import Software
from core.dao.SoftwareCategory import SoftwareCategory
from core.dao.SoftwareSoftwareCategory import SoftwareCategorySoftware
from core.lib.utils import *
from core import Environment
from core.pages import *
from core.lib.session import Session
from core.lib.page import Page
from core.lib.unipath.path import *

def sw(req, subdomain=None, action=None):

    def swlistCategorized(req):
        swcateId = req.args.get('id')
        swcatelist = SoftwareCategorySoftware().select(id_software_category = swcateId)
        pageData = {'file' : 'software_list',
                   "swcatelist":swcatelist,
                    'swcateId':swcateId
                    #'fileList' : fileList
                        }
        return Page(req).render(pageData)

    def swDetail(req):
        swId = req.args.get('id')
        sw = Software(req=req).getRecord(id=swId)
        #ultimenews = News(req=req).select(batchSize=5)
        sw.clicks = int(sw.clicks or 0)+1
        sw.persist()
        pageData = {'file' : 'software_detail',
                    'swdetail' : sw,
                    #'ultimenews' :ultimenews,
                    #'pth':pth,
                    'swid':swId,
                    #'fileList' : fileList
                        }
        return Page(req).render(pageData)

    def swDetailByDenomination(req, denomination=None):
        swl = Software(req=req).select(denominationEM=denomination)
        if swl:
            sw = swl[0]
            sw.clicks = int(sw.clicks or 0)+1
            sw.persist()
            pageData = {'file' : 'software_detail',
                        'swdetail' : sw,
    }
            return Page(req).render(pageData)
        else:
            pageData = {'file' : 'not_found',
    }
            return Page(req).render(pageData)


    def swList(req, subdomain=None, action=None):
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
            sws = Software(req=req).select(denominazionec = searchword,
                                                offset=defaultOffset)
            item = len(sws)
        else:
            sws = Software(req=req).select(offset=defaultOffset)
        pageData = {'file' : 'swAction',
                    'item': item,
                    'pag' : defaultOffsetIndex,
                    'sws' : sws,
                    #'pth':pth,
                    #'fileList' : fileList
    }
        return Page(req).render(pageData)

    def swAdd(req, subdomain=None, action=None):
        """Aggiunge una pagina a contenuto statico"""
        idrr = Session(req).getUserId()
        userEnvDir = prepareUserEnv(req)
        fileList = os.listdir(userEnvDir)
        #categories = SoftwareCategory().select()
        if req.args.get('new') =="":
            # Add vuoto per cui non è un aggiornamento
            sw = Software(req=req)
            pageData = {'file' : 'swAction',
                        'sw' : sw,
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
            im1.thumbnail ( (128,128), Image.ANTIALIAS )
            newname= 'swimg_'+ str(imgid)
            im1.save(Environment.CONFIGPATH+"/templates/software_img/"+newname+".jpg","JPEG",quality=85)
            swi = Software(req=req).getRecord(id=imgid)
            swi.imagepath = newname
            swi.persist()
            redirectUrl='siteAdmin/swAdd?edit='+str(imgid)
            return Page(req).redirect(redirectUrl)
        elif req.args.get("edit"):
            sw = Software(req=req).getRecord(id =req.args.get("edit"))
            pageData = {'file' : 'swAction',
                        'sw' : sw,
    }
            return Page(req).render(pageData)
        elif req.args.get('add') == ""\
                    and req.form.get('denomination')\
                    and req.form.get('description'):
            sw = Software(req=req)
        elif req.args.get('update')\
                    and req.form.get('denomination')\
                    and req.form.get('description'):
            sw = Software(req=req).getRecord(id =req.args.get("update"))
        if sw:
            sw.denomination = req.form.get('denomination')
            sw.description = req.form.get('description')
            sw.abstract = req.form.get('abstract')
            sw.license = req.form.get('license')
            sw.versione = req.form.get('release')
            sw.opensource = req.form.get('opensource')
            #new.permalink = permalinkaTitle(req.form.get('newsTitle'))
            sw.url = req.form.get('url')
            sw.email = req.form.get('email')
            sw.insert_date = datetime.datetime.now()
            #new.publication_date = datetime.datetime.utcnow()
            if req.form.get('languageId'):
                languageId = req.form.get('languageId')
                if languageId != "None":
                    sw.id_language = languageId
                else:
                    sw.id_language = 1
            if req.form.getlist('categoriaId'):
                categoriaId = req.form.getlist('categoriaId')
                if categoriaId != "None":
                    sw.categorie = categoriaId
                else:
                    sw.categorie = "1"
            sw.id_user = idrr
            sw.persist()
            redirectUrl='/siteAdmin/swList'
            return Page(req).redirect(redirectUrl)


    def swDel(req, subdomain=None, action=None):
        """Cancella una news"""
        swId = req.args.get('swId')
        sw = Software(req=req).getRecord(id=swId)
        sw.delete()
        redirectUrl='/siteAdmin/swList'
        return Page(req).redirect(redirectUrl)

    def swActive(req,subdomain=None, action=None):
        """
        Funzione che si occupa di gestire lo stato della news
        Attivo o disattivo
        """
        swId = req.args.get('id')
        sw = Software(req=req).getRecord(id=swId)
        if sw.active==False:
            sw.active = True
            #if not news.publication_date:
                #news.publication_date = datetime.datetime.now()
        else:
            sw.active = False
        sw.persist()
        redirectUrl='/siteAdmin/swList'
        return Page(req).redirect(redirectUrl)

    if action.upper() =="SWLIST": # sezione software
        return swList(req,subdomain=subdomain, action=action)
    elif action.upper() == "SWDEL":
        return swDel(req,subdomain=subdomain,action=action)
    elif action.upper() == "SWADD":
        return swAdd(req,subdomain=subdomain,action=action)
    elif action.upper() == "SWACTIVE":
        return swActive(req,subdomain=subdomain,action=action)
