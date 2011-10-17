#-*- coding: utf-8 -*-
#
# Promogest - Janas
#
# Copyright (C) 2010 by Promotux Informatica - http://www.promotux.it/
# Author: Francesco Meloni <francesco@promotux.it>

from promogest.lib.page import Page
from promogest.dao.Promemoria import Promemoria

def promemoria(req):
    """
    Funzione di gestione delle preview
    """
    pageData = {'file' : "promemoriamain",
                "daos" : Promemoria().select(batchSize=None)
                }
    return Page(req).render(pageData)
