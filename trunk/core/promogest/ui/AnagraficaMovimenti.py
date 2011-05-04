# -*- coding: utf-8 -*-

#    Copyright (C) 2005, 2006, 2007 2008, 2009, 2010 by Promotux
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


from AnagraficaComplessa import Anagrafica
from promogest.ui.AnagraficaComplessaReport import AnagraficaReport
from promogest.ui.AnagraficaComplessaHtml import AnagraficaHtml

from AnagraficaMovimentiEdit import AnagraficaMovimentiEdit
from AnagraficaMovimentiFilter import AnagraficaMovimentiFilter
from AnagraficaDocumentiEditUtils import *
from utils import *
from utilsCombobox import *

if posso("PW"):
    from promogest.modules.PromoWear.ui import AnagraficaDocumentiEditPromoWearExt

class AnagraficaMovimenti(Anagrafica):

    def __init__(self, idMagazzino=None, aziendaStr=None):
        """
        """
        self._magazzinoFissato = (idMagazzino <> None)
        self._idMagazzino=idMagazzino
        Anagrafica.__init__(self,
                            windowTitle='Promogest - Registrazione movimenti',
                            recordMenuLabel='_Movimenti',
                            filterElement=AnagraficaMovimentiFilter(self),
                            htmlHandler=AnagraficaMovimentiHtml(self),
                            reportHandler=AnagraficaMovimentiReport(self),
                            editElement=AnagraficaMovimentiEdit(self),
                            aziendaStr=aziendaStr)
        self.duplica_button.set_sensitive(True)
        self.record_duplicate_menu.set_property('visible', True)
        self.records_file_export.set_sensitive(True)

    def duplicate(self, dao):
        """ Duplica le informazioni relative ad un movimento scelto su uno nuovo """
        if dao is None:
            return

        from DuplicazioneMovimento import DuplicazioneMovimento
        anag = DuplicazioneMovimento(dao,self)
        showAnagraficaRichiamata(self.getTopLevel(), anag.getTopLevel(), None, self.filter.refresh)


class AnagraficaMovimentiHtml(AnagraficaHtml):
    def __init__(self, anagrafica):
        """
        """
        AnagraficaHtml.__init__(self, anagrafica, 'movimento',
                                'Informazioni sul movimento merce')


class AnagraficaMovimentiReport(AnagraficaReport):
    def __init__(self, anagrafica):
        """
        """
        AnagraficaReport.__init__(self, anagrafica=anagrafica,
                                  description='Elenco dei movimenti',
                                  defaultFileName='movimenti',
                                  htmlTemplate='movimenti',
                                  sxwTemplate='movimenti')
