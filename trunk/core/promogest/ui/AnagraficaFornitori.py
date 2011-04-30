# -*- coding: utf-8 -*-

#    Copyright (C) 2005, 2006, 2007 2008, 2009, 2010 by Promotux
#                        di Francesco Meloni snc - http://www.promotux.it/

#    Author: Francesco Meloni  <francesco@promotux.it>
#    Author: Andrea Argiolas   <andrea@promotux.it>
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
from promogest.ui.AnagraficaFornitoriEdit import AnagraficaFornitoriEdit
from promogest.ui.AnagraficaFornitoriFilter import AnagraficaFornitoriFilter
from promogest.modules.Contatti.dao.ContattoFornitore import ContattoFornitore
from promogest.dao.TestataDocumento import TestataDocumento
from promogest.dao.DaoUtils import *
from utils import *
from utilsCombobox import *


class AnagraficaFornitori(Anagrafica):
    """ Anagrafica fornitori """

    def __init__(self, aziendaStr=None):
        Anagrafica.__init__(self,
                            windowTitle='Promogest - Anagrafica fornitori',
                            recordMenuLabel='_Fornitori',
                            filterElement=AnagraficaFornitoriFilter(self),
                            htmlHandler=AnagraficaFornitoriHtml(self),
                            reportHandler=AnagraficaFornitoriReport(self),
                            editElement=AnagraficaFornitoriEdit(self),
                            aziendaStr=aziendaStr)
        self.records_file_export.set_sensitive(True)
        self.duplica_button.set_sensitive(False)

    def on_record_delete_activate(self, widget):
        dao = self.filter.getSelectedDao()
        tdoc = TestataDocumento().select(idFornitore=dao.id, batchSize=None)
        if tdoc:
            messageInfo(msg= "CI SONO DOCUMENTI LEGATI A QUESTO FORNITORE\nNON E' POSSIBILE RIMUOVERLO")
            return
        if not YesNoDialog(msg='Confermi l\'eliminazione ?', transient=self.getTopLevel()):
            return
        dao = self.filter.getSelectedDao()
        cnnt = ContattoFornitore().select(idFornitore=dao.id, batchSize=None)
        if cnnt:
            for c in cnnt:
                for l in c.recapiti:
                    l.delete()
                c.delete()
        dao.delete()
        self.filter.refresh()
        self.htmlHandler.setDao(None)
        self.setFocus()


class AnagraficaFornitoriHtml(AnagraficaHtml):

    def __init__(self, anagrafica):
        AnagraficaHtml.__init__(self, anagrafica, 'fornitore',
                                'Informazioni sul fornitore')


class AnagraficaFornitoriReport(AnagraficaReport):

    def __init__(self, anagrafica):
        AnagraficaReport.__init__(self, anagrafica=anagrafica,
                                  description='Elenco dei fornitori',
                                  defaultFileName='fornitori',
                                  htmlTemplate='fornitori',
                                  sxwTemplate='fornitori')
