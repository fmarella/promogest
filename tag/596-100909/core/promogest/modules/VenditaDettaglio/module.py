# -*- coding: utf-8 -*-

# Promogest
#
# Copyright (C) 2005-2008 by Promotux Informatica - http://www.promotux.it/

from promogest import Environment
import promogest.ui.Login
from promogest.modules.VenditaDettaglio.data.VenditaDettaglioDB import *
from promogest.modules.VenditaDettaglio.ui.AnagraficaVenditaDettaglio import AnagraficaVenditaDettaglio

MODULES_NAME = "VenditaDettaglio"
MODULES_FOR_EXPORT = ['VenditaDettaglio']
GUI_DIR = getattr(Environment.conf.Moduli, 
                'cartella_moduli', 'promogest/modules')+'/VenditaDettaglio/gui/'
START_CALL_IS_IN_THREAD = True        # False if you  do NOT want to put execution
START_CALL = None                              # of this call in a separated Thread

"""
    view_type è composto da:

    0 TIPO : 'type' ( opzioni possibili sono: anagrafica, parametro,
                                     anagrafica_diretta, frame, permanent_frame)
    1 TITOLO o LABEL
    2 ICONS :
    es:
        VIEW_TYPE = ('parametro', 'Colori Stampa', 'colori_stampa24x24.png')
"""
#testataMovimentoTable = Table('testata_movimento', params['metadata'], autoload=True, schema=params['schema'])

class VenditaDettaglio(object):
    VIEW_TYPE = ('anagrafica_diretta', 'Vendita Dettaglio',
                                                    'vendita_dettaglio48x48.png')
    def getApplication(self):
        anag = AnagraficaVenditaDettaglio()
        return anag
