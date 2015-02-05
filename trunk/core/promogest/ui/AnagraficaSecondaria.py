# -*- coding: utf-8 -*-

#    Copyright (C) 2005-2015 by Promotux
#                        di Francesco Meloni snc - http://www.promotux.it/

#    Author: Francesco Meloni  <francesco@promotux.it>
#    Author: Francesco Marella <francesco.marella@anche.no>

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

from promogest.ui.AnagraficaSecondariaEdit import AnagraficaSecondariaEdit
from promogest.ui.AnagraficaSecondariaFilter import AnagraficaSecondariaFilter

from promogest.dao.DaoUtils import *
from promogest.lib.utils import *
from promogest.ui.utilsCombobox import *


class AnagraficaSecondarie(Anagrafica):
    """ Anagrafica fornitori """

    def __init__(self, aziendaStr=None, daoRole=None):

        if daoRole:
            nome_anag_seco = daoRole.name
        else:
            nome_anag_seco = None
        title = 'Promogest - Anagrafiche %s' %nome_anag_seco


        Anagrafica.__init__(self,
                            windowTitle=title,
                            recordMenuLabel='_Secondarie',
                            filterElement=AnagraficaSecondariaFilter(self, daoRole),
                            htmlHandler=AnagraficaSecondariaHtml(self),
                            reportHandler=AnagraficaSecondariaReport(self),
                            editElement=AnagraficaSecondariaEdit(self,daoRole),
                            aziendaStr=aziendaStr)
        self.records_file_export.set_sensitive(True)


class AnagraficaSecondariaHtml(AnagraficaHtml):

    def __init__(self, anagrafica):
        AnagraficaHtml.__init__(self, anagrafica, 'anagrafica_secondaria',
                                'Informazioni sul anagrafica secondaria')


class AnagraficaSecondariaReport(AnagraficaReport):

    def __init__(self, anagrafica):
        AnagraficaReport.__init__(self, anagrafica=anagrafica,
                                  description='Elenco delle anagrafiche secondarie',
                                  defaultFileName='anagrafica_scondaria',
                                  htmlTemplate='anagrafica_secondaria',
                                  sxwTemplate='anagrafica_secondaria')
