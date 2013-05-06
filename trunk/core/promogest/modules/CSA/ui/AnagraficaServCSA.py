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
from promogest.modules.CSA.ui.AnagraficaServCSAEdit import \
    AnagraficaServCSAEdit
from promogest.modules.CSA.ui.AnagraficaServCSAFilter import \
    AnagraficaServCSAFilter


class AnagraficaServCSA(Anagrafica):
    """ Anagrafica gestione file """

    def __init__(self, mainWindow=None, daos=None, daoFrom=None, tipo=""):
        Anagrafica.__init__(self,
                            windowTitle='Promogest - Anagrafica Servizi CSA',
                            recordMenuLabel='_Anagrafica Servizi CSA',
                            filterElement=AnagraficaServCSAFilter(self, daoFrom=daoFrom, tipo=tipo),
                            htmlHandler=AnagraficaServCSAHtml(self),
                            reportHandler=AnagraficaServCSAReport(self),
                            editElement=AnagraficaServCSAEdit(self, daoFrom=daoFrom, tipo=tipo),
                            aziendaStr=Environment.azienda,
                            )
#        self.records_print_on_screen_button.set_sensitive(False)
        self.records_print_button.set_sensitive(False)
        self.records_file_export.set_sensitive(True)
        self.record_duplicate_menu.set_sensitive(False)
        self.record_duplicate_menu.set_sensitive(False)


class AnagraficaServCSAHtml(AnagraficaHtml):

    def __init__(self, anagrafica):
        AnagraficaHtml.__init__(self, anagrafica, 'anagrafica_serv_csa',
                                'Anagrafica Servizi CSA')


class AnagraficaServCSAReport(AnagraficaReport):

    def __init__(self, anagrafica):
        AnagraficaReport.__init__(self, anagrafica=anagrafica,
                                  description='Elenco dei Servizi CSA',
                                  defaultFileName='anagrafica_serv_csa',
                                  htmlTemplate='anagrafica_serv_csa',
                                  sxwTemplate='anagrafica_serv_csa')
