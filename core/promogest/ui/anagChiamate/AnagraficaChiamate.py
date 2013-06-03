# -*- coding: utf-8 -*-

#    Copyright (C) 2005-2013 by Promotux
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

from promogest.ui.AnagraficaComplessa import Anagrafica
from promogest.ui.AnagraficaComplessaReport import AnagraficaReport
from promogest.ui.AnagraficaComplessaHtml import AnagraficaHtml
from promogest.ui.anagChiamate.AnagraficaChiamateEdit import\
                                                     AnagraficaChiamateEdit
from promogest.ui.anagChiamate.AnagraficaChiamateFilter import\
                                                     AnagraficaChiamateFilter

from promogest.lib.utils import *
from promogest.ui.utilsCombobox import *
from promogest.ui.gtk_compat import *


class AnagraficaChiamate(Anagrafica):
    """ Anagrafica stoccaggi articoli """

    def __init__(self, idArticolo=None, idMagazzino=None, aziendaStr=None):
        self._articoloFissato = idArticolo
        self._magazzinoFissato = idMagazzino
        self._idArticolo = idArticolo
        self._idMagazzino = idMagazzino
        Anagrafica.__init__(self,
                            windowTitle='Promogest - Situazione magazzino',
                            recordMenuLabel='_Stoccaggi',
                            filterElement=AnagraficaStoccaggiFilter(self),
                            htmlHandler=AnagraficaStoccaggiHtml(self),
                            reportHandler=AnagraficaStoccaggiReport(self),
                            editElement=AnagraficaStoccaggiEdit(self),
                            aziendaStr=aziendaStr)
        self.records_file_export.set_sensitive(True)


class AnagraficaChiamateHtml(AnagraficaHtml):
    def __init__(self, anagrafica):
        AnagraficaHtml.__init__(self, anagrafica, 'chiamate',
                                'Informazioni sulle chiamate')


class AnagraficaChiamateReport(AnagraficaReport):
    def __init__(self, anagrafica):
        AnagraficaReport.__init__(self, anagrafica=anagrafica,
                                  description='Elenco delle chiamate',
                                  defaultFileName='chiamate',
                                  htmlTemplate='chiamate',
                                  sxwTemplate='chiamate')
