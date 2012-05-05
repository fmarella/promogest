# -*- coding: utf-8 -*-

#    Copyright (C) 2005-2012 by Promotux
#                       di Francesco Meloni snc - http://www.promotux.it/

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

from decimal import *
from promogest.ui.AnagraficaComplessa import Anagrafica
from promogest.ui.AnagraficaComplessaReport import AnagraficaReport
from promogest.ui.AnagraficaComplessaHtml import AnagraficaHtml

from AnagraficaCommesseFilter import AnagraficaCommesseFilter
from AnagraficaCommesseEdit import AnagraficaCommesseEdit
from promogest.modules.GestioneCommesse.dao.StadioCommessa import StadioCommessa
from promogest.modules.GestioneCommesse.dao.TestataCommessa import TestataCommessa
from promogest.modules.GestioneCommesse.dao.RigaCommessa import RigaCommessa
from promogest.dao.Cliente import Cliente
from promogest.dao.TestataDocumento import TestataDocumento
from promogest.lib.relativedelta import relativedelta
from promogest.lib.utils import *
from promogest.ui.utilsCombobox import *


class AnagraficaCommesse(Anagrafica):
    """ Anagrafica Comesse """

    def __init__(self, aziendaStr=None):
        Anagrafica.__init__(self,
                            windowTitle='Promogest - Anagrafica Gestione Commesse',
                            recordMenuLabel='_Gestione commesse',
                            filterElement=AnagraficaCommesseFilter(self),
                            htmlHandler=AnagraficaCommesseHtml(self),
                            reportHandler=AnagraficaCommesseReport(self),
                            editElement=AnagraficaCommesseEdit(self),
                            aziendaStr=aziendaStr)
        self.records_print_on_screen_button.set_sensitive(False)
        self.records_print_button.set_sensitive(False)
        self.records_file_export.set_sensitive(True)


class AnagraficaCommesseHtml(AnagraficaHtml):

    def __init__(self, anagrafica):
        AnagraficaHtml.__init__(self, anagrafica, 'commessa',
                                'Dettaglio Commessa')


class AnagraficaCommesseReport(AnagraficaReport):

    def __init__(self, anagrafica):
        AnagraficaReport.__init__(self, anagrafica=anagrafica,
                                  description='Elenco delle commesse',
                                  defaultFileName='commessa',
                                  htmlTemplate='commessa',
                                  sxwTemplate='commessa')
