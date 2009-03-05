# -*- coding: utf-8 -*-

# Promogest
#
# Copyright (C) 2007 by Promotux Informatica - http://www.promotux.it/
# Author: Dr astico (Pinna Marco) <zoccolodignu@gmail.com>
# Author: M3nt0r3 <m3nt0r3@gmail.com>

import pygtk
import gobject, datetime
from decimal import *
import string
from random import Random
import threading
from promogest import Environment
from promogest.ui.AnagraficaComplessa import Anagrafica, AnagraficaFilter, AnagraficaHtml, AnagraficaReport, AnagraficaEdit
from promogest.modules.SchedaLavorazione.ui.AnagraficaCaratteriStampa import AnagraficaCaratteriStampa
from promogest.modules.SchedaLavorazione.ui.AnagraficaColoriStampa import AnagraficaColoriStampa
from promogest.modules.SchedaLavorazione.dao import SchedaOrdinazione
from promogest.modules.SchedaLavorazione.dao.SchedaOrdinazione import SchedaOrdinazione
from promogest.modules.SchedaLavorazione.dao.RigaSchedaOrdinazione import RigaSchedaOrdinazione
from promogest.modules.SchedaLavorazione.dao.ScontoSchedaOrdinazione import ScontoSchedaOrdinazione
from promogest.modules.SchedaLavorazione.dao.ColoreStampa import ColoreStampa
from promogest.modules.SchedaLavorazione.dao.CarattereStampa import CarattereStampa
from promogest.ui.AnagraficaClienti import AnagraficaClienti
from promogest.dao.Listino import Listino
from promogest.dao.ListinoArticolo import ListinoArticolo
from promogest.dao.Magazzino import Magazzino
#from promogest.dao.Pagamento import Pagamento
from promogest.modules.SchedaLavorazione.dao.ScontoRigaScheda import ScontoRigaScheda
from promogest.modules.DistintaBase.dao.AssociazioneArticolo import AssociazioneArticolo
from promogest.dao.Articolo import Articolo
from promogest.dao.UnitaBase import UnitaBase
from promogest.dao.Cliente import Cliente
from promogest.modules.SchedaLavorazione.dao.PromemoriaSchedaOrdinazione import PromemoriaSchedaOrdinazione
from promogest.dao.TestataDocumento import TestataDocumento
from promogest.ui.GladeWidget import GladeWidget
from promogest.ui.utils import *
from promogest.ui.utilsCombobox import *
from SchedaLavorazioneUtils import *
from widgets.SchedeOrdinazioniEditWidget import SchedeOrdinazioniEditWidget
from DuplicaInFattura import DuplicaInFattura

class AnagraficaSchedeOrdinazioniEdit(SchedeOrdinazioniEditWidget,AnagraficaEdit):
    """
    Modifica i dati relativi ad una scheda lavorazione
    """

    def __init__(self, anagrafica):
        #SchedeOrdinazioniEditWidget.__init__(self)
        AnagraficaEdit.__init__(self,
                                anagrafica,
                                'anagrafica_schede_ordinazioni_detail_vbox',
                                'Dettagli scheda lavorazione',
                                gladeFile='./promogest/modules/SchedaLavorazione/gui/SchedaLavorazione.glade',
                                module=True)
        #self.pack_widgets()
        #self.connect_callbacks()
        #self.main_widget = self.anagrafica_schede_ordinazioni_detail_vbox
        self._prepareWindowPlacement()
        #self.window =  self.anagrafica_schede_ordinazioni_detail_vbox
        #self._windowTitle ='Dettagli scheda lavorazione'
        self._anagrafica = anagrafica
        #import pdb
        #pdb.set_trace()
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
        self.righeTEMP = []
        self.scontiTEMP = []
        self.scontiSuTotale = []
        #self._clear()
        #self.draw()


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
        fillComboboxCarattereStampa(self.carattere_stampa_combobox)
        fillComboboxColoreStampa(self.colore_stampa_combobox)
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

        renderer = gtk.CellRendererSpin()
        renderer.set_property('editable', True)
        renderer.set_property('xalign', 0.5)
        adjustment = gtk.Adjustment(1, 1, 1000,1,2)
        renderer.set_property("adjustment", adjustment)
        renderer.set_property("digits",2)
        renderer.set_property("climb-rate",3)
        renderer.connect('edited', self.on_column_quantita_edited, treeview, False)
        #renderer.set_data('column', 3)
        #renderer.set_data('min_length', 100)
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
        self.righeTEMP = []

        if not dao:
            self.dao = SchedaOrdinazione()
            self.dao.data_presa_in_carico = datetime.datetime.today()
            self._dataScheda = dateToString(self.dao.data_presa_in_carico)
            self._numeroScheda = 0
            self._articoliTreeviewModel.clear()
            self._clear()
            self.scontiTEMP = []
            self._refresh()
        else:
            self._dataScheda = dateToString(dao.data_presa_in_carico)
            self._numeroScheda=dao.numero
            self.dao = dao
            self.dettagli_scheda_notebook.set_current_page(0)
            self._refresh(firstLoad=True)

    def _refresh(self, firstLoad=False):
        """
        Riempie  tutti i form della scheda con i relativi valori del dao (se impostati)
        """

        self._loading = True
        self._parzialeLordo = int(0)
        self._parzialeNetto = int(0)
        # controlliamo se è il dao è fresco o no

        if not firstLoad:
            self._getStrings()
        else:
            if self.dao.colore_stampa:
                self.daoColoreStampa = self.dao.colore_stampa
            if self.dao.carattere_stampa:
                self.daoCarattereStampa = self.dao.carattere_stampa
            if self.dao.id_cliente:
                self.daoCliente = Cliente().getRecord(id=self.dao.id_cliente)
            if self.dao.righe:
                self._id_listino = self.dao.righe[0].id_listino
                self.daoListino = Listino().select(id=self._id_listino)[0]
                #asswgno alla variabile temporanea il valore di righe
                self.righeTEMP = self.dao.righe
                self.scontiTEMP = self.dao.sconti
            # il dao è fresco per cui mi prendo le righe e le metto
            self._articoliTreeviewModel.clear()
            model = self.articoli_treeview.get_model()
            for m in model:
                self.setRigaTreeview(m)
        #pulisco tutto
        self._clear()

        if  self._id_listino is None and self.righeTEMP:
            self._id_listino = self.righeTEMP[0].id_listino
            self.daoListino = Listino().select(id=self._id_listino)

        #mi occupo delle righe articolo nella treeview pulendo
        self._articoliTreeviewModel.clear()
        #ciclo per riempire la treeview
        for row in self.righeTEMP:
            articoloRiga = Articolo().getRecord(id=row.id_articolo)
            if not articoloRiga:
                unitaBaseRiga = "pz"
                codice = ""
                idArticolo = None
            else:
                unitaBaseRigaobgj = UnitaBase().getRecord(id=articoloRiga.id_unita_base)
                unitaBaseRiga = unitaBaseRigaobgj.denominazione_breve
                codice = articoloRiga.codice
                idArticolo = articoloRiga.id

            self.setScontiRiga(row)
            try:
                row.scontiRiga
            except:
                row.scontiRiga = []
            row = getPrezzoNetto(row)
            self._parzialeLordo = self._parzialeLordo + mN(float(row.valore_unitario_lordo)*float(row.quantita))
            self._parzialeNetto = self._parzialeNetto + row.valore_unitario_netto * row.quantita
            #findComboboxRowFromId(self.listino_combobox, row.id_listino)
            self._articoliTreeviewModel.append([row,
                                                idArticolo,
                                                codice,
                                                row.descrizione,
                                                unitaBaseRiga,
                                                row.quantita,
                                                row.valore_unitario_lordo,
                                                row.valore_unitario_netto,
                                                row.totaleRiga])

        # questi dati sono a posto,
        self.data_matrimonio_entry.set_text(dateToString(self.dao.data_matrimonio))
        self.data_ordine_al_fornitore_entry.set_text(dateToString(self.dao.data_ordine_al_fornitore))
        self.data_consegna_entry.set_text(dateToString(self.dao.data_consegna))
        self.data_spedizione_entry.set_text(dateToString(self.dao.data_spedizione))
        self.data_consegna_bozza_entry.set_text(dateToString(self.dao.data_consegna_bozza))
        self.data_presa_in_carico_entry.set_text(dateToString(self.dao.data_presa_in_carico or ""))
        self.provenienza_entry.set_text(self.dao.provenienza or '')
        self.materiale_disponibile_si_checkbutton.set_active(self.dao.disp_materiale or False)
        if self.dao.disp_materiale is not None:
            self.materiale_disponibile_no_checkbutton.set_active( not self.dao.disp_materiale)
        else:
            self.materiale_disponibile_no_checkbutton.set_active(False)
        self.nomi_sposi_entry.set_text(self.dao.nomi_sposi or '')
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
        self.data_ricevuta_entry.set_text(dateToString(self.dao.data_ricevuta))
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

        self.user_id_entry.set_text(self.dao.userid_cliente or '')
        self.lui_e_lei_entry.set_text(self.dao.lui_e_lei or '')
        self.password_sito_entry.set_text(self.dao.password_sito or "")
        self.password_user_entry.set_text(self.dao.passwd_cliente or '')
        self.password_amici_entry.set_text(self.dao.password_amici or "")



        if self.dao.id_colore_stampa is not None:
            findComboboxRowFromId(self.colore_stampa_combobox, self.dao.id_colore_stampa)
        if self.dao.id_carattere_stampa is not None:
            findComboboxRowFromId(self.carattere_stampa_combobox, self.dao.id_carattere_stampa)
        if self.dao.id_magazzino is not None:
            findComboboxRowFromId(self.magazzino_combobox, self.dao.id_magazzino)
        self.associazione_articoli_comboboxentry.set_active(-1)
        self.sconti_scheda_widget.setValues(self.scontiTEMP, self.dao.applicazione_sconti)
        self.id_cliente_customcombobox.setId(self.dao.id_cliente)
        self.calcolaTotaleScheda()
        findComboboxRowFromId(self.listino_combobox, self._id_listino)
        self._loading=False
        #return True

    def setRigaTreeview(self,modelRow=None,rowArticolo=None ):

        if rowArticolo:
            idArticolo = rowArticolo[0].id
            denArticolo = rowArticolo[0].denominazione
            quantita = 0
        elif modelRow:
            idArticolo = modelRow[1]
            denArticolo = modelRow[3]
            quantita = modelRow[5]
        listinoSel = ListinoArticolo().select(idListino=self._id_listino,
                                            idArticolo=idArticolo,
                                            listinoAttuale=True,
                                            batchSize=None)
        if listinoSel:
            listino = listinoSel[0]
        else:
            msg = 'Nessun listino associato all\'articolo %s' % denArticolo
            obligatoryField(None, self.listino_combobox, msg)
        lettura_articolo = leggiArticolo(idArticolo)

        daoRiga = RigaSchedaOrdinazione()
        #daoRiga.id_scheda = self.dao.id
        daoRiga.id_articolo = idArticolo
        daoRiga.id_magazzino = self.dao.id_magazzino
        daoRiga.descrizione = denArticolo
        daoRiga.codiceArticoloFornitore = None
        daoRiga.id_listino = self._id_listino
        daoRiga.percentuale_iva = lettura_articolo['percentualeAliquotaIva']
        self.setScontiRiga(daoRiga)
        try:
            daoRiga.scontiRiga
        except:
            daoRiga.scontiRiga = []

        daoRiga.quantita = quantita
        daoRiga.id_multiplo = None
        daoRiga.moltiplicatore = 1
        daoRiga.valore_unitario_lordo = listino.prezzo_dettaglio
        daoRiga = getPrezzoNetto(daoRiga)
        self.righeTEMP.append(daoRiga)
        #self.dao.righe.append(daoRiga)


    def setScontiRiga(self, daoRiga, tipo=None):
        scontiRiga = []
        _descrizione = daoRiga.descrizione[0:6]
        _descrizione1 = daoRiga.descrizione[0:12]
        if (_descrizione.lower() == 'stampa') or (_descrizione1.lower() == 'contrassegno'):
            daoRiga.applicazione_sconti = 'scalare'
            daoRiga.scontiRiga = []
        else:
            daoRiga.applicazione_sconti = self.dao.applicazione_sconti
            #for sconto in self.dao.sconti:
            for sconto in self.scontiTEMP:
                if tipo == 'documento':
                    from promogest.dao.ScontoRigaDocumento import ScontoRigaDocumento
                    scontoRiga = ScontoRigaDocumento()
                else:
                    scontoRiga = ScontoRigaScheda()
                scontoRiga.valore = sconto.valore
                scontoRiga.tipo_sconto = sconto.tipo_sconto
                scontiRiga.append(scontoRiga)
                daoRiga.scontiRiga = scontiRiga
        return daoRiga

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
        if not self.dao.righe and not self.righeTEMP:
            obligatoryField(None, msg='Si sta cercando di creare un documento vuoto.\nInserire le righe della scheda.')


        allarmi = []
        if self.dao.numero is None:
            queryString = Environment.params['session'].query(SchedaOrdinazione.numero).order_by(desc("numero")).all()
            if queryString:
                rif_num_scheda = queryString[0][0]+1
            else:
                rif_num_scheda = 1
        else:
            rif_num_scheda = self.dao.numero

        if hasattr(Environment.conf.SchedaLavorazione,''):
            def setPromemoriaSchedaData():
                allarme.data_inserimento = datetime.datetime.today()
                allarme.incaricato = self.dao.operatore
                allarme.autore = 'Partecipazioni Nozze'
                allarme.in_scadenza = False
                allarme.scaduto=False
                allarme.completato=False
            target1 = getattr(Environment.conf.SchedaLavorazione,'target1')
            target2 = getattr(Environment.conf.SchedaLavorazione,'target2')
            target3 = getattr(Environment.conf.SchedaLavorazione,'target3')
            soglia1 = getattr(Environment.conf.SchedaLavorazione,'soglia1')
            soglia2 = getattr(Environment.conf.SchedaLavorazione,'soglia2')
            soglia3 = getattr(Environment.conf.SchedaLavorazione,'soglia3')
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
                    delta = datetime.timedelta(int(Environment.conf.SchedaLavorazione.intervallo_spedizione))
                    allarme = PromemoriaSchedaOrdinazione()
                    allarme.data_scadenza = self.dao.data_spedizione + delta
                    allarme.descrizione = "Spedizione: codice "+self.dao.codice_spedizione+" Del "+dateToString(self.dao.data_spedizione)+" numero scheda: "+str(rif_num_scheda)+". Attenzione: la consegna non e' ancora avvenuta o non e' stata aggiornata la scheda"
                    allarme.oggetto  = 'Consegna Partecipazione in sospeso'
                    allarme.giorni_preavviso = int(getattr(Environment.conf.SchedaLavorazione, 'soglia4'))
                    setPromemoriaSchedaData()
                    allarmi.append(allarme)
        self.dao.promemoria = allarmi

        self.righeTEMP = []
        scontiSuTotale = []#{}

        res = self.sconti_scheda_widget.getSconti()
        #res = []
        if res:
            for sc in res:
                daoSconto = ScontoSchedaOrdinazione()
                daoSconto.valore = mN(sc["valore"])
                daoSconto.tipo_sconto = sc["tipo"]
                #scontiSuTotale[self.dao]=daoSconto
                scontiSuTotale.append(daoSconto)

        self.dao.scontiSuTotale = scontiSuTotale
        self.scontiTEMP = scontiSuTotale

        model = self.articoli_treeview.get_model()
        for m in model:
            self.setRigaTreeview(modelRow = m)
        self.dao.numero = rif_num_scheda
        self._numeroScheda = rif_num_scheda
        self._dataScheda = dateToString(self.dao.data_presa_in_carico)
        self.dao.righe = self.righeTEMP
        self.dao.sconti = self.scontiSuTotale
        #self.dao.scontiSuTotale = self.scontiSuTotale
        self.dao.persist()

        #self._refresh()

    def on_associazione_articoli_comboboxentry_changed(self, combobox=None, codart=None):
        if self._loading:
            return
        #this combobox has been filled with "articolo" data such as "denominazione", "id"
        if self._id_listino is None:
            obligatoryField(None, self.listino_combobox,\
                                            msg='Selezionare prima un listino.')
        if codart:
            print "CODAAAAAAAAAAAAAAAART", codart
            search_string=codart
        else:
            search_string = combobox.child.get_text()
        model = combobox.get_model()
        selected = combobox.get_active()
        if selected < 0:
            fillComboboxAssociazioneArticoli(self.associazione_articoli_comboboxentry, search_string)
        else:
            row = model[selected]
            if row[0]:
            #this call will return a list of "AssociazioneArticoli" (In the future: "Distinta Base") Dao objects
                #self.setRigaTreeview(modelRow=[],rowArticolo=row)
                #articoli = AssociazioneArticolo().select(idPadre= row[0].id)
                articoli = row[0].articoliAss
                for art in articoli:
                    if self._id_listino is not None:
                        a = Articolo().getRecord(id=art.id_figlio)
                        row[0] = a
                        row[1] = a.codice
                        row[2] = a.denominazione
                        self.setRigaTreeview(modelRow=[],rowArticolo=row)
                self._refresh()
                return
                #print "MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM"
            else:
                msg="Nessuna Associazione di articoli e' stata ancora inserita"
                dialog = gtk.MessageDialog(None, gtk.DIALOG_MODAL | gtk.
                                                                DIALOG_DESTROY_WITH_PARENT,
                                                                gtk.MESSAGE_INFO, gtk.BUTTONS_OK, msg)
                dialog.run()
                dialog.destroy()
                if self.associazione_articoli_comboboxentry.get_property("can-focus"):
                    self.associazione_articoli_comboboxentry.grab_focus()
        #import pdb
        #pdb.set_trace()

    def on_rimuovi_articolo_button_clicked(self, button):
        selection = self.articoli_treeview.get_selection()
        model, iter = selection.get_selected()
        index = model.get_path(iter)[0]
        del self.righeTEMP[index]
        button.set_sensitive(False)
        self._refresh()

    def on_articoli_treeview_cursor_changed(self, treeview):
        self.rimuovi_articolo_button.set_sensitive(True)

    def on_articoli_treeview_key_press_event(self, treeview, event):
        """ Gestisce la pressione del tab su una cella """
        if event.keyval == 65289:
            self._tabPressed = True

    def on_column_quantita_edited(self, cell, path, value, treeview, editNext=True):
        """ Function ti set the value quantita edit in the cell """
        model = treeview.get_model()
        value=value.replace(",",".")
        value = mN(value)
        model[path][5] = value
        model[path][0].quantita = value
        self._refresh()

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
        dao.valore_unitario_lordo = mN(str(valore_unitario_lordo))
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
        if res:
            for sc in res:
                daoSconto = ScontoSchedaOrdinazione()
                daoSconto.valore = float(sc["valore"])
                daoSconto.tipo_sconto = sc["tipo"]
                scontiSuTotale.append(daoSconto)
        self.dao.sconti = scontiSuTotale
        self.scontiSuTotale = scontiSuTotale
        self.scontiTEMP=scontiSuTotale
        self._refresh()

    def on_aggiungi_articolo_button_clicked(self, button):
        self.ricercaArticolo()

    def ricercaArticolo(self):
        """
        apre una finestra di ricerca avanzata degli articoli
        """
        def on_ricerca_articolo_hide(anagWindow, anag):
            if anag.dao is None:
                anagWindow.destroy()
                return

            anagWindow.destroy()
            self.mostraArticolo(anag.dao)

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
        if self.daoListino:
            self.setRigaTreeview(rowArticolo=[id])
        self._refresh()

    def on_generazione_fattura_button_clicked(self, button):
        print "DUPLICHIAMO IN FATTURA"
        DuplicaInFattura(dao=self.dao, ui = self).checkField()

    def calcolaTotaleScheda(self):
        """
        Calcola il totale della scheda
        """
        totaleImponibile = calcolaPrezzoIva(self._parzialeNetto, (-1*20))
        totaleImposta = self._parzialeNetto* Decimal( str(0.20))
        totaleNonScontato = self._parzialeLordo

        totaleScontato = self._parzialeNetto

        self.tot_lordo_entry.set_text(str(mN(str(totaleNonScontato),2) or 0))
        self.tot_scontato_entry.set_text(str(mN(str(totaleScontato),2) or 0))
        self.dao.totale_lordo = mN(totaleScontato,2) or 0


    def on_listino_combobox_changed(self, combobox):
        if self._loading:
            return
        self._id_listino = findIdFromCombobox(combobox)
        self.daoListino = Listino().select(id=self._id_listino)[0]
        for riga in self.righeTEMP:
            riga.id_listino = self._id_listino
        self._refresh()

    def on_magazzino_combobox_changed(self, combobox):
        if self._loading:
            return

        self.dao.id_magazzino = findIdFromCombobox(combobox)

        #self._refresh()

    def on_colore_stampa_combobox_changed(self, combobox):
        if self._loading:
            return
        self.dao.id_colore_stampa = findIdFromCombobox(self.colore_stampa_combobox)
        self.daoColoreStampa = ColoreStampa().getRecord(id=self.dao.id_colore_stampa)
        #self._refresh()

    def on_carattere_stampa_combobox_changed(self, combobox):
        if self._loading:
            return
        self.dao.id_carattere_stampa = findIdFromCombobox(self.carattere_stampa_combobox)
        self.daoCarattereStampa = CarattereStampa().getRecord(id=self.dao.id_carattere_stampa)
        #self._refresh()

    def on_ricevuta_checkbutton_toggled(self, checkbutton):
        if self._loading:
            return
        #se a true allora fattura_checkbutton a false e viceversa
        status = checkbutton.get_active()
        self.dao.fattura = not status
        #self._refresh()

    def on_fattura_checkbutton_toggled(self, checkbutton):
        if self._loading:
            return
        status = checkbutton.get_active()
        self.dao.fattura = status
        #self._refresh()

    def on_bomba_si_checkbutton_toggled(self, checkbutton):
        if self._loading:
            return
        status = checkbutton.get_active()
        self.dao.bomba_in_cliche = status
        #self._refresh()

    def on_bomba_no_checkbutton_toggled(self, checkbutton):
        if self._loading:
            return
        status = checkbutton.get_active()
        self.dao.bomba_in_cliche = not status
        #self._refresh()

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
        #self._refresh()

    def on_materiale_disponibile_no_checkbutton_toggled(self, checkbutton):
        if self._loading:
            return
        status = checkbutton.get_active()
        self.dao.disp_materiale = not status
        #self._refresh()



    def _getStrings(self):
        """
        recupera i dati inseriti nelle entry dell'interfaccia e setta gli attributi del dao di conseguenza.
        Questo metodo viene chiamato per primo in refresh() per evitare di resettare tutte le modifiche
        apportate alla scheda quando viene generato un qualunque altro segnale da un widget che modifica il dao.
        """
        print "MAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
        buffer = self.note_text_textview.get_buffer()
        start, end = buffer.get_bounds()
        self.dao.note_text = buffer.get_text(start, end)
        self.dao.note_final = self.note_final_entry.get_text()
        self.dao.note_fornitore = self.note_fornitore_entry.get_text()
        self.dao.note_spedizione = self.note_spedizione_entry.get_text()
        self.dao.referente = self.referente_entry.get_text()
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
        self.dao.userid_cliente = self.user_id_entry.get_text()
        self.dao.passwd_cliente = self.password_user_entry.get_text()
        self.dao.lui_e_lei = self.lui_e_lei_entry.get_text()
        self.dao.password_sito = self.password_sito_entry.get_text()
        self.dao.password_amici = self.password_amici_entry.get_text()

    def _clear(self):
        print "OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO"
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
        self.user_id_entry.set_text('')
        self.lui_e_lei_entry.set_text('')
        self.password_user_entry.set_text('')
        self.password_sito_entry.set_text('')
        self.password_amici_entry.set_text('')
        self.colore_stampa_combobox.set_active(-1)
        self.carattere_stampa_combobox.set_active(-1)

    def on_anagrafica_colori_button_clicked(self, button):
        anag = AnagraficaColoriStampa()
        anagWindow = anag.getTopLevel()
        showAnagraficaRichiamata(None, anagWindow, button, self._refresh)

    def on_anagrafica_caratteri_button_clicked(self, button):
        anag = AnagraficaCaratteriStampa()
        anagWindow = anag.getTopLevel()
        showAnagraficaRichiamata(None, anagWindow, button, self._refresh)

    def advertise(self, msg):
        dialog = gtk.MessageDialog(self.dialogTopLevel,
                                   gtk.DIALOG_MODAL
                                   | gtk.DIALOG_DESTROY_WITH_PARENT,
                                   gtk.MESSAGE_QUESTION,
                                   gtk.BUTTONS_YES_NO, msg)
        response = dialog.run()
        dialog.destroy()
        return response

    def on_anag_clienti_button_clicked(self, button):
        anag = AnagraficaClienti()
        anagWindow = anag.getTopLevel()
        showAnagraficaRichiamata(None, anagWindow, self._refresh)

    def on_cliente_changed(self):
        if self._loading:
            return
        from promogest.dao.Cliente import Cliente
        self.dao.id_cliente = self.id_cliente_customcombobox.getId()
        self.daoCliente = Cliente().getRecord(id=self.dao.id_cliente)


    def on_email_import_button_clicked(self, button):
        print "FILL THE DATA FROM EMAIL"
        if self.dao:
            altriDati= fillSchedaLavorazioneFromEmail(self)
        else:
            print "mettici un dialogo che avvisa"
        self.nome_contatto_entry.set_text("ANTO")
        self.stato_entry.set_text("Italia")
        idColore = ColoreStampa().select(denominazione = altriDati["colore_stampa"])
        if idColore:
            findComboboxRowFromId(self.colore_stampa_combobox, idColore[0].id)
        idCarattere = CarattereStampa().select(denominazione = altriDati["carattere_stampa"])
        if idCarattere:
            findComboboxRowFromId(self.carattere_stampa_combobox, idCarattere[0].id)
        idMagazzino = Magazzino().select(denominazione = "PARTECIPAZIONI")
        if idMagazzino:
            findComboboxRowFromId(self.magazzino_combobox, idMagazzino[0].id)
        idListino = Listino().select(denominazione = "WEB")
        if idListino:
            findComboboxRowFromId(self.listino_combobox, idListino[0].id)
        codart = altriDati["codParte"]
        self.on_associazione_articoli_comboboxentry_changed(self.associazione_articoli_comboboxentry,codart=codart)
        self.materiale_disponibile_si_checkbutton.set_active(True)
        #self.on_materiale_disponibile_si_checkbutton_toggled(self.materiale_disponibile_si_checkbutton)
        #self.on_column_quantita_edited(cell, path, value, treeview, editNext=True):
        #self._refresh(firstLoad=False)

    def on_genera_button_clicked(self, button):
        username = self.nomi_sposi_entry.get_text().replace("-","").replace(" ","").strip()[0:8]+"Web"
        self.user_id_entry.set_text(username)
        self.lui_e_lei_entry.set_text(self.nome_sposo_entry.get_text().upper()+"&"+self.nome_sposa_entry.get_text().upper())
        self.password_user_entry.set_text(str(''.join( Random().sample(string.letters+string.digits, 6))))
        self.password_sito_entry.set_text(str(''.join( Random().sample(string.letters+string.digits, 6))))
        self.password_amici_entry.set_text(str(''.join( Random().sample(string.letters+string.digits, 6))))
        print "GENERA I DATI PER L'EMAIL"

    def on_email_send_button_clicked(self, button):

        if not Environment.conf.emailcompose:
            msg = '\nErrore nella apertura del client di posta Thunderbird\n controllare il file configure, GRAZIE'
            overDialog = gtk.MessageDialog(None, gtk.DIALOG_MODAL
                                                | gtk.DIALOG_DESTROY_WITH_PARENT,
                                                    gtk.MESSAGE_ERROR,
                                                    gtk.BUTTONS_CANCEL, msg)
            response = overDialog.run()
            overDialog.destroy()
            return
            #self.printDialog.riferimento2_combobox_entry.child.set_text("")
        else:
            email = self.prima_email_entry.get_text()
            userid_cliente = self.user_id_entry.get_text()
            passwd_cliente = self.password_user_entry.get_text()
            lui_e_lei = self.lui_e_lei_entry.get_text()
            password_sito = self.password_sito_entry.get_text()
            password_amici = self.password_amici_entry.get_text()

            emailAPP = Environment.conf.emailcompose
            soggetto = Environment.conf.SchedaLavorazione.soggetto
            bodypart = ",body="+ Environment.conf.SchedaLavorazione.body %(lui_e_lei,
                                                                userid_cliente,
                                                                passwd_cliente,
                                                                password_sito,
                                                                password_amici)
            bodypart2 = Environment.conf.SchedaLavorazione.signature
            body = bodypart+bodypart2


            def applicationThread():
                toemail = " -compose to=%s" %email
                #fileName = self._pdfName +'.pdf'
                subject= ",subject="+soggetto
                #attachemail = ",attachment=file://%s" %pdfFile
                os.system(emailAPP + toemail+subject+body)
                
            t = threading.Thread(group=None, target=applicationThread,\
                                    name='email composer',\
                                    args=(), kwargs={})
            t.setDaemon(True) # FIXME: are we sure?
            t.start()

        print "SPEDISCI I DATI PER L?EMAIL"