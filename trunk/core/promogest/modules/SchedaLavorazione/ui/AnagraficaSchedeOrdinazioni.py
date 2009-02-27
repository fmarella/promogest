# -*- coding: utf-8 -*-

# Promogest
#
# Copyright (C) 2007 by Promotux Informatica - http://www.promotux.it/
# Author: Dr astico (Pinna Marco) <zoccolodignu@gmail.com>
# Author: M3nt0r3 <m3nt0r3@gmail.com>

#import pygtk
#import gobject,
import datetime
from decimal import *

from promogest.ui.AnagraficaComplessa import Anagrafica, AnagraficaFilter, AnagraficaHtml, AnagraficaReport
#from promogest.modules.SchedaLavorazione.ui.AnagraficaCaratteriStampa import AnagraficaCaratteriStampa
#from promogest.modules.SchedaLavorazione.ui.AnagraficaColoriStampa import AnagraficaColoriStampa
from promogest import Environment
#from promogest.modules.SchedaLavorazione.dao import SchedaOrdinazione
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
        #self.record_duplicate_menu.set_property('visible', False)
        #pbuf = gtk.gdk.pixbuf_new_from_file(Environment.conf.guiDir + 'leggi_mail24x24.png')
        #button = gtk.ToolButton(icon_widget=pbuf, label='Importa da Mail')
        #button.connect('clicked', self.on_mail_import_button_clicked)
        #separator = gtk.SeparatorToolItem()
        #self.toolbar1.insert(separator,-1)
        #self.toolbar1.insert(button,-1)

    #def duplicate(self,dao):
        #""" Duplica le informazioni relative ad una scheda scelta su una nuova (a meno del numero) """
        #if dao is None:
            #return

        #self.editElement._duplicatedDaoId = dao.id
        #self.editElement.dao = SchedaOrdinazione(Environment.connection)
###------------------------------------------------------------------------------
        ##copia dei dati della vecchia scheda Ordinazione in una nuova
        #self.editElement.dao.note_text = dao.note_text
        #self.editElement.dao.note_final = dao.note_final
        #self.editElement.dao.note_spedizione = dao.note_spedizione
        #self.editElement.dao.note_fornitore = dao.note_fornitore
        #self.editElement.dao.nomi_sposi = dao.nomi_sposi
        #self.editElement.dao.provenienza = dao.provenienza
        #self.editElement.dao.referente = dao.referente
        #self.editElement.dao.via = dao.via
        #self.editElement.dao.num_civ = dao.num_civ
        #self.editElement.dao.zip = dao.zip
        #self.editElement.dao.localita = dao.localita
        #self.editElement.dao.provincia = dao.provincia
        #self.editElement.dao.stato  = dao.stato
        #self.editElement.dao.id_colore_stampa = dao.id_colore_stampa
        #self.editElement.dao.id_carattere_stampa = dao.id_carattere_stampa
        #self.editElement.dao.id_listino = dao.id_listino
        #self.editElement.dao.data_matrimonio = dao.data_matrimonio
        #self.editElement.dao.data_presa_in_carico = dao.data_presa_in_carico
        #self.editElement.dao.data_ricevuta = dao.data_ricevuta
        #self.editElement.dao.data_spedizione = dao.data_spedizione
        #self.editElement.dao.data_ordine_al_fornitore = dao.data_ordine_al_fornitore
        #self.editElement.dao.data_consegna_bozza = dao.data_consegna_bozza
        #self.editElement.dao.data_consegna = dao.data_consegna
        #self.editElement.dao.nome_contatto = dao.nome_contatto
        #self.editElement.dao.prima_email = dao.prima_email
        #self.editElement.dao.seconda_email = dao.seconda_email
        #self.editElement.dao.telefono = dao.telefono
        #self.editElement.dao.cellulare = dao.cellulare
        #self.editElement.dao.skype = dao.skype
        #self.editElement.dao.operatore = dao.operatore
        #self.editElement.dao.applicazione_sconti = dao.applicazione_sconti
        #self.editElement.dao.righe = dao.righe
        #self.editElement.dao.documento_saldato = dao.documento_saldato
        #self.editElement.dao.ricevuta_associata = dao.ricevuta_associata
        #self.editElement.dao.fattura_associata = dao.fattura_associata
        #self.editElement.dao.totale_lordo = dao.totale_lordo
        #self.editElement.dao.disp_materiale = dao.disp_materiale
        #self.editElement.setVisible(True)
        #self.editElement._refresh()

    #def on_mail_import_button_clicked(self, button):
        #import promogest.modules.SchedaLavorazione.lib.PopReader
        #thread = threading.Thread(target=PopReader.fetchMail)
        #thread.start()
        #thread.join(1.3)
        #create_schede_ordinazioni(PopReader.returned_mail_list)

class AnagraficaSchedeOrdinazioniFilter(AnagraficaFilter):
    """ Filtro per la ricerca nell'anagrafica degli articoli """

    def __init__(self, anagrafica):
        AnagraficaFilter.__init__(self,
                                  anagrafica,
                                  'anagrafica_schede_ordinazioni_filter_table',
                                    gladeFile='SchedaLavorazione/gui/SchedaLavorazione.glade',
                                    module=True)
        self._widgetFirstFocus = self.nome_sposi_filter_entry
        self.orderBy = 'id'

    def draw(self):
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

        self.refresh()

    def refresh(self):
        """
        Aggiornamento TreeView
        """
        _da_data_matrimonio = self.da_data_matrimonio_filter_entry.get_text()
        daDataMatrimonio = stringToDate(_da_data_matrimonio)
        _a_data_matrimonio = self.a_data_matrimonio_filter_entry.get_text()
        aDataMatrimonio = stringToDate(_a_data_matrimonio)
        _da_data_spedizione = self.da_data_spedizione_filter_entry.get_text()
        daDataSpedizione = stringToDate(_da_data_spedizione)
        _a_data_spedizione = self.a_data_spedizione_filter_entry.get_text()
        aDataSpedizione = stringToDate(_a_data_spedizione)
        _da_data_consegna = self.da_data_consegna_filter_entry.get_text()
        daDataConsegna = stringToDate(_da_data_consegna)
        _a_data_consegna = self.a_data_consegna_filter_entry.get_text()
        aDataConsegna = stringToDate(_a_data_consegna)
        _da_numero = self.da_numero_filter_entry.get_text()
        daNumero = prepareFilterString(_da_numero)
        _a_numero = self.a_numero_filter_entry.get_text()
        aNumero = prepareFilterString(_a_numero)
        _codice_spedizione = self.codice_spedizione_filter_entry.get_text()
        codiceSpedizione = prepareFilterString(_codice_spedizione)
        _numero_ricevuta = self.numero_ricevuta_filter_entry.get_text()
        numeroRicevuta = prepareFilterString(_numero_ricevuta)
        _nome_referente = self.referente_filter_entry.get_text()
        nomeReferente = prepareFilterString(_nome_referente)
        _nomi_sposi = self.nome_sposi_filter_entry.get_text()
        nomiSposi = prepareFilterString(_nomi_sposi)
        documentoSaldato = self.documento_saldato_checkbutton.get_active() or None
        coloreStampa = findIdFromCombobox(self.colore_stampa_filter_combobox)
        carattereStampa = findIdFromCombobox(self.carattere_stampa_filter_combobox)

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
                                                documentoSaldato=documentoSaldato)

        self._filterCountClosure = filterCountClosure
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
                                                documentoSaldato=documentoSaldato,
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
                                'Scheda Ordinazione',
                                templatesHTMLDir ="promogest/modules/SchedaLavorazione/templates/")

class AnagraficaSchedeOrdinazioniReport(AnagraficaReport):
    def __init__(self, anagrafica):
        AnagraficaReport.__init__(self, anagrafica=anagrafica,
                                  description='Scheda Ordinazione',
                                  defaultFileName='schede_ordinazioni',
                                  htmlTemplate='schede_ordinazioni',
                                  sxwTemplate='schede_ordinazioni',
                                    templatesDir ="promogest/modules/SchedaLavorazione/templates/")

