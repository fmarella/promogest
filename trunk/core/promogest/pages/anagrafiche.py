#-*- coding: utf-8 -*-
#
# Promogest - Janas
#
# Copyright (C) 2010 by Promotux Informatica - http://www.promotux.it/
# Author: Francesco Meloni <francesco@promotux.it>

from promogest.lib.page import Page

def anagrafiche(req):
    """
    Funzione di gestione delle preview
    """
    promowear = False
    pageData = {'file' : "anagrafiche",
                'pw': promowear}
    return Page(req).render(pageData)
