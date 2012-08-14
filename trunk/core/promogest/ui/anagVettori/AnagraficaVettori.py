# -*- coding: utf-8 -*-

#    Copyright (C) 2005-2012 by Promotux
#                        di Francesco Meloni snc - http://www.promotux.it/

#    Author: Francesco Meloni  <francesco@promotux.it>
#    Author: Andrea Argiolas  <andrea@promotux.it>
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
from promogest.ui.anagVettori.AnagraficaVettoriFilter import AnagraficaVettoriFilter
from promogest.ui.anagVettori.AnagraficaVettoriEdit import AnagraficaVettoriEdit

from promogest import Environment
import promogest.dao.Vettore
from promogest.dao.Vettore import Vettore

from promogest.lib.utils import *
from promogest.ui.utilsCombobox import *


class AnagraficaVettori(Anagrafica):
    """ Anagrafica vettori """

    def __init__(self, aziendaStr=None):
        Anagrafica.__init__(self,
                            windowTitle='Promogest - Anagrafica vettori',
                            recordMenuLabel='_Vettori',
                            filterElement=AnagraficaVettoriFilter(self),
                            htmlHandler=AnagraficaVettoriHtml(self),
                            reportHandler=AnagraficaVettoriReport(self),
                            editElement=AnagraficaVettoriEdit(self),
                            aziendaStr=aziendaStr)
        self.records_file_export.set_sensitive(True)

class AnagraficaVettoriHtml(AnagraficaHtml):
    def __init__(self, anagrafica):
        AnagraficaHtml.__init__(self, anagrafica, 'vettore',
                                'Informazioni sul vettore')



class AnagraficaVettoriReport(AnagraficaReport):
    def __init__(self, anagrafica):
        AnagraficaReport.__init__(self, anagrafica=anagrafica,
                                  description='Elenco dei vettori',
                                  defaultFileName='vettori',
                                  htmlTemplate='vettori',
                                  sxwTemplate='vettori')
