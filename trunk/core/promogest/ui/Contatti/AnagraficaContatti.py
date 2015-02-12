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

from promogest.ui.gtk_compat import *

from promogest.ui.AnagraficaComplessa import Anagrafica
from promogest.ui.AnagraficaComplessaReport import AnagraficaReport
from promogest.ui.AnagraficaComplessaHtml import AnagraficaHtml
from promogest.ui.Contatti.AnagraficaContattiEdit import AnagraficaContattiEdit
from promogest.ui.Contatti.AnagraficaContattiFilter import AnagraficaContattiFilter
from promogest.ui.utilsCombobox import *


class AnagraficaContatti(Anagrafica):

    def __init__(self, ownerKey=None, ownerType=None, aziendaStr=None):
        """ Anagrafica contatti
        """
        self._ownerKey = None
        self._ownerType = None
        if (((ownerType == 'cliente') or (ownerType == 'fornitore') or
             (ownerType == 'magazzino') or (ownerType == 'azienda')) and
                                             (ownerKey is not None)):
            self._ownerKey = ownerKey
            self._ownerType = ownerType

        Anagrafica.__init__(self,
                            windowTitle='Promogest - Anagrafica contatti',
                            recordMenuLabel='_Contatti',
                            filterElement=AnagraficaContattiFilter(self),
                            htmlHandler=AnagraficaContattiHtml(self),
                            reportHandler=AnagraficaContattiReport(self),
                            editElement=AnagraficaContattiEdit(self),
                            aziendaStr=aziendaStr)


class AnagraficaContattiHtml(AnagraficaHtml):
    def __init__(self, anagrafica):
        AnagraficaHtml.__init__(self, anagrafica, 'contatto',
                                'Informazioni sul contatto')


class AnagraficaContattiReport(AnagraficaReport):
    def __init__(self, anagrafica):
        AnagraficaReport.__init__(self, anagrafica=anagrafica,
                                  description='Elenco dei contatti',
                                  defaultFileName='contatti',
                                  htmlTemplate='contatti',
                                  sxwTemplate='contatti')
