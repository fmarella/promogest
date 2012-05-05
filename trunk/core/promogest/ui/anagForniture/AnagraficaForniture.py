# -*- coding: utf-8 -*-

#    Copyright (C) 2005-2012 by Promotux
#                        di Francesco Meloni snc - http://www.promotux.it/

#    Author: Francesco Meloni  <francesco@promotux.it>
#    Author: Andrea Argiolas  <andrea@promotux.it>
#    Author: Francesco Marella <francesco.marella@gmail.com>

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

from promogest.ui.anagForniture.AnagraficaFornitureFilter import AnagraficaFornitureFilter
from promogest.ui.anagForniture.AnagraficaFornitureEdit import AnagraficaFornitureEdit

from promogest import Environment
from promogest.dao.Fornitura import Fornitura
from promogest.dao.Fornitore import Fornitore
from promogest.dao.ScontoFornitura import ScontoFornitura
from promogest.lib.utils import *
from promogest.ui.utilsCombobox import *
from promogest.ui.gtk_compat import *


class AnagraficaForniture(Anagrafica):
    """ Anagrafica forniture articoli """

    def __init__(self, idArticolo=None, idFornitore=None, aziendaStr=None):
        self._articoloFissato = (idArticolo <> None)
        self._fornitoreFissato = (idFornitore <> None)
        self._idArticolo=idArticolo
        self._idFornitore=idFornitore
        if posso("PW"):
            import promogest.modules.PromoWear.dao.ArticoloTagliaColore
            from promogest.modules.PromoWear.dao.ArticoloTagliaColore import ArticoloTagliaColore
        Anagrafica.__init__(self,
                            windowTitle='Promogest - Anagrafica forniture articoli',
                            recordMenuLabel='_Forniture',
                            filterElement=AnagraficaFornitureFilter(self),
                            htmlHandler=AnagraficaFornitureHtml(self),
                            reportHandler=AnagraficaFornitureReport(self),
                            editElement=AnagraficaFornitureEdit(self),
                            aziendaStr=aziendaStr)
        self.records_file_export.set_sensitive(True)


class AnagraficaFornitureHtml(AnagraficaHtml):
    def __init__(self, anagrafica):
        AnagraficaHtml.__init__(self, anagrafica, 'fornitura',
                                'Informazioni sulla fornitura')


class AnagraficaFornitureReport(AnagraficaReport):
    def __init__(self, anagrafica):
        AnagraficaReport.__init__(self, anagrafica=anagrafica,
                                  description='Elenco delle forniture',
                                  defaultFileName='forniture',
                                  htmlTemplate='forniture',
                                  sxwTemplate='forniture')
