#-*- coding: utf-8 -*-
#
#Promogest
#
# Copyright (C) 2005 by Promotux Informatica - http://www.promotux.it/
# Author: Francesco Meloni  <francesco@promotux.it>
#
import os
import datetime
import Image
from sqlalchemy import *
from sqlalchemy.orm import *
from core.dao.Servizio import Servizio
from core.lib.utils import *
from core import Environment
from core.pages import *
from core.lib.session import Session
from core.lib.page import Page
from core.lib.unipath.path import *
#from core.pages.common.rssgen import rssgen

def service(req, subdomain=None, action=None):

    def serviceList(req, subdomain=None, action=None):
        item = 0
        searchword = str(req.form.get('search'))
        defaultOffset = 0
        defaultOffsetIndex = 0
        service = Servizio(req=req).select(batchSize=None)
        pageData = {'file' : 'serviceAction',
                    "subdomain": addSlash(subdomain),
                    'item': item,
                    'pag' : defaultOffsetIndex,
                    'services' : service}
        return Page(req).render(pageData)

    def serviceAdd(req, subdomain="", action=None):
        """Aggiunge una pagina a contenuto statico"""
        idrr = Session(req).getUserId()
        promogestDir = prepareUserEnv(req)
        listaservizi = Servizio().select(batchSize=None)
        if req.args.get('new') =="":
            # Add vuoto per cui non è un aggiornamento
            service = Servizio(req=req)
            pageData = {'file' : 'serviceAction',
                        "subdomain": addSlash(subdomain),
                        'service' : service}
            return Page(req).render(pageData)
        elif req.args.get("upload"):
            imgid = req.args.get('upload')
            #prepareUserEnv(req)
            f = req.files['image']
            name = f.filename
            data = f.read()
            if os.path.exists(promogestDir+"/"+name):
                os.remove(promogestDir+"/"+name)
            fileObj = open(promogestDir+"/"+name ,"wb")
            fileObj.write(data)
            fileObj.close()
            im1 = Image.open(promogestDir+"/"+name)
            #print "DFGDFHFHFHHF", im1
            im1.thumbnail ( (180,180), Image.ANTIALIAS )
            newname= 'serviceimg_'+ str(imgid)
            im1.save(Environment.CONFIGPATH+"/templates/service_img/"+newname+".png","PNG",quality=98)
            dao = Modulo(req=req).getRecord(id=imgid)
            dao.imagepath = newname+".png"
            dao.persist()
            redirectUrl=addSlash(subdomain)+'/siteAdmin/serviceAdd?edit='+str(imgid)
            return Page(req).redirect(redirectUrl)
        elif req.args.get("edit"):
            service = Servizio(req=req).getRecord(id =req.args.get("edit"))
            pageData = {'file' : 'serviceAction',
                        "subdomain": addSlash(subdomain),
                        'service' : service}
            return Page(req).render(pageData)
        elif req.args.get('add') == ""\
                        and req.form.get('serviceTitle') \
                        and req.form.get('serviceAbstract'):
            service = Servizio(req=req)
        elif req.args.get('update')\
                        and req.form.get('serviceTitle') \
                        and req.form.get('serviceAbstract'):
            service = Servizio(req=req).getRecord(id =req.args.get("update"))
        if service:
            service.denomination = req.form.get('serviceTitle')
            service.codice = req.form.get('serviceCodice')
            service.body = req.form.get('serviceBody')
            service.abstract = req.form.get('serviceAbstract')
            service.prezzo = req.form.get('servicePrezzo') or 0
            service.prezzo_rinnovo = req.form.get('servicePrezzoRinnovo') or 0
            pp = Servizio().select(batchSize=None)
            ultimoOrdine = max([p.ordine for p in pp])
            service.ordine = ultimoOrdine+1
            service.permalink = permalinkaTitle(req.form.get('serviceTitle'))
            service.persist()
            redirectUrl=addSlash(subdomain)+'/siteAdmin/serviceList'
            return Page(req).redirect(redirectUrl)

    def serviceDel(req, subdomain=None, action=None):
        """
        Cancella una news
        """
        serviceId = req.args.get('serviceId')
        service = Servizio(req=req).getRecord(id=serviceId)
        service.delete()
        redirectUrl='/siteAdmin/serviceList'
        return Page(req).redirect(redirectUrl)

    def serviceActive(req,subdomain=None, action=None):
        """
        Funzione che si occupa di gestire lo stato della news
        Attivo o disattivo
        """
        serviceId = req.args.get('id')
        service = Servizio(req=req).getRecord(id=serviceId)
        if service.active==False:
            service.active = True
        else:
            service.active = False
        service.persist()
        redirectUrl='/siteAdmin/serviceList'
        return Page(req).redirect(redirectUrl)

    def servicePosition(req,subdomain=None, action=None):
        """
        Funzione che si occupa di gestire lo stato della news
        Attivo o disattivo
        """
        pp = Servizio().select(batchSize=None)
        ultimoOrdine = max([p.ordine for p in pp])
        serviceId = req.args.get('id')
        serviceOrd = req.args.get("pos")
        service = Servizio(req=req).getRecord(id=serviceId)
        vecchioOrdine = service.ordine
        if serviceOrd == "su" and service.ordine!=1:
            secondoServizio = Servizio(req=req).select(ordine= vecchioOrdine-1)
            if secondoServizio:
                secondoServizio[0].ordine = (vecchioOrdine+1000)
                secondoServizio[0].persist()
            service.ordine = vecchioOrdine-1
            service.persist()
            secondoServizio2 = Servizio(req=req).select(ordine= (vecchioOrdine+1000))
            secondoServizio2[0].ordine = vecchioOrdine
            secondoservizio2[0].persist()
        elif serviceOrd == "giu" and service.ordine!=ultimoOrdine:
            secondoServizio = Servizio(req=req).select(ordine= vecchioOrdine+1)
            if secondoServizio:
                secondoServizio[0].ordine = (vecchioOrdine+1000)
                secondoServizio[0].persist()
            service.ordine = vecchioOrdine+1
            service.persist()
            secondoServizio2 = Servizio(req=req).select(ordine= (vecchioOrdine+1000))
            secondoServizio2[0].ordine = vecchioOrdine
            secondoServizio2[0].persist()

        redirectUrl='/siteAdmin/serviceList'
        return Page(req).redirect(redirectUrl)


    if action.upper() =="SERVICELIST": # sezione moduli
        return serviceList(req,subdomain=subdomain, action=action)
    elif action.upper() == "SERVICEDEL":
        return serviceDel(req,subdomain=subdomain,action=action)
    elif action.upper() == "SERVICEADD":
        return serviceAdd(req,subdomain=subdomain,action=action)
    elif action.upper() == "SERVICEACTIVE":
        return serviceActive(req,subdomain=subdomain,action=action)
    elif action.upper() == "SERVICEPOSITION":
        return servicePosition(req,subdomain=subdomain,action=action)
