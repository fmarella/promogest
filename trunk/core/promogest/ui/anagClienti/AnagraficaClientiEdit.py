# -*- coding: utf-8 -*-

#    Copyright (C) 2005-2012 by Promotux
#                        di Francesco Meloni snc - http://www.promotux.it/

#    Author: Francesco Meloni  <francesco@promotux.it>
#    Author: Andrea Argiolas <andrea@promotux.it>
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

from promogest import Environment
from promogest.ui.gtk_compat import *
from promogest.ui.AnagraficaComplessaEdit import AnagraficaEdit
from promogest.ui.AnagraficaPGEdit import AnagraficaPGEdit
import promogest.dao.Cliente

from promogest.dao.Cliente import Cliente
from promogest.dao.ClienteCategoriaCliente import ClienteCategoriaCliente
from promogest.dao.daoContatti.ContattoCliente import ContattoCliente
from promogest.dao.DaoUtils import *
from promogest.lib.utils import *
from promogest.ui.utilsCombobox import *

if posso("IP"):
    from promogest.modules.InfoPeso.ui.InfoPesoNotebookPage import \
                                                InfoPesoNotebookPage


class AnagraficaClientiEdit(AnagraficaEdit, AnagraficaPGEdit):
    """ Modifica un record dell'anagrafica dei clienti """

    def __init__(self, anagrafica):
        AnagraficaEdit.__init__(self,
                                anagrafica,
                                'Dati cliente',
                                root='anagrafica_clienti_detail_notebook',
                                path='_anagrafica_clienti_elements.glade')

        AnagraficaPGEdit.__init__(self, "cliente")
        self._widgetFirstFocus = self.codice_entry
        self.anagrafica_clienti_detail_notebook.set_current_page(0)

    def draw(self, cplx=False):
        #Popola combobox categorie clienti
        fillComboboxCategorieClienti(
            self.id_categoria_cliente_customcombobox.combobox)
        self.id_categoria_cliente_customcombobox.connect('clicked',
                             on_id_categoria_cliente_customcombobox_clicked)
        #Elenco categorie

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
        fillComboboxAliquoteIva(self.id_aliquota_iva_customcombobox.combobox)
        self.id_aliquota_iva_customcombobox.connect('clicked',
                                on_id_aliquota_iva_customcombobox_clicked)

        self.cliente_insegna = setconf("Clienti", "cliente_insegna")
        if not self.cliente_insegna:
            self.insegna_entry.destroy()
            self.insegna_label.destroy()
        self.on_pg_radio_toggled()
        #self.cliente_nome = setconf("Clienti", "cliente_nome") or False
        #if not self.cliente_nome:
            #self.nome_entry.destroy()
            #self.nome_label.destroy()
#
        #self.cliente_cognome = setconf("Clienti", "cliente_cognome") or False
        #if not self.cliente_cognome:
            #self.cognome_entry.destroy()
            #self.cognome_label.destroy()

#        if not setconf(key="INFOPESO", section="General"):
        if posso("IP"):
            self.infopeso_page = InfoPesoNotebookPage(self, "")
            self.anagrafica_clienti_detail_notebook.append_page(
                            self.infopeso_page.infopeso_frame,
                            self.infopeso_page.infopeso_page_label)

    def on_anag_variazioni_listini_togglebutton_toggled(self, toggleButton):
        if toggleButton.get_active():
            from promogest.ui.AnagraficaVariazioniListini import AnagraficaVariazioniListini
            anag = AnagraficaVariazioniListini()
            anagWindow = anag.getTopLevel()
            showAnagraficaRichiamata(self.dialogTopLevel, anagWindow, toggleButton)
        else:
            toggleButton.set_active(False)
            self._refresh_variazioni_listini()
            self.anagrafica_clienti_detail_notebook.set_current_page(2)

    def on_variazioni_listini_toggle_toggled(self, cell, path):
        self.variazioni_tv_liststore[path][2] = not self.variazioni_tv_liststore[path][2]
        if self.variazioni_tv_liststore[path][2] == 0:
            self.dao.vl.remove(self.variazioni_tv_liststore[path][0])
        else:
            self.dao.vl.append(self.variazioni_tv_liststore[path][0])

    def on_pf_radio_toggled(self, button=None):
        if self.pf_radio:
            self.ragione_sociale_entry.set_sensitive(False)
            self.cognome_entry.set_sensitive(True)
            self.nome_entry.set_sensitive(True)

    def on_pg_radio_toggled(self, button=None):
        if self.pg_radio:
            self.ragione_sociale_entry.set_sensitive(True)
            self.cognome_entry.set_sensitive(False)
            self.nome_entry.set_sensitive(False)

    def on_categorie_clienti_add_row_button_clicked(self, widget):
        """
        Aggiunge una categoria cliente al dao selezionato
        """
        id = findIdFromCombobox(
            self.id_categoria_cliente_customcombobox.combobox)
        if id is not None:
            categoria = findStrFromCombobox(
                self.id_categoria_cliente_customcombobox.combobox, 2)
            model = self.categorie_treeview.get_model()
            for c in model:
                if c[0] == id:
                    return
            if Environment.pg3:
                ah = self.marcatore_add.get_stock()
                anagPixbuf = self.marcatore_add.render_icon(ah[0], ah[1], None)
            else:
                image = gtk.Image()
                anagPixbuf = image.render_icon(gtk.STOCK_ADD,
                                                GTK_ICON_SIZE_BUTTON)
            model.append((id, categoria, anagPixbuf, 'added'))
        self.categorie_treeview.get_selection().unselect_all()

    def on_categorie_clienti_delete_row_button_clicked(self, widget):
        """
        Rimuove una categoria al dao selezionato
        """
        id = findIdFromCombobox(
            self.id_categoria_cliente_customcombobox.combobox)
        if id is not None:
            if Environment.pg3:
                ah = self.marcatore_remove.get_stock()
                anagPixbuf = self.marcatore_remove.render_icon(
                                                        ah[0], ah[1], None)
            else:
                image = gtk.Image()
                anagPixbuf = image.render_icon(gtk.STOCK_REMOVE,
                                            GTK_ICON_SIZE_BUTTON)
            model = self.categorie_treeview.get_model()
            for c in model:
                if c[0] == id:
                    if c[2] is None:
                        c[2] = anagPixbuf
                        c[3] = 'deleted'
                    else:
                        model.remove(c.iter)
        self.categorie_treeview.get_selection().unselect_all()

    def on_categorie_clienti_undelete_row_button_clicked(self, widget):
        id = findIdFromCombobox(
                    self.id_categoria_cliente_customcombobox.combobox)
        if id is not None:
            model = self.categorie_treeview.get_model()
            for c in model:
                if c[0] == id:
                    if c[3] == 'deleted':
                        c[2] = None
                        c[3] = None
        self.categorie_treeview.get_selection().unselect_all()

    def on_categorie_treeview_cursor_changed(self, treeview=None):
        """ quando si clicca su una riga della treeview """
        sel = treeview.get_selection()
        (model, iterator) = sel.get_selected()
        if iterator is not None:
            idCategoriaCliente = model.get_value(iterator, 0)
            findComboboxRowFromId(
                            self.id_categoria_cliente_customcombobox.combobox,
                            idCategoriaCliente)
            status = model.get_value(iterator, 3)
            self.categorie_clienti_delete_row_button.set_sensitive(
                                                        status != 'deleted')
            self.categorie_clienti_undelete_row_button.set_sensitive(
                                                        status == 'deleted')

    def setDao(self, dao):
        self.dao = dao
        if dao is None:
            # Crea un nuovo Dao vuoto
            self.dao = Cliente()
            self.dao.codice = promogest.dao.Cliente.getNuovoCodiceCliente()

        if posso("IP"):
            self.infopeso_page.infoPesoSetDao(self.dao)
            self.infopeso_page.nome_cognome_label.set_text(
                            str(self.dao.ragione_sociale) or\
                            "" + "\n" + \
                            str(self.dao.cognome) or \
                            "" + " " + \
                            str(self.dao.nome) or "")

        if dao is None:
            self.dao_contatto = ContattoCliente()
        else:
            self.dao_contatto = ContattoCliente().select(idCliente=self.dao.id)
            if self.dao_contatto:
                self.dao_contatto = self.dao_contatto[0]
            else:
                self.dao_contatto = ContattoCliente()
        self._refresh()
        return self.dao

    def _refresh_variazioni_listini(self):
        from promogest.dao.VariazioneListino import VariazioneListino
        from promogest.lib.utils import fill_treeview_with_data
        diff = lambda l1,l2: [x for x in l1 if x not in l2]

        tutti = VariazioneListino().select(batchSize=None)
        if not self.dao.id:
            fill_treeview_with_data(self.variazioni_treeview, tutti)
        else:
            fill_treeview_with_data(self.variazioni_treeview, self.dao.vl, flag=True)
            fill_treeview_with_data(self.variazioni_treeview, diff(tutti, self.dao.vl), clear=False)

    def _refresh(self):
        self.codice_entry.set_text(self.dao.codice or '')
        if self.dao.ragione_sociale:
            rag_soc = self.dao.ragione_sociale
        elif self.dao.cognome or self.dao.nome:
            rag_soc = str(self.dao.cognome) + " " + str(self.dao.nome)
        elif self.dao.insegna:
            rag_soc = self.dao.insegna
        else:
            rag_soc = ""
        self.ragione_sociale_entry.set_text(rag_soc)
        if self.cliente_insegna:
            self.insegna_entry.set_text(self.dao.insegna or '')
        self.cognome_entry.set_text(self.dao.cognome or '')
        self.nome_entry.set_text(self.dao.nome or '')
        if self.dao.tipo == "PG":
            self.pg_radio.set_active(True)
            self.ragione_sociale_entry.set_sensitive(True)
            self.cognome_entry.set_sensitive(False)
            self.nome_entry.set_sensitive(False)
        if self.dao.tipo == "PF":
            self.pf_radio.set_active(True)
            self.ragione_sociale_entry.set_sensitive(False)
            self.cognome_entry.set_sensitive(True)
            self.nome_entry.set_sensitive(True)
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
        self.cap_sede_legale_entry.set_text(self.dao.sede_legale_cap or '')
        self.localita_sede_legale_entry.set_text(
            self.dao.sede_legale_localita or '')
        self.provincia_sede_legale_entry.set_text(
            self.dao.sede_legale_provincia or '')
        self.codice_fiscale_entry.set_text(self.dao.codice_fiscale or '')
        self.partita_iva_entry.set_text(self.dao.partita_iva or '')
        text_buffer = self.note_textview.get_buffer()
        text_buffer.set_text(self.dao.note or '')

        self.id_categoria_cliente_customcombobox.combobox.set_active(-1)
        self._refreshCategorie()

        findComboboxRowFromId(self.id_pagamento_customcombobox.combobox,
                              self.dao.id_pagamento)
        findComboboxRowFromId(self.id_magazzino_customcombobox.combobox,
                              self.dao.id_magazzino)
        findComboboxRowFromId(self.id_listino_customcombobox.combobox,
                              self.dao.id_listino)
        findComboboxRowFromId(self.id_banca_customcombobox.combobox,
                              self.dao.id_banca)
        findComboboxRowFromId(self.id_aliquota_iva_customcombobox.combobox,
                              self.dao.id_aliquota_iva)
        findComboboxRowFromStr(self.nazione_combobox, self.dao.nazione, 0)
        #finComboBoxNazione(self.nazione_combobox, default="Italia")
        #if Environment.conf.hasPagamenti == True:
        if posso("IP"):
            self.infopeso_page.infoPeso_refresh()
        self.showTotaliDareAvere()
        self.cellulare_principale_entry.set_text(
            self.dao.cellulare_principale or "")
        self.telefono_principale_entry.set_text(
            self.dao.telefono_principale or "")
        self.email_principale_entry.set_text(self.dao.email_principale or "")
        self.fax_principale_entry.set_text(self.dao.fax_principale or "")
        self.sito_web_principale_entry.set_text(self.dao.sito_principale or "")
        self.spese_checkbox.set_active(self.dao.pagante or False )

        self._refresh_variazioni_listini()

    def showTotaliDareAvere(self):

        if self.dao.id:
            totaleDareAnnuale = TotaleAnnualeCliente(id_cliente=self.dao.id)
            self.totale_annuale_dare_entry.set_text(
                                       str(mN(totaleDareAnnuale, 2)))
            # Calcoliamo il totale sospeso:
            totaleDareAperto = TotaleClienteAperto(id_cliente=self.dao.id)
            self.totale_dare_entry.set_text(str(mN(totaleDareAperto, 2)))

        self.anagrafica_clienti_detail_notebook.set_current_page(0)

    def _refreshCategorie(self, widget=None, orderBy=None):

        model = self.categorie_treeview.get_model()
        model.clear()
        if not self.dao.id:
            return
        categorie = self.dao.categorieCliente
        for c in categorie:
            model.append([c.id_categoria_cliente,
                        c.categoria_cliente.denominazione, None, None])

    def on_icon_press_primary(self, entry, position, event):
        if position.value_nick == "primary":
            codice = promogest.dao.Cliente.getNuovoCodiceCliente()
            self.codice_entry.set_text(codice)


    def saveDao(self, tipo=None):
        if self.pg_radio.get_active():
            if (self.ragione_sociale_entry.get_text() == ''):
                obligatoryField(self.dialogTopLevel,
                                self.ragione_sociale_entry,
                                msg='Campo obbligatorio !\n\nRagione sociale')
        if self.pf_radio.get_active():
            if (self.cognome_entry.get_text() == ''):
                obligatoryField(self.dialogTopLevel,
                                self.cognome_entry,
                                msg='Campo obbligatorio !\n\nCognome')
            if (self.nome_entry.get_text() == ''):
                obligatoryField(self.dialogTopLevel,
                                self.nome_entry,
                                msg='Campo obbligatorio !\n\nNome')
#        self.verificaListino()

        self.dao.pagante = self.spese_checkbox.get_active()
        self.dao.codice = self.codice_entry.get_text().upper()
        self.dao.codice = omogeneousCode(section="Clienti",
                                        string=self.dao.codice)
        self.dao.ragione_sociale = self.ragione_sociale_entry.get_text()

        #self.cliente_nome = setconf("Clienti", "cliente_nome") or False
        #if self.cliente_nome:
        self.dao.nome = self.nome_entry.get_text()

        #self.cliente_cognome = setconf("Clienti", "cliente_cognome") or False
        #if self.cliente_cognome:
        self.dao.cognome = self.cognome_entry.get_text()

        if self.cliente_insegna:
            self.dao.insegna = self.insegna_entry.get_text()
        if self.pf_radio.get_active():
            self.dao.ragione_sociale = self.cognome_entry.get_text()\
                            + " " + self.nome_entry.get_text()
            self.dao.tipo = "PF"

        if (self.dao.codice and\
                    (self.dao.ragione_sociale or \
                    self.dao.insegna or \
                    self.dao.cognome or \
                    self.dao.nome)) == '':
            msg = """Il codice è obbligatorio.
    Inserire anche ragione sociale / cognome e nome """
            messageInfo(msg=msg)
            raise Exception,\
                'Operation aborted Campo minimo cliente non inserito'
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
        self.dao.partita_iva = self.partita_iva_entry.get_text()
        text_buffer = self.note_textview.get_buffer()
        self.dao.note = text_buffer.get_text(text_buffer.get_start_iter(),
                                            text_buffer.get_end_iter(), True)
        #if self.dao.partita_iva != '':
            #partiva = checkPartIva(self.dao.partita_iva)
            #if not partiva:
                #raise Exception, 'Operation aborted: Partita iva non corretta'
        self.dao.id_pagamento = findIdFromCombobox(
            self.id_pagamento_customcombobox.combobox)
        self.dao.id_magazzino = findIdFromCombobox(
            self.id_magazzino_customcombobox.combobox)
        self.dao.id_listino = findIdFromCombobox(
            self.id_listino_customcombobox.combobox)
        self.dao.id_banca = findIdFromCombobox(
            self.id_banca_customcombobox.combobox)
        self.dao.id_aliquota_iva = findIdFromCombobox(
            self.id_aliquota_iva_customcombobox.combobox)
        self.dao.nazione = findStrFromCombobox(self.nazione_combobox, 0)
        self.dao.persist()
        if posso("IP"):
            (dao_testata_infopeso, dao_generalita_infopeso) = \
                                    self.infopeso_page.infoPesoSaveDao()
            dao_testata_infopeso.id_cliente = self.dao.id
            dao_testata_infopeso.persist()
            dao_generalita_infopeso.id_cliente = self.dao.id
            dao_generalita_infopeso.persist()

        model = self.categorie_treeview.get_model()
        cleanClienteCategoriaCliente = ClienteCategoriaCliente()\
                                            .select(idCliente=self.dao.id,
                                            batchSize=None)
        for cli in cleanClienteCategoriaCliente:
            cli.delete()
        for c in model:
            if c[3] == 'deleted':
                pass
            else:
                daoClienteCategoriaCliente = ClienteCategoriaCliente()
                daoClienteCategoriaCliente.id_cliente = self.dao.id
                daoClienteCategoriaCliente.id_categoria_cliente = c[0]
                daoClienteCategoriaCliente.persist()
        #self.dao.categorieCliente = categorie
        self._refreshCategorie()

        #SEzione dedicata ai contatti/recapiti principali
        self.aggiungi_contatto_pg(self, "cliente")

        self.save_contatto_cellulare_principale(self, self.dao_contatto)
        self.save_contatto_telefono_principale(self, self.dao_contatto)
        self.save_contatto_fax_principale(self, self.dao_contatto)
        self.save_contatto_email_principale(self, self.dao_contatto)
        self.save_contatto_sito_principale(self, self.dao_contatto)

    def on_scheda_contabile_togglebutton_clicked(self, toggleButton):
        """
        Apre la finestra di registrazione documenti, ricercando solo
        i documenti del cliente
        """

        if not(toggleButton.get_active()):
            toggleButton.set_active(False)
            return

        if self.dao.id is None:
            msg = 'Prima di poter visualizzare la registrazione documenti occorre salvare il cliente.\n Salvare? '
            if YesNoDialog(msg=msg, transient=self.dialogTopLevel):
                self.on_anagrafica_complessa_detail_dialog_response(
                        self.dialogTopLevel, GTK_RESPONSE_APPLY)
            else:
                toggleButton.set_active(False)
                return

        from promogest.ui.anagDocumenti.AnagraficaDocumenti import \
                                                    AnagraficaDocumenti
        anag = AnagraficaDocumenti()
        anagWindow = anag.getTopLevel()
        showAnagraficaRichiamata(self.dialogTopLevel, anagWindow,
                toggleButton)
        anag.filter.id_cliente_filter_customcombobox.setId(self.dao.id)
        anag.filter.solo_contabili_check.set_active(True)
        anag.filter.refresh()


    def on_abbina_pg_toggle_clicked(self, toggleButton):
        if not(toggleButton.get_active()):
            toggleButton.set_active(False)
            return
        if self.dao.id is None:
            msg = 'Prima di poter inserire gli abbinamenti persona giuridica occorre salvare il cliente.\n Salvare ?'
            if YesNoDialog(msg=msg, transient=self.dialogTopLevel):
                self.on_anagrafica_complessa_detail_dialog_response(
                    self.dialogTopLevel,
                    GTK_RESPONSE_APPLY)
            else:
                toggleButton.set_active(False)
                return
        from promogest.ui.AbbinamentoPersonaGiuridica import AbbinamentoPersonaGiuridica
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
                self.on_anagrafica_complessa_detail_dialog_response(
                            self.dialogTopLevel,
                            GTK_RESPONSE_APPLY)
            else:
                toggleButton.set_active(False)
                return

        from promogest.modules.RuoliAzioni.ui.AnagraficaUtenti import \
                                                            AnagraficaUtenti
        from promogest.dao.User import User
        a = AnagraficaUtenti()
        if self.dao.id_user:
            art = User().getRecord(id=self.dao.id_user)
            a.on_record_edit_activate(a, dao=art)
        else:
            a.on_record_new_activate(a, from_other_dao=self.dao)
            a.editElement.username_entry.set_text(
                self.dao.ragione_sociale.strip().replace(" ", "").lower() or\
         (self.dao.cognome + self.dao.nome).strip().replace(" ", "").lower())
            a.editElement.password_entry.set_text(
                self.dao.partita_iva.lower()[0:6] or \
                    self.dao.codice_fiscale.lower()[0:6])
            a.editElement.confirm_password_entry.set_text(
                self.dao.partita_iva.lower()[0:6] or\
                self.dao.codice_fiscale.lower()[0:6])
            findComboboxRowFromStr(a.editElement.azienda_combobox,
                            Environment.azienda, 0)
            a.editElement.active_user_checkbutton.set_active(True)
            a.editElement.email_entry.set_text(self.dao.email_principale or "")

    def on_destinazioni_merce_togglebutton_clicked(self, toggleButton):
        if not(toggleButton.get_active()):
            toggleButton.set_active(False)
            return

        if self.dao.id is None:
            msg = 'Prima di poter inserire le destinazioni merce occorre salvare il cliente.\n Salvare ?'
            if YesNoDialog(msg=msg, transient=self.dialogTopLevel):
                self.on_anagrafica_complessa_detail_dialog_response(
                    self.dialogTopLevel,
                    GTK_RESPONSE_APPLY)
            else:
                toggleButton.set_active(False)
                return

        from promogest.ui.AnagraficaDestinazioniMerce import AnagraficaDestinazioniMerce
        anag = AnagraficaDestinazioniMerce(self.dao.id)
        anagWindow = anag.getTopLevel()

        showAnagraficaRichiamata(self.dialogTopLevel, anagWindow, toggleButton)

    def on_label_togglebutton_clicked(self, toggleButton):
        if not(toggleButton.get_active()):
            toggleButton.set_active(False)
            return

        if self.dao.id is None:
            msg = 'Prima di poter stampare una label occorre salvare l\' il cliente.\n Salvare ?'
            if YesNoDialog(msg=msg, transient=self.dialogTopLevel):
                self.on_anagrafica_complessa_detail_dialog_response(
                            self.dialogTopLevel,
                            GTK_RESPONSE_APPLY)
            else:
                toggleButton.set_active(False)
                return

        if posso("LA"):
            from promogest.modules.Label.ui.ManageLabelsToPrintCliente import\
                                                ManageLabelsToPrintCliente
            a = ManageLabelsToPrintCliente(mainWindow=self, daos=[],
                                                        cliente=self.dao)
            anagWindow = a.getTopLevel()
            returnWindow = self.getTopLevel().get_toplevel()
            anagWindow.set_transient_for(returnWindow)
            anagWindow.show_all()
        else:
            fencemsg()
        toggleButton.set_active(False)

    def on_filechooserbutton_file_set(self, filechooser):
        #import StringIO
        #output = StringIO.StringIO()
        #image.save(output)
        #contents = output.getvalue()
        #output.close()

        print "LA FOTO SELEZIONATA", filechooser.get_file().get_path(), \
                                                     filechooser.get_file()
        self.photo_src = filechooser.get_filename()
        self.userlogo_image.set_from_file(self.photo_src)
        #im1 = Image.fromstring(self.photo_src)
        f = open(self.photo_src, "r")
        g = f.read()
        #im = Image.open(g)
        #im.thumbnail(size, Image.ANTIALIAS)
        #im.tostring(self.photo_src + ".thumbnail)
        self.imgblob = base64.b64encode(str(g))
        f.close()

    def on_rimuovi_foto_button_clicked(self, button):
        self.imgblob = "RIMUOVO"
        self.userlogo_image.set_from_file("")
