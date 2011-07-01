# -*- coding: utf-8 -*-

# Promogest
#
# Copyright (C) 2005-2008 by Promotux Informatica - http://www.promotux.it/

from promogest import Environment
#from promogest.ui.GladeWidget import GladeWidget
#import promogest.ui.Login
if hasattr(Environment.conf, "PromoWear")\
            and getattr(Environment.conf.PromoWear,'mod_enable')=="yes"\
            and hasattr(Environment.conf.PromoWear,'primoavvio')\
            and getattr(Environment.conf.PromoWear,'primoavvio')=="yes"\
            and Environment.tipodb !="sqlite":
    from promogest.modules.PromoWear.data.PromoWearDB import *
from promogest.modules.PromoWear.ui.AnagraficaColori import AnagraficaColori
from promogest.modules.PromoWear.ui.AnagraficaGruppiTaglia import AnagraficaGruppiTaglia
from promogest.modules.PromoWear.ui.AnagraficaTaglie import AnagraficaTaglie
from promogest.modules.PromoWear.ui.AnagraficaModelli import AnagraficaModelli
from promogest.modules.PromoWear.ui.TaglieColori import GestioneTaglieColori
from promogest.modules.PromoWear.ui.PromowearUtils import *

MODULES_NAME = "PromoWear"
MODULES_FOR_EXPORT = ['Taglie', 'Colori','GruppiTaglia', 'Modelli']
GUI_DIR = Environment.cartella_moduli+'/PromoWear/gui/'
#COMPANY = Environment.conf.PromoWear.company_name
START_CALL_IS_IN_THREAD = True        # False if you  do NOT want to put execution
START_CALL = None
TEMPLATES = Environment.cartella_moduli+"/PromoWear/templates/"

class Taglie(object):
    VIEW_TYPE = ('anagrafica', 'Taglie', 'taglia48x48.png')
    def getApplication(self):
        anag = AnagraficaTaglie()
        return anag

class Colori(object):
    VIEW_TYPE = ('anagrafica', 'Colori', 'colore48x48.png')
    def getApplication(self):
        anag = AnagraficaColori()
        return anag

class Modelli(object):
    VIEW_TYPE = ('anagrafica', 'Modelli', 'taglia_colore48x48.png')
    def getApplication(self):
        anag = AnagraficaModelli()
        return anag

class GruppiTaglia(object):
    VIEW_TYPE = ('anagrafica', 'Gruppi Taglia', 'gruppo_taglia48x48.png')
    def getApplication(self):
        anag = AnagraficaGruppiTaglia()
        return anag
