# -*- coding: utf-8 -*-

#    Copyright (C) 2005, 2006, 2007 2008, 2009, 2010 by Promotux
#                        di Francesco Meloni snc - http://www.promotux.it/

# Author: Andrea Argiolas <andrea@promotux.it>
# Author: Francesco Meloni <francesco@promotux.it>

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

import gtk
import datetime
import string
from AnagraficaComplessa import Anagrafica, AnagraficaFilter, AnagraficaHtml, AnagraficaReport,  AnagraficaEdit, AnagraficaLabel
from promogest.ui.AnagraficaListiniArticoliEdit import AnagraficaListiniArticoliEdit
from promogest.ui.AnagraficaListiniArticoliFilter import AnagraficaListiniArticoliFilter
from promogest import Environment
from promogest.dao.Articolo import Articolo
from promogest.dao.ListinoArticolo import ListinoArticolo
from promogest.dao.ScontoVenditaDettaglio import ScontoVenditaDettaglio
from promogest.dao.ScontoVenditaIngrosso import ScontoVenditaIngrosso
from promogest.dao.ListinoComplessoListino import ListinoComplessoListino
from utils import *
from utilsCombobox import fillComboboxListini,findIdFromCombobox,findComboboxRowFromId

if posso("PW"):
    from promogest.modules.PromoWear.ui.AnagraficaListinoArticoliExpand import *

class AnagraficaListiniArticoli(Anagrafica):
    """ Anagrafica listini vendita articoli """

    def __init__(self, idArticolo=None, idListino=None,aziendaStr=None):
        """
        FIXME
        """
        self._articoloFissato = (idArticolo <> None)
        self._listinoFissato = (idListino <> None)
        self._idArticolo=idArticolo
        self._idListino=idListino
        if posso("PW"):
            from promogest.modules.PromoWear.dao.ArticoloTagliaColore import ArticoloTagliaColore
        Anagrafica.__init__(self,
                            windowTitle='Promogest - Anagrafica listini di vendita',
                            recordMenuLabel='_Listini',
                            filterElement=AnagraficaListiniArticoliFilter(self),
                            htmlHandler=AnagraficaListiniArticoliHtml(self),
                            reportHandler=AnagraficaListiniArticoliReport(self),
                            labelHandler=AnagraficaListiniArticoliLabel(self),
                            editElement=AnagraficaListiniArticoliEdit(self),
                            aziendaStr=aziendaStr)

        self.Stampa_Frontaline.set_visible_horizontal(True)
        #if "Label" not in Environment.modulesList:
            #self.Stampa_Frontaline.set_sensitive(False)
        self.records_file_export.set_sensitive(True)

class AnagraficaListiniArticoliHtml(AnagraficaHtml):

    def __init__(self, anagrafica):
        """
        Gestisce l'anteprima html dei listini articolo
        """
        AnagraficaHtml.__init__(self, anagrafica, 'listino_articolo',
                                'Informazioni articolo/listino')


class AnagraficaListiniArticoliReport(AnagraficaReport):

    def __init__(self, anagrafica):
        """
        Gestisce i report dei listini articolo
        """
        AnagraficaReport.__init__(self, anagrafica=anagrafica,
                                  description='Elenco dei listini',
                                  defaultFileName='listini_articolo',
                                  htmlTemplate='listini_articolo',
                                  sxwTemplate='listini_articolo')


class AnagraficaListiniArticoliLabel(AnagraficaLabel):

    def __init__(self, anagrafica):
        """
        Gestisce la creazione delle frontaline o label
        """
        AnagraficaLabel.__init__(self, anagrafica=anagrafica,
                                  description='Elenco dei listini',
                                  htmlTemplate='label',
                                  sxwTemplate='label',
                                  defaultFileName='label')
