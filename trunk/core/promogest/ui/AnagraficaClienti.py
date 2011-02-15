# -*- coding: utf-8 -*-

#    Copyright (C) 2005, 2006, 2007 2008, 2009, 2010 by Promotux
#                        di Francesco Meloni snc - http://www.promotux.it/

#    Author: Francesco Meloni  <francesco@promotux.it>
#    Author: Andrea Argiolas <andrea@promotux.it>
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
from sqlalchemy.orm import join
from sqlalchemy import or_
from AnagraficaComplessa import Anagrafica, AnagraficaFilter, \
                        AnagraficaHtml, AnagraficaReport, AnagraficaEdit
import promogest.dao.Cliente
from promogest import Environment
from promogest.dao.Cliente import Cliente
from promogest.dao.PersonaGiuridica import PersonaGiuridica_
from promogest.dao.ClienteCategoriaCliente import ClienteCategoriaCliente
from promogest.ui.AnagraficaClientiEdit import AnagraficaClientiEdit
from promogest.ui.AnagraficaClientiFilter import AnagraficaClientiFilter
from promogest.dao.DaoUtils import *
from utils import *
from utilsCombobox import *


class AnagraficaClienti(Anagrafica):
    """ Anagrafica clienti """

    def __init__(self, aziendaStr=None):
        Anagrafica.__init__(self,
                            windowTitle='Promogest - Anagrafica clienti',
                            recordMenuLabel='_Clienti',
                            filterElement=AnagraficaClientiFilter(self),
                            htmlHandler=AnagraficaClientiHtml(self),
                            reportHandler=AnagraficaClientiReport(self),
                            editElement=AnagraficaClientiEdit(self),
                            aziendaStr=aziendaStr)
        self.records_file_export.set_sensitive(True)

    def on_record_delete_activate(self, widget):
        dialog = gtk.MessageDialog(self.getTopLevel(),
                                   gtk.DIALOG_MODAL
                                   | gtk.DIALOG_DESTROY_WITH_PARENT,
                                   gtk.MESSAGE_QUESTION, gtk.BUTTONS_YES_NO,
                                   'Confermi l\'eliminazione ?')

        response = dialog.run()
        dialog.destroy()
        if response !=  gtk.RESPONSE_YES:
            return

        #verificare se ci sono relazioni con documenti o con contatti o recapiti
        #chiedere se si vuole rimuovere ugualmente tutto, nel caso procedere
        #davvero alla rimozione ed a quel punto gestire il "delete" a livello di
        #dao
        dao = self.filter.getSelectedDao()
        print dao.__dict__
#        dao.delete()
#        self.filter.refresh()
#        self.htmlHandler.setDao(None)
#        self.setFocus()

class AnagraficaClientiHtml(AnagraficaHtml):
    """
    Anteprima Html
    """
    def __init__(self, anagrafica):
        AnagraficaHtml.__init__(self, anagrafica, 'cliente',
                                'Informazioni sul cliente')


class AnagraficaClientiReport(AnagraficaReport):
    def __init__(self, anagrafica):
        AnagraficaReport.__init__(self, anagrafica=anagrafica,
                                  description='Elenco dei clienti',
                                  defaultFileName='clienti',
                                  htmlTemplate='clienti',
                                  sxwTemplate='clienti')
