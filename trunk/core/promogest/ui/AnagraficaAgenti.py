# -*- coding: iso-8859-15 -*-

"""
 Promogest
 Copyright (C) 2005-2008 by Promotux Informatica - http://www.promotux.it/
 Author: Andrea Argiolas <andrea@promotux.it>
 Author: Francesco Meloni <francesco@promotux.it>
 License: GNU GPLv2
"""

import gtk
import gobject

from AnagraficaComplessa import Anagrafica, AnagraficaFilter, AnagraficaHtml, AnagraficaReport, AnagraficaEdit

from promogest import Environment
from promogest.dao.Dao import Dao
import promogest.dao.Agente
from promogest.dao.Agente import Agente

from utils import *
from utilsCombobox import *


class AnagraficaAgenti(Anagrafica):
    """ Anagrafica agenti """

    def __init__(self,aziendaStr=None):
        Anagrafica.__init__(self,
                            windowTitle='Promogest - Anagrafica agenti',
                            recordMenuLabel='_Agenti',
                            filterElement=AnagraficaAgentiFilter(self),
                            htmlHandler=AnagraficaAgentiHtml(self),
                            reportHandler=AnagraficaAgentiReport(self),
                            editElement=AnagraficaAgentiEdit(self),
                            aziendaStr=aziendaStr)



class AnagraficaAgentiFilter(AnagraficaFilter):
    """ Filtro per la ricerca nell'anagrafica degli agenti """

    def __init__(self, anagrafica):
        AnagraficaFilter.__init__(self,
                                  anagrafica,
                                  'anagrafica_agenti_filter_table',
                                  gladeFile='_anagrafica_agenti_elements.glade')
     ##   self._widgetFirstFocus = self.ragione_sociale_filter_entry
        self.orderBy = 'ragione_sociale'


    def draw(self):
        # Colonne della Treeview per il filtro
        treeview = self._anagrafica.anagrafica_filter_treeview
        renderer = gtk.CellRendererText()

        column = gtk.TreeViewColumn('Codice', renderer, text=1)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        column.connect("clicked", self._changeOrderBy, 'codice')
        column.set_resizable(True)
        column.set_expand(False)
        column.set_min_width(100)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Ragione Sociale', renderer, text=2)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        column.connect("clicked", self._changeOrderBy, 'ragione_sociale')
        column.set_resizable(True)
        column.set_expand(True)
        column.set_min_width(200)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Cognome - Nome', renderer, text=3)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        column.connect("clicked", self._changeOrderBy, 'cognome, nome')
        column.set_resizable(True)
        column.set_expand(False)
        column.set_min_width(200)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Localita''', renderer, text=4)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        column.connect("clicked", self._changeOrderBy, 'sede_operativa_localita')
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

        self._treeViewModel = gtk.ListStore(gobject.TYPE_PYOBJECT, str, str, str, str, str)
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
        self.ragione_sociale_filter_entry.grab_focus()
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

        def filterCountClosure():
            return Agente(isList=True).count(codice=codice,
                                            ragioneSociale=ragioneSociale,
                                            insegna=insegna,
                                            cognomeNome=cognomeNome,
                                            localita=localita,
                                            partitaIva=partitaIva,
                                            codiceFiscale=codiceFiscale)

        self._filterCountClosure = filterCountClosure

        self.numRecords = self.countFilterResults()

        self._refreshPageCount()

        # Let's save the current search as a closure
        def filterClosure(offset, batchSize):
            return Agente(isList=True).select(orderBy=self.orderBy,
                                            codice=codice,
                                            ragioneSociale=ragioneSociale,
                                            insegna=insegna,
                                            cognomeNome=cognomeNome,
                                            localita=localita,
                                            partitaIva=partitaIva,
                                            codiceFiscale=codiceFiscale,
                                            offset=offset,
                                            batchSize=batchSize)

        self._filterClosure = filterClosure

        fors = self.runFilter()

        self._treeViewModel.clear()

        for f in fors:
            pvcf = ''
            if (f.ragione_sociale or '') == '':
                pvcf = f.codice_fiscale
            else:
                pvcf = f.partita_iva
            self._treeViewModel.append((f,
                                        (f.codice or ''),
                                        (f.ragione_sociale or ''),
                                        (f.cognome or '') + ' ' + (f.nome or ''),
                                        (f.sede_operativa_localita or ''),
                                        pvcf))



class AnagraficaAgentiHtml(AnagraficaHtml):
    def __init__(self, anagrafica):
        AnagraficaHtml.__init__(self, anagrafica, 'agente',
                                'Informazioni sull''agente')



class AnagraficaAgentiReport(AnagraficaReport):
    def __init__(self, anagrafica):
        AnagraficaReport.__init__(self, anagrafica=anagrafica,
                                  description='Elenco degli agenti',
                                  defaultFileName='agenti',
                                  htmlTemplate='agenti',
                                  sxwTemplate='agenti')



class AnagraficaAgentiEdit(AnagraficaEdit):
    """ Modifica un record dell'anagrafica degli agenti """

    def __init__(self, anagrafica):
        AnagraficaEdit.__init__(self,
                                anagrafica,
                                'anagrafica_agenti_detail_table',
                                'Dati agente',
                                gladeFile='_anagrafica_agenti_elements.glade')
        self._widgetFirstFocus = self.codice_entry


    def draw(self):
        pass


    def setDao(self, dao):
        if dao is None:
            # Crea un nuovo Dao vuoto
            self.dao = Agente().getRecord()
            self.dao.codice = promogest.dao.Agente.getNuovoCodiceAgente()
        else:
            # Ricrea il Dao con una connessione al DBMS SQL
            self.dao = Agente(id=dao.id).getRecord()
        self._refresh()


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


    def saveDao(self):
        self.dao.codice = self.codice_entry.get_text()
        self.dao.codice = omogeneousCode(section="Agenti", string=self.dao.codice )
        self.dao.ragione_sociale = self.ragione_sociale_entry.get_text()
        self.dao.insegna = self.insegna_entry.get_text()
        self.dao.cognome = self.cognome_entry.get_text()
        self.dao.nome = self.nome_entry.get_text()
        if (self.dao.codice and (self.dao.ragione_sociale or self.dao.insegna or self.dao.cognome or self.dao.nome)) =='':
            msg="""Il codice è obbligatorio!
    Inserire almeno un campo a scelta tra:
    ragione sociale, insegna, cognome o nome """
            dialog = gtk.MessageDialog(None, gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
                               gtk.MESSAGE_INFO, gtk.BUTTONS_OK, msg)
            dialog.run()
            dialog.destroy()
            return
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
                return
        self.dao.partita_iva = self.partita_iva_entry.get_text()
        if self.dao.partita_iva != '':
            partiva = checkPartIva(self.dao.partita_iva)
            if not partiva:
                return
        self.dao.persist()
