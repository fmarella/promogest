# -*- coding: utf-8 -*-

#    Copyright (C) 2005-2012 by Promotux
#                        di Francesco Meloni snc - http://www.promotux.it/

#    Author: Francesco Meloni  <francesco@promotux.it>

#    This file is part of Promogest.

#    Promogest is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 2 of the License, or
#    (at your option) any later version.

#    Promogest is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

#    You should have received a copy of the GNU General Public License
#    along with Promogest.  If not, see <http://www.gnu.org/licenses/>.

from promogest import Environment
#import promogest.ui.Login
from promogest.modules.VenditaDettaglio.ui.AnagraficaVenditaDettaglio import AnagraficaVenditaDettaglio
MODULES_NAME = "VenditaDettaglio"
MODULES_FOR_EXPORT = ['VenditaDettaglio']
GUI_DIR = Environment.cartella_moduli+'/VenditaDettaglio/gui/'
START_CALL_IS_IN_THREAD = True        # False if you  do NOT want to put execution
START_CALL = None                              # of this call in a separated Thread
TEMPLATES = Environment.cartella_moduli+"/VenditaDettaglio/templates/"

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
