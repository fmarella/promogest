#-*- coding: utf-8 -*-
#
# Promogest - Janas
#
# Copyright (C) 2010 by Promotux Informatica - http://www.promotux.it/
# Author: Francesco Meloni <francesco@promotux.it>

from promogest.lib.page import Page
from promogest.dao.Articolo import Articolo

def anagraficaArticoli(req, action=None):
    """
    Funzione di gestione delle preview
    """
    def _list_(req):
        daos = Articolo(req=req).select()
        promowear = False
        pageData = {'file' : "anagraficaArticoli",
                    'pw': promowear,
                    "daos":daos}
        return Page(req).render(pageData)


    if action=="list":
        return _list_(req)
