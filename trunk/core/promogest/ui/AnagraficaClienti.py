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



class AnagraficaClientiFilter(AnagraficaFilter):
    """ Filtro per la ricerca nell'anagrafica dei clienti """

    def __init__(self, anagrafica):
        AnagraficaFilter.__init__(self,
                                  anagrafica,
                                  'anagrafica_clienti_filter_vbox',
                                  gladeFile='_ricerca_clienti.glade')
        self._widgetFirstFocus = self.ragione_sociale_filter_entry
        self.orderBy = 'ragione_sociale'
        self.ricerca_avanzata_clienti_filter_hbox.destroy()
        self.ricerca_avanzata_clienti_filter_vbox.destroy()
        self.joinT = None # join(cliente, perso_giuri)

    def draw(self):
        """ Disegno la treeview e gli altri oggetti della gui """
        treeview = self._anagrafica.anagrafica_filter_treeview
        renderer = gtk.CellRendererText()

        column = gtk.TreeViewColumn('Codice', renderer, text=1)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        column.connect("clicked", self._changeOrderBy, (None,PersonaGiuridica_.codice))
        column.set_resizable(True)
        column.set_expand(False)
        column.set_min_width(100)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Ragione Sociale', renderer, text=2)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)

        column.connect("clicked", self._changeOrderBy,(None,PersonaGiuridica_.ragione_sociale))
        column.set_resizable(True)
        column.set_expand(True)
        column.set_min_width(200)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Cognome - Nome', renderer, text=3)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        column.connect("clicked", self._changeOrderBy, (None,PersonaGiuridica_.cognome))
        column.set_resizable(True)
        column.set_expand(False)
        column.set_min_width(200)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Localita''', renderer, text=4)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        column.connect("clicked", self._changeOrderBy, (None,PersonaGiuridica_.sede_operativa_localita))
        column.set_resizable(True)
        column.set_expand(False)
        column.set_min_width(100)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Partita IVA / Codice fiscale', renderer, text=5)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(False)
        column.set_resizable(True)
        column.set_expand(False)
        column.set_min_width(100)
        treeview.append_column(column)

        treeview.set_search_column(1)

        self._treeViewModel = gtk.ListStore(object, str, str, str, str, str)
        self._anagrafica.anagrafica_filter_treeview.set_model(self._treeViewModel)

        self.clear()

    def clear(self):
        # Annullamento filtro
        self.codice_filter_entry.set_text('')
        self.ragione_sociale_filter_entry.set_text('')
        self.insegna_filter_entry.set_text('')
        self.cognome_nome_filter_entry.set_text('')
        self.localita_filter_entry.set_text('')
        self.provincia_filter_entry.set_text('')
        self.codice_fiscale_filter_entry.set_text('')
        self.partita_iva_filter_entry.set_text('')
        fillComboboxCategorieClienti(self.id_categoria_cliente_filter_combobox, True)
        self.id_categoria_cliente_filter_combobox.set_active(0)
        self.refresh()

    def refresh(self):
        """
        Aggiorno l'interfaccia con i dati filtrati
        """
        codice = prepareFilterString(self.codice_filter_entry.get_text())
        ragioneSociale = prepareFilterString(self.ragione_sociale_filter_entry.get_text())
        insegna = prepareFilterString(self.insegna_filter_entry.get_text())
        cognomeNome = prepareFilterString(self.cognome_nome_filter_entry.get_text())
        localita = prepareFilterString(self.localita_filter_entry.get_text())
        provincia = prepareFilterString(self.provincia_filter_entry.get_text())
        partitaIva = prepareFilterString(self.partita_iva_filter_entry.get_text())
        codiceFiscale = prepareFilterString(self.codice_fiscale_filter_entry.get_text())
        idCategoria = findIdFromCombobox(self.id_categoria_cliente_filter_combobox)

        def filterCountClosure():
            return Cliente().count( codice=codice,
                                    ragioneSociale=ragioneSociale,
                                    insegna=insegna,
                                    cognomeNome=cognomeNome,
                                    localita=localita,
                                    provincia=provincia,
                                    partitaIva=partitaIva,
                                    codiceFiscale=codiceFiscale,
                                    idCategoria=idCategoria)

        self._filterCountClosure = filterCountClosure

        self.numRecords = self.countFilterResults()

        self._refreshPageCount()

        # Let's save the current search as a closure
        def filterClosure(offset, batchSize):
            return Cliente().select(orderBy=self.orderBy,
                                    join=self.join,
                                    codice=codice,
                                    ragioneSociale=ragioneSociale,
                                    insegna=insegna,
                                    cognomeNome=cognomeNome,
                                    localita=localita,
                                    provincia=provincia,
                                    partitaIva=partitaIva,
                                    codiceFiscale=codiceFiscale,
                                    idCategoria=idCategoria,
                                    offset=offset,
                                    batchSize=batchSize)

        self._filterClosure = filterClosure

        clis = self.runFilter()

        self._treeViewModel.clear()

        for c in clis:
            pvcf = ''
            if (c.ragione_sociale or '') == '':
                pvcf = (c.codice_fiscale or '')
            else:
                pvcf = (c.partita_iva or '')
            self._treeViewModel.append((c,
                                        (c.codice or ''),
                                        (c.ragione_sociale or ''),
                                        (c.cognome or '') + ' ' + (c.nome or ''),
                                        (c.sede_operativa_localita or ''),
                                        pvcf))


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


class AnagraficaClientiEdit(AnagraficaEdit):
    """ Modifica un record dell'anagrafica dei clienti """

    def __init__(self, anagrafica):
        AnagraficaEdit.__init__(self,
                                anagrafica,
                                'anagrafica_clienti_detail_notebook',
                                'Dati cliente',
                                gladeFile='_anagrafica_clienti_elements.glade')
        self._widgetFirstFocus = self.codice_entry

    def draw(self,cplx=False):
        #Popola combobox categorie clienti
        fillComboboxCategorieClienti(self.id_categoria_cliente_customcombobox.combobox)
        self.id_categoria_cliente_customcombobox.connect('clicked',
                                                         on_id_categoria_cliente_customcombobox_clicked)
        #Elenco categorie
        rendererText = gtk.CellRendererText()
        column = gtk.TreeViewColumn('Categoria', rendererText, text=1)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(False)
        column.set_resizable(True)
        column.set_expand(True)
        self.categorie_treeview.append_column(column)

        rendererPixbuf = gtk.CellRendererPixbuf()
        column = gtk.TreeViewColumn('', rendererPixbuf, pixbuf=2)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(False)
        column.set_resizable(False)
        column.set_expand(False)
        column.set_min_width(20)
        self.categorie_treeview.append_column(column)

        model = gtk.ListStore(int, str, gtk.gdk.Pixbuf, str)
        self.categorie_treeview.set_model(model)

        fillComboBoxNazione(self.nazione_combobox, default="Italia")
        #Popola combobox pagamenti
        fillComboboxPagamenti(self.id_pagamento_customcombobox.combobox)
        self.id_pagamento_customcombobox.connect('clicked',
                                 on_id_pagamento_customcombobox_clicked)
        #Popola combobox magazzini
        fillComboboxMagazzini(self.id_magazzino_customcombobox.combobox)
        self.id_magazzino_customcombobox.connect('clicked',
                                 on_id_magazzino_customcombobox_clicked)
        #Popola combobox listini
        fillComboboxListini(self.id_listino_customcombobox.combobox)
        self.id_listino_customcombobox.connect('clicked',
                               on_id_listino_customcombobox_clicked)
        fillComboboxBanche(self.id_banca_customcombobox.combobox)
        self.id_banca_customcombobox.connect('clicked',
                                 on_id_banca_customcombobox_clicked)
        #Popola combobox aliquote iva
        fillComboboxAliquoteIva(self.id_aliquota_iva_customcombobox.combobox)
        self.id_aliquota_iva_customcombobox.connect('clicked',
                                on_id_aliquota_iva_customcombobox_clicked)

    def on_categorie_clienti_add_row_button_clicked(self, widget):
        """
        Aggiunge una categoria cliente al dao selezionato
        """
        id = findIdFromCombobox(self.id_categoria_cliente_customcombobox.combobox)
        if id is not None:
            categoria = findStrFromCombobox(self.id_categoria_cliente_customcombobox.combobox, 2)
            model = self.categorie_treeview.get_model()
            for c in model:
                if c[0] == id:
                    return
            image = gtk.Image()
            anagPixbuf = image.render_icon(gtk.STOCK_ADD,
                                               gtk.ICON_SIZE_BUTTON)
            model.append((id, categoria, anagPixbuf, 'added'))
        self.categorie_treeview.get_selection().unselect_all()

    def on_categorie_clienti_delete_row_button_clicked(self, widget):
        """
        Rimuove una categoria al dao selezionato
        """
        id = findIdFromCombobox(self.id_categoria_cliente_customcombobox.combobox)
        if id is not None:
            image = gtk.Image()
            anagPixbuf = image.render_icon(gtk.STOCK_REMOVE,
                                           gtk.ICON_SIZE_BUTTON)
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
        id = findIdFromCombobox(self.id_categoria_cliente_customcombobox.combobox)
        if id is not None:
            model = self.categorie_treeview.get_model()
            for c in model:
                if c[0] == id:
                    if c[3] == 'deleted':
                        c[2] = None
                        c[3] = None
        self.categorie_treeview.get_selection().unselect_all()

    def on_categorie_treeview_cursor_changed(self, treeview = None):
        """ quando si clicca su una riga della treeview """
        sel = treeview.get_selection()
        (model, iterator) = sel.get_selected()
        if iterator is not None:
            idCategoriaCliente = model.get_value(iterator, 0)
            findComboboxRowFromId(self.id_categoria_cliente_customcombobox.combobox, idCategoriaCliente)
            status = model.get_value(iterator, 3)
            self.categorie_clienti_delete_row_button.set_sensitive(status != 'deleted')
            self.categorie_clienti_undelete_row_button.set_sensitive(status == 'deleted')

    def setDao(self, dao):
        if dao is None:
            # Crea un nuovo Dao vuoto
            self.dao = Cliente()
            self.dao.codice = promogest.dao.Cliente.getNuovoCodiceCliente()
            self._oldDaoRicreato = False
        else:
            # Ricrea il Dao con una connessione al DBMS SQL
            self.dao = Cliente().getRecord(id=dao.id)
            self._oldDaoRicreato = True
        self._refresh()
        return self.dao

    def _refresh(self):
        self.codice_entry.set_text(self.dao.codice or '')
        self.ragione_sociale_entry.set_text(self.dao.ragione_sociale or '')
        self.insegna_entry.set_text(self.dao.insegna or '')
        self.cognome_entry.set_text(self.dao.cognome or '')
        self.nome_entry.set_text(self.dao.nome or '')
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
        findComboboxRowFromStr(self.nazione_combobox,self.dao.nazione, 0)
        #finComboBoxNazione(self.nazione_combobox, default="Italia")
        #if Environment.conf.hasPagamenti == True:
        self.showTotaliPrimaNota()

    def showTotaliPrimaNota(self):

        if self.dao.id:
            totaleDareAnnuale = TotaleAnnualeCliente(id_cliente=self.dao.id)
            self.totale_annuale_dare_entry.set_text('%.2f' % totaleDareAnnuale)
            # Calcoliamo il totale sospeso:
            totaleDareAperto = TotaleClienteAperto(id_cliente=self.dao.id)
            self.totale_dare_entry.set_text('%.2f' % totaleDareAperto)

        self.anagrafica_clienti_detail_notebook.set_current_page(0)

    def _refreshCategorie(self, widget=None, orderBy=None):

        model = self.categorie_treeview.get_model()
        model.clear()
        if not self.dao.id:
            return
        categorie = self.dao.categorieCliente
        for c in categorie:
            model.append([c.id_categoria_cliente, c.categoria_cliente.denominazione, None, None])

    def saveDao(self):
        self.verificaListino()

        self.dao.codice = self.codice_entry.get_text()
        self.dao.codice = omogeneousCode(section="Clienti", string=self.dao.codice )
        self.dao.ragione_sociale = self.ragione_sociale_entry.get_text()
        self.dao.insegna = self.insegna_entry.get_text()
        self.dao.cognome= self.cognome_entry.get_text()
        self.dao.nome= self.nome_entry.get_text()
        if (self.dao.codice and (self.dao.ragione_sociale or self.dao.insegna or self.dao.cognome or self.dao.nome)) =='':
            msg="""Il codice è obbligatorio.
    Inserire almeno un campo a scelta tra:
    ragione sociale, insegna, cognome o nome """
            dialog = gtk.MessageDialog(None, gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
                               gtk.MESSAGE_INFO, gtk.BUTTONS_OK, msg)
            dialog.run()
            dialog.destroy()
            raise Exception, 'Operation aborted Campo minimo cliente non inserito'
        self.dao.sede_operativa_indirizzo = self.indirizzo_sede_operativa_entry.get_text()
        self.dao.sede_operativa_cap = self.cap_sede_operativa_entry.get_text()
        self.dao.sede_operativa_localita = self.localita_sede_operativa_entry.get_text()
        self.dao.sede_operativa_provincia = self.provincia_sede_operativa_entry.get_text()
        self.dao.sede_legale_indirizzo = self.indirizzo_sede_legale_entry.get_text()
        self.dao.sede_legale_cap = self.cap_sede_legale_entry.get_text()
        self.dao.sede_legale_localita = self.localita_sede_legale_entry.get_text()
        self.dao.sede_legale_provincia = self.provincia_sede_legale_entry.get_text()
        self.dao.codice_fiscale = self.codice_fiscale_entry.get_text()
        self.dao.partita_iva = self.partita_iva_entry.get_text()
        if self.dao.partita_iva != '':
            partiva = checkPartIva(self.dao.partita_iva)
            if not partiva:
                raise Exception, 'Operation aborted: Partita iva non corretta'
        self.dao.id_pagamento = findIdFromCombobox(self.id_pagamento_customcombobox.combobox)
        self.dao.id_magazzino = findIdFromCombobox(self.id_magazzino_customcombobox.combobox)
        self.dao.id_listino = findIdFromCombobox(self.id_listino_customcombobox.combobox)
        self.dao.id_banca = findIdFromCombobox(self.id_banca_customcombobox.combobox)
        self.dao.nazione = findStrFromCombobox(self.nazione_combobox,0)
        if self.dao.codice_fiscale != '':
            codfis = checkCodFisc(self.dao.codice_fiscale)
            if not codfis:
                raise Exception, 'Operation aborted: Codice Fiscale non corretto'
        self.dao.persist()
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
            dialog = gtk.MessageDialog(self.dialogTopLevel,
                    gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
                    gtk.MESSAGE_QUESTION,
                    gtk.BUTTONS_YES_NO,
                    msg)
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
        showAnagraficaRichiamata(self.dialogTopLevel, anagWindow,
                toggleButton)
        anag.filter.id_cliente_filter_customcombobox.setId(self.dao.id)
        anag.filter.refresh()

    def on_contatti_togglebutton_clicked(self, toggleButton):
        if not(toggleButton.get_active()):
            toggleButton.set_active(False)
            return
        if posso("CN"):
            if self.dao.id is None:
                msg = 'Prima di poter inserire i contatti occorre salvare il cliente.\n Salvare ?'
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

            from promogest.modules.Contatti.ui.AnagraficaContatti import AnagraficaContatti
            anag = AnagraficaContatti(self.dao.id, 'cliente')
            anagWindow = anag.getTopLevel()

            showAnagraficaRichiamata(self.dialogTopLevel, anagWindow, toggleButton)
        else:
            fenceDialog()
            toggleButton.set_active(False)

    def on_destinazioni_merce_togglebutton_clicked(self, toggleButton):
        if not(toggleButton.get_active()):
            toggleButton.set_active(False)
            return

        if self.dao.id is None:
            msg = 'Prima di poter inserire le destinazioni merce occorre salvare il cliente.\n Salvare ?'
            dialog = gtk.MessageDialog(self.dialogTopLevel, gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
                                       gtk.MESSAGE_QUESTION, gtk.BUTTONS_YES_NO, msg)
            response = dialog.run()
            dialog.destroy()
            if response == gtk.RESPONSE_YES:
                self.on_anagrafica_complessa_detail_dialog_response(self.dialogTopLevel, gtk.RESPONSE_APPLY)
            else:
                toggleButton.set_active(False)
                return

        from AnagraficaDestinazioniMerce import AnagraficaDestinazioniMerce
        anag = AnagraficaDestinazioniMerce(self.dao.id)
        anagWindow = anag.getTopLevel()

        showAnagraficaRichiamata(self.dialogTopLevel, anagWindow, toggleButton)

    def verificaListino(self):
        """ Verifica se il listino inserito e' compatibile con le categorie e il magazzino associati al cliente """
        from promogest.dao.ListinoCategoriaCliente import ListinoCategoriaCliente
        from promogest.dao.ListinoMagazzino import ListinoMagazzino
        listino = findIdFromCombobox(self.id_listino_customcombobox.combobox)
        #FIXME : ricontrollare
        #if listino is not None:
            #categoriaOk = True
            #magazzinoOk = True
            #model = self.categorie_treeview.get_model()
            #categorie = set(c[0] for c in model if c[3] != 'deleted')
            #categorieListino = set(c.id_categoria_cliente for c in ListinoCategoriaCliente()\
                                        #.select(idListino=listino,batchSize=None, orderBy="id_listino"))
            #categoriaOk = len(categorieListino.intersection(categorie)) > 0
            #magazzino = findIdFromCombobox(self.id_magazzino_customcombobox.combobox)
            #if magazzino is not None:
                #magazziniListino = set(m.id_magazzino for m in ListinoMagazzino()\
                                        #.select(idListino=listino,batchSize=None, orderBy="id_listino"))
                #magazzinoOk = (magazzino in magazziniListino)
            #print "FIXME: RICONTROLLLLLLLAAAAAARREEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE"
            #if not(categoriaOk and magazzinoOk):
                #msg = 'Il listino inserito non sembra compatibile con il magazzino e le categorie indicate.\nContinuare ?'
                #dialog = gtk.MessageDialog(self.dialogTopLevel, gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
                                           #gtk.MESSAGE_WARNING, gtk.BUTTONS_YES_NO, msg)
                #response = dialog.run()
                #dialog.destroy()
                #if response != gtk.RESPONSE_YES:
                    #raise Exception, 'Operation aborted'
