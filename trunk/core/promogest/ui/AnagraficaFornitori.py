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
import gobject

from AnagraficaComplessa import Anagrafica, AnagraficaFilter, AnagraficaHtml, AnagraficaReport, AnagraficaEdit

from promogest import Environment
import promogest.dao.Fornitore
from promogest.dao.Fornitore import Fornitore
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

class AnagraficaFornitoriFilter(AnagraficaFilter):
    """ Filtro per la ricerca nell'anagrafica dei fornitori """

    def __init__(self, anagrafica):
        AnagraficaFilter.__init__(self,
                                  anagrafica,
                                  'anagrafica_fornitori_filter_vbox',
                                  gladeFile='_ricerca_fornitori.glade')
        self._widgetFirstFocus = self.ragione_sociale_filter_entry
        self.orderBy = 'ragione_sociale'
        persona_giuridica=Table('persona_giuridica', Environment.params['metadata'],schema = Environment.params['schema'], autoload=True)
        fornitore=Table('fornitore', Environment.params['metadata'],schema = Environment.params['schema'], autoload=True)
        self.joinT = join(fornitore, persona_giuridica)
        self.ricerca_avanzata_fornitori_filter_hbox.destroy()
        self.ricerca_avanzata_fornitori_filter_vbox.destroy()


    def draw(self):
        # Colonne della Treeview per il filtro
        treeview = self._anagrafica.anagrafica_filter_treeview
        renderer = gtk.CellRendererText()

        column = gtk.TreeViewColumn('Codice', renderer, text=1)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        column.connect("clicked", self._changeOrderBy, (self.joinT,Fornitore.codice))
        column.set_resizable(True)
        column.set_expand(False)
        column.set_min_width(100)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Ragione Sociale', renderer, text=2)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        column.connect("clicked", self._changeOrderBy, (self.joinT,Fornitore.ragione_sociale))
        column.set_resizable(True)
        column.set_expand(True)
        column.set_min_width(200)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Cognome - Nome', renderer, text=3)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        column.connect("clicked", self._changeOrderBy, (self.joinT,Fornitore.cognome))
        column.set_resizable(True)
        column.set_expand(False)
        column.set_min_width(200)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Localita''', renderer, text=4)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        column.connect("clicked", self._changeOrderBy, (self.joinT,Fornitore.sede_operativa_localita))
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
        self.codice_fiscale_filter_entry.set_text('')
        self.partita_iva_filter_entry.set_text('')
        fillComboboxCategorieFornitori(self.id_categoria_fornitore_filter_combobox, True)
        self.id_categoria_fornitore_filter_combobox.set_active(0)
        self.refresh()

    def refresh(self):
        # Aggiornamento TreeView
        codice = prepareFilterString(self.codice_filter_entry.get_text())
        ragioneSociale = prepareFilterString(self.ragione_sociale_filter_entry.get_text())
        insegna = prepareFilterString(self.insegna_filter_entry.get_text())
        cognomeNome = prepareFilterString(self.cognome_nome_filter_entry.get_text())
        localita = prepareFilterString(self.localita_filter_entry.get_text())
        partitaIva = prepareFilterString(self.partita_iva_filter_entry.get_text())
        codiceFiscale = prepareFilterString(self.codice_fiscale_filter_entry.get_text())
        idCategoria = findIdFromCombobox(self.id_categoria_fornitore_filter_combobox)

        def filterCountClosure():
            return Fornitore().count(codice=codice,
                                    ragioneSociale=ragioneSociale,
                                    insegna=insegna,
                                    cognomeNome=cognomeNome,
                                    localita=localita,
                                    partitaIva=partitaIva,
                                    codiceFiscale=codiceFiscale,
                                    idCategoria=idCategoria)

        self._filterCountClosure = filterCountClosure
        self.numRecords = self.countFilterResults()
        self._refreshPageCount()

        # Let's save the current search as a closure
        def filterClosure(offset, batchSize):
            return Fornitore().select(orderBy=self.orderBy,
                                                    codice=codice,
                                                    ragioneSociale=ragioneSociale,
                                                    insegna=insegna,
                                                    cognomeNome=cognomeNome,
                                                    localita=localita,
                                                    partitaIva=partitaIva,
                                                    codiceFiscale=codiceFiscale,
                                                    idCategoria=idCategoria,
                                                    offset=offset,
                                                    batchSize=batchSize)

        self._filterClosure = filterClosure

        fors = self.runFilter()

        self._treeViewModel.clear()

        for f in fors:
            pvcf = ''
            if (f.ragione_sociale or '') == '':
                pvcf = (f.codice_fiscale or '')
            else:
                pvcf = (f.partita_iva or '')
            self._treeViewModel.append((f,
                                        (f.codice or ''),
                                        (f.ragione_sociale or ''),
                                        (f.cognome or '') + ' ' + (f.nome or ''),
                                        (f.sede_operativa_localita or ''),
                                        pvcf))



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


    def setDao(self, dao):
        if dao is None:
            # Crea un nuovo Dao vuoto
            self.dao = Fornitore()
            self.dao.codice = promogest.dao.Fornitore.getNuovoCodiceFornitore()
        else:
            # Ricrea il Dao con una connessione al DBMS SQL
            self.dao = Fornitore().getRecord(id=dao.id)
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
        findComboboxRowFromId(self.id_categoria_fornitore_customcombobox.combobox,
                              self.dao.id_categoria_fornitore)
        findComboboxRowFromId(self.id_pagamento_customcombobox.combobox,
                              self.dao.id_pagamento)
        findComboboxRowFromId(self.id_magazzino_customcombobox.combobox,
                              self.dao.id_magazzino)
        findComboboxRowFromStr(self.nazione_combobox,self.dao.nazione, 0)
        self.showTotaliPrimaNota()

    def showTotaliPrimaNota(self):

        if self.dao.id:
            #Calcoliamo il totale annuale:
            totaleAvereAnnuale = TotaleAnnualeFornitore(id_fornitore=self.dao.id)
            self.totale_annuale_avere_entry.set_text('%.2f' % totaleAvereAnnuale)
            #Calcoliamo il totale sospeso:
            totaleAvereSospeso = TotaleFornitoreAperto(id_fornitore=self.dao.id)
            self.totale_avere_entry.set_text('%.2f' % totaleAvereSospeso)
        self.anagrafica_fornitori_detail_notebook.set_current_page(0)


    def saveDao(self):
        self.dao.codice = self.codice_entry.get_text()
        self.dao.codice = omogeneousCode(section="Fornitori", string=self.dao.codice )
        self.dao.ragione_sociale = self.ragione_sociale_entry.get_text()
        self.dao.insegna = self.insegna_entry.get_text()
        self.dao.cognome= self.cognome_entry.get_text()
        self.dao.nome = self.nome_entry.get_text()
        if (self.dao.codice and (self.dao.ragione_sociale or self.dao.insegna or self.dao.cognome or self.dao.nome)) =='':
            msg="""Il codice è obbligatorio.
    Inserire almeno un campo a scelta tra:
    ragione sociale, insegna, cognome o nome """
            dialog = gtk.MessageDialog(None, gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
                               gtk.MESSAGE_INFO, gtk.BUTTONS_OK, msg)
            dialog.run()
            dialog.destroy()
            raise Exception, 'Operation aborted'
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
                raise Exception, 'Operation aborted'
        self.dao.partita_iva = self.partita_iva_entry.get_text()
        if self.dao.partita_iva != '':
            partiva = checkPartIva(self.dao.partita_iva)
            if not partiva:
                raise Exception, 'Operation aborted'
        self.dao.id_categoria_fornitore = findIdFromCombobox(self.id_categoria_fornitore_customcombobox.combobox)
        self.dao.id_pagamento = findIdFromCombobox(self.id_pagamento_customcombobox.combobox)
        self.dao.id_magazzino = findIdFromCombobox(self.id_magazzino_customcombobox.combobox)
        self.dao.nazione = findStrFromCombobox(self.nazione_combobox,0)
        self.dao.persist()

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
        anag.filter.refresh()

    def on_contatti_togglebutton_clicked(self, toggleButton):
        if ("Contatti" in Environment.modulesList) or \
                ("pan" in Environment.modulesList) or \
                                ("basic" in Environment.modulesList):
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
