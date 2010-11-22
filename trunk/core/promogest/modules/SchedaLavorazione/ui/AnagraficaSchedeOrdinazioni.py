# -*- coding: utf-8 -*-

# Promogest
#
# Copyright (C) 2007 by Promotux Informatica - http://www.promotux.it/
# Author: Dr astico (Pinna Marco) <zoccolodignu@gmail.com>
# Author: M3nt0r3 <m3nt0r3@gmail.com>

import datetime
from decimal import *

from promogest.ui.AnagraficaComplessa import Anagrafica, AnagraficaFilter, AnagraficaHtml, AnagraficaReport
from promogest import Environment
from promogest.modules.SchedaLavorazione.dao.SchedaOrdinazione import SchedaOrdinazione
from promogest.ui.utils import *
from SchedaLavorazioneUtils import fillComboboxColoreStampa, fillComboboxCarattereStampa, fillComboboxAssociazioneArticoli, fetch_date, get_nomi_sposi, create_schede_ordinazioni, getPrezzoNetto
from AnagraficaSchedeOrdinazioniEdit import AnagraficaSchedeOrdinazioniEdit

class AnagraficaSchedeOrdinazioni(Anagrafica):
    """ Anagrafica Schede Ordinazione (Modulo SchedaLavorazione) """

    def __init__(self, aziendaStr=None):
        Anagrafica.__init__(self,
                            windowTitle='Promogest - Anagrafica Schede Lavorazione',
                            recordMenuLabel='_Schede Lavorazione',
                            filterElement=AnagraficaSchedeOrdinazioniFilter(self),
                            htmlHandler=AnagraficaSchedeOrdinazioniHtml(self),
                            reportHandler=AnagraficaSchedeOrdinazioniReport(self),
                            editElement=AnagraficaSchedeOrdinazioniEdit(self),
                            aziendaStr=aziendaStr)


class AnagraficaSchedeOrdinazioniFilter(AnagraficaFilter):
    """ Filtro per la ricerca nell'anagrafica degli articoli """

    def __init__(self, anagrafica):
        AnagraficaFilter.__init__(self,
                                  anagrafica,
                                  'anagrafica_schede_ordinazione_filter_vbox',
                                    gladeFile='SchedaLavorazione/gui/SchedaLavorazione.glade',
                                    module=True)
        self._widgetFirstFocus = self.nome_sposi_filter_entry
        self.orderBy = 'id'

    def draw(self, cplx=False):
        treeview = self._anagrafica.anagrafica_filter_treeview

        renderer = gtk.CellRendererText()
        column = gtk.TreeViewColumn('Numero', renderer, text=1)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        column.connect("clicked", self._changeOrderBy,(None, 'numero'))
        column.set_resizable(True)
        column.set_expand(False)
        column.set_min_width(100)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Numero Ricevuta/Fattura', renderer, text=2)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        column.connect("clicked", self._changeOrderBy, (None,'ricevuta_associata'))
        column.set_resizable(True)
        column.set_expand(False)
        column.set_min_width(100)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Sposi', renderer, text=3)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        column.connect("clicked", self._changeOrderBy, (None,'nomi_sposi'))
        column.set_resizable(True)
        column.set_expand(True)
        column.set_min_width(300)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Data Matrimonio', renderer, text=4)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        column.connect("clicked", self._changeOrderBy, 'data_matrimonio')
        column.set_resizable(True)
        column.set_expand(False)
        column.set_min_width(100)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Data Ordinazione', renderer, text=5, )
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        column.connect("clicked", self._changeOrderBy, 'data_presa_in_carico')
        column.set_resizable(True)
        column.set_expand(False)
        column.set_min_width(100)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Referente', renderer, text=6)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        column.connect("clicked", self._changeOrderBy, 'referente')
        column.set_resizable(True)
        column.set_expand(False)
        column.set_min_width(100)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Colore Stampa', renderer, text=7)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        column.connect("clicked", self._changeOrderBy, 'colore_stampa')
        column.set_resizable(True)
        column.set_expand(False)
        column.set_min_width(100)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Carattere Stampa', renderer, text=8)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        column.connect("clicked", self._changeOrderBy, 'carattere_stampa')
        column.set_resizable(True)
        column.set_expand(False)
        column.set_min_width(100)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Note', renderer, text=9)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        column.set_resizable(True)
        column.set_expand(False)
        column.set_min_width(100)
        treeview.append_column(column)

        self._treeViewModel = gtk.ListStore(object, str, str, str, str, str, str, str, str, str)
        self._anagrafica.anagrafica_filter_treeview.set_model(self._treeViewModel)

        fillComboboxColoreStampa(self.colore_stampa_filter_combobox, filter=True)
        fillComboboxCarattereStampa(self.carattere_stampa_filter_combobox, filter=True)
        fillComboboxPagamenti(self.tipo_pagamento_filter_combobox, filter=True)

        self.clear()

    def clear(self):
        # Annullamento filtro
        self.da_numero_filter_entry.set_text('')
        self.a_numero_filter_entry.set_text('')
        self.operatore_filter_entry.set_text('')
        self.da_data_matrimonio_filter_entry.set_text('01/01/'+Environment.workingYear)
        self.a_data_matrimonio_filter_entry.set_text('')
        self.da_data_spedizione_filter_entry.set_text('' )
        self.a_data_spedizione_filter_entry.set_text('')
        self.da_data_consegna_filter_entry.set_text('')
        self.a_data_consegna_filter_entry.set_text('')
        self.codice_spedizione_filter_entry.set_text('')
        self.numero_ricevuta_filter_entry.set_text('')
        self.referente_filter_entry.set_text('')
        self.colore_stampa_filter_combobox.set_active(0)
        self.carattere_stampa_filter_combobox.set_active(0)
        self.tipo_pagamento_filter_combobox.set_active(0)
        self.id_articolo_filter_customcombobox.set_active(0)

        self.refresh()

    def refresh(self):
        """
        Aggiornamento TreeView
        """
        daDataMatrimonio = stringToDate(self.da_data_matrimonio_filter_entry.get_text())
        aDataMatrimonio = stringToDate(self.a_data_matrimonio_filter_entry.get_text())
        daDataSpedizione = stringToDate(self.da_data_spedizione_filter_entry.get_text())
        aDataSpedizione = stringToDate(self.a_data_spedizione_filter_entry.get_text())
        daDataConsegna = stringToDate(self.da_data_consegna_filter_entry.get_text())
        aDataConsegna = stringToDate(self.a_data_consegna_filter_entry.get_text())
        daNumero = prepareFilterString(self.da_numero_filter_entry.get_text())
        aNumero = prepareFilterString(self.a_numero_filter_entry.get_text())
        codiceSpedizione = prepareFilterString(self.codice_spedizione_filter_entry.get_text())
        numeroRicevuta = prepareFilterString(self.numero_ricevuta_filter_entry.get_text())
        nomeReferente = prepareFilterString(self.referente_filter_entry.get_text())
        nomiSposi = prepareFilterString(self.nome_sposi_filter_entry.get_text())
        schedeAperte = self.schede_aperte_filter_combobox.get_active()
        if schedeAperte == -1 or schedeAperte == 0:
            schedeAperte = None
        elif schedeAperte == 1:
            schedeAperte = None
        elif schedeAperte == 2:
            schedeAperte = "FALSE"
        elif schedeAperte == 3:
            schedeAperte = "TRUE"
        else:
            schedeAperte = None

#        schedeAperte = self.schede_aperte_checkbutton.get_active() or None
        coloreStampa = findIdFromCombobox(self.colore_stampa_filter_combobox)
        carattereStampa = findIdFromCombobox(self.carattere_stampa_filter_combobox)
        idArticolo = self.id_articolo_filter_customcombobox.getId()
#        print "SCHEDE LAVORAZIONE", schedeAperte
        def filterCountClosure():
            return SchedaOrdinazione().count(daNumero=daNumero,
                                            aNumero=aNumero,
                                            daDataMatrimonio=daDataMatrimonio,
                                            aDataMatrimonio=aDataMatrimonio,
                                            daDataSpedizione=daDataSpedizione,
                                            aDataSpedizione=aDataSpedizione,
                                            daDataConsegna=daDataConsegna,
                                            aDataConsegna=aDataConsegna,
                                            codiceSpedizione=codiceSpedizione,
                                            coloreStampa=coloreStampa,
                                            carattereStampa=carattereStampa,
                                            nomiSposi = nomiSposi,
                                            referente=nomeReferente,
                                            ricevutaAssociata=numeroRicevuta,
                                            schedeAperte=schedeAperte,
                                            idArticolo = idArticolo)

        self._filterCountClosure = filterCountClosure
        #self.totaleRecords =
        self.numRecords = self.countFilterResults()
        self._refreshPageCount()

        # Let's save the current search as a closure
        def filterClosure(offset, batchSize):
            return SchedaOrdinazione().select(  orderBy=self.orderBy,
                                                daNumero=daNumero,
                                                aNumero=aNumero,
                                                daDataMatrimonio=daDataMatrimonio,
                                                aDataMatrimonio=aDataMatrimonio,
                                                daDataSpedizione=daDataSpedizione,
                                                aDataSpedizione=aDataSpedizione,
                                                daDataConsegna=daDataConsegna,
                                                aDataConsegna=aDataConsegna,
                                                codiceSpedizione=codiceSpedizione,
                                                coloreStampa=coloreStampa,
                                                carattereStampa=carattereStampa,
                                                nomiSposi = nomiSposi,
                                                referente=nomeReferente,
                                                ricevutaAssociata=numeroRicevuta,
                                                schedeAperte=schedeAperte,
                                                idArticolo = idArticolo,
                                                offset=offset,
                                                batchSize=batchSize)

        self._filterClosure = filterClosure
        tdos = self.runFilter()
        self._treeViewModel.clear()

        for t in tdos:
            data_matrimonio = dateToString(t.data_matrimonio)
            data_presa_in_carico = dateToString(t.data_presa_in_carico)
            self._treeViewModel.append((t,
                                        (t.numero or 0),
                                        (t.ricevuta_associata or ''),
                                        (t.nomi_sposi or ''),
                                        data_matrimonio,
                                        data_presa_in_carico,
                                        (t.referente or ''),
                                        (t.colore_stampa or ''),
                                        (t.carattere_stampa or ''),
                                        (t.note_final or '')))

class AnagraficaSchedeOrdinazioniHtml(AnagraficaHtml):
    def __init__(self, anagrafica):
        AnagraficaHtml.__init__(self, anagrafica, 'scheda_ordinazione',
                                'Scheda Ordinazione'
                                )

class AnagraficaSchedeOrdinazioniReport(AnagraficaReport):
    def __init__(self, anagrafica):
        AnagraficaReport.__init__(self, anagrafica=anagrafica,
                                  description='Scheda Ordinazione',
                                  defaultFileName='schede_ordinazioni',
                                  htmlTemplate='schede_ordinazioni',
                                  sxwTemplate='schede_ordinazioni',
                                  templatesDir ="promogest/modules/SchedaLavorazione/templates/")
