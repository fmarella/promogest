# -*- coding: iso-8859-15 -*-

# Promogest
#
# Copyright (C) 2005 by Promotux Informatica - http://www.promotux.it/

import gtk, gobject
from promogest import Environment
from promogest.ui.GladeWidget import GladeWidget
import promogest.ui.Login
from promogest.modules.PromoWear.data.PromoWearDB import *
#import promogest.modules.PromoWear.ui.AnagraficaColori
#from promogest.modules.PromoWear.ui.AnagraficaColori import AnagraficaColori
#import promogest.modules.PromoWear.ui.AnagraficaGruppiTaglia
#from promogest.modules.PromoWear.ui.AnagraficaGruppiTaglia import AnagraficaGruppiTaglia
from promogest.modules.PromoWear.ui.AnagraficaTaglie import AnagraficaTaglie
import promogest.modules.PromoWear.ui.TaglieColori
from promogest.modules.PromoWear.ui.TaglieColori import GestioneTaglieColori
#from promogest.modules.PromoWear.ui.AnagraficaArticoli import AnagraficaArticoli
#from promogest.modules.PromoWear.ui.AnagraficaSchedeOrdinazioni import AnagraficaSchedeOrdinazioni
from promogest.modules.PromoWear.ui.PromowearUtils import *

MODULES_NAME = "PromoWear"
MODULES_FOR_EXPORT = ['Taglie']
GUI_DIR = getattr(Environment.conf.Moduli, 'cartella_moduli', 'promogest/modules')+'/PromoWear/gui/'
COMPANY = Environment.conf.PromoWear.company_name
START_CALL_IS_IN_THREAD = True        # False if you  do NOT want to put execution
START_CALL = None

if Environment.conf.PromoWear.taglie_colori == "yes" and Environment.conf.PromoWear.mod_enable == "yes" :
    Environment.taglia_colore = True
else:
    Environment.taglia_colore = False


class Taglie(object):
    VIEW_TYPE = ('anagrafica', 'Taglie', 'taglia48x48.png')
    def getApplication(self):
        anag = AnagraficaTaglie()
        return anag

