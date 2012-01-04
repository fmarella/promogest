# -*- coding: utf-8 -*-

#    Copyright (C) 2005, 2006, 2007 2008, 2009, 2010 by Promotux
#                        di Francesco Meloni snc - http://www.promotux.it/

#    Author: Francesco Meloni  <francesco@promotux.it>
#    Author: Andrea Argiolas   <andrea@promotux.it>
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
from promogest.ui.AnagraficaFornitoriEdit import AnagraficaFornitoriEdit
from promogest.ui.AnagraficaFornitoriFilter import AnagraficaFornitoriFilter
from promogest.modules.Contatti.dao.ContattoFornitore import ContattoFornitore
from promogest.dao.TestataDocumento import TestataDocumento
from promogest.dao.DaoUtils import *
from promogest.ui.utils import *
from promogest.ui.utilsCombobox import *


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
        self.duplica_in_cliente.set_sensitive(True)

    def on_record_delete_activate(self, widget):
        widget.set_sensitive(False)
        dao = self.filter.getSelectedDao()
        
        tdoc = TestataDocumento().select(idFornitore=dao.id, batchSize=None)
        if tdoc:
            messageInfo(msg="<big><b>Non è possibile cancellare il fornitore.</b></big>\n\nAlcuni documenti sono legati a questo fornitore.",
                        transient=self.getTopLevel())
            widget.set_sensitive(True)
            return
        if not YesNoDialog(msg='Confermi l\'eliminazione ?', transient=self.getTopLevel()):
            widget.set_sensitive(True)
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
        widget.set_sensitive(True)

    def on_duplica_in_cliente_activate_item(self, widget):
        dao = self.filter.getSelectedDao()
        if not dao:
            messageInfo(msg="SELEZIONARE UN FORNITORE")
            return
        import promogest.dao.Cliente
        from promogest.dao.Cliente import Cliente
        from promogest.modules.Contatti.dao.ContattoCliente import ContattoCliente
        from promogest.modules.Contatti.dao.RecapitoContatto import RecapitoContatto
        from promogest.modules.Contatti.dao.Contatto import Contatto
        d = Cliente()

        d.codice = promogest.dao.Cliente.getNuovoCodiceCliente()
        d.ragione_sociale = dao.ragione_sociale
        d.insegna = dao.insegna
        d.cognome = dao.cognome
        d.nome = dao.nome
        d.sede_operativa_indirizzo= dao.sede_operativa_indirizzo
        d.sede_operativa_cap = dao.sede_operativa_cap
        d.sede_operativa_localita = dao.sede_operativa_localita
        d.sede_operativa_provincia = dao.sede_operativa_provincia
        d.sede_legale_indirizzo = dao.sede_legale_indirizzo
        d.sede_legale_cap = dao.sede_legale_cap
        d.sede_legale_localita = dao.sede_legale_localita
        d.sede_legale_provincia = dao.sede_legale_provincia
        d.codice_fiscale = dao.codice_fiscale
        d.note = dao.note
        d.partita_iva = dao.partita_iva
        #dao.id_categoria_fornitore
        d.id_pagamento = dao.id_pagamento
        d.id_magazzino = dao.id_magazzino
        d.nazione = dao.nazione
        d.persist()
        #SEzione dedicata ai contatti/recapiti principali
        dao_contatto = ContattoCliente()
        if Environment.tipo_eng =="sqlite":
            forMaxId = Contatto().select(batchSize=None)
            if not forMaxId:
                dao_contatto.id = 1
            else:
                idss = []
                for l in forMaxId:
                    idss.append(l.id)
                dao_contatto.id = (max(idss)) +1
        appa = ""
        if d.ragione_sociale:
            appa = appa +" "+d.ragione_sociale
        if d.cognome:
            appa = appa+" " +d.cognome
        dao_contatto.cognome = appa
        if d.nome:
            dao_contatto.nome = d.nome
        dao_contatto.tipo_contatto ="cliente"
        dao_contatto.id_cliente =d.id
        dao_contatto.persist()


        contatti = getRecapitiFornitore(dao.id)
        for c in contatti:
            reco = RecapitoContatto()
            reco.id_contatto = dao_contatto.id
            reco.tipo_recapito = c.tipo_recapito
            reco.recapito = c.recapito
            reco.persist()
        messageInfo(msg="FORNITORE DUPLICATO IN CLIENTE")


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
