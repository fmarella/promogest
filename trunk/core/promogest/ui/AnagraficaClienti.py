# -*- coding: utf-8 -*-

#    Copyright (C) 2005, 2006, 2007 2008, 2009, 2010, 2011 by Promotux
#                        di Francesco Meloni snc - http://www.promotux.it/

#    Author: Francesco Meloni  <francesco@promotux.it>
#    Author: Andrea Argiolas <andrea@promotux.it>
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

from sqlalchemy.orm import join
from sqlalchemy import or_
from promogest.ui.AnagraficaComplessa import Anagrafica
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
from promogest.ui.utils import *
from promogest.ui.utilsCombobox import *


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
        self.duplica_in_fornitore.set_sensitive(True)

    def on_record_delete_activate(self, widget):
        dao = self.filter.getSelectedDao()
        tdoc = TestataDocumento().select(idCliente=dao.id, batchSize=None)
        if tdoc:
            messageInfo(msg= "CI SONO DOCUMENTI LEGATI A QUESTO CLIENTE\nNON E' POSSIBILE RIMUOVERLO")
            return
        if not YesNoDialog(msg='Confermi l\'eliminazione ?', transient=self.getTopLevel()):
            return

        #verificare se ci sono relazioni con documenti o con contatti o recapiti
        #chiedere se si vuole rimuovere ugualmente tutto, nel caso procedere
        #davvero alla rimozione ed a quel punto gestire il "delete" a livello di
        #dao

        #try:
        if posso("IP"):
            from promogest.modules.InfoPeso.dao.TestataInfoPeso import TestataInfoPeso
            from promogest.modules.InfoPeso.dao.ClienteGeneralita import ClienteGeneralita
            cltip = TestataInfoPeso().select(idCliente=dao.id, batchSize=None)
            if cltip:
                for l in cltip:
                    l.delete()
            clcg = ClienteGeneralita().select(idCliente = dao.id, batchSize=None)
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

    def on_duplica_in_fornitore_activate_item(self, widget):
        dao = self.filter.getSelectedDao()
        if not dao:
            messageInfo(msg="SELEZIONARE UN CLIENTE")
            return
        import promogest.dao.Fornitore
        from promogest.dao.Fornitore import Fornitore
        from promogest.modules.Contatti.dao.ContattoFornitore import ContattoFornitore
        from promogest.modules.Contatti.dao.RecapitoContatto import RecapitoContatto
        from promogest.modules.Contatti.dao.Contatto import Contatto
        d = Fornitore()

        d.codice = promogest.dao.Fornitore.getNuovoCodiceFornitore()
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
        dao_contatto = ContattoFornitore()
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
        dao_contatto.tipo_contatto ="fornitore"
        dao_contatto.id_fornitore =d.id
        dao_contatto.persist()


        contatti = getRecapitiCliente(dao.id)
        for c in contatti:
            reco = RecapitoContatto()
            reco.id_contatto = dao_contatto.id
            reco.tipo_recapito = c.tipo_recapito
            reco.recapito = c.recapito
            reco.persist()
        messageInfo(msg="CLIENTE DUPLICATO IN FORNITORE")


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