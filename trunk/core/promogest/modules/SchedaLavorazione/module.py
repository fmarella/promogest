# -*- coding: utf-8 -*-

# Promogest
#
# Copyright (C) 2005 by Promotux Informatica - http://www.promotux.it/

from promogest import Environment
from promogest.ui.GladeWidget import GladeWidget
from promogest.modules.SchedaLavorazione.data.SchedeLavorazioneDB import *
#import promogest.modules.SchedaLavorazione.ui.AnagraficaAssociazioniArticoli
#from promogest.modules.SchedaLavorazione.ui.AnagraficaAssociazioniArticoli import AnagraficaAssociazioniArticoli
import promogest.modules.SchedaLavorazione.ui.AnagraficaCaratteriStampa
from promogest.modules.SchedaLavorazione.ui.AnagraficaCaratteriStampa import AnagraficaCaratteriStampa
import promogest.modules.SchedaLavorazione.ui.AnagraficaColoriStampa
from promogest.modules.SchedaLavorazione.ui.AnagraficaColoriStampa import AnagraficaColoriStampa
from promogest.modules.SchedaLavorazione.ui.AnagraficaSchedeOrdinazioni import AnagraficaSchedeOrdinazioni
from promogest.modules.SchedaLavorazione.ui.SchedaLavorazioneUtils import *

MODULES_NAME = "SchedaLavorazione"
MODULES_FOR_EXPORT = ['CaratteriStampa','ColoriStampa','SchedeLavorazione']
GUI_DIR = Environment.cartella_moduli+'/SchedaLavorazione/gui/'
START_CALL_IS_IN_THREAD = True        # False if you  do NOT want to put execution
START_CALL = None                              # of this call in a separated Thread
TEMPLATES = Environment.cartella_moduli+"/SchedaLavorazione/templates/"

class CaratteriStampa(object):
    VIEW_TYPE = ('parametro', 'Caratteri Stampa', 'caratteri_stampa24x24.png')
    def getApplication(self):
        anag = AnagraficaCaratteriStampa()
        return anag

class ColoriStampa(object):
    VIEW_TYPE = ('parametro', 'Colori Stampa', 'colori_stampa24x24.png')
    def getApplication(self):
        anag = AnagraficaColoriStampa()
        return anag

class SchedeLavorazione(object):
    VIEW_TYPE = ('anagrafica_diretta', 'Schede\nLavorazione', 'scheda_lavorazione48x48.png')
    def getApplication(self):
        anag = AnagraficaSchedeOrdinazioni()
        return anag
