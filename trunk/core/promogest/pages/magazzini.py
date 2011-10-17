#-*- coding: utf-8 -*-
#
# Promogest - Janas
#
# Copyright (C) 2010 by Promotux Informatica - http://www.promotux.it/
# Author: Francesco Meloni <francesco@promotux.it>

from promogest.lib.page import Page
from promogest.dao.Magazzino import Magazzino

def magazzini(req):
    """
    Funzione di gestione delle preview
    """
    daos = Magazzino().select(batchSize=None)
    pageData = {'file' : "magazzini",
                'daos': daos}
    return Page(req).render(pageData)
