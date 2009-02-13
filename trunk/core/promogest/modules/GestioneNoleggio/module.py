# -*- coding: utf-8 -*-

# Promogest
#
# Copyright (C) 2005-2009 by Promotux Informatica - http://www.promotux.it/

#import gtk, gobject
from promogest import Environment
#from promogest.ui.GladeWidget import GladeWidget
from promogest.modules.GestioneNoleggio.data.GestioneNoleggioDB import *
#import promogest.modules.SchedaLavorazione.ui.AnagraficaAssociazioniArticoli
#from promogest.modules.GestioneNoleggio.ui.AnagraficaAssociazioniArticoli import AnagraficaAssociazioniArticoli


MODULES_NAME = "GestioneNoleggio"
MODULES_FOR_EXPORT = []
GUI_DIR = getattr(Environment.conf.Moduli, 'cartella_moduli', 'promogest/modules')+'/GestioneNoleggio/gui/'
START_CALL_IS_IN_THREAD = True        # False if you  do NOT want to put execution
START_CALL = None                              # of this call in a separated Thread


#class AssociazioniArticoli(object):
    #VIEW_TYPE = ('anagrafica', 'Associazioni Articoli', 'associazione_articolo24x24.png')
    #def getApplication(self):
        #anag = AnagraficaAssociazioniArticoli()
        #return anag

#class CaratteriStampa(object):
    #VIEW_TYPE = ('parametro', 'Caratteri Stampa', 'caratteri_stampa24x24.png')
    #def getApplication(self):
        #anag = AnagraficaCaratteriStampa()
        #return anag

#class ColoriStampa(object):
    #VIEW_TYPE = ('parametro', 'Colori Stampa', 'colori_stampa24x24.png')
    #def getApplication(self):
        #anag = AnagraficaColoriStampa()
        #return anag

#class SchedeLavorazione(object):
    #VIEW_TYPE = ('anagrafica_diretta', 'Schede\nLavorazione', 'scheda_lavorazione48x48.png')
    #def getApplication(self):
        #anag = AnagraficaSchedeOrdinazioni()
        #return anag

