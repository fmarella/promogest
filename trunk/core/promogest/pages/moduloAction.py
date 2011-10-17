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
from core.dao.Modulo import Modulo
from core.dao.ModuliAbbinati import ModuliAbbinati
from core.dao.VideoModulo import VideoModulo
from core.lib.utils import *
from core import Environment
from core.pages import *
from core.lib.session import Session
from core.lib.page import Page
from core.lib.unipath.path import *
#from core.pages.common.rssgen import rssgen

def module(req, subdomain=None, action=None):
    def moduleList(req, subdomain=None, action=None):
        item = 0
        searchword = str(req.form.get('search'))
        defaultOffset = 0
        defaultOffsetIndex = 0
        module = Modulo(req=req).select(batchSize=None)
        pageData = {'file' : 'moduleAction',
                    "subdomain": addSlash(subdomain),
                    'item': item,
                    'pag' : defaultOffsetIndex,
                    'module' : module,
    }
        return Page(req).render(pageData)

    def moduleAdd(req, subdomain="", action=None):
        """Aggiunge una pagina a contenuto statico"""
        idrr = Session(req).getUserId()
        userEnvDir = prepareUserEnv(req)
        listamoduli = Modulo().select(batchSize=None)
        module = None
        if not listamoduli:
            listamoduli=[]
        if req.args.get('new') =="":
            # Add vuoto per cui non è un aggiornamento
            module = Modulo(req=req)
            pageData = {'file' : 'moduleAction',
                        "subdomain": addSlash(subdomain),
                        "listamoduli": listamoduli,
                        "mediaAbbinati":[1,2,3,4,5],
                        'module' : module,
    }
            return Page(req).render(pageData)
        elif req.args.get("upload"):
            imgid = req.args.get('upload')
            #prepareUserEnv(req)
            f = req.files['image']
            name = f.filename
            data = f.read()
            if os.path.exists(userEnvDir+"/"+name):
                os.remove(userEnvDir+"/"+name)
            fileObj = open(userEnvDir+"/"+name ,"wb")
            fileObj.write(data)
            fileObj.close()
            im1 = Image.open(userEnvDir+"/"+name)
            #print "DFGDFHFHFHHF", im1
            im1.thumbnail ( (180,180), Image.ANTIALIAS )
            newname= 'moduleimg_'+ str(imgid)
            im1.save(Environment.CONFIGPATH+"/templates/module_img/"+newname+".png","PNG",quality=98)
            dao = Modulo(req=req).getRecord(id=imgid)
            dao.imagepath = newname+".png"
            dao.persist()
            redirectUrl=addSlash(subdomain)+'/siteAdmin/moduleAdd?edit='+str(imgid)
            return Page(req).redirect(redirectUrl)
        elif req.args.get("edit"):
            module = Modulo(req=req).getRecord(id =req.args.get("edit"))
            mediaAbbinati = VideoModulo().select(idModulo=module.id)
            ciccio = []
            for med in mediaAbbinati:
                ciccio.append(med.numero)
            for a in range(1,5):
                if a not in ciccio:mediaAbbinati.append(a)

            modulia = ModuliAbbinati().select(idModulo = module.id)
            moduliassociati = [x.id_modulo_abbinato for x in modulia]
            print "MODULI ASSOIATIIIIIIIIIIIIIIIII", moduliassociati
            pageData = {'file' : 'moduleAction',
                        "subdomain": addSlash(subdomain),
                        "listamoduli": listamoduli,
                        'mediaAbbinati':mediaAbbinati,
                        'moduliassociati': moduliassociati,
                        'module' : module,
    }
            return Page(req).render(pageData)
        elif req.args.get('add') == ""\
                        and req.form.get('moduleTitle') \
                        and req.form.get('moduleBody'):
            module = Modulo(req=req)
            pp = Modulo().select(batchSize=None)
            ultimoOrdine = max([p.ordine for p in pp])
            module.ordine = ultimoOrdine+1
        elif req.args.get('update')\
                        and req.form.get('moduleTitle') \
                        and req.form.get('moduleBody'):
            module = Modulo(req=req).getRecord(id =req.args.get("update"))
        if module:
            module.denomination = req.form.get('moduleTitle')
            module.codice = req.form.get('moduleCodice')
            module.versione = req.form.get('moduleVersione')
            module.body = req.form.get('moduleBody')
            module.abstract = req.form.get('moduleAbstract')
            module.prezzo = req.form.get('modulePrezzo') or 0
            module.prezzo_rinnovo = req.form.get('modulePrezzoRinnovo') or 0
            if req.form.get('moduleLite'):
                lite = True
            else:
                lite = False
            module.lite = lite
            if req.form.get('moduleNormal'):
                normal = True
            else:
                normal = False
            module.normal = normal
            module.permalink = permalinkaTitle(req.form.get('moduleTitle'))
            module.insertdate = datetime.datetime.now()
            #new.publication_date = datetime.datetime.utcnow()
            if req.form.get('languageId'):
                languageId = req.form.get('languageId')
                if languageId != "None":
                    module.id_language = languageId
                else:
                    module.id_language = 1
            module.persist()
            if req.form.get('categoriaId'):
                moduliassociati = req.form.getlist('categoriaId')
                oldy = ModuliAbbinati().select(idModulo = module.id)
                for o in oldy:
                    o.delete()
                for c in moduliassociati:
                    mod = ModuliAbbinati()
                    mod.id_modulo = module.id
                    mod.id_modulo_abbinato = int(c)
                    mod.persist()
            dd = VideoModulo().select(idModulo=module.id)
            for d in dd:
                d.delete()
            if req.form.get("moduleMedia1"):
                v = VideoModulo()
                v.id_modulo = module.id
                v.numero = 1
                v.testo_alternativo = "Supporto multimediale UNO per il modulo %s" %module.denomination
                v.imagepath = req.form.get("moduleMedia1")
                v.persist()
            if req.form.get("moduleMedia2"):
                v = VideoModulo()
                v.id_modulo = module.id
                v.numero = 2
                v.testo_alternativo = "Supporto multimediale DUE per il modulo %s" %module.denomination
                v.imagepath = req.form.get("moduleMedia2")
                v.persist()
            if req.form.get("moduleMedia3"):
                v = VideoModulo()
                v.id_modulo = module.id
                v.numero = 3
                v.testo_alternativo = "Supporto multimediale TRE per il modulo %s" %module.denomination
                v.imagepath = req.form.get("moduleMedia3")
                v.persist()
            if req.form.get("moduleMedia4"):
                v = VideoModulo()
                v.id_modulo = module.id
                v.numero = 4
                v.testo_alternativo = "Supporto multimediale QUATTRO per il modulo %s" %module.denomination
                v.imagepath = req.form.get("moduleMedia4")
                v.persist()
            if req.form.get("moduleMedia5"):
                v = VideoModulo()
                v.id_modulo = module.id
                v.numero = 5
                v.testo_alternativo = "Supporto multimediale CINQUE per il modulo %s" %module.denomination
                v.imagepath = req.form.get("moduleMedia5")
                v.persist()
            redirectUrl=addSlash(subdomain)+'/siteAdmin/moduleList'
            return Page(req).redirect(redirectUrl)

    def moduleDel(req, subdomain=None, action=None):
        """
        Cancella una news
        """
        moduleId = req.args.get('moduleId')
        module = Modulo(req=req).getRecord(id=moduleId)
        module.delete()
        dd = VideoModulo().select(idModulo=module.id)
        for d in dd:
            d.delete()
        oldy = ModuliAbbinati().select(idModulo = module.id)
        for o in oldy:
            o.delete()
        redirectUrl='/siteAdmin/moduleList'
        return Page(req).redirect(redirectUrl)

    def moduleActive(req,subdomain=None, action=None):
        """
        Funzione che si occupa di gestire lo stato della news
        Attivo o disattivo
        """
        moduleId = req.args.get('id')
        module = Modulo(req=req).getRecord(id=moduleId)
        if module.active==False:
            module.active = True
        else:
            module.active = False
        module.persist()
        redirectUrl='/siteAdmin/moduleList'
        return Page(req).redirect(redirectUrl)

    def modulePosition(req,subdomain=None, action=None):
        """
        Funzione che si occupa di gestire lo stato della news
        Attivo o disattivo
        """
        pp = Modulo().select(batchSize=None)
        ultimoOrdine = max([p.ordine for p in pp])
        moduleId = req.args.get('id')
        moduleOrd = req.args.get("pos")
        module = Modulo(req=req).getRecord(id=moduleId)
        vecchioOrdine = module.ordine
        if moduleOrd == "su" and module.ordine!=1:
            secondoModulo = Modulo(req=req).select(ordine= vecchioOrdine-1)
            if secondoModulo:
                secondoModulo[0].ordine = (vecchioOrdine+1000)
                secondoModulo[0].persist()
            module.ordine = vecchioOrdine-1
            module.persist()
            secondoModulo2 = Modulo(req=req).select(ordine= (vecchioOrdine+1000))
            secondoModulo2[0].ordine = vecchioOrdine
            secondoModulo2[0].persist()
        elif moduleOrd == "giu" and module.ordine!=ultimoOrdine:
            secondoModulo = Modulo(req=req).select(ordine= vecchioOrdine+1)
            if secondoModulo:
                secondoModulo[0].ordine = (vecchioOrdine+1000)
                secondoModulo[0].persist()
            module.ordine = vecchioOrdine+1
            module.persist()
            secondoModulo2 = Modulo(req=req).select(ordine= (vecchioOrdine+1000))
            secondoModulo2[0].ordine = vecchioOrdine
            secondoModulo2[0].persist()

        redirectUrl='/siteAdmin/moduleList'
        return Page(req).redirect(redirectUrl)

    if action.upper() =="MODULELIST": # sezione moduli
        return moduleList(req,subdomain=subdomain, action=action)
    elif action.upper() == "MODULEDEL":
        return moduleDel(req,subdomain=subdomain,action=action)
    elif action.upper() == "MODULEADD":
        return moduleAdd(req,subdomain=subdomain,action=action)
    elif action.upper() == "MODULEACTIVE":
        return moduleActive(req,subdomain=subdomain,action=action)
    elif action.upper() == "MODULEPOSITION":
        return modulePosition(req,subdomain=subdomain,action=action)
