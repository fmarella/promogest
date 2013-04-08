# -*- coding: utf-8 -*-

#    Copyright (C) 2005-2013 by Promotux
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
from promogest import Environment
from promogest.modules.Provvigione.ui.AnagraficaProvvEdit import \
    AnagraficaProvvEdit
from promogest.modules.Provvigione.ui.AnagraficaProvvFilter import \
    AnagraficaProvvFilter


class AnagraficaProvv(Anagrafica):
    """ Anagrafica gestione file """

    def __init__(self, mainWindow=None, daos=None, dao=None, tipo=""):
        Anagrafica.__init__(self,
                            windowTitle='Promogest - Anagrafica Provvigioni',
                            recordMenuLabel='_Anagrafica Provvigioni',
                            filterElement=AnagraficaProvvFilter(self, dao=dao, tipo=tipo),
                            htmlHandler=AnagraficaProvvHtml(self),
                            reportHandler=AnagraficaProvvReport(self),
                            editElement=AnagraficaProvvEdit(self, dao=dao, tipo=tipo),
                            aziendaStr=Environment.azienda,
                            )
#        self.records_print_on_screen_button.set_sensitive(False)
        self.records_print_button.set_sensitive(False)
        self.records_file_export.set_sensitive(True)
        self.record_duplicate_menu.set_sensitive(False)
        self.record_duplicate_menu.set_sensitive(False)


class AnagraficaProvvHtml(AnagraficaHtml):

    def __init__(self, anagrafica):
        AnagraficaHtml.__init__(self, anagrafica, 'anagrafica_provv',
                                'Anagrafica Provvigioni')


class AnagraficaProvvReport(AnagraficaReport):

    def __init__(self, anagrafica):
        AnagraficaReport.__init__(self, anagrafica=anagrafica,
                                  description='Elenco delle provvigioni',
                                  defaultFileName='anagrafica_provv',
                                  htmlTemplate='anagrafica_provv',
                                  sxwTemplate='anagrafica_provv')
