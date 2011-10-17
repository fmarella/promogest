#-*- coding: utf-8 -*-
#
# Promogest - Janas
#
# Copyright (C) 2005 by Promotux Informatica - http://www.promotux.it/
# Author: Francesco Meloni  <francesco@promotux.it>
#
from sqlalchemy import *
from sqlalchemy.orm import *
from core.lib.utils import *
from core.dao.News import News
from core.pages import *
from core.lib.page import Page
from core.lib.unipath.path import *
import math

def newsDetailByDenomination(req,subdomain=None, denomination=None):
    news = News(req=req).select(permalink=denomination, active=True)
    ultimenews = News().select(batchSize=5, active=True)
    if news:
        mo = news[0]
        mo.clicks = int(mo.clicks or 0)+1
        mo.persist()
        pageData = {'file' : 'news_detail',
                    "subdomain": subdomain,
                    "ultimenews":ultimenews,
                    "news":mo}
        return Page(req).render(pageData)
    else:
        pageData = {'file' : 'not_found'}
        return Page(req).render(pageData)

def newss_list(req, static=None, subdomain=""):
    count = News().count(searchkey=req.form.get('searchkey'))
    batch = 10
    args = pagination(req,batch,count)
    args["page_list"] = subdomain.template+"/news_list_home"
    newss = News().select(batchSize=batch,offset=args["offset"],active=True)
    pageData = {'file' : 'news_list_home',
                "subdomain": subdomain,
                "args":args,
                "newss" :newss}
    return Page(req).render(pageData)
