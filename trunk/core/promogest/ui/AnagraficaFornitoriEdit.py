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

import gtk

from promogest.ui.AnagraficaComplessaEdit import AnagraficaEdit

import promogest.dao.Fornitore
from promogest.dao.Fornitore import Fornitore
from promogest.modules.Contatti.dao.ContattoFornitore import ContattoFornitore
from promogest.modules.Contatti.dao.RecapitoContatto import RecapitoContatto
from promogest.modules.Contatti.dao.Contatto import Contatto
from promogest.dao.DaoUtils import *
from utils import *
from utilsCombobox import *


class AnagraficaFornitoriEdit(AnagraficaEdit):
    """ Modifica un record dell'anagrafica dei fornitori """

    def __init__(self, anagrafica):
        AnagraficaEdit.__init__(self,
                            anagrafica,
                            'anagrafica_fornitori_detail_notebook',
                            'Dati fornitore',
                            gladeFile='_anagrafica_fornitori_elements.glade')
        self._widgetFirstFocus = self.codice_entry

    def draw(self,cplx=False):
        fillComboBoxNazione(self.nazione_combobox, default="Italia")
        #Popola combobox categorie fornitori
        fillComboboxCategorieFornitori(self.id_categoria_fornitore_customcombobox.combobox)
        self.id_categoria_fornitore_customcombobox.connect('clicked',
                                                           on_id_categoria_fornitore_customcombobox_clicked)
        #Popola combobox pagamenti
        fillComboboxPagamenti(self.id_pagamento_customcombobox.combobox)
        self.id_pagamento_customcombobox.connect('clicked',
                                                 on_id_pagamento_customcombobox_clicked)
        #Popola combobox magazzini
        fillComboboxMagazzini(self.id_magazzino_customcombobox.combobox)
        self.id_magazzino_customcombobox.connect('clicked',
                                                 on_id_magazzino_customcombobox_clicked)

        self.nome_entry.destroy()
        self.cognome_entry.destroy()
        self.insegna_entry.destroy()
        self.insegna_label.destroy()
        self.cognome_label.destroy()
        self.nome_label.destroy()


    def setDao(self, dao):
        if dao is None:
            # Crea un nuovo Dao vuoto
            self.dao = Fornitore()
            self.dao.codice = promogest.dao.Fornitore.getNuovoCodiceFornitore()
        else:
            # Ricrea il Dao con una connessione al DBMS SQL
            self.dao = Fornitore().getRecord(id=dao.id)
        if dao is None:
            self.dao_contatto = ContattoFornitore()
        else:
            self.dao_contatto = ContattoFornitore().select(idFornitore=self.dao.id)
            if self.dao_contatto:
                self.dao_contatto = self.dao_contatto[0]
            else:
                self.dao_contatto = ContattoFornitore()
        self._refresh()
        return self.dao

    def _refresh(self):
        if self.dao.ragione_sociale:
            rag_soc= self.dao.ragione_sociale
        elif self.dao.cognome or self.dao.nome:
            rag_soc = str(self.dao.cognome)+" "+str(self.dao.nome)
        elif self.dao.insegna:
            rag_soc = self.dao.insegna
        else:
            rag_soc = ""
        self.codice_entry.set_text(self.dao.codice or '')
        self.ragione_sociale_entry.set_text(rag_soc)
#        self.insegna_entry.set_text(self.dao.insegna or '')
#        self.cognome_entry.set_text(self.dao.cognome or '')
#        self.nome_entry.set_text(self.dao.nome or '')
        self.indirizzo_sede_operativa_entry.set_text(self.dao.sede_operativa_indirizzo or '')
        self.cap_sede_operativa_entry.set_text(self.dao.sede_operativa_cap or '')
        self.localita_sede_operativa_entry.set_text(self.dao.sede_operativa_localita or '')
        self.provincia_sede_operativa_entry.set_text(self.dao.sede_operativa_provincia or '')
        self.indirizzo_sede_legale_entry.set_text(self.dao.sede_legale_indirizzo or '')
        self.cap_sede_legale_entry.set_text(self.dao.sede_legale_cap or '')
        self.localita_sede_legale_entry.set_text(self.dao.sede_legale_localita or '')
        self.provincia_sede_legale_entry.set_text(self.dao.sede_legale_provincia or '')
        self.codice_fiscale_entry.set_text(self.dao.codice_fiscale or '')
        self.partita_iva_entry.set_text(self.dao.partita_iva or '')
        findComboboxRowFromId(self.id_categoria_fornitore_customcombobox.combobox,
                              self.dao.id_categoria_fornitore)
        findComboboxRowFromId(self.id_pagamento_customcombobox.combobox,
                              self.dao.id_pagamento)
        findComboboxRowFromId(self.id_magazzino_customcombobox.combobox,
                              self.dao.id_magazzino)
        findComboboxRowFromStr(self.nazione_combobox,self.dao.nazione, 0)
        self.showTotaliDareAvere()
        self.cellulare_principale_entry.set_text("")
        self.telefono_principale_entry.set_text("")
        self.email_principale_entry.set_text("")
        self.fax_principale_entry.set_text("")
        self.sito_web_principale_entry.set_text("")
        for reca in getRecapitiContatto(self.dao_contatto.id):
            if reca.tipo_recapito =="Cellulare":
                self.cellulare_principale_entry.set_text(reca.recapito)
            elif reca.tipo_recapito=="Telefono":
                self.telefono_principale_entry.set_text(reca.recapito)
            elif reca.tipo_recapito =="Email":
                self.email_principale_entry.set_text(reca.recapito)
            elif reca.tipo_recapito =="Fax":
                self.fax_principale_entry.set_text(reca.recapito)
            elif reca.tipo_recapito =="Sito":
                self.sito_web_principale_entry.set_text(reca.recapito)

    def showTotaliDareAvere(self):

        if self.dao.id:
            #Calcoliamo il totale annuale:
            totaleAvereAnnuale = TotaleAnnualeFornitore(id_fornitore=self.dao.id)
            self.totale_annuale_avere_entry.set_text('%.2f' % totaleAvereAnnuale)
            #Calcoliamo il totale sospeso:
            totaleAvereSospeso = TotaleFornitoreAperto(id_fornitore=self.dao.id)
            self.totale_avere_entry.set_text('%.2f' % totaleAvereSospeso)
        self.anagrafica_fornitori_detail_notebook.set_current_page(0)


    def saveDao(self, tipo=None):
        self.dao.codice = self.codice_entry.get_text().upper()
#        self.dao.codice = omogeneousCode(section="Fornitori", string=self.dao.codice )
        self.dao.ragione_sociale = self.ragione_sociale_entry.get_text()
#        self.dao.insegna = self.insegna_entry.get_text()
#        self.dao.cognome= self.cognome_entry.get_text()
#        self.dao.nome = self.nome_entry.get_text()
        if (self.dao.codice and (self.dao.ragione_sociale or self.dao.insegna or self.dao.cognome or self.dao.nome)) =='':
            msg="""Il codice è obbligatorio.
    Inserire almeno un campo a scelta tra:
    ragione sociale, insegna, cognome o nome """
            dialog = gtk.MessageDialog(None, gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
                               gtk.MESSAGE_INFO, gtk.BUTTONS_OK, msg)
            dialog.run()
            dialog.destroy()
            raise Exception, 'Operation aborted: Codice Fornitore obbligatorio'
        self.dao.sede_operativa_indirizzo = self.indirizzo_sede_operativa_entry.get_text()
        self.dao.sede_operativa_cap = self.cap_sede_operativa_entry.get_text()
        self.dao.sede_operativa_localita = self.localita_sede_operativa_entry.get_text()
        self.dao.sede_operativa_provincia = self.provincia_sede_operativa_entry.get_text()
        self.dao.sede_legale_indirizzo = self.indirizzo_sede_legale_entry.get_text()
        self.dao.sede_legale_cap = self.cap_sede_legale_entry.get_text()
        self.dao.sede_legale_localita = self.localita_sede_legale_entry.get_text()
        self.dao.sede_legale_provincia = self.provincia_sede_legale_entry.get_text()
        self.dao.codice_fiscale = self.codice_fiscale_entry.get_text()
        if self.dao.codice_fiscale != '':
            codfis = checkCodFisc(self.dao.codice_fiscale)
            if not codfis:
                raise Exception, 'Operation aborted: Codice fiscale errato'
        self.dao.partita_iva = self.partita_iva_entry.get_text()
        if self.dao.partita_iva != '':
            partiva = checkPartIva(self.dao.partita_iva)
            if not partiva:
                raise Exception, 'Operation aborted: Partita iva errata'
        self.dao.id_categoria_fornitore = findIdFromCombobox(self.id_categoria_fornitore_customcombobox.combobox)
        self.dao.id_pagamento = findIdFromCombobox(self.id_pagamento_customcombobox.combobox)
        self.dao.id_magazzino = findIdFromCombobox(self.id_magazzino_customcombobox.combobox)
        self.dao.nazione = findStrFromCombobox(self.nazione_combobox,0)
        self.dao.persist()


        #SEzione dedicata ai contatti/recapiti principali
        if Environment.tipo_eng =="sqlite" and not self.dao_contatto.id:
            forMaxId = Contatto().select(batchSize=None)
            if not forMaxId:
                self.dao_contatto.id = 1
            else:
                idss = []
                for l in forMaxId:
                    idss.append(l.id)
                self.dao_contatto.id = (max(idss)) +1
        appa = ""
        if self.dao.ragione_sociale:
            appa = appa +" "+self.dao.ragione_sociale
        if self.dao.cognome:
            appa = appa+" " +self.dao.cognome
        self.dao_contatto.cognome = appa
        if self.dao.nome:
            self.dao_contatto.nome = self.dao.nome
        self.dao_contatto.tipo_contatto ="fornitore"
        self.dao_contatto.id_fornitore =self.dao.id
        self.dao_contatto.persist()

        recont = RecapitoContatto().select(idContatto=self.dao_contatto.id,tipoRecapito="Cellulare")
        if recont:
            reco = recont[0]
            if self.cellulare_principale_entry.get_text() =="" or reco.recapito=="":
                reco.delete()
            else:
                reco.id_contatto = self.dao_contatto.id
                reco.tipo_recapito = "Cellulare"
                reco.recapito = self.cellulare_principale_entry.get_text()
                reco.persist()

        else:
            reco = RecapitoContatto()
            reco.id_contatto = self.dao_contatto.id
            reco.tipo_recapito = "Cellulare"
            reco.recapito = self.cellulare_principale_entry.get_text()
            reco.persist()

        recont = RecapitoContatto().select(idContatto=self.dao_contatto.id,tipoRecapito="Telefono")
        if recont:
            reco = recont[0]
            if self.telefono_principale_entry.get_text() =="" or reco.recapito=="":
                reco.delete()
            else:
                reco.id_contatto = self.dao_contatto.id
                reco.tipo_recapito = "Telefono"
                reco.recapito = self.telefono_principale_entry.get_text()
                reco.persist()
        else:
            reco = RecapitoContatto()
            reco.id_contatto = self.dao_contatto.id
            reco.tipo_recapito = "Telefono"
            reco.recapito = self.telefono_principale_entry.get_text()
            reco.persist()


        recont = RecapitoContatto().select(idContatto=self.dao_contatto.id,tipoRecapito="Email")
        if recont:
            reco = recont[0]
            if self.email_principale_entry.get_text() =="" or reco.recapito=="":
                reco.delete()
            else:
                reco.id_contatto = self.dao_contatto.id
                reco.tipo_recapito = "Email"
                reco.recapito = self.email_principale_entry.get_text()
                reco.persist()
        else:
            reco = RecapitoContatto()
            reco.id_contatto = self.dao_contatto.id
            reco.tipo_recapito = "Email"
            reco.recapito = self.email_principale_entry.get_text()
            reco.persist()

        recontw = RecapitoContatto().select(idContatto=self.dao_contatto.id,tipoRecapito="Sito")
        if recontw:
            recow = recontw[0]
            if self.sito_web_principale_entry.get_text() =="" or recow.recapito=="":
                recow.delete()
            else:
                recow.id_contatto = self.dao_contatto.id
                recow.tipo_recapito = "Sito"
                recow.recapito = self.sito_web_principale_entry.get_text()
                recow.persist()
        else:
            recow = RecapitoContatto()
            recow.id_contatto = self.dao_contatto.id
            recow.tipo_recapito = "Sito"
            recow.recapito = self.sito_web_principale_entry.get_text()
            recow.persist()

        recont = RecapitoContatto().select(idContatto=self.dao_contatto.id,tipoRecapito="Fax")
        if recont:
            reco = recont[0]
            if self.fax_principale_entry.get_text() =="" or reco.recapito=="":
                reco.delete()
            else:
                reco.id_contatto = self.dao_contatto.id
                reco.tipo_recapito = "Fax"
                reco.recapito = self.fax_principale_entry.get_text()
                reco.persist()
        else:
            reco = RecapitoContatto()
            reco.id_contatto = self.dao_contatto.id
            reco.tipo_recapito = "Fax"
            reco.recapito = self.fax_principale_entry.get_text()
            reco.persist()

    def on_scheda_contabile_togglebutton_clicked(self, toggleButton):
        """
        Apre la finestra di registrazione documenti, ricercando solo
        i documenti del fornitore
        """

        if not(toggleButton.get_active()):
            toggleButton.set_active(False)
            return

        if self.dao.id is None:
            msg = 'Prima di poter visualizzare la registrazione documenti occorre salvare il fornitore.\n Salvare? '
            dialog = gtk.MessageDialog(self.dialogTopLevel,
                gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
                gtk.MESSAGE_QUESTION,
                gtk.BUTTONS_YES_NO, msg)
            response = dialog.run()
            dialog.destroy()

            if response == gtk.RESPONSE_YES:
                self.on_anagrafica_complessa_detail_dialog_response(
                    self.dialogTopLevel, gtk.RESPONSE_APPLY)
            else:
                toggleButton.set_active(False)
                return

        from AnagraficaDocumenti import AnagraficaDocumenti
        anag = AnagraficaDocumenti()
        anagWindow = anag.getTopLevel()
        showAnagraficaRichiamata(self.dialogTopLevel, anagWindow, toggleButton)
        anag.filter.id_fornitore_filter_customcombobox.setId(self.dao.id)
        anag.filter.solo_contabili_check.set_active(True)
        anag.filter.refresh()


    def on_promemoria_togglebutton_toggled(self, toggleButton):
        if not(toggleButton.get_active()):
            toggleButton.set_active(False)
            return
        if posso("PR"):
            if self.dao.id is None:
                msg = 'Prima di poter inserire i contatti occorre salvare il Fornitore.\n Salvare ?'
                dialog = gtk.MessageDialog(self.dialogTopLevel,
                        gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
                        gtk.MESSAGE_QUESTION, gtk.BUTTONS_YES_NO,
                        msg)
                response = dialog.run()
                dialog.destroy()
                if response == gtk.RESPONSE_YES:
                    self.on_anagrafica_complessa_detail_dialog_response(self.dialogTopLevel, gtk.RESPONSE_APPLY)
                else:
                    toggleButton.set_active(False)
                    return

            from promogest.ui.AnagraficaPromemoria import AnagraficaPromemoria
            if self.dao.ragione_sociale:
                stringa = self.dao.ragione_sociale
            elif self.dao.cognome:
                stringa = self.dao.cognome
            else:
                stringa = None
            anag = AnagraficaPromemoria(pg=stringa)
            anagWindow = anag.getTopLevel()

            showAnagraficaRichiamata(self.dialogTopLevel, anagWindow, toggleButton)
        else:
            fenceDialog()
            toggleButton.set_active(False)



    def on_contatti_togglebutton_clicked(self, toggleButton):
        if posso("CN"):
            if not(toggleButton.get_active()):
                toggleButton.set_active(False)
                return

            if self.dao.id is None:
                msg = 'Prima di poter inserire i contatti occorre salvare il fornitore.\n Salvare ?'
                dialog = gtk.MessageDialog(self.dialogTopLevel, gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
                                        gtk.MESSAGE_QUESTION, gtk.BUTTONS_YES_NO, msg)
                response = dialog.run()
                dialog.destroy()
                if response == gtk.RESPONSE_YES:
                    self.on_anagrafica_complessa_detail_dialog_response(self.dialogTopLevel, gtk.RESPONSE_APPLY)
                else:
                    toggleButton.set_active(False)
                    return

            from promogest.modules.Contatti.ui.AnagraficaContatti import AnagraficaContatti
            anag = AnagraficaContatti(self.dao.id, 'fornitore')
            anagWindow = anag.getTopLevel()

            showAnagraficaRichiamata(self.dialogTopLevel, anagWindow, toggleButton)
        else:
            fenceDialog()
            toggleButton.set_active(False)

    def on_forniture_togglebutton_clicked(self, toggleButton):
        if not(toggleButton.get_active()):
            toggleButton.set_active(False)
            return

        if self.dao.id is None:
            msg = 'Prima di poter inserire delle forniture occorre salvare il fornitore.\n Salvare ?'
            dialog = gtk.MessageDialog(self.dialogTopLevel, gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
                                       gtk.MESSAGE_QUESTION, gtk.BUTTONS_YES_NO, msg)
            response = dialog.run()
            dialog.destroy()
            if response == gtk.RESPONSE_YES:
                self.on_anagrafica_complessa_detail_dialog_response(self.dialogTopLevel, gtk.RESPONSE_APPLY)
            else:
                toggleButton.set_active(False)
                return

        from AnagraficaForniture import AnagraficaForniture
        anag = AnagraficaForniture(None, self.dao.id)
        anagWindow = anag.getTopLevel()

        showAnagraficaRichiamata(self.dialogTopLevel, anagWindow, toggleButton)
