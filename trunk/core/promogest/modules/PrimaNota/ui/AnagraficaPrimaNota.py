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

from promogest.ui.AnagraficaComplessa import Anagrafica
from promogest.ui.AnagraficaComplessaReport import AnagraficaReport
from promogest.ui.AnagraficaComplessaHtml import AnagraficaHtml

from promogest.ui.AnagraficaFornitoriEdit import AnagraficaFornitoriEdit
from promogest.ui.AnagraficaFornitoriFilter import AnagraficaFornitoriFilter
from promogest.modules.PrimaNota.ui.\
                        AnagraficaPrimaNotaEdit import AnagraficaPrimaNotaEdit
from promogest.modules.PrimaNota.ui.\
                    AnagraficaPrimaNotaFilter import AnagraficaPrimaNotaFilter
#from promogest.ui.utils import *
#from promogest.ui.utilsCombobox import *


class AnagraficaPrimaNota(Anagrafica):
    """ Anagrafica Variazioni Listini """

    def __init__(self, aziendaStr=None):
        Anagrafica.__init__(self,
                        windowTitle='Promogest - Anagrafica Prima Nota Cassa',
                        recordMenuLabel='_Prima nota cassa',
                        filterElement=AnagraficaPrimaNotaFilter(self),
                        htmlHandler=AnagraficaPrimaNotaHtml(self),
                        reportHandler=AnagraficaPrimaNotaReport(self),
                        editElement=AnagraficaPrimaNotaEdit(self),
                        aziendaStr=aziendaStr)
#        self.records_print_on_screen_button.set_sensitive(False)
        self.records_print_button.set_sensitive(False)
        self.records_file_export.set_sensitive(True)
        self.record_duplicate_menu.set_sensitive(False)
        self.record_duplicate_menu.set_sensitive(False)

class AnagraficaPrimaNotaHtml(AnagraficaHtml):

    def __init__(self, anagrafica):
        AnagraficaHtml.__init__(self, anagrafica, 'prima_nota',
                                'Dettaglio Prima Nota Cassa')


class AnagraficaPrimaNotaReport(AnagraficaReport):

    def __init__(self, anagrafica):
        AnagraficaReport.__init__(self, anagrafica=anagrafica,
                                  description='Elenco delle Prime Note Cassa',
                                  defaultFileName='prime_note',
                                  htmlTemplate='prime_note',
                                  sxwTemplate='prime_note')
