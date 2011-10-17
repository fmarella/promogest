#-*- coding: utf-8 -*-
#
# Promogest - Janas
#
# Copyright (C) 2010 by Promotux Informatica - http://www.promotux.it/
# Author: Francesco Meloni <francesco@promotux.it>

from promogest.lib.page import Page
from promogest.dao.Promemoria import Promemoria

def mainpage(req, subdomain=None):
    """
    Main
    """
    prome = Promemoria().select(batchSize=None)
    pageData = {'file' : "mainpage",
                "promemoria":prome}
    return Page(req).render(pageData)
