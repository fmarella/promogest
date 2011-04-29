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

from sqlalchemy.orm import join
from sqlalchemy import or_
from AnagraficaComplessa import Anagrafica
from promogest.ui.AnagraficaComplessaReport import AnagraficaReport
from promogest.ui.AnagraficaComplessaHtml import AnagraficaHtml
import promogest.dao.Cliente
from promogest import Environment
from promogest.dao.Cliente import Cliente
from promogest.dao.PersonaGiuridica import PersonaGiuridica_
from promogest.dao.ClienteCategoriaCliente import ClienteCategoriaCliente
from promogest.modules.Contatti.dao.ContattoCliente import ContattoCliente
from promogest.ui.AnagraficaClientiEdit import AnagraficaClientiEdit
from promogest.ui.AnagraficaClientiFilter import AnagraficaClientiFilter
from promogest.dao.TestataDocumento import TestataDocumento
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
        dao = self.filter.getSelectedDao()
        tdoc = TestataDocumento().select(idCliente=dao.id, batchSize=None)
        if tdoc:
            messageInfo(msg= "CI SONO DOCUMENTI LEGATI A QUESTO CLIENTE\nNON E' POSSIBILE RIMUOVERLO")
            return
        if YesNoDialog(msg='Confermi l\'eliminazione ?', transient=self.getTopLevel()):
            return

        #verificare se ci sono relazioni con documenti o con contatti o recapiti
        #chiedere se si vuole rimuovere ugualmente tutto, nel caso procedere
        #davvero alla rimozione ed a quel punto gestire il "delete" a livello di
        #dao

        #try:
        if posso("IP"):
            cltip = TestataInfoPeso().select(idCliente=dao.id, batchSize=None)
            if cltip:
                for l in cltip:
                    l.delete()
            clcg = ClienteGeneralita().select(IdCliente = dao.id, batchSize=None)
            if clcg:
                for l in clcg:
                    l.delete()
        cnnt = ContattoCliente().select(idCliente=dao.id, batchSize=None)
        if cnnt:
            for c in cnnt:
                for l in c.recapiti:
                    l.delete()
                c.delete()
        dao.delete()
        self.filter.refresh()
        self.htmlHandler.setDao(None)
        self.setFocus()



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
