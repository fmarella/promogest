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

import datetime
from sqlalchemy import *
from sqlalchemy.orm import *
from promogest.lib.webutils import *
from promogest import Environment
from promogest.dao.Company import Company
#from promogest.pages import *
from promogest.lib.session import Session
from promogest.lib.page import Page
from promogest.lib.unipath.path import *
#from core.dao.CompanyCompanyCategory import CompanyCategoryCompany

def company(req, subdomain=None, action=None):

    def companylistCategorized(req):
        compcateId = req.args.get('id')
        compcatelist = CompanyCategoryCompany().select(id_company_category = compcateId)
        pageData = {'file' : 'company_list',
                   "compcatelist":compcatelist,
                    'compcateId':compcateId
                    #'fileList' : fileList
                        }
        return Page(req).render(pageData)

    def companyDetailByDenomination(req, denomination=None):
        cmpl = Company(req=req).select(denominationEM=denomination)
        if cmpl:
            azienda = cmpl[0]
            azienda.clicks = int(azienda.clicks or 0)+1
            azienda.persist()
            pageData = {'file' : 'company_detail',
                        'azienda' : azienda}
            return Page(req).render(pageData)
        else:
            pageData = {'file' : 'not_found'}
            return Page(req).render(pageData)


    def companyDetail(req):
        compId = req.args.get('id')
        azienda = Company(req=req).getRecord(id=compId)
        #ultimenews = News(req=req).select(batchSize=5)
        azienda.clicks = int(azienda.clicks or 0)+1
        azienda.persist()
        pageData = {'file' : 'company_detail',
                    'azienda' : azienda}
        return Page(req).render(pageData)

    def companyList(req, subdomain=None, action=None):
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
            companies = Company(req=req).select(denominazione = searchword,
                                            offset=defaultOffset)
            item = len(companies)
        else:
            companies = Company(req=req).select(offset=defaultOffset)
            item = len(companies)
        pageData = {'file' : 'companyAction',
                    'item': item,
                    'pag' : defaultOffsetIndex,
                    'companies' : companies,
                    #'pth':pth,
                    #'fileList' : fileList
                    }
        return Page(req).render(pageData)

    def companyAdd(req, subdomain=None, action=None):
        """
        Aggiunge una azienda
        """
        idrr = Session(req).getUserId()
        azienda = None
        aziendaedit = None
        userEnvDir = prepareUserEnv(req)
        if req.args.get('new') =="":
            # Add vuoto per cui non è un aggiornamento
            azienda = Company(req=req)
            pageData = {'file' : 'companyAction',
                        "azienda" :azienda}
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
            newname= 'companyimg_'+ str(imgid)
            im1.save(Environment.CONFIGPATH+"/templates/company_img/"+newname+".jpg","JPEG",quality=85)
            swi = Company(req=req).getRecord(id=imgid)
            swi.imagepath = newname
            swi.persist()
            redirectUrl='siteAdmin/companyAdd?edit='+str(imgid)
            return Page(req).redirect(redirectUrl)
        elif req.args.get("edit"):
            azienda = Company().getRecord(id=req.args.get("edit"))
            pageData = {'file' : 'companyAction',
                        "azienda" :azienda}
            return Page(req).render(pageData)
        elif req.args.get('add') == ""\
                    and req.form.get('social'):
            azienda = Company(req=req)
        elif req.args.get('update')\
                    and req.form.get('social'):
            azienda = Company().getRecord(id=req.args.get("update"))
        if azienda:
            azienda.social = req.form.get('social')
            azienda.ensign = req.form.get('ensign')
            azienda.firstname = req.form.get('firstname')
            azienda.lastname = req.form.get('lastname')
            azienda.iva = req.form.get('iva')
            azienda.fiscalcode = req.form.get('fiscalcode')
            azienda.address = req.form.get('address')
            azienda.cap = req.form.get('cap')
            azienda.city = req.form.get('city')
            azienda.telephone = req.form.get('telephone')
            azienda.mobile = req.form.get('mobile')
            azienda.url = req.form.get('url')
            azienda.email = req.form.get('email')
            azienda.abstract = req.form.get('abstract')
            azienda.description = req.form.get('description')
            azienda.insert_date = datetime.datetime.now()
            if req.form.get('languageId'):
                languageId = req.form.get('languageId')
                if languageId != "None":
                    azienda.id_language = languageId
                else:
                    new.id_language = 1
            if req.form.getlist('categoriaId'):
                categoriaId = req.form.getlist('categoriaId')
                if categoriaId != "None":
                    azienda.categorie = categoriaId
                    azienda.option_number = len(categoriaId)
                else:
                    azienda.categorie = "1"
                    azienda.option_number = 1
            azienda.id_user = idrr
            azienda.persist()
            redirectUrl='/siteAdmin/companyList'
            return Page(req).redirect(redirectUrl)


    def companyDel(req, subdomain=None, action=None):
        """Cancella una news"""
        compaId = req.args.get('id')
        azienda = Company(req=req).getRecord(id=compaId)
        azienda.delete()
        redirectUrl='/siteAdmin/companyList'
        return Page(req).redirect(redirectUrl)

    def companyActive(req,subdomain=None, action=None):
        """
        Funzione che si occupa di gestire lo stato della news
        Attivo o disattivo
        """
        compaId = req.args.get('id')
        azienda = Company(req=req).getRecord(id=compaId)
        if azienda.active==False:
            azienda.active = True
        else:
            azienda.active = False
        azienda.persist()
        redirectUrl='/siteAdmin/companyList'
        return Page(req).redirect(redirectUrl)

    if action.upper() =="COMPANYLIST": # sezione software
        return companyList(req,subdomain=subdomain, action=action)
    elif action.upper() == "COMPANYDEL":
        return companyDel(req,subdomain=subdomain,action=action)
    elif action.upper() == "COMPANYEDIT":
        return companyEdit(req,subdomain=subdomain,action=action)
    elif action.upper() == "COMPANYADD":
        return companyAdd(req,subdomain=subdomain,action=action)
    elif action.upper() == "COMPANYACTIVE":
        return companyActive(req,subdomain=subdomain,action=action)
