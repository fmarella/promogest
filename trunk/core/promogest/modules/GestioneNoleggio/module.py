# -*- coding: utf-8 -*-

# Promogest
#
# Copyright (C) 2005-2009 by Promotux Informatica - http://www.promotux.it/

#import gtk, gobject
from promogest import Environment
#from promogest.ui.GladeWidget import GladeWidget
#from promogest.modules.GestioneNoleggio.data.GestioneNoleggioDB import *
#import promogest.modules.SchedaLavorazione.ui.AnagraficaAssociazioniArticoli
#from promogest.modules.GestioneNoleggio.ui.AnagraficaAssociazioniArticoli import AnagraficaAssociazioniArticoli


MODULES_NAME = "GestioneNoleggio"
MODULES_FOR_EXPORT = []
GUI_DIR = Environment.cartella_moduli+'/GestioneNoleggio/gui/'
START_CALL_IS_IN_THREAD = True        # False if you  do NOT want to put execution
START_CALL = None                              # of this call in a separated Thread
