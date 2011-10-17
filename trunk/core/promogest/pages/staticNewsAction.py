#-*- coding: utf-8 -*-
#
# Promogest - Janas
#
# Copyright (C) 2005 by Promotux Informatica - http://www.promotux.it/
#

import datetime
import Image
from sqlalchemy import *
from sqlalchemy.orm import *
from core.dao.News import News
from core.dao.NewsCategory import NewsCategory
from core.lib.utils import *
from core import Environment
from core.pages import *
from core.lib.session import Session
from core.lib.page import Page
from core.lib.unipath.path import *
from core.pages.common.rssgen import rssgen


def news(req,subdomain=None, action=None):

    def newsDetail(req):
        newsId = req.args.get('id')
        news = News(req=req).getRecord(id=newsId)
        if not news:
            pageData = {'file' : 'not_found'}
            return Page(req).render(pageData)
        ultimenews = News(req=req).select(batchSize=10)
        news.clicks = int(news.clicks or 0)+1
        news.persist()
        pageData = {'file' : 'news_detail',
                    'news' : news,
                    'ultimenews' :ultimenews,
                    'newsid':newsId}
        return Page(req).render(pageData)

    def newsList(req, subdomain=None, action=None):
        batch = 50
        count = News().count(searchkey=req.form.get('searchkey'))
        args = pagination(req,batch,count)
        args["page_list"] = "siteAdmin/newsList"
        newslist = News().select(searchkey=req.form.get('searchkey'),
                                    batchSize=batch,
                                    offset=args["offset"])

        pageData = {'file' : 'newsAction',
                    "args":args,
                    'news' : newslist}
        return Page(req).render(pageData)

    def newsAdd(req, subdomain=None, action=None):
        """Aggiunge una pagina a contenuto statico"""
        idrr = Session(req).getUserId()
        userEnvDir = prepareUserEnv(req)
        newsCategory = NewsCategory().select()
        if req.args.get('new') =="":
            # Add vuoto per cui non è un aggiornamento
            news = News(req=req)
            pageData = {'file' : 'newsAction',
                        'newsCategory' : newsCategory,
                        'news' : news}
            rssgen(req)
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
            newname= 'newsimg_'+ str(imgid)
            im1.save(Environment.CONFIGPATH+"/templates/news_img/"+newname+".jpg","JPEG",quality=85)
            dao = News(req=req).getRecord(id=imgid)
            dao.imagepath = newname
            dao.persist()
            redirectUrl='siteAdmin/newsAdd?edit='+str(imgid)
            return Page(req).redirect(redirectUrl)
        elif req.args.get("edit"):
            news = News(req=req).getRecord(id =req.args.get("edit"))
            pageData = {'file' : 'newsAction',
                        'newsCategory':newsCategory,
                        'news' : news}
            rssgen(req)
            return Page(req).render(pageData)
        elif req.args.get('add') == ""\
                        and req.form.get('newsTitle') \
                        and req.form.get('newsBody'):
            news = News(req=req)
        elif req.args.get('update')\
                        and req.form.get('newsTitle') \
                        and req.form.get('newsBody'):
            news = News(req=req).getRecord(id =req.args.get("update"))
        if news:
            news.title = req.form.get('newsTitle')
            news.body = req.form.get('newsBody')
            news.abstract = req.form.get('newsAbstract')
            news.permalink = permalinkaTitle(req.form.get('newsTitle'))
            news.source_url = req.form.get('newsSourceUrl')
            news.source_url_alt_text = req.form.get('newsSourceUrlAltText')
            news.insert_date = datetime.datetime.now()
            #new.publication_date = datetime.datetime.utcnow()
            if req.form.get('languageId'):
                languageId = req.form.get('languageId')
                if languageId != "None":
                    news.id_language = languageId
                else:
                    new.id_language = 1
            if req.form.get('categoriaId'):
                categoriaId = req.form.get('categoriaId')
                if categoriaId != "None":
                    news.id_categoria = categoriaId
                else:
                    news.id_categoria = 1
            news.id_user = idrr
            news.persist()
            rssgen(req) # creo il file dei feeds
            redirectUrl='/siteAdmin/newsList'
            return Page(req).redirect(redirectUrl)

    def newsDel(req, subdomain=None, action=None):
        """
        Cancella una news
        """
        newsId = req.args.get('newsId')
        news = News(req=req).getRecord(id=newsId)
        news.delete()
        redirectUrl='/siteAdmin/newsList'
        return Page(req).redirect(redirectUrl)

    def newsActive(req,subdomain=None, action=None):
        """
        Funzione che si occupa di gestire lo stato della news
        Attivo o disattivo
        """
        newsId = req.args.get('id')
        news = News(req=req).getRecord(id=newsId)
        if news.active==False:
            news.active = True
            if not news.publication_date:
                news.publication_date = datetime.datetime.now()
        else:
            news.active = False
        news.persist()
        redirectUrl='/siteAdmin/newsList'
        return Page(req).redirect(redirectUrl)

    if action.upper() =="NEWSLIST": # sezione News
        return newsList(req,subdomain=subdomain, action=action)
    elif action.upper() == "NEWSDEL":
        return newsDel(req,subdomain=subdomain,action=action)
    elif action.upper() == "NEWSEDIT":
        return newsEdit(req,subdomain=subdomain,action=action)
    elif action.upper() == "NEWSADD":
        return newsAdd(req,subdomain=subdomain,action=action)
    elif action.upper() == "NEWSACTIVE":
        return newsActive(req,subdomain=subdomain,action=action)
