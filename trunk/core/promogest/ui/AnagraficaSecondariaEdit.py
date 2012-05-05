# -*- coding: utf-8 -*-

#    Copyright (C) 2005-2012 by Promotux
#                        di Francesco Meloni snc - http://www.promotux.it/

#    Author: Francesco Meloni  <francesco@promotux.it>
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

from promogest.ui.AnagraficaComplessaEdit import AnagraficaEdit
from promogest.ui.AnagraficaPGEdit import AnagraficaPGEdit
import promogest.dao.AnagraficaSecondaria
from promogest.dao.AnagraficaSecondaria import \
                            AnagraficaSecondaria_ as AnagraficaSecondaria

from promogest.modules.Contatti.dao.ContattoAnagraficaSecondaria import \
                                                ContattoAnagraficaSecondaria
from promogest.dao.DaoUtils import *
from promogest.dao.PersonaGiuridicaPersonaGiuridica import \
                                            PersonaGiuridicaPersonaGiuridica
from promogest.dao.Cliente import Cliente
from promogest.lib.utils import *
from promogest.ui.utilsCombobox import *
from promogest.ui.gtk_compat import *


class AnagraficaSecondariaEdit(AnagraficaEdit, AnagraficaPGEdit):
    """ Modifica un record dell'anagrafica secondaria """

    def __init__(self, anagrafica,daoRole):

        nome_anag_seco = daoRole.name
        title = 'Dati - Anagrafica %s' % nome_anag_seco

        AnagraficaEdit.__init__(self,
                        anagrafica,
                        'anagrafica_secondaria_detail_notebook',
                        title,
                        gladeFile='_anagrafica_secondaria_elements.glade')
        self._widgetFirstFocus = self.codice_entry
        self.idRole = daoRole.id

    def draw(self,cplx=False):
        fillComboBoxNazione(self.nazione_combobox, default="Italia")

        fillComboboxPagamenti(self.id_pagamento_customcombobox.combobox)
        self.id_pagamento_customcombobox.connect('clicked',
                                 on_id_pagamento_customcombobox_clicked)
        fillComboboxMagazzini(self.id_magazzino_customcombobox.combobox)
        self.id_magazzino_customcombobox.connect('clicked',
                                 on_id_magazzino_customcombobox_clicked)
        fillComboboxListini(self.id_listino_customcombobox.combobox)
        self.id_listino_customcombobox.connect('clicked',
                               on_id_listino_customcombobox_clicked)
        fillComboboxBanche(self.id_banca_customcombobox.combobox)
        self.id_banca_customcombobox.connect('clicked',
                                 on_id_banca_customcombobox_clicked)
        #fillComboboxAliquoteIva(self.id_aliquota_iva_customcombobox.combobox)
        #self.id_aliquota_iva_customcombobox.connect('clicked',
                                #on_id_aliquota_iva_customcombobox_clicked)

        #if not self.fornitore_insegna:
            #self.insegna_entry.destroy()
            #self.insegna_label.destroy()
        self.nome_entry.destroy()
        self.cognome_entry.destroy()
        self.cognome_label.destroy()
        self.nome_label.destroy()

    def setDao(self, dao):
        self.dao = dao
        if dao is None:
            # Crea un nuovo Dao vuoto
            self.dao = AnagraficaSecondaria()
            self.dao.codice = promogest.dao.AnagraficaSecondaria.\
                                        getNuovoCodiceAnagraficaSecondaria()

        if dao is None:
            self.dao_contatto = ContattoAnagraficaSecondaria()
        else:
            self.dao_contatto = ContattoAnagraficaSecondaria().select(
                                        idAnagraficaSecondaria=self.dao.id)
            if self.dao_contatto:
                self.dao_contatto = self.dao_contatto[0]
            else:
                self.dao_contatto = ContattoAnagraficaSecondaria()

        self._refresh()
        return self.dao

    def _refresh(self):
        if self.dao.ragione_sociale:
            rag_soc = self.dao.ragione_sociale
        elif self.dao.cognome or self.dao.nome:
            rag_soc = str(self.dao.cognome) + " " + str(self.dao.nome)
        elif self.dao.insegna:
            rag_soc = self.dao.insegna
        else:
            rag_soc = ""
        self.codice_entry.set_text(self.dao.codice or '')
        self.ragione_sociale_entry.set_text(rag_soc)

        self.indirizzo_sede_operativa_entry.set_text(
                                    self.dao.sede_operativa_indirizzo or '')
        self.cap_sede_operativa_entry.set_text(
                                    self.dao.sede_operativa_cap or '')
        self.localita_sede_operativa_entry.set_text(
                                    self.dao.sede_operativa_localita or '')
        self.provincia_sede_operativa_entry.set_text(
                                    self.dao.sede_operativa_provincia or '')
        self.indirizzo_sede_legale_entry.set_text(
                                    self.dao.sede_legale_indirizzo or '')
        self.cap_sede_legale_entry.set_text(
                                    self.dao.sede_legale_cap or '')
        self.localita_sede_legale_entry.set_text(
                                    self.dao.sede_legale_localita or '')
        self.provincia_sede_legale_entry.set_text(
                                    self.dao.sede_legale_provincia or '')
        self.codice_fiscale_entry.set_text(
                                    self.dao.codice_fiscale or '')
        self.partita_iva_entry.set_text(
                                    self.dao.partita_iva or '')
        textview_set_text(self.note_textview, self.dao.note or '')
        findComboboxRowFromId(self.id_pagamento_customcombobox.combobox,
                              self.dao.id_pagamento)
        findComboboxRowFromId(self.id_magazzino_customcombobox.combobox,
                              self.dao.id_magazzino)
        findComboboxRowFromId(self.id_listino_customcombobox.combobox,
                              self.dao.id_listino)
        findComboboxRowFromId(self.id_banca_customcombobox.combobox,
                              self.dao.id_banca)
        #findComboboxRowFromId(self.id_aliquota_iva_customcombobox.combobox,
                              #self.dao.id_aliquota_iva)
        findComboboxRowFromStr(self.nazione_combobox, self.dao.nazione, 0)
        self.showTotaliDareAvere()
        self.cellulare_principale_entry.set_text(self.dao.cellulare_principale)
        self.telefono_principale_entry.set_text(self.dao.telefono_principale)
        self.email_principale_entry.set_text(self.dao.email_principale)
        self.fax_principale_entry.set_text(self.dao.fax_principale)
        self.sito_web_principale_entry.set_text(self.dao.sito_principale)

    def showTotaliDareAvere(self):
        return
        if self.dao.id:
            #Calcoliamo il totale annuale:
            totaleAvereAnnuale = TotaleAnnualeFornitore(
                                                    id_fornitore=self.dao.id)
            self.totale_annuale_avere_entry.set_text(
                                            '%.2f' % totaleAvereAnnuale)
            #Calcoliamo il totale sospeso:
            totaleAvereSospeso = TotaleFornitoreAperto(id_fornitore=self.dao.id)
            self.totale_avere_entry.set_text('%.2f' % totaleAvereSospeso)
        self.anagrafica_fornitori_detail_notebook.set_current_page(0)

    def saveDao(self, tipo=None):
        if (self.ragione_sociale_entry.get_text() == ''):
            obligatoryField(self.dialogTopLevel,
                            self.ragione_sociale_entry,
                            msg='Campo obbligatorio !\n\nRagione sociale')

        self.dao.ragione_sociale = self.ragione_sociale_entry.get_text()
        if (self.dao.codice and \
                    (self.dao.ragione_sociale or \
                    self.dao.insegna or \
                    self.dao.cognome or \
                    self.dao.nome)) == '':
            msg="""Il codice è obbligatorio.
    Inserire almeno un campo a scelta tra:
    ragione sociale, insegna, cognome o nome """
            messageInfo(msg=msg)
            raise Exception('Operation aborted: Codice Fornitore obbligatorio')
        self.dao.sede_operativa_indirizzo = \
                                self.indirizzo_sede_operativa_entry.get_text()
        self.dao.sede_operativa_cap = self.cap_sede_operativa_entry.get_text()
        self.dao.sede_operativa_localita = \
                                self.localita_sede_operativa_entry.get_text()
        self.dao.sede_operativa_provincia = \
                                self.provincia_sede_operativa_entry.get_text()
        self.dao.sede_legale_indirizzo = \
                                self.indirizzo_sede_legale_entry.get_text()
        self.dao.sede_legale_cap = self.cap_sede_legale_entry.get_text()
        self.dao.sede_legale_localita = \
                                self.localita_sede_legale_entry.get_text()
        self.dao.sede_legale_provincia = \
                                self.provincia_sede_legale_entry.get_text()
        self.dao.codice_fiscale = self.codice_fiscale_entry.get_text()
        self.dao.note = textview_get_text(self.note_textview)
        if self.dao.codice_fiscale != '':
            codfis = checkCodFisc(self.dao.codice_fiscale)
            if not codfis:
                raise Exception('Operation aborted: Codice fiscale errato')
        self.dao.partita_iva = self.partita_iva_entry.get_text()
        if self.dao.partita_iva != '':
            partiva = checkPartIva(self.dao.partita_iva)
            if not partiva:
                raise Exception('Operation aborted: Partita iva errata')
        self.dao.id_pagamento = findIdFromCombobox(
                                self.id_pagamento_customcombobox.combobox)
        self.dao.id_magazzino = findIdFromCombobox(
                                self.id_magazzino_customcombobox.combobox)
        self.dao.id_listino = findIdFromCombobox(
                                self.id_listino_customcombobox.combobox)
        self.dao.id_banca = findIdFromCombobox(
                                self.id_banca_customcombobox.combobox)
        self.dao.id_ruolo = self.idRole
        self.dao.nazione = findStrFromCombobox(self.nazione_combobox, 0)
        self.dao.persist()


        self.aggiungi_contatto_pg(self, "generico")

        self.save_contatto_cellulare_principale(self, self.dao_contatto)
        self.save_contatto_telefono_principale(self, self.dao_contatto)
        self.save_contatto_fax_principale(self, self.dao_contatto)
        self.save_contatto_email_principale(self, self.dao_contatto)
        self.save_contatto_sito_principale(self, self.dao_contatto)

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
            if YesNoDialog(msg=msg, transient=self.dialogTopLevel):
                self.on_anagrafica_complessa_detail_dialog_response(
                    self.dialogTopLevel, GTK_RESPONSE_APPLY)
            else:
                toggleButton.set_active(False)
                return

        from promogest.ui.anagDocumenti.AnagraficaDocumenti import AnagraficaDocumenti
        anag = AnagraficaDocumenti()
        anagWindow = anag.getTopLevel()
        showAnagraficaRichiamata(self.dialogTopLevel, anagWindow, toggleButton)

        daos = []
        pgg = PersonaGiuridicaPersonaGiuridica().select(idPersonaGiuridica =self.dao.id, batchSize=None)
        if pgg:
            for p in pgg:
                cli = Cliente().getRecord(id=p.id_persona_giuridica_abbinata)
                if cli:
                    daos.append(cli.id)
        #TODO: Al momento funziona solo con le attività ( primi livelli )
        # andrà sistemato per gestire anche i livelli superiori
        #anag.filter.id_cliente_filter_customcombobox.setId(daos)
        anag.filter.id_clienti_abbinati = daos
        anag.filter.solo_contabili_check.set_active(True)
        anag.filter.refresh()


    def on_promemoria_togglebutton_toggled(self, toggleButton):
        if not(toggleButton.get_active()):
            toggleButton.set_active(False)
            return
        if posso("PR"):
            if self.dao.id is None:
                msg = 'Prima di poter inserire i contatti occorre salvare il Fornitore.\n Salvare ?'
                if YesNoDialog(msg=msg, transient=self.dialogTopLevel):
                    self.on_anagrafica_complessa_detail_dialog_response(self.dialogTopLevel, GTK_RESPONSE_APPLY)
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

    def on_icon_press_primary(self,entry,position,event):
        if position.value_nick == "primary":
            codice = promogest.dao.Fornitore.getNuovoCodiceFornitore()
            self.codice_entry.set_text(codice)

    def on_contatti_togglebutton_clicked(self, toggleButton):
        if posso("CN"):
            if not(toggleButton.get_active()):
                toggleButton.set_active(False)
                return

            if self.dao.id is None:
                msg = 'Prima di poter inserire i contatti occorre salvare il fornitore.\n Salvare ?'
                if YesNoDialog(msg=msg, transient=self.dialogTopLevel):
                    self.on_anagrafica_complessa_detail_dialog_response(self.dialogTopLevel, GTK_RESPONSE_APPLY)
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
            if YesNoDialog(msg=msg, transient=self.dialogTopLevel):
                self.on_anagrafica_complessa_detail_dialog_response(self.dialogTopLevel, GTK_RESPONSE_APPLY)
            else:
                toggleButton.set_active(False)
                return

        from promogest.ui.anagForniture.AnagraficaForniture import AnagraficaForniture
        anag = AnagraficaForniture(None, self.dao.id)
        anagWindow = anag.getTopLevel()

        showAnagraficaRichiamata(self.dialogTopLevel, anagWindow, toggleButton)

    def on_abbina_pg_toggle_clicked(self, toggleButton):
        if not(toggleButton.get_active()):
            toggleButton.set_active(False)
            return
        if self.dao.id is None:
            msg = 'Prima di poter inserire gli abbinamenti persona giuridica occorre salvare il cliente.\n Salvare ?'
            if YesNoDialog(msg=msg, transient=self.dialogTopLevel):
                self.on_anagrafica_complessa_detail_dialog_response(self.dialogTopLevel, GTK_RESPONSE_APPLY)
            else:
                toggleButton.set_active(False)
                return
        from AbbinamentoPersonaGiuridica import AbbinamentoPersonaGiuridica
        anag = AbbinamentoPersonaGiuridica(self.dao.id)
        anagWindow = anag.getTopLevel()

        showAnagraficaRichiamata(self.dialogTopLevel, anagWindow, toggleButton)

    def on_abbinamento_utente_togglebutton_toggled(self, toggleButton):
        if not(toggleButton.get_active()):
            toggleButton.set_active(False)
            return

        if self.dao.id is None:
            msg = 'Prima di poter abbinare un utente occorre salvare il cliente.\n Salvare ?'
            if YesNoDialog(msg=msg, transient=self.dialogTopLevel):
                self.on_anagrafica_complessa_detail_dialog_response(self.dialogTopLevel, GTK_RESPONSE_APPLY)
            else:
                toggleButton.set_active(False)
                return

        from promogest.modules.RuoliAzioni.ui.AnagraficaUtenti import AnagraficaUtenti
        from promogest.dao.User import User
        a = AnagraficaUtenti()
        if self.dao.id_user:
            art = User().getRecord(id=self.dao.id_user)
            a.on_record_edit_activate(a, dao=art)
        else:
            a.on_record_new_activate(a, from_other_dao=self.dao)
            a.editElement.username_entry.set_text(self.dao.ragione_sociale.strip().replace(" ","").lower() or (self.dao.cognome+self.dao.nome).strip().replace(" ","").lower())
            a.editElement.password_entry.set_text(self.dao.partita_iva.lower()[0:5] or
            self.dao.codice_fiscale.lower()[0:6])
            a.editElement.confirm_password_entry.set_text(self.dao.partita_iva.lower()[0:5] or self.dao.codice_fiscale.lower()[0:6])
            findComboboxRowFromStr(a.editElement.azienda_combobox, Environment.azienda,0)
            a.editElement.active_user_checkbutton.set_active(True)
            a.editElement.email_entry.set_text(self.dao.email_principale or "")
