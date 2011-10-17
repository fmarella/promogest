#-*- coding: utf-8 -*-
#
# Promogest - Janas
#
# Copyright (C) 2005-2009 by Promotux Informatica - http://www.promotux.it/
# Author: Francesco Meloni <francesco@promotux.it>

from core.lib.page import Page
from core.lib.utils import addSlash, permalinkaTitle
#from core.dao.StaticPages import StaticPages

def staticpages(req,pages=None, subdomain=None):
    """ Funzione per la visualizzazione pagine statiche
    """
    staticPages = StaticPages(req=req).select(permalink=pages)
    if not staticPages:
        staticPages = StaticPages(req=req).select(titlePage=pages)
        if staticPages:
            staticPages[0].permalink = permalinkaTitle(pages)
            staticPages[0].persist()
    if staticPages:
        staticPages = staticPages[0]
    pageData = {'file' : 'static',
                "subdomain": subdomain,
                'staticPages' : staticPages,
                "bodyTags":["staticPages"]}
    return Page(req).render(pageData)
