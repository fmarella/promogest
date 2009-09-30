# -*- coding: utf-8 -*-
#
# Promogest
#
# Copyright (C) 2005-2008 by Promotux Informatica - http://www.promotux.it/

from promogest import Environment
#import promogest.ui.Login
#from promogest.modules.DistintaBase.data.DistintaBaseDB import *
from promogest.modules.Calendario.ui.Calendario import Calendario

MODULES_NAME = "Calendario"
MODULES_FOR_EXPORT = ["Calendari"]
GUI_DIR = getattr(Environment.conf.Moduli, 'cartella_moduli', 'promogest/modules')+'/Calendario/gui/'
START_CALL_IS_IN_THREAD = True        # False if you  do NOT want to put execution
START_CALL = None                              # of this call in a separated Thread
TEMPLATES = getattr(Environment.conf.Moduli, 'cartella_moduli', 'promogest/modules')+'/Calendario/templates/'

"""
    view_type è composto da:

    0 TIPO : 'type' ( opzioni possibili sono: anagrafica, parametro, anagrafica_diretta, frame, permanent_frame)
    1 TITOLO o LABEL
    2 ICONS :
    es:
        VIEW_TYPE = ('parametro', 'Colori Stampa', 'colori_stampa24x24.png')
"""
#testataMovimentoTable = Table('testata_movimento', params['metadata'], autoload=True, schema=params['schema'])

class Calendari(object):
    VIEW_TYPE = ('anagrafica_diretta', 'Calendario ', 'calendar.svg')
    def getApplication(self):
        anag = Calendario()
        return anag

