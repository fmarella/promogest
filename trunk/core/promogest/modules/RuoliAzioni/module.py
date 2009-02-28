# -*- coding: utf-8 -*-

# Promogest
#
# Copyright (C) 2005-2008 by Promotux Informatica - http://www.promotux.it/

from promogest import Environment
import promogest.ui.Login
from promogest.modules.RuoliAzioni.ui.AnagraficaRuoli import AnagraficaRuoli
from promogest.modules.RuoliAzioni.ui.AnagraficaUtenti import AnagraficaUtenti
from promogest.modules.RuoliAzioni.ui.ManageRoleAction import ManageRuoloAzioni




MODULES_NAME = "RuoliAzioni"
MODULES_FOR_EXPORT = ['Ruoli',"Utenti","RuoliAzioni"]
GUI_DIR = getattr(Environment.conf.Moduli, 'cartella_moduli', 'promogest/modules')+'/RuoliAzioni/gui/'
START_CALL_IS_IN_THREAD = True        # False if you  do NOT want to put execution
START_CALL = None                              # of this call in a separated Thread

"""
    view_type è composto da:

    0 TIPO : 'type' ( opzioni possibili sono: anagrafica, parametro, anagrafica_diretta, frame, permanent_frame)
    1 TITOLO o LABEL
    2 ICONS :
    es:
        VIEW_TYPE = ('parametro', 'Colori Stampa', 'colori_stampa24x24.png')
"""
#testataMovimentoTable = Table('testata_movimento', params['metadata'], autoload=True, schema=params['schema'])

class Ruoli(object):
    VIEW_TYPE = ('parametro', 'Anagrafica Ruoli', 'ruori_48.png')
    def getApplication(self):
        anag = AnagraficaRuoli()
        return anag

class Utenti(object):
    VIEW_TYPE = ('parametro', 'Anagrafica Utenti', 'utenti_48.png')
    def getApplication(self):
        anag = AnagraficaUtenti()
        return anag

class RuoliAzioni(object):
    VIEW_TYPE = ('parametro', 'Anagrafica RuoliAzioni', 'utenti_ruoli_48.png')
    def getApplication(self):
        anag = ManageRuoloAzioni()
        return anag

