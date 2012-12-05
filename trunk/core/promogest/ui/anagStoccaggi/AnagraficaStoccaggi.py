# -*- coding: utf-8 -*-

#    Copyright (C) 2005-2012 by Promotux
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
from promogest.ui.anagStoccaggi.AnagraficaStoccaggiEdit import\
                                                     AnagraficaStoccaggiEdit
from promogest.ui.anagStoccaggi.AnagraficaStoccaggiFilter import\
                                                     AnagraficaStoccaggiFilter

from promogest.lib.utils import *
from promogest.ui.utilsCombobox import *
from promogest.ui.gtk_compat import *

if posso("PW"):
    from promogest.modules.PromoWear.ui.PromowearUtils import *


class AnagraficaStoccaggi(Anagrafica):
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


class AnagraficaStoccaggiHtml(AnagraficaHtml):
    def __init__(self, anagrafica):
        AnagraficaHtml.__init__(self, anagrafica, 'stoccaggio',
                                'Informazioni sullo stoccaggio')


class AnagraficaStoccaggiReport(AnagraficaReport):
    def __init__(self, anagrafica):
        AnagraficaReport.__init__(self, anagrafica=anagrafica,
                                  description='Elenco degli stoccaggi',
                                  defaultFileName='stoccaggi',
                                  htmlTemplate='stoccaggi',
                                  sxwTemplate='stoccaggi')
