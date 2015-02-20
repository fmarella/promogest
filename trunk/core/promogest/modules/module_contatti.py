# -*- coding: utf-8 -*-

# Promogest
#
# Copyright (C) 2005-2008 by Promotux Informatica - http://www.promotux.it/

from promogest.ui.Contatti.AnagraficaContatti import AnagraficaContatti

MODULES_NAME = "Contatti"
MODULES_FOR_EXPORT = ['Contatti']
GUI_DIR = 'gui/'
START_CALL_IS_IN_THREAD = True        # False if you  do NOT want to put execution
START_CALL = None                              # of this call in a separated Thread


class Contatti(object):
    VIEW_TYPE = ('anagrafica_diretta', 'Contatti', 'address_book.png')
    def getApplication(self):
        anag = AnagraficaContatti()
        return anag
