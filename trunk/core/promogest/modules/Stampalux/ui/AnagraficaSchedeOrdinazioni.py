# -*- coding: utf-8 -*-

# Promogest
#
# Copyright (C) 2007 by Promotux Informatica - http://www.promotux.it/
# Author: Dr astico (Pinna Marco) <zoccolodignu@gmail.com>
# Author: M3nt0r3 <m3nt0r3@gmail.com>

import pygtk
import gobject, datetime
from decimal import *

from promogest.ui.AnagraficaComplessa import Anagrafica, AnagraficaFilter, AnagraficaHtml, AnagraficaReport, AnagraficaEdit
from promogest.modules.Stampalux.ui.AnagraficaCaratteriStampa import AnagraficaCaratteriStampa
from promogest.modules.Stampalux.ui.AnagraficaColoriStampa import AnagraficaColoriStampa
from promogest import Environment
from promogest.dao.Dao import Dao
from promogest.modules.Stampalux.dao import SchedaOrdinazione
from promogest.modules.Stampalux.dao.SchedaOrdinazione import SchedaOrdinazione
from promogest.modules.Stampalux.dao.RigaSchedaOrdinazione import RigaSchedaOrdinazione
from promogest.modules.Stampalux.dao.ScontoSchedaOrdinazione import ScontoSchedaOrdinazione
from promogest.modules.Stampalux.dao.ColoreStampa import ColoreStampa
from promogest.modules.Stampalux.dao.CarattereStampa import CarattereStampa
from promogest.dao.Listino import Listino
from promogest.dao.ListinoArticolo import ListinoArticolo
from promogest.dao.Pagamento import Pagamento
from promogest.modules.Stampalux.dao.ScontoRigaScheda import ScontoRigaScheda
from promogest.modules.Stampalux.dao.AssociazioneArticoli import AssociazioneArticoli
from promogest.dao.Articolo import Articolo
from promogest.dao.UnitaBase import UnitaBase
from promogest.dao.Cliente import Cliente
from promogest.modules.Stampalux.dao.PromemoriaSchedaOrdinazione import PromemoriaSchedaOrdinazione
from promogest.dao.TestataDocumento import TestataDocumento
from promogest.ui.GladeWidget import GladeWidget
from promogest.ui.utils import *
from StampaluxUtils import fillComboboxColoreStampa, fillComboboxCarattereStampa, fillComboboxAssociazioneArticoli, fetch_date, get_nomi_sposi, create_schede_ordinazioni, getPrezzoNetto
from widgets.SchedeOrdinazioniEditWidget import SchedeOrdinazioniEditWidget

class AnagraficaSchedeOrdinazioni(Anagrafica):
    """ Anagrafica Schede Ordinazione (Modulo Stampalux) """

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

    def duplicate(self,dao):
        """ Duplica le informazioni relative ad una scheda scelta su una nuova (a meno del numero) """
        if dao is None:
            return

        self.editElement._duplicatedDaoId = dao.id
        self.editElement.dao = SchedaOrdinazione(Environment.connection)
##-----------------------------------------------------------------------------------------------------
        #copia dei dati della vecchia scheda Ordinazione in una nuova
        self.editElement.dao.note_text = dao.note_text
        self.editElement.dao.note_final = dao.note_final
        self.editElement.dao.note_spedizione = dao.note_spedizione
        self.editElement.dao.note_fornitore = dao.note_fornitore
        self.editElement.dao.nomi_sposi = dao.nomi_sposi
        self.editElement.dao.provenienza = dao.provenienza
        self.editElement.dao.referente = dao.referente
        self.editElement.dao.via = dao.via
        self.editElement.dao.num_civ = dao.num_civ
        self.editElement.dao.zip = dao.zip
        self.editElement.dao.localita = dao.localita
        self.editElement.dao.provincia = dao.provincia
        self.editElement.dao.stato  = dao.stato
        self.editElement.dao.id_colore_stampa = dao.id_colore_stampa
        self.editElement.dao.id_carattere_stampa = dao.id_carattere_stampa
        self.editElement.dao.id_listino = dao.id_listino
        self.editElement.dao.data_matrimonio = dao.data_matrimonio
        self.editElement.dao.data_presa_in_carico = dao.data_presa_in_carico
        self.editElement.dao.data_ricevuta = dao.data_ricevuta
        self.editElement.dao.data_spedizione = dao.data_spedizione
        self.editElement.dao.data_ordine_al_fornitore = dao.data_ordine_al_fornitore
        self.editElement.dao.data_consegna_bozza = dao.data_consegna_bozza
        self.editElement.dao.data_consegna = dao.data_consegna
        self.editElement.dao.nome_contatto = dao.nome_contatto
        self.editElement.dao.prima_email = dao.prima_email
        self.editElement.dao.seconda_email = dao.seconda_email
        self.editElement.dao.telefono = dao.telefono
        self.editElement.dao.cellulare = dao.cellulare
        self.editElement.dao.skype = dao.skype
        self.editElement.dao.operatore = dao.operatore
        self.editElement.dao.applicazione_sconti = dao.applicazione_sconti
        self.editElement.dao.righe = dao.righe
        self.editElement.dao.documento_saldato = dao.documento_saldato
        self.editElement.dao.ricevuta_associata = dao.ricevuta_associata
        self.editElement.dao.fattura_associata = dao.fattura_associata
        self.editElement.dao.totale_lordo = dao.totale_lordo
        self.editElement.dao.disp_materiale = dao.disp_materiale
        self.editElement.setVisible(True)
        self.editElement._refresh()

    def on_mail_import_button_clicked(self, button):
        import promogest.modules.Stampalux.lib.PopReader
        thread = threading.Thread(target=PopReader.fetchMail)
        thread.start()
        thread.join(1.3)
        create_schede_ordinazioni(PopReader.returned_mail_list)

class AnagraficaSchedeOrdinazioniFilter(AnagraficaFilter):
    """ Filtro per la ricerca nell'anagrafica degli articoli """

    def __init__(self, anagrafica):
        AnagraficaFilter.__init__(self,
                                  anagrafica,
                                  'anagrafica_schede_ordinazioni_filter_table', gladeFile='Stampalux/gui/Stampalux.glade', module=True)
        self._widgetFirstFocus = self.nome_sposi_filter_entry
        self.orderBy = 'id'

    def draw(self):
        treeview = self._anagrafica.anagrafica_filter_treeview

        renderer = gtk.CellRendererText()
        column = gtk.TreeViewColumn('Numero', renderer, text=1)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        column.connect("clicked", self._changeOrderBy, 'numero')
        column.set_resizable(True)
        column.set_expand(False)
        column.set_min_width(100)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Numero Ricevuta/Fattura', renderer, text=2)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        column.connect("clicked", self._changeOrderBy, 'ricevuta_associata')
        column.set_resizable(True)
        column.set_expand(False)
        column.set_min_width(100)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Sposi', renderer, text=3)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        column.connect("clicked", self._changeOrderBy, 'nomi_sposi')
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
        fillComboboxCarattereStampa(self.carattere_stampa_filter_combobox, True)
        fillComboboxPagamenti(self.tipo_pagamento_filter_combobox, filter=True)

        self.clear()

    def clear(self):
        # Annullamento filtro
        self.da_numero_filter_entry.set_text('')
        self.a_numero_filter_entry.set_text('')
        self.operatore_filter_entry.set_text('')
        self.da_data_matrimonio_filter_entry.set_text('01/01/'+Environment.conf.workingYear)
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
                                'Scheda Ordinazione')

class AnagraficaSchedeOrdinazioniReport(AnagraficaReport):
    def __init__(self, anagrafica):
        AnagraficaReport.__init__(self, anagrafica=anagrafica,
                                  description='Scheda Ordinazione',
                                  defaultFileName='schede_ordinazioni',
                                  htmlTemplate='schede_ordinazioni',
                                  sxwTemplate='schede_ordinazioni')

class AnagraficaSchedeOrdinazioniEdit(SchedeOrdinazioniEditWidget, AnagraficaEdit):
    """
    Modifica i dati relativi ad una scheda lavorazione
    """

    def __init__(self, anagrafica):
        SchedeOrdinazioniEditWidget.__init__(self)
        self.pack_widgets()
        self.connect_callbacks()
        self.main_widget = self.anagrafica_schede_ordinazioni_detail_vbox
        self._prepareWindowPlacement()
        self.window =  self.anagrafica_schede_ordinazioni_detail_vbox
        self._windowTitle ='Dettagli scheda lavorazione'
        self._anagrafica = anagrafica
        self._widgetFirstFocus = self.nomi_sposi_entry
        self.rimuovi_articolo_button.set_sensitive(False)
        self._loading = False
        self._tabPressed = False
        self._id_listino = None
        self.daoListino = None
        self.daoCarattereStampa = None
        self.daoPagamento = None
        self.daoColoreStampa = None
        self._sconti = None
        self.daoCliente = None
        self._tipoPersonaGiuridica = 'cliente'
        self._parzialeLordo = Decimal(str(0))
        self._parzialeNetto = Decimal(str(0))

        self._articoliTreeviewModel = gtk.ListStore(object, str, str, str, str, str, str, str, str)

    def draw(self):
        """
        popola le combobox della gui e imposta le colonne degli articoli nella treeview articoli
        """
        fillComboboxListini(self.listino_combobox)
        fillComboboxMagazzini(self.magazzino_combobox)
        fillComboboxAssociazioneArticoli(self.associazione_articoli_comboboxentry)
        self.id_cliente_customcombobox.setSingleValue()
        self.id_cliente_customcombobox.setOnChangedCall(self.on_cliente_changed)
        self.id_cliente_customcombobox.setType(self._tipoPersonaGiuridica)

        #popolazione delle treeview
        treeview = self.articoli_treeview

        renderer = gtk.CellRendererText()
        renderer.set_data('column', 0)
        renderer.set_data('min_length', 150)
        column = gtk.TreeViewColumn('Codice articolo', renderer, text=2)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_FIXED)
        column.set_clickable(False)
        column.set_resizable(False)
        column.set_expand(False)
        column.set_alignment(0.5)
        column.set_fixed_width(150)
        treeview.append_column(column)

        renderer = gtk.CellRendererText()
        renderer.set_property('editable', True)
        renderer.set_property('xalign', 0)
        renderer.connect('edited', self.on_column_edited, treeview, False)
        renderer.set_data('max_length', 200)
        renderer.set_data('column', 1)
        column = gtk.TreeViewColumn('Descrizione', renderer, text=3)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_FIXED)
        column.set_clickable(False)
        column.set_resizable(True)
        column.set_expand(True)
        column.set_alignment(0.5)
        column.set_min_width(300)
        treeview.append_column(column)

        renderer = gtk.CellRendererText()
        renderer.set_data('column', 2)
        renderer.set_property('xalign', 0.5)
        renderer.set_data('min_length', 50)
        column = gtk.TreeViewColumn('U.M.', renderer, text=4)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_FIXED)
        column.set_clickable(False)
        column.set_resizable(False)
        column.set_expand(False)
        column.set_alignment(0.5)
        column.set_fixed_width(50)
        treeview.append_column(column)

        renderer = gtk.CellRendererText()
        renderer.set_property('editable', True)
        renderer.set_property('xalign', 0.5)
        renderer.connect('edited', self.on_column_edited, treeview, False)
        renderer.set_data('column', 3)
        renderer.set_data('min_length', 100)
        column = gtk.TreeViewColumn('Q.ta', renderer, text=5)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_FIXED)
        column.set_clickable(False)
        column.set_resizable(False)
        column.set_expand(False)
        column.set_alignment(0.5)
        column.set_fixed_width(80)
        treeview.append_column(column)

        renderer = gtk.CellRendererText()
        renderer.set_property('editable', True)
        renderer.set_property('xalign', 1)
        renderer.connect('edited', self.on_column_edited, treeview, False)
        renderer.set_data('column', 4)
        renderer.set_data('max_length', 200)
        column = gtk.TreeViewColumn('Prezzo lordo', renderer, text=6)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_FIXED)
        column.set_clickable(False)
        column.set_resizable(False)
        column.set_expand(False)
        column.set_alignment(0.5)
        column.set_fixed_width(100)
        treeview.append_column(column)

        renderer = gtk.CellRendererText()
        renderer.set_property('xalign', 1)
        renderer.set_data('column', 5)
        renderer.set_data('max_length', 200)
        column = gtk.TreeViewColumn('Prezzo netto', renderer, text=7)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_FIXED)
        column.set_clickable(False)
        column.set_resizable(False)
        column.set_expand(False)
        column.set_alignment(0.5)
        column.set_fixed_width(100)
        treeview.append_column(column)

        renderer = gtk.CellRendererText()
        renderer.set_data('column', 6)
        renderer.set_property('xalign', 1)
        column = gtk.TreeViewColumn('Totale', renderer, text=8)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_FIXED)
        column.set_clickable(False)
        column.set_resizable(False)
        column.set_expand(False)
        column.set_alignment(0.5)
        column.set_fixed_width(100)
        treeview.append_column(column)

        self._articoliTreeviewModel = gtk.ListStore(object, str, str, str, str, str, str,str,str)
        self.articoli_treeview.set_model(self._articoliTreeviewModel)

        self.sconti_scheda_widget.button.connect('toggled',self.on_sconti_scheda_widget_button_toggled)

    def setDao(self, dao):

        if dao is None:
            self.dao = SchedaOrdinazione()
            self.dao.data_presa_in_carico = datetime.datetime.today()
            self._dataScheda = dateToString(self.dao.data_presa_in_carico)
            self._numeroScheda = 0
            self._clear()
            self._refresh()
        else:
            self._dataScheda = dateToString(dao.data_presa_in_carico)
            self._numeroScheda=dao.numero
            self.dao = dao
            if self.dao.id_colore_stampa:
                self.daoColoreStampa = ColoreStampa().getRecord(id =self.dao.id_colore_stampa)
            if self.dao.id_carattere_stampa:
                self.daoCarattereStampa = CarattereStampa().getRecord(id=self.dao.id_carattere_stampa)
            if self.dao.id_cliente:
                self.daoCliente = Cliente().getRecord(id=self.dao.id_cliente)

            if len(self.dao.righe) > 0:
                self._id_listino = self.dao.righe[0].id_listino
                self.daoListino = Listino().getRecord(id=self._id_listino)
            self.dettagli_scheda_notebook.set_current_page(0)
            self._refresh( firstLoad=True)

    def _refresh(self, firstLoad=False):
        """
        Riempie  tutti i form della scheda con i relativi valori del dao (se impostati)
        """

        self._loading = True
        self._parzialeLordo = Decimal(str(0))
        self._parzialeNetto = Decimal(str(0))
        if not firstLoad:
            self._getStrings()
        self._clear()
        fillComboboxCarattereStampa(self.carattere_stampa_combobox)
        fillComboboxColoreStampa(self.colore_stampa_combobox)
        if  self._id_listino is None and len(self.dao.righe) > 0:
            self._id_listino = self.dao.righe[0].id_listino
            self.daoListino = Listino().getRecord(id=self._id_listino)
        _data_matrimonio = dateToString(self.dao.data_matrimonio)
        self.data_matrimonio_entry.set_text(_data_matrimonio)
        _data_ordine_al_fornitore = dateToString(self.dao.data_ordine_al_fornitore)
        self.data_ordine_al_fornitore_entry.set_text(_data_ordine_al_fornitore)
        _data_consegna = dateToString(self.dao.data_consegna)
        self.data_consegna_entry.set_text(_data_consegna)
        _data_spedizione = dateToString(self.dao.data_spedizione)
        self.data_spedizione_entry.set_text(_data_spedizione)
        _data_consegna_bozza = dateToString(self.dao.data_consegna_bozza)
        self.data_consegna_bozza_entry.set_text(_data_consegna_bozza)
        _data_presa_in_carico = dateToString(self.dao.data_presa_in_carico)
        self.data_presa_in_carico_entry.set_text(_data_presa_in_carico)


        self.provenienza_entry.set_text(self.dao.provenienza or '')
        self.materiale_disponibile_si_checkbutton.set_active(self.dao.disp_materiale or False)
        if self.dao.disp_materiale is not None:
            self.materiale_disponibile_no_checkbutton.set_active( not self.dao.disp_materiale)
        else:
            self.materiale_disponibile_no_checkbutton.set_active(False)
        self.data_presa_in_carico_entry.set_text(dateToString(self.dao.data_presa_in_carico or ''))
        self.nomi_sposi_entry.set_text(self.dao.nomi_sposi or '')
        self.lui_e_lei_entry.set_text(self.dao.lui_e_lei or '')
        self.numero_scheda_entry.set_text(str(self.dao.numero or 0))
        self.bomba_si_checkbutton.set_active(self.dao.bomba_in_cliche or False)
        if self.dao.bomba_in_cliche is not None:
            self.bomba_no_checkbutton.set_active(not self.dao.bomba_in_cliche)
        else:
            self.bomba_no_checkbutton.set_active(False)
        self.mezzo_ordinazione_entry.set_text(self.dao.mezzo_ordinazione or '')
        self.mezzo_spedizione_entry.set_text(self.dao.mezzo_spedizione or '')
        self.codice_spedizione_entry.set_text(self.dao.codice_spedizione or '')

        self.saldato_checkbutton.set_active(self.dao.documento_saldato or False)
        if self.dao.fattura is None:
            self.dao.fattura = False
        self.fattura_checkbutton.set_active(self.dao.fattura)
        self.ricevuta_checkbutton.set_active(not self.dao.fattura)

        self.n_documento_entry.set_text(self.dao.ricevuta_associata or '')
        _data_ricevuta = dateToString(self.dao.data_ricevuta)
        self.data_ricevuta_entry.set_text(_data_ricevuta)
        self.referente_entry.set_text(self.dao.referente or '')
        self.presso_entry.set_text(self.dao.presso or '')
        self.via_piazza_entry.set_text(self.dao.via_piazza or '')
        self.num_civ_entry.set_text(self.dao.num_civ or '')
        self.zip_entry.set_text(self.dao.zip or '')
        self.localita_entry.set_text(self.dao.localita or '')
        self.provincia_entry.set_text(self.dao.provincia or '')
        self.stato_entry.set_text(self.dao.stato or '')
        self.prima_email_entry.set_text(self.dao.prima_email or '')
        self.seconda_email_entry.set_text(self.dao.seconda_email or '')
        self.telefono_entry.set_text(self.dao.telefono or '')
        self.cellulare_entry.set_text(self.dao.cellulare or '')
        self.skype_entry.set_text(self.dao.skype or '')
        self.nome_contatto_entry.set_text(self.dao.operatore or '')
        buffer = self.note_text_textview.get_buffer()
        buffer.set_text(self.dao.note_text or '')
        self.note_final_entry.set_text(self.dao.note_final or '')
        self.note_fornitore_entry.set_text(self.dao.note_fornitore or '')
        self.note_spedizione_entry.set_text(self.dao.note_spedizione or '')
        self.userid_entry.set_text(self.dao.userid_cliente or '')
        self.passwd_entry.set_text(self.dao.passwd_cliente or '')
        if self.dao.id_colore_stampa is not None:
            findComboboxRowFromId(self.colore_stampa_combobox, self.dao.id_colore_stampa)
        if self.dao.id_carattere_stampa is not None:
            findComboboxRowFromId(self.carattere_stampa_combobox, self.dao.id_carattere_stampa)

        if self.dao.id_magazzino is not None:
            findComboboxRowFromId(self.magazzino_combobox, self.dao.id_magazzino)

        self._articoliTreeviewModel.clear()
        if len(self.dao.righe) > 0:
            for riga_ in self.dao.righe:
                riga=riga_
                articoloRiga = Articolo().getRecord(riga.id_articolo)
                unitaBaseRiga = UnitaBase().getRecord(id=articoloRiga.id_unita_base)
                self.setScontiRiga(riga)
                riga = getPrezzoNetto(riga)
                self._parzialeLordo += Decimal(str(riga.valore_unitario_lordo))*riga.quantita
                self._parzialeNetto += riga.valore_unitario_netto*riga.quantita
                findComboboxRowFromId(self.listino_combobox, riga.id_listino)
                ModelListContent = [riga,
                                    riga.id,
                                    articoloRiga.codice,
                                    riga.descrizione,
                                    unitaBaseRiga.denominazione_breve,
                                    riga.quantita,
                                    riga.valore_unitario_lordo,
                                    riga.valore_unitario_netto,riga.totaleRiga]
                self._articoliTreeviewModel.append(ModelListContent)
        self.associazione_articoli_comboboxentry.set_active(-1)
        self.sconti_scheda_widget.setValues(self.dao.sconti, self.dao.applicazione_sconti)
        self.id_cliente_customcombobox.setId(self.dao.id_cliente)
        self.calcolaTotaleScheda()
        findComboboxRowFromId(self.listino_combobox, self._id_listino)
        self._loading=False

        return True

    def setRigaTreeview(self, idListino, idArticolo):
        model = self._articoliTreeviewModel
        articolo = Articolo(Environment.connection, idArticolo)
        try:
            listino = ListinoArticolo().getRecord(id=[idListino,idArticolo])
        except:
            msg = 'Nessun listino associato all\'articolo %s' % articolo.denominazione[:10]
            obligatoryField(None, self.listino_combobox, msg)
        lettura_articolo = leggiArticolo(idArticolo)

        daoRiga = RigaSchedaOrdinazione()
        daoRiga.id_scheda = self.dao.id
        daoRiga.id_articolo = articolo.id
        daoRiga.id_magazzino = self.dao.id_magazzino
        daoRiga.descrizione = articolo.denominazione
        daoRiga.codiceArticoloFornitore = None
        daoRiga.id_listino = idListino
        daoRiga.percentuale_iva = lettura_articolo['percentualeAliquotaIva']
        self.setScontiRiga(daoRiga)
        daoRiga.quantita = 0
        daoRiga.id_multiplo = None
        daoRiga.moltiplicatore = None
        daoRiga.valore_unitario_lordo = listino.prezzo_dettaglio
        daoRiga = getPrezzoNetto(daoRiga)

        self.dao.righe.append(daoRiga)

    def setScontiRiga(self, daoRiga, tipo=None):
        daoRiga.sconti = []
        _descrizione = daoRiga.descrizione[0:6]
        _descrizione1 = daoRiga.descrizione[0:12]
        if (_descrizione.lower() == 'stampa') or\
            (_descrizione1.lower() == 'contrassegno'):
            daoRiga.applicazione_sconti = 'scalare'
            daoRiga.sconti = []
        else:
            daoRiga.applicazione_sconti = self.dao.applicazione_sconti
            for sconto in self.dao.sconti:
                if tipo == 'documento':
                    from promogest.dao.ScontoRigaDocumento import ScontoRigaDocumento
                    scontoRiga = ScontoRigaDocumento()
                else:
                    scontoRiga = ScontoRigaScheda(Environment.connection)
                    scontoRiga.valore = sconto.valore
                    scontoRiga.tipo_sconto = sconto.tipo_sconto
                    daoRiga.sconti.append(scontoRiga)

    def advertise(self, msg):
        dialog = gtk.MessageDialog(self.dialogTopLevel,
                                   gtk.DIALOG_MODAL
                                   | gtk.DIALOG_DESTROY_WITH_PARENT,
                                   gtk.MESSAGE_QUESTION,
                                   gtk.BUTTONS_YES_NO, msg)
        response = dialog.run()
        dialog.destroy()
        return response


    def  saveDao(self):
        """
        Recupera tutte le inforamzioni necessarie al salvataggio del Dao
        """
        self._getStrings()
        if self.dao.id is not None:
            inizio,fine = getDateRange(self.data_presa_in_carico_entry.get_text())
            if self.numero_scheda_entry.get_text() != str(self._numeroScheda) or dateToString(self.dao.data_presa_in_carico) != self._dataScheda:
                result = SchedaOrdinazione().select(daNumero=int(self.numero_scheda_entry.get_text()),
                                                    aNumero=str(self.numero_scheda_entry.get_text()),
                                                    daDataScheda=inizio,
                                                    aDataScheda=fine,
                                                    offset=None,
                                                    batchSize=None)
                if len(result) != 0:
                    if len(result) == 1 and result[0].id != self.dao.id:
                        response = self.advertise("E' gia' presente una scheda con questo numero. Continuare comunque?")
                    elif len(result) > 1:
                        response = self.advertise("Attenzione! sono state individuate piu' schede lavorazione con questo numero.\nSi consiglia una verifica della situazione. Continuare comunque?")
                    else:
                        response = gtk.RESPONSE_YES
                    if response != gtk.RESPONSE_YES:
                        return
                    else:
                        self.dao.numero = int(self.numero_scheda_entry.get_text())
        if self.dao.referente == '':
            obligatoryField(None, self.referente_entry,
                                    msg='Indicare un referente per la lavorazione')
        if (self.dao.data_matrimonio is None):
            obligatoryField(None, self.data_matrimonio_entry,
                                    msg='Inserire la data del matrimonio.')
        if (self.dao.data_presa_in_carico is None):
            obligatoryField(None, self.data_presa_in_carico_entry,
                                    msg='Inserire la data dell\'ordine.')
        if (self.dao.data_consegna_bozza is None):
            obligatoryField(None, self.data_consegna_bozza_entry,
                                    msg='Inserire la data prevista di consegna bozza.')
        if self.dao.nomi_sposi == '':
            obligatoryField(None, self.nomi_sposi_entry,
                                    msg='Inserire i nomi degli sposi.')
        if self.dao.prima_email == '':
            obligatoryField(None, self.prima_email_entry,
                                    msg="Inserire almeno un'indirizzo email di riferimento.")
        if self.dao.id_colore_stampa is None:
            obligatoryField(None, self.colore_stampa_combobox,\
                                    msg='Scegliere un colore per la stampa.')
        if self.dao.id_carattere_stampa is None:
            obligatoryField(None, self.carattere_stampa_combobox, \
                                    msg='Scegliere un carattere per la stampa.')
        if not self.dao.disp_materiale:
            if not self.materiale_disponibile_no_checkbutton.get_active():
                obligatoryField(None, msg='Disponibiltà materiale? ')
        if not self.dao.bomba_in_cliche :
            if not self.bomba_no_checkbutton.get_active():
                obligatoryField(None, msg='Bomboniera nel cliché?')
        if len(self.dao.righe) == 0:
            obligatoryField(None, msg='Si sta cercando di creare un documento vuoto.\nInserire le righe della scheda.')


        allarmi = []
        if self.dao.numero is None:
            queryString = ("select numero from partecipazioni_nozze.schede_ordinazioni where numero < 1000000 order by  numero desc limit 1")
            argList = []
            Environment.connection._cursor.execute(queryString, argList)
            rif_num_scheda = Environment.connection._cursor.fetchone()[0]+1
        else:
            rif_num_scheda = self.dao.numero

        if hasattr(Environment.conf.Stampalux,''):
            def setPromemoriaSchedaData():
                allarme.data_inserimento = datetime.datetime.today()
                allarme.incaricato = self.dao.operatore
                allarme.autore = 'Partecipazioni Nozze'
                allarme.in_scadenza = False
                allarme.scaduto=False
                allarme.completato=False
            target1 = getattr(Environment.conf.Stampalux,'target1')
            target2 = getattr(Environment.conf.Stampalux,'target2')
            target3 = getattr(Environment.conf.Stampalux,'target3')
            soglia1 = getattr(Environment.conf.Stampalux,'soglia1')
            soglia2 = getattr(Environment.conf.Stampalux,'soglia2')
            soglia3 = getattr(Environment.conf.Stampalux,'soglia3')
            targets = [(target1,soglia1), (target2,soglia2), (target3,soglia3)]
            if self.dao.data_spedizione is None:
                for target in targets:
                    if target[0] == 'data_spedizione' and  self.dao.data_spedizione is not None:
                        allarme = PromemoriaSchedaOrdinazione()
                        allarme.data_scadenza = self.dao.data_spedizione
                        allarme.descrizione = u'Scheda Lavorazione numero '+str(rif_num_scheda)+u' per promemoria impostato sulla data spedizione'
                        allarme.oggetto = 'Spedizione'
                        allarme.giorni_preavviso = int(target[1])
                        setPromemoriaSchedaData()
                        allarmi.append(allarme)
                    elif target == 'data_ordine_al_fornitore'and self.dao.data_ordine_al_fornitore is not None :
                        allarme = PromemoriaSchedaOrdinazione()
                        allarme.data_scadenza = self.dao.data_ordine_al_fornitore
                        allarme.descrizione = 'Scheda Lavorazione numero '+str(rif_num_scheda)+' per promemoria impostato sulla data ordine al fornitore'
                        allarme.oggetto = 'Ordine al Fornitore'
                        allarme.giorni_preavviso = int(target[1])
                        setPromemoriaSchedaData()
                        allarmi.append(allarme)
            else:
                if self.dao.data_consegna is not None:
                    delta = datetime.timedelta(int(Environment.conf.Stampalux.intervallo_spedizione))
                    allarme = PromemoriaSchedaOrdinazione()
                    allarme.data_scadenza = self.dao.data_spedizione + delta
                    allarme.descrizione = "Spedizione: codice "+self.dao.codice_spedizione+" Del "+dateToString(self.dao.data_spedizione)+" numero scheda: "+str(rif_num_scheda)+". Attenzione: la consegna non e' ancora avvenuta o non e' stata aggiornata la scheda"
                    allarme.oggetto  = 'Consegna Partecipazione in sospeso'
                    allarme.giorni_preavviso = int(getattr(Environment.conf.Stampalux, 'soglia4'))
                    setPromemoriaSchedaData()
                    allarmi.append(allarme)
        self.dao.promemoria = allarmi


        self.dao.persist()
        self.dao.numero = rif_num_scheda
        self._numeroScheda = rif_num_scheda
        self._dataScheda = dateToString(self.dao.data_presa_in_carico)

        self._refresh()

    def on_listino_combobox_changed(self, combobox):
        if self._loading:
            return

        self._id_listino = findIdFromCombobox(combobox)
        self.daoListino = Listino().getRecord(id=self._id_listino)
        for riga in self.dao.righe:
            riga.id_listino = self._id_listino
        self._refresh()

    def on_magazzino_combobox_changed(self, combobox):
        if self._loading:
            return

        self.dao.id_magazzino = findIdFromCombobox(combobox)

        self._refresh()

    def on_colore_stampa_combobox_changed(self, combobox):
        if self._loading:
            return
        self.dao.id_colore_stampa = findIdFromCombobox(self.colore_stampa_combobox)
        self.daoColoreStampa = ColoreStampa().getRecord(id=self.dao.id_colore_stampa)
        self._refresh()

    def on_carattere_stampa_combobox_changed(self, combobox):
        if self._loading:
            return
        self.dao.id_carattere_stampa = findIdFromCombobox(self.carattere_stampa_combobox)
        self.daoCarattereStampa = CarattereStampa().getRecord(id=self.dao.id_carattere_stampa)
        self._refresh()

    def on_ricevuta_checkbutton_toggled(self, checkbutton):
        if self._loading:
            return
        #se a true allora fattura_checkbutton a false e viceversa
        status = checkbutton.get_active()
        self.dao.fattura = not status
        self._refresh()


    def on_fattura_checkbutton_toggled(self, checkbutton):
        if self._loading:
            return
        status = checkbutton.get_active()
        self.dao.fattura = status
        self._refresh()

    def on_bomba_si_checkbutton_toggled(self, checkbutton):
        if self._loading:
            return
        status = checkbutton.get_active()
        self.dao.bomba_in_cliche = status
        self._refresh()

    def on_bomba_no_checkbutton_toggled(self, checkbutton):
        if self._loading:
            return
        status = checkbutton.get_active()
        self.dao.bomba_in_cliche = not status
        self._refresh()

    def on_saldato_checkbutton_toggled(self, checkbutton):
        if self._loading:
            return
        status = checkbutton.get_active()
        self.dao.documento_saldato = status

    def on_materiale_disponibile_si_checkbutton_toggled(self, checkbutton):
        if self._loading:
            return
        status = checkbutton.get_active()
        self.dao.disp_materiale = status
        self._refresh()

    def on_materiale_disponibile_no_checkbutton_toggled(self, checkbutton):
        if self._loading:
            return
        status = checkbutton.get_active()
        self.dao.disp_materiale = not status
        self._refresh()


    def on_associazione_articoli_comboboxentry_changed(self, combobox):
        if self._loading:
            return
        #this combobox has been filled with "articolo" data such as "denominazione", "id"
        if self._id_listino is None:
            obligatoryField(None, self.listino_combobox,\
                                            msg='Selezionare prima un listino.')

        search_string = combobox.child.get_text()
        model = combobox.get_model()
        selected = combobox.get_active()
        if selected < 0:
            fillComboboxAssociazioneArticoli(self.associazione_articoli_comboboxentry, search_string)
        else:
            row = model[selected]
            if row[0] is not None:
            #this call will return a list of "AssociazioneArticoli" (In the future: "Distinta Base") Dao objects
                articoli = AssociazioneArticoli().select(idPadre= row[1])
                for art in articoli:
                    if self._id_listino is not None:
                        self.setRigaTreeview(self._id_listino, art.id_articolo)
                self._refresh()
            else:
                msg="Nessuna Associazione di articoli e' stata ancora inserita"
                dialog = gtk.MessageDialog(None, gtk.DIALOG_MODAL | gtk.
                                                                DIALOG_DESTROY_WITH_PARENT,
                                                                gtk.MESSAGE_INFO, gtk.BUTTONS_OK, msg)
                dialog.run()
                dialog.destroy()
                if self.associazione_articoli_comboboxentry.get_property("can-focus"):
                    self.associazione_articoli_comboboxentry.grab_focus()
        return


    def on_aggiungi_articolo_button_clicked(self, button):
        self.ricercaArticolo()

    def on_rimuovi_articolo_button_clicked(self, button):
        selection = self.articoli_treeview.get_selection()
        model, iter = selection.get_selected()
        index = model.get_path(iter)[0]
        del self.dao.righe[index]
        button.set_sensitive(False)
        self._refresh()


    def on_articoli_treeview_cursor_changed(self, treeview):
        self.rimuovi_articolo_button.set_sensitive(True)

    def on_articoli_treeview_key_press_event(self, treeview, event):
        """ Gestisce la pressione del tab su una cella """
        if event.keyval == 65289:
            self._tabPressed = True

    def on_column_edited(self, cell, path, value, treeview, editNext=True):
        """ Gestisce l'immagazzinamento dei valori nelle celle """
        model = treeview.get_model()
        iterator = model.get_iter(path)
        column = cell.get_data('column')
        row = model[iterator]
        if cell.__class__ is gtk.CellRendererText:
            try:
                length = cell.get_data('max_length')
                model.set_value(iterator, column+2, value[:length])
            except:
                model.set_value(iterator, column+2, value)
        dao = row[0]
        dao.descrizione = model.get_value(iterator, 3)
        dao.quantita = Decimal(model.get_value(iterator, 5))
        valore_unitario_lordo = model.get_value(iterator, 6)
        dao.valore_unitario_lordo = Decimal(str(valore_unitario_lordo)).quantize(Decimal('.0001'), rounding=ROUND_HALF_UP)
        dao = getPrezzoNetto(dao)
        columns = treeview.get_columns()
        newColumn = column+1
        if newColumn <= columns:
            if self._tabPressed:
                self._tabPressed = False
            treeColumn = treeview.get_column(column+1)
            gobject.timeout_add(1, treeview.set_cursor, path, treeColumn, editNext)
        self._refresh()

    def on_sconti_scheda_widget_button_toggled(self, button):

        if button.get_property('active') is True:
            return

        self.dao.applicazione_sconti = self.sconti_scheda_widget.getApplicazione()
        scontiSuTotale = []
        res = self.sconti_scheda_widget.getSconti()
        if res is not None:
            for k in range(0, len(res)):
                daoSconto = ScontoSchedaOrdinazione()
                daoSconto.valore = float(res[k]["valore"])
                daoSconto.tipo_sconto = res[k]["tipo"]
                scontiSuTotale.append(daoSconto)

        self.dao.sconti = scontiSuTotale

        self._refresh()

    def calcolaTotaleScheda(self):
        """
        Calcola il totale della scheda
        """
        totaleImponibile = calcolaPrezzoIva(self._parzialeNetto, (-1*20))
        totaleImposta = self._parzialeNetto* Decimal( str(0.20))
        totaleNonScontato = self._parzialeLordo.quantize(Decimal('.01'), rounding=ROUND_HALF_UP)

        totaleScontato = self._parzialeNetto.quantize(Decimal('.01'), rounding=ROUND_HALF_UP)

        self.tot_lordo_entry.set_text(str(totaleNonScontato or 0))
        self.tot_scontato_entry.set_text(str(totaleScontato or 0))
        self.dao.totale_lordo = totaleScontato or 0

    def ricercaArticolo(self):
        """
        apre una finestra di ricerca avanzata degli articoli
        """
        def on_ricerca_articolo_hide(anagWindow, anag):
            if anag.dao is None:
                anagWindow.destroy()
                return

            anagWindow.destroy()
            self.mostraArticolo(anag.dao.id)

        codice = None
        codiceABarre = None
        denominazione = None
        codiceArticoloFornitore = None

        orderBy = "denominazione"

        from promogest.ui.RicercaComplessaArticoli import RicercaComplessaArticoli
        anag = RicercaComplessaArticoli(denominazione=denominazione,
                                        codice=codice,
                                        codiceABarre=codiceABarre,
                                        codiceArticoloFornitore=codiceArticoloFornitore)
        anag.setTreeViewSelectionType(gtk.SELECTION_SINGLE)

        anagWindow = anag.getTopLevel()
        anagWindow.connect("hide",
                           on_ricerca_articolo_hide,
                           anag)
        anagWindow.set_transient_for(self.dialogTopLevel)
        anag.show_all()


    def mostraArticolo(self, id):
        if self.daoListino is not None:
            self.setRigaTreeview(self.daoListino.id, id)
        self._refresh()

    def on_generazione_fattura_button_clicked(self, button):

        if self.dao.id_cliente == None:
                obligatoryField(None, msg='scegliere prima un cliente da associare al documento')
                return
        if self.dao.id is None:
            msg = "Prima di poter generare la fattura di questa scheda e' necessario salvarla .\n Salvare ?"
            response = self.advertise(msg)
            if response == gtk.RESPONSE_YES:
                if not self.dao.fattura:
                    self.on_anagrafica_complessa_detail_dialog_response(self.dialogTopLevel, gtk.RESPONSE_APPLY)
                    idFattura = self.creaFatturaDaScheda()
                    self.dao.ricevuta_associata = TestataDocumento().getRecord(id=idFattura).numero
                    self.n_documento_entry.set_text(str(self.dao.ricevuta_associata))
                    self.dao.fattura = True
                    self.on_anagrafica_complessa_detail_dialog_response(self.dialogTopLevel, gtk.RESPONSE_APPLY)
                    self._refresh()
                else:
                    if self.dao.ricevuta_associata is not None:
                        ricevuta_num = self.dao.ricevuta_associata
                        self.advertise("La presente scheda ha gia' generato una fattura (numero "+ricevuta_num+").")
                return
            else:
                return
        else:
            if not self.dao.fattura:
                self.on_anagrafica_complessa_detail_dialog_response(self.dialogTopLevel, gtk.RESPONSE_APPLY)
                idFattura = self.creaFatturaDaScheda()
                self.dao.ricevuta_associata = TestataDocumento().getRecord(id=idFattura).numero
                self.n_documento_entry.set_text(str(self.dao.ricevuta_associata))
                self.dao.fattura = True
                self.on_anagrafica_complessa_detail_dialog_response(self.dialogTopLevel, gtk.RESPONSE_APPLY)
                self._refresh()
                return
            else:
                if self.dao.ricevuta_associata is not None:
                    ricevuta_num = self.dao.ricevuta_associata
                    msg = "La presente scheda ha gia' generato una fattura (numero "+ricevuta_num+")."
                else:
                    msg = "La presente scheda ha gia' generato una fattura,\nma non è possibile stabilire il numero del documento."
                self.advertise(msg)
                return


    def on_anagrafica_clienti_button_clicked(self, button):
        anag = AnagraficaClienti()
        anag.getTopLevel()
        showAnagraficaRichiamata(None, anag, self._refresh)

    def on_cliente_changed(self):
        if self._loading:
            return
        from promogest.dao.Cliente import Cliente
        self.dao.id_cliente = self.id_cliente_customcombobox.getId()
        self.daoCliente = Cliente().getRecord(id=self.dao.id_cliente)

    def creaFatturaDaScheda(self):
        """
        Genera una testata documento come Fattura di vendita per la fatturazione
        degli articoli nella scheda ordinazione.
        """

        from promogest.dao.RigaDocumento import RigaDocumento
        from promogest.dao.ScontoTestataDocumento import ScontoTestataDocumento
        from promogest.dao.DestinazioneMerce import DestinazioneMerce
        daoTestataFattura = TestataDocumento()
        daoTestataFattura.data_documento = datetime.datetime.today()
        daoTestataFattura.id_cliente = self.dao.id_cliente
        #controlla la creazione della destinazione merce secondo la scheda
        if self.dao.presso or self.dao.via_piazza or self.dao.num_civ or\
            self.dao.localita or self.dao.provincia:
            dmt = DestinazioneMerce().select(idCliente=self.dao.id_cliente)
            if len(dmt) == 1 or len(dmt) > 1:
                daoTestataFattura.id_destinazione_merce = dmt[0].id
            elif len(dmt) == 0:
                destinazione_merce_testata = DestinazioneMerce()
                destinazione_merce_testata.denominazione = self.dao.presso or self.dao.referente
                destinazione_merce_testata.indirizzo = 'Via '+self.dao.via_piazza+' '+self.dao.num_civ
                destinazione_merce_testata.localita = self.dao.localita
                destinazione_merce_testata.cap = self.dao.zip
                destinazione_merce_testata.provincia = self.dao.provincia
                destinazione_merce_testata.id_cliente = self.dao.id_cliente
                destinazione_merce_testata.persist()
                daoTestataFattura.id_destinazione_merce = destinazione_merce_testata.id
        if self.dao.id_magazzino is None:
            obligatoryField(None, msg='Selezionare un magazzino per la generazione della fattura.')
        daoTestataFattura.id_aliquota_iva_esenzione = None
        daoTestataFattura.causale_trasporto = None
        daoTestataFattura.aspetto_esteriore_beni = None
        daoTestataFattura.totale_colli = None
        daoTestataFattura.note_interne = 'Fattura associata a scheda lavorazione numero '+str(self.dao.numero)
        daoTestataFattura.note_pie_pagina = None
        daoTestataFattura.documento_saldato = self.dao.documento_saldato or False
##        daoTestataFattura.sconti = self.dao.sconti
        daoTestataFattura.registro_numerazione = 'registro_fattura_vendita'
        daoTestataFattura.operazione = 'Fattura vendita'
        daoTestataFattura.protocollo = ''
        daoTestataFattura.inizio_trasporto =None
        daoTestataFattura.fine_trasporto = None
        daoTestataFattura.incaricato_trasporto = 'mittente'
        daoTestataFattura.totale_peso = None
        daoTestataFattura.applicazione_sconti = self.dao.applicazione_sconti
        daoTestataFattura.porto = 'franco'
        daoTestataFattura.ripartire_importo = False
        if daoTestataFattura.documento_saldato:
            daoTestataFattura.totale_pagato = float(self.totale_scontato_entry.get_text())
        else:
            daoTestataFattura.totale_pagato = 0
            daoTestataFattura.totale_sospeso =  float(self.tot_scontato_entry.get_text())
        daoTestataFattura.id_banca = None
        righe_testata = []

        for riga in self.dao.righe:
            riga_testata = RigaDocumento()
            riga_testata.id_articolo = riga.id_articolo
            riga_testata.id_magazzino = riga.id_magazzino
            riga_testata.descrizione = riga.descrizione
            riga_testata.id_listino = riga.id_listino
            riga_testata.percentuale_iva = riga.percentuale_iva
            riga_testata.applicazione_sconti = riga.applicazione_sconti
            riga_testata.quantita = riga.quantita
            riga_testata.id_multiplo = riga.id_multiplo
            riga_testata.moltiplicatore = riga.moltiplicatore
            riga_testata.sconti = []
            if len(riga.sconti) > 0:
                for sconto in riga.sconti:
                    self.setScontiRiga(riga_testata, 'documento')
            riga_testata.valore_unitario_lordo = calcolaPrezzoIva(riga.valore_unitario_lordo, (-1*riga.percentuale_iva))
            riga_testata.valore_unitario_netto =calcolaPrezzoIva(riga.valore_unitario_netto, (-1*riga.percentuale_iva))
            righe_testata.append(riga_testata)
        daoTestataFattura.righe = righe_testata

##        scontiTestata = []
##        scontoTestata = None
##        for sconto in self.dao.sconti:
##            scontoTestata = ScontoTestataDocumento(Environment.connection)
##            scontoTestata.tipo_sconto =sconto.tipo_sconto
##            scontoTestata.valore = sconto.valore
##            scontiTestata.append(scontoTestata)
        daoTestataFattura.persist()
        return daoTestataFattura.id

    def _getStrings(self):
        """
        recupera i dati inseriti nelle entry dell'interfaccia e setta gli attributi del dao di conseguenza.
        Questo metodo viene chiamato per primo in refresh() per evitare di resettare tutte le modifiche
        apportate alla scheda quando viene generato un qualunque altro segnale da un widget che modifica il dao.
        """
        buffer = self.note_text_textview.get_buffer()
        start, end = buffer.get_bounds()
        self.dao.note_text = buffer.get_text(start,end)
        self.dao.note_final = self.note_final_entry.get_text()
        self.dao.note_fornitore = self.note_fornitore_entry.get_text()
        self.dao.note_spedizione = self.note_spedizione_entry.get_text()
        self.dao.referente = self.referente_entry.get_text()
        self.dao.userid_cliente = self.userid_entry.get_text()
        self.dao.passwd_cliente = self.passwd_entry.get_text()
        self.dao.lui_e_lei = self.lui_e_lei_entry.get_text()
        self.dao.via_piazza = self.via_piazza_entry.get_text()
        self.dao.presso = self.presso_entry.get_text()
        self.dao.zip = self.zip_entry.get_text()
        self.dao.stato = self.stato_entry.get_text()
        self.dao.localita = self.localita_entry.get_text()
        self.dao.num_civ = self.num_civ_entry.get_text()
        self.dao.provincia = self.provincia_entry.get_text()
        self.dao.prima_email = self.prima_email_entry.get_text()
        self.dao.seconda_email = self.seconda_email_entry.get_text()
        self.dao.telefono = self.telefono_entry.get_text()
        self.dao.cellulare = self.cellulare_entry.get_text()
        self.dao.skype = self.skype_entry.get_text()
        self.dao.operatore = self.nome_contatto_entry.get_text()
        self.dao.data_matrimonio = stringToDate(self.data_matrimonio_entry.get_text())
        self.dao.data_consegna_bozza = stringToDate(self.data_consegna_bozza_entry.get_text())
        self.dao.data_consegna = stringToDate(self.data_consegna_entry.get_text())
        self.dao.data_ordine_al_fornitore = stringToDate(self.data_ordine_al_fornitore_entry.get_text())
        self.dao.data_presa_in_carico = stringToDate(self.data_presa_in_carico_entry.get_text())
        self.dao.data_spedizione = stringToDate(self.data_spedizione_entry.get_text())
        self.dao.data_ricevuta = stringToDate(self.data_ricevuta_entry.get_text())
        self.dao.nomi_sposi = self.nomi_sposi_entry.get_text()
        self.dao.provenienza = self.provenienza_entry.get_text()
        self.dao.ricevuta_associata = self.n_documento_entry.get_text()
        self.dao.mezzo_ordinazione = self.mezzo_ordinazione_entry.get_text()
        self.dao.mezzo_spedizione = self.mezzo_spedizione_entry.get_text()
        self.dao.codice_spedizione = self.codice_spedizione_entry.get_text()

    def _clear(self):
        buffer = self.note_text_textview.get_buffer()
        start,end = buffer.get_bounds()
        buffer.delete(start,end)
        if self._loading:
            self.associazione_articoli_comboboxentry.set_active(-1)
        self.listino_combobox.set_active(-1)
        self.magazzino_combobox.set_active(-1)
        self.numero_scheda_entry.set_text(str(0))
        self.note_final_entry.set_text('')
        self.note_fornitore_entry.set_text('')
        self.note_spedizione_entry.set_text('')
        self.referente_entry.set_text('')
        self.userid_entry.set_text('')
        self.passwd_entry.set_text('')
        self.via_piazza_entry.set_text('')
        self.presso_entry.set_text('')
        self.zip_entry.set_text('')
        self.stato_entry.set_text('')
        self.localita_entry.set_text('')
        self.num_civ_entry.set_text('')
        self.provincia_entry.set_text('')
        self.prima_email_entry.set_text('')
        self.seconda_email_entry.set_text('')
        self.telefono_entry.set_text('')
        self.cellulare_entry.set_text('')
        self.skype_entry.set_text('')
        self.nome_contatto_entry.set_text('')
        self.data_matrimonio_entry.set_text('')
        self.data_consegna_bozza_entry.set_text('')
        self.data_consegna_entry.set_text('')
        self.data_ordine_al_fornitore_entry.set_text('')
        self.data_presa_in_carico_entry.set_text('')
        self.data_spedizione_entry.set_text('')
        self.data_ricevuta_entry.set_text('')
        self.nomi_sposi_entry.set_text('')
        self.provenienza_entry.set_text('')
        self.n_documento_entry.set_text('')
        self.mezzo_ordinazione_entry.set_text('')
        self.mezzo_spedizione_entry.set_text('')

    def on_anagrafica_colori_button_clicked(self, button):
        anag = AnagraficaColoriStampa()
        anagWindow = anag.getTopLevel()
        showAnagraficaRichiamata(None, anagWindow, button, self._refresh)

    def on_anagrafica_caratteri_button_clicked(self, button):
        anag = AnagraficaCaratteriStampa()
        anagWindow = anag.getTopLevel()
        showAnagraficaRichiamata(None, anagWindow, button, self._refresh)
