# -*- coding: iso-8859-15 -*-

# Promogest
#
# Copyright (C) 2007 by Promotux Informatica - http://www.promotux.it/
# Author: Andrea Argiolas <andrea@promotux.it>
# Author: JJDaNiMoTh <jjdanimoth@gmail.com>
# Author: Dr astico  (Marco Pinna)<marco@promotux.it>
# Author: Francesco Meloni  <francesco@promotux.it>

#!/usr/local/bin/python
# coding: UTF-8

from AnagraficaComplessa import AnagraficaEdit
import gtk
import promogest.dao.TestataDocumento
from promogest.dao.TestataDocumento import TestataDocumento
from promogest.dao.TestataMovimento import TestataMovimento
import promogest.dao.RigaDocumento
from promogest.dao.RigaDocumento import RigaDocumento
import promogest.dao.ScontoRigaDocumento
from promogest.dao.ScontoRigaDocumento import ScontoRigaDocumento
import promogest.dao.ScontoTestataDocumento
from promogest.dao.ScontoTestataDocumento import ScontoTestataDocumento
from promogest.dao.Articolo import Articolo
from utils import *
from utilsCombobox import *
#from promogest.lib.TreeViewTooltips import TreeViewTooltips
#from promogest.ui.widgets.MultiLineEditor import MultiLineEditor
from GladeWidget import GladeWidget

class AnagraficaDocumentiEdit(AnagraficaEdit):
    """ Modifica un record dei documenti """

    def __init__(self, anagrafica):
        AnagraficaEdit.__init__(self,
                                anagrafica,
                                'anagrafica_documenti_detail_vbox', 'Dati Documento', 'anagrafica_documenti.glade')

        if "SuMisura" not in Environment.modulesList:
            self.hideSuMisura()
        else:
            import promogest.modules.SuMisura.dao.MisuraPezzo
            from promogest.modules.SuMisura.dao.MisuraPezzo import MisuraPezzo

        #self.notebook.remove_page(3)
        #else:
        from promogest.modules.Pagamenti.Pagamenti import Pagamenti
        self.Pagamenti = Pagamenti(self)

        self._widgetFirstFocus = self.data_documento_entry
        # contenitore (dizionario) righe (riga 0 riservata per  variazioni in corso)
        self._righe = []
        self._righe.append({})
        # numero riga corrente
        self._numRiga = 0

        self.noClean=False
        """ modello righe: magazzino, codice articolo,
        descrizione, percentuale iva, unita base, multiplo, listino,
        quantita, prezzo lordo, sconti, prezzo netto, totale, altezza, larghezza,molt_pezzi
        """
        self.modelRiga = gtk.ListStore(str, str, str, str, str, str, str,
                                        str, str, str, str, str, str, str,str)
        # iteratore riga corrente
        self._iteratorRiga = None
        # cliente o fornitore ?
        self._tipoPersonaGiuridica = None
        self._operazione = None
        # prezzo vendita/acquisto, ivato/non ivato
        self._fonteValore = None
        # carico (+) o scarico (-)
        self._segno = None
        # pagamento preferenziale dell'intestatario
        self._id_pagamento = None
        # magazzino preferenziale dell'intestatario
        self._id_magazzino = None
        # listino preferenziale dell'intestatario
        self._id_listino = None
        # banca preferenziale dell'intestatario
        self._id_banca = None
        # caricamento documento (interrompe l'azione degli eventi on_changed nelle combobox)
        self._loading = False
        # risposta richiesta variazione listini per costo variato: 'yes', 'no', 'all', 'none'
        self._variazioneListiniResponse = ''
        # mostrare variazione listini ?
        self._variazioneListiniShow = True
        #campi controllo modifica
        self._controllo_data_documento = None
        self._controllo_numero_documento = None
        self.reuseDataRow = False
        if "PromoWear" in Environment.modulesList:
            self.promowear_manager_taglia_colore_togglebutton.set_property("visible", True)
            self.promowear_manager_taglia_colore_togglebutton.set_sensitive(False)
            self.promowear_data_label.set_text("Gruppo Taglia:")
        else:
            self.promowear_manager_taglia_colore_togglebutton.set_property("visible", False)
            self.promowear_manager_taglia_colore_togglebutton.set_sensitive(False)
            self.promowear_data_label.set_text('')

    def hideSuMisura(self):
        """
        funzione per SuMisura .....rimuove dalla vista quando modulo è disattivato
        """
        self.altezza_entry.destroy()
        self.larghezza_entry.destroy()
        self.moltiplicatore_entry.destroy()
        self.label_moltiplicatore.hide()
        self.altezza_label.hide()
        self.lunghezza_label.hide()
        self.cmLabel1_label.set_text('')
        self.cmLabel_label.set_text('')
        self.x_misure_label.hide()

    def azzeraRiga(self, numero = 0):
        """
        Azzera i campi del dizionario privato delle righe, alla riga
        indicata (o alla 0-esima)
        """

        self._righe[numero] = {"idRiga": None,
                                "idMagazzino": None,
                                "magazzino": '',
                                "idArticolo": None,
                                "codiceArticolo": '',
                                "descrizione": '',
                                "percentualeIva": 0,
                                "idUnitaBase": None,
                                "unitaBase": '',
                                "idMultiplo": None,
                                "multiplo": '',
                                "idListino": None,
                                "listino": '',
                                "quantita": 0,
                                "moltiplicatore": 0,
                                "prezzoLordo": 0,
                                "applicazioneSconti": 'scalare',
                                "sconti": [],
                                "prezzoNetto": 0,
                                "totale": 0,
                                "codiceArticoloFornitore": '',
                                "prezzoNettoUltimo": 0,
                                "altezza": '',
                                "larghezza": '',
                                "molt_pezzi": 0}


    def azzeraRigaPartial(self, numero = 0, rigatampone=None):
        """
        Azzera i campi del dizionario privato delle righe, alla riga
        indicata (o alla 0-esima)
        """

        self._righe[numero] = {"idRiga": None,
                                "idMagazzino": rigatampone['idMagazzino'],
                                "magazzino": rigatampone['magazzino'],
                                "idArticolo": rigatampone['idArticolo'],
                                "codiceArticolo": rigatampone['codiceArticolo'],
                                "descrizione": rigatampone['descrizione'],
                                "percentualeIva": rigatampone['percentualeIva'],
                                "idUnitaBase": rigatampone['idUnitaBase'],
                                "unitaBase": rigatampone['unitaBase'],
                                "idMultiplo": rigatampone['idMultiplo'],
                                "multiplo": rigatampone['multiplo'],
                                "idListino": rigatampone['idListino'],
                                "listino": rigatampone['idListino'],
                                "quantita": rigatampone['quantita'],
                                "moltiplicatore": rigatampone['moltiplicatore'],
                                "prezzoLordo": rigatampone['prezzoLordo'],
                                "applicazioneSconti": 'scalare',
                                "sconti": rigatampone['sconti'],
                                "prezzoNetto": rigatampone['prezzoNetto'],
                                "totale": rigatampone['totale'],
                                "codiceArticoloFornitore": rigatampone['codiceArticoloFornitore'],
                                "prezzoNettoUltimo": rigatampone['prezzoNettoUltimo'],
                                "altezza": rigatampone['altezza'],
                                "larghezza": rigatampone['larghezza'],
                                "molt_pezzi": rigatampone['molt_pezzi']}

    def nuovaRiga(self):
        """
        Prepara per l'inserimento di una nuova riga
        """
        self._numRiga = 0
        self.azzeraRiga(0)

        self.articolo_entry.set_text('')
        self.unitaBaseLabel.set_text('')
        self.descrizione_entry.set_text('')
        self.codice_articolo_fornitore_entry.set_text('')
        self.percentuale_iva_entry.set_text('0')
        self.id_multiplo_customcombobox.combobox.clear()
        self.id_listino_customcombobox.combobox.clear()
        self.prezzo_lordo_entry.set_text('0')
        self.quantita_entry.set_text('0')
        self.prezzo_netto_label.set_text('0')
        self.sconti_widget.clearValues()
        self.totale_riga_label.set_text('0')
        if "SuMisura" in Environment.modulesList:
            self.altezza_entry.set_text('')
            self.larghezza_entry.set_text('')
            self.moltiplicatore_entry.set_text('')

        if len(self._righe) > 1:
            self.data_documento_entry.set_sensitive(False)
            self.id_operazione_combobox.set_sensitive(False)
            self.id_persona_giuridica_customcombobox.set_sensitive(False)
            self.articolo_entry.grab_focus()
        else:
            self.data_documento_entry.set_sensitive(True)
            self.id_persona_giuridica_customcombobox.set_sensitive(self.id_operazione_combobox.get_active() != -1)
            self.id_operazione_combobox.set_sensitive(True)
            #if Environment.tipo_documento_predefinito != "":
                #findComboboxRowFromStr(self.id_operazione_combobox,Environment.tipo_documento_predefinito,1)
            if self._anagrafica._magazzinoFissato:
                findComboboxRowFromId(self.id_magazzino_combobox, self._anagrafica._idMagazzino)
            elif self._id_magazzino is not None:
                findComboboxRowFromId(self.id_magazzino_combobox, self._id_magazzino)
            self.id_magazzino_combobox.grab_focus()
        if Environment.conf.hasPagamenti == True:
            self.Pagamenti.attiva_prima_scadenza(False, True)
            self.Pagamenti.attiva_seconda_scadenza(False, True)
            self.Pagamenti.attiva_terza_scadenza(False, True)
            self.Pagamenti.attiva_quarta_scadenza(False, True)

    def nuovaRigaNoClean(self, rigatampone=None):
        """
        Prepara per l'inserimento di una nuova riga seza cancellare i campi
        """
        self._numRiga = 0
        self.azzeraRigaPartial(0, rigatampone=rigatampone)
        self.unitaBaseLabel.set_text(rigatampone['unitaBase'])
        self.codice_articolo_fornitore_entry.set_text(rigatampone['codiceArticoloFornitore'])

    def clearRows(self):
        """ pulisce i campi per il trattamento e la conservazione delle righe """

        self._righe = []
        self._righe.append({})
        self._numRiga = 0
        self.modelRiga.clear()
        self._iteratorRiga = None
        self.nuovaRiga()

    def draw(self):

        treeview = self.righe_treeview
        rendererSx = gtk.CellRendererText()
        rendererDx = gtk.CellRendererText()
        rendererDx.set_property('xalign', 1)

        column = gtk.TreeViewColumn('Magazzino', rendererSx, text=0)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(False)
        column.set_resizable(True)
        column.set_expand(False)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Codice articolo', rendererSx, text=1)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(False)
        column.set_resizable(True)
        column.set_expand(False)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Descrizione', rendererSx, text=2)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(False)
        column.set_resizable(True)
        column.set_expand(True)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('% IVA', rendererDx, text=3)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(False)
        column.set_resizable(True)
        column.set_expand(False)
        treeview.append_column(column)
        if "SuMisura" in Environment.modulesList:
            column = gtk.TreeViewColumn('H', rendererSx, text=4)
            column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
            column.set_clickable(False)
            column.set_resizable(True)
            column.set_expand(False)
            treeview.append_column(column)

            column = gtk.TreeViewColumn('L', rendererSx, text=5)
            column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
            column.set_clickable(False)
            column.set_resizable(True)
            column.set_expand(False)
            treeview.append_column(column)

            column = gtk.TreeViewColumn('Pezzi', rendererSx, text=6)
            column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
            column.set_clickable(False)
            column.set_resizable(True)
            column.set_expand(False)
            treeview.append_column(column)

        column = gtk.TreeViewColumn('Multiplo', rendererSx, text=7)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(False)
        column.set_resizable(True)
        column.set_expand(False)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Listino', rendererSx, text=8)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(False)
        column.set_resizable(True)
        column.set_expand(False)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('U.M.', rendererSx, text=9)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(False)
        column.set_resizable(True)
        column.set_expand(False)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Quantita''', rendererDx, text=10)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(False)
        column.set_resizable(True)
        column.set_expand(False)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Prezzo lordo', rendererDx, text=11)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(False)
        column.set_resizable(True)
        column.set_expand(False)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Sconti', rendererSx, text=12)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(False)
        column.set_resizable(True)
        column.set_expand(False)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Prezzo netto', rendererDx, text=13)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(False)
        column.set_resizable(True)
        column.set_expand(False)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Totale', rendererDx, text=14)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(False)
        column.set_resizable(True)
        column.set_expand(False)
        treeview.append_column(column)

        fillComboboxOperazioni(self.id_operazione_combobox, 'documento')
        fillComboboxMagazzini(self.id_magazzino_combobox)
        fillComboboxPagamenti(self.id_pagamento_customcombobox.combobox)
        fillComboboxBanche(self.id_banca_customcombobox.combobox)
        fillComboboxAliquoteIva(self.id_aliquota_iva_esenzione_customcombobox.combobox)
        fillComboboxCausaliTrasporto(self.causale_trasporto_comboboxentry)
        fillComboboxAspettoEsterioreBeni(self.aspetto_esteriore_beni_comboboxentry)

        self.porto_combobox.set_active(-1)
        self.porto_combobox.set_sensitive(False)

        self.nuovaRiga()

        # preferenza ricerca articolo ?
        if hasattr(Environment.conf,'Documenti'):
            if hasattr(Environment.conf.Documenti,'ricerca_per'):
                if Environment.conf.Documenti.ricerca_per == 'codice':
                    self.ricerca_codice_button.set_active(True)
                elif Environment.conf.Documenti.ricerca_per == 'codice_a_barre':
                    self.ricerca_codice_a_barre_button.set_active(True)
                elif Environment.conf.Documenti.ricerca_per == 'descrizione':
                    self.ricerca_descrizione_button.set_active(True)
                elif Environment.conf.Documenti.ricerca_per == 'codice_articolo_fornitore':
                    self.ricerca_codice_articolo_fornitore_button.set_active(True)

        self.id_operazione_combobox.connect('changed',
                self.on_id_operazione_combobox_changed)
        self.id_persona_giuridica_customcombobox.setSingleValue()
        self.id_persona_giuridica_customcombobox.setOnChangedCall(self.persona_giuridica_changed)
        self.id_magazzino_combobox.connect('changed',
                self.on_id_magazzino_combobox_changed)
        self.id_multiplo_customcombobox.connect('clicked',
                self.on_id_multiplo_customcombobox_button_clicked)
        self.id_multiplo_customcombobox.combobox.connect('changed',
                self.on_id_multiplo_customcombobox_changed)
        self.id_listino_customcombobox.connect('clicked',
                self.on_id_listino_customcombobox_button_clicked)
        self.id_listino_customcombobox.combobox.connect('changed',
                self.on_id_listino_customcombobox_changed)
        self.id_listino_customcombobox.button.connect('toggled',
                self.on_id_listino_customcombobox_button_toggled)
        self.sconti_widget.button.connect('toggled',
                self.on_sconti_widget_button_toggled)
        self.id_destinazione_merce_customcombobox.connect('clicked',
                self.on_id_destinazione_merce_customcombobox_button_clicked)
        idHandler = self.id_vettore_customcombobox.connect('changed',
                on_combobox_vettore_search_clicked)
        self.id_vettore_customcombobox.setChangedHandler(idHandler)
        idHandler = self.id_agente_customcombobox.connect('changed',
                on_combobox_agente_search_clicked)
        self.id_agente_customcombobox.setChangedHandler(idHandler)
        self.sconti_testata_widget.button.connect('toggled',
                self.on_sconti_testata_widget_button_toggled)
        self.id_pagamento_customcombobox.connect('clicked',
                on_id_pagamento_customcombobox_clicked)
        self.id_banca_customcombobox.connect('clicked',
                on_id_banca_customcombobox_clicked)
        self.id_aliquota_iva_esenzione_customcombobox.connect('clicked',
                on_id_aliquota_iva_customcombobox_clicked)
        self.ricerca_codice_button.connect('clicked',
                self.on_ricerca_codice_button_clicked)
        self.ricerca_codice_a_barre_button.connect('clicked',
                self.on_ricerca_codice_a_barre_button_clicked)
        self.ricerca_descrizione_button.connect('clicked',
                self.on_ricerca_descrizione_button_clicked)
        self.ricerca_codice_articolo_fornitore_button.connect('clicked',
                self.on_ricerca_codice_articolo_fornitore_button_clicked)
        if Environment.conf.hasPagamenti == True:
            self.Pagamenti.connectEntryPag()

        #Castelletto iva
        rendererText = gtk.CellRendererText()

        column = gtk.TreeViewColumn('Aliquota I.V.A.', rendererText, text=0)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(False)
        column.set_resizable(True)
        column.set_expand(True)
        self.riepiloghi_iva_treeview.append_column(column)

        rendererText = gtk.CellRendererText()
        rendererText.set_property('xalign', 1)

        column = gtk.TreeViewColumn('Imponibile', rendererText, text=1)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(False)
        column.set_resizable(True)
        column.set_expand(True)
        self.riepiloghi_iva_treeview.append_column(column)

        column = gtk.TreeViewColumn('Imposta', rendererText, text=2)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(False)
        column.set_resizable(True)
        column.set_expand(True)
        self.riepiloghi_iva_treeview.append_column(column)

        model = gtk.ListStore(str, str, str)
        self.riepiloghi_iva_treeview.set_model(model)

    def on_id_operazione_combobox_changed(self, combobox):

        self._operazione = findIdFromCombobox(self.id_operazione_combobox)
        operazione = leggiOperazione(self._operazione)
        if self._tipoPersonaGiuridica != operazione["tipoPersonaGiuridica"]:
            self.id_persona_giuridica_customcombobox.refresh(clear=True, filter=False)
        self._tipoPersonaGiuridica = operazione["tipoPersonaGiuridica"]
        self._fonteValore = operazione["fonteValore"]
        self._segno = operazione["segno"]

        if (self._tipoPersonaGiuridica == "fornitore"):
            self.persona_giuridica_label.set_text('Fornitore')
            self.id_persona_giuridica_customcombobox.setType(self._tipoPersonaGiuridica)
            self.id_persona_giuridica_customcombobox.set_sensitive(True)
            self.label_listino.set_property('visible', False)
            self.id_listino_customcombobox.set_property('visible', False)
            self.prz_lordo_label.set_text('Costo')
            self.prz_netto_label.set_text('Costo netto')
            self.codice_articolo_fornitore_label.set_property('visible', True)
            self.codice_articolo_fornitore_entry.set_property('visible', True)
            self.protocollo_label.set_property('visible', True)
            self.protocollo_entry1.set_property('visible', True)
            self.numero_documento_label.set_text('N. reg.')
        elif (self._tipoPersonaGiuridica == "cliente"):
            self.persona_giuridica_label.set_text('Cliente')
            self.id_persona_giuridica_customcombobox.setType(self._tipoPersonaGiuridica)
            self.id_persona_giuridica_customcombobox.set_sensitive(True)
            self.label_listino.set_property('visible', True)
            self.id_listino_customcombobox.set_property('visible', True)
            self.prz_lordo_label.set_text('Prezzo')
            self.prz_netto_label.set_text('Prezzo netto')
            self.codice_articolo_fornitore_label.set_property('visible', False)
            self.codice_articolo_fornitore_entry.set_property('visible', False)
            self.protocollo_label.set_property('visible', False)
            self.protocollo_entry1.set_property('visible', False)
            self.numero_documento_label.set_text('Numero')
        else:
            self.persona_giuridica_label.set_text('Cliente/Fornitore ?')
            self.id_persona_giuridica_customcombobox.set_sensitive(False)
            self.label_listino.set_property('visible', True)
            self.id_listino_customcombobox.set_property('visible', True)
            self.prz_lordo_label.set_text('Prezzo')
            self.prz_netto_label.set_text('Prezzo netto')
            self.codice_articolo_fornitore_label.set_property('visible', False)
            self.codice_articolo_fornitore_entry.set_property('visible', False)
            self.protocollo_label.set_property('visible', False)
            self.protocollo_entry1.set_property('visible', False)
            self.numero_documento_label.set_text('Numero')

        self.persona_giuridica_changed()
        self.data_documento_entry.grab_focus()

    def on_pulisci_scadenza_button_clicked(self, button):
        """
        Pulisce tutti i campi relativi alla tab pagamenti
        """

        self.Pagamenti.attiva_prima_scadenza(False,False)
        self.Pagamenti.attiva_seconda_scadenza(False,False)
        self.Pagamenti.attiva_terza_scadenza(False,False)
        self.Pagamenti.attiva_quarta_scadenza(False,False)
        self.numero_primo_documento_entry.set_text('')
        self.numero_secondo_documento_entry.set_text('')
        self.importo_primo_documento_entry.set_text('')
        self.importo_secondo_documento_entry.set_text('')

    def on_controlla_rate_scadenza_button_clicked(self, button):
        """
        bottone che controlla le rate scadenza"
        """
        self.Pagamenti.controlla_rate_scadenza(True)

    def on_calcola_importi_scadenza_button_clicked(self, button):
        """
        calcola importi scadenza pagamenti
        """
        self.Pagamenti.attiva_scadenze()
        self.Pagamenti.dividi_importo()
        self.Pagamenti.ricalcola_sospeso_e_pagato()

    def on_seleziona_prima_nota_button_clicked(self, button):
        """
        Seleziona la prima nota da utilizzare come riferimento
        """
        if self.numero_primo_documento_entry.get_text() != "":
            response = self.Pagamenti.impostaDocumentoCollegato(
                    int(self.numero_primo_documento_entry.get_text()))
            if __debug__:
                print "on_seleziona_prima_nota: response = ", response
        else:
            self.showMessage("Inserisci il numero del documento")
            response = False

        if response != False:
            self.Pagamenti.importo_primo_documento_entry.set_text(str(response))
            self.Pagamenti.dividi_importo()
            self.Pagamenti.ricalcola_sospeso_e_pagato()
            self.numero_secondo_documento_entry.set_sensitive(True)
            self.seleziona_seconda_nota_button.set_sensitive(True)
            self.importo_secondo_documento_entry.set_sensitive(True)

    def on_seleziona_seconda_nota_button_clicked(self, button):
        """
        Seleziona la seconda nota di credito da utilizzare come riferimento
        """
        if self.numero_secondo_documento_entry.get_text() != "":
            response = self.Pagamenti.impostaDocumentoCollegato(
                    int(self.numero_secondo_documento_entry.get_text()))
        else:
            self.showMessage("Inserisci il numero del documento")
            response = False
        if response != False:
            self.Pagamenti.importo_primo_documento_entry.set_text(str(response))
            self.Pagamenti.dividi_importo()
            self.Pagamenti.ricalcola_sospeso_e_pagato()

    def on_data_pagamento_prima_scadenza_entry_changed(self, entry):
        """
        Reimposta i totali saldato e da saldare alla modifica della data di pagamento
        della prima scadenza
        """
        self.Pagamenti.ricalcola_sospeso_e_pagato()

    def on_data_pagamento_seconda_scadenza_entry_changed(self, entry):
        """ Reimposta i totali saldato e da saldare alla modifica della data di pagamento
        della seconda scadenza
        """
        self.Pagamenti.ricalcola_sospeso_e_pagato()

    def on_data_pagamento_terza_scadenza_entry_changed(self, entry):
        """
        Reimposta i totali saldato e da saldare alla modifica della data di pagamento
        della terza scadenza
        """

        self.Pagamenti.ricalcola_sospeso_e_pagato()

    def on_data_pagamento_quarta_scadenza_entry_changed(self, entry):
        """
        Reimposta i totali saldato e da saldare alla modifica della data di pagamento
        della quarta scadenza
        """
        self.Pagamenti.ricalcola_sospeso_e_pagato()

    def persona_giuridica_changed(self):
        if self._loading:
            return

        inseritoIntestatario = (self.id_persona_giuridica_customcombobox.getId() is not None)
        if inseritoIntestatario:
            datiIntestatario = self.id_persona_giuridica_customcombobox.getData()
            self._id_pagamento = datiIntestatario["id_pagamento"]
            self._id_magazzino = datiIntestatario["id_magazzino"]
            if self._tipoPersonaGiuridica == "cliente":
                self._id_listino = datiIntestatario["id_listino"]
                self._id_banca = datiIntestatario["id_banca"]

            if self.id_pagamento_customcombobox.combobox.get_active() == -1:
                findComboboxRowFromId(self.id_pagamento_customcombobox.combobox, self._id_pagamento)
            if self.id_magazzino_combobox.get_active() == -1:
                findComboboxRowFromId(self.id_magazzino_combobox, self._id_magazzino)
            if self.id_banca_customcombobox.combobox.get_active() == -1:
                findComboboxRowFromId(self.id_banca_customcombobox.combobox, self._id_banca)

        if self._tipoPersonaGiuridica == "cliente":
            self.id_destinazione_merce_customcombobox.set_sensitive(True)
            if self.id_persona_giuridica_customcombobox.getId() is None:
                self.id_destinazione_merce_customcombobox.combobox.clear
                self.id_destinazione_merce_customcombobox.set_sensitive(False)
            else:
                fillComboboxDestinazioniMerce(self.id_destinazione_merce_customcombobox.combobox,
                        self.id_persona_giuridica_customcombobox.getId())
                self.id_destinazione_merce_customcombobox.set_sensitive(True)
            self.refresh_combobox_listini()
        else:
            self.id_destinazione_merce_customcombobox.set_sensitive(False)

    def on_id_destinazione_merce_customcombobox_button_clicked(self, widget, toggleButton):
        on_id_destinazione_merce_customcombobox_clicked(widget,
                                                toggleButton,
                                                self.id_persona_giuridica_customcombobox.getId())

    def on_incaricato_trasporto_radiobutton_toggled(self, radiobutton):

        self.id_vettore_customcombobox.set_sensitive(self.vettore_radiobutton.get_active())
        self.porto_combobox.set_sensitive(self.vettore_radiobutton.get_active())
        # Se e` selezionato mittente o destinatario, riempe automaticamente il campo porto
        # con Franco o Assegnato.
        if not self.vettore_radiobutton.get_active():
            self.id_vettore_customcombobox.set_active(0)
        if self.mittente_radiobutton.get_active():
            self.porto_combobox.set_active(0)
        elif self.destinatario_radiobutton.get_active():
            self.porto_combobox.set_active(1)

    def on_id_magazzino_combobox_changed(self, combobox):
        if self._loading:
            return

        self._righe[0]["idMagazzino"] = findIdFromCombobox(self.id_magazzino_combobox)
        magazzino = leggiMagazzino(self._righe[0]["idMagazzino"])
        self._righe[0]["magazzino"] = magazzino["denominazione"]
        self.refresh_combobox_listini()


    def refresh_combobox_listini(self):

        if self._righe[0]["idArticolo"] is None:
            self.id_listino_customcombobox.combobox.clear
        else:
            fillComboboxListiniFiltrati(self.id_listino_customcombobox.combobox,
                    self._righe[0]["idArticolo"],
                    self._righe[0]["idMagazzino"],
                    self.id_persona_giuridica_customcombobox.getId())
            if self._id_listino is not None:
                findComboboxRowFromId(self.id_listino_customcombobox.combobox, self._id_listino)

    def on_id_multiplo_customcombobox_button_clicked(self, widget, toggleButton):

        on_id_multiplo_customcombobox_clicked(widget, toggleButton, self._righe[0]["idArticolo"])

    def on_id_multiplo_customcombobox_changed(self, combobox):

        if self._loading:
            return
        self._righe[0]["idMultiplo"] = findIdFromCombobox(self.id_multiplo_customcombobox.combobox)
        multiplo = leggiMultiplo(self._righe[0]["idMultiplo"])
        self._righe[0]["multiplo"] = multiplo["denominazioneBreve"] + ' ( ' + str('%.2f' % multiplo["moltiplicatore"]) + ' X )'
        self._righe[0]["moltiplicatore"] = multiplo["moltiplicatore"]
        self.calcolaTotaleRiga()

    def on_id_listino_customcombobox_button_clicked(self, widget, toggleButton):
        on_id_listino_customcombobox_clicked(widget, toggleButton, self._righe[0]["idArticolo"], None)

    def on_id_listino_customcombobox_button_toggled(self, button):
        if button.get_property('active') is True:
            return
        self.refresh_combobox_listini()

    def on_id_listino_customcombobox_changed(self, combobox):
        """ """
        if self._loading:
            return
        idListino = findIdFromCombobox(self.id_listino_customcombobox.combobox)
        idArticolo = self._righe[0]["idArticolo"]
        self.getPrezzoVenditaLordo(idListino, idArticolo)
        self.prezzo_lordo_entry.set_text(Environment.conf.number_format % float(self._righe[0]["prezzoLordo"]))
        self.on_show_totali_riga()

    def getPrezzoVenditaLordo(self, idListino, idArticolo):
        """ cerca il prezzo di vendita """
        prezzoLordo = 0
        if idListino is not None and idArticolo is not None:
            listino = leggiListino(idListino, idArticolo)
            self._righe[0]["listino"] = listino["denominazione"]
            if (self._fonteValore == "vendita_iva"):
                prezzoLordo = listino["prezzoDettaglio"]
            elif (self._fonteValore == "vendita_senza_iva"):
                prezzoLordo = listino["prezzoIngrosso"]
        self._righe[0]["prezzoLordo"] = prezzoLordo
        self._righe[0]["idListino"] = idListino

    def getPrezzoNetto(self):
        """ calcola il prezzo netto dal prezzo lordo e dagli sconti """
        prezzoLordo = float(self._righe[0]["prezzoLordo"])
        prezzoNetto = float(self._righe[0]["prezzoLordo"])
        applicazione = self._righe[0]["applicazioneSconti"]
        sconti = self._righe[0]["sconti"]
        for s in sconti:
            if s["tipo"] == 'percentuale':
                if applicazione == 'scalare':
                    prezzoNetto = prezzoNetto * (1 - float(s["valore"]) / 100)
                elif applicazione == 'non scalare':
                    prezzoNetto = prezzoNetto - prezzoLordo * float(s["valore"]) / 100
            elif s["tipo"] == 'valore':
                prezzoNetto = prezzoNetto - float(s["valore"])
        self._righe[0]["prezzoNetto"] = prezzoNetto

    def getTotaleRiga(self):

        segnoIva = 1
        percentualeIva = float(self._righe[0]["percentualeIva"])
        prezzoNetto = float(self._righe[0]["prezzoNetto"])
        quantita = float(self._righe[0]["quantita"])
        moltiplicatore = float(self._righe[0]["moltiplicatore"])
        #il totale riga non e' sempre l'imponibile (dipende dal tipo di prezzo)
        #if (self._fonteValore == "vendita_iva" or self._fonteValore == "acquisto_iva"):
        #    segnoIva = -1
        #    prezzoNetto = calcolaPrezzoIva(prezzoNetto, segnoIva * percentualeIva)

        self._righe[0]["totale"] = prezzoNetto * quantita * moltiplicatore

    def on_sconti_widget_button_toggled(self, button):

        if button.get_property('active') is True:
            return

        self._righe[0]["sconti"] = self.sconti_widget.getSconti()
        self._righe[0]["applicazioneSconti"] = self.sconti_widget.getApplicazione()
        self.on_show_totali_riga()

    def on_sconti_testata_widget_button_toggled(self, button):

        if button.get_property('active') is True:
            return

        self.calcolaTotale()

    def on_multi_line_button_clicked(self, widget):
        mleditor = GladeWidget('multi_linea_editor', callbacks_proxy=self)
        mleditor.multi_linea_editor.set_modal(modal=True)#
        #mleditor.multi_linea_editor.set_transient_for(self)
        #self.placeWindow(mleditor.multi_linea_editor)
        desc = self.descrizione_entry.get_text()
        textBuffer = mleditor.multi_line_editor_textview.get_buffer()
        textBuffer.set_text(desc)
        mleditor.multi_line_editor_textview.set_buffer(textBuffer)
        mleditor.multi_linea_editor.show_all()
        self.a = 0
        self.b = 0
        def test(widget, event):
            #print dir(textBuffer)
            char_count = textBuffer.get_char_count()
            line_count = textBuffer.get_line_count()
            if char_count >= 500:
                on_ok_button_clicked(button)
            if self.b != line_count:
                self.b = line_count
                self.a = -1
            self.a += 1
            colonne = Environment.multilinelimit
            if self.a <= (Environment.multilinelimit-1):
                pass
            else:
                textBuffer.insert_at_cursor("\n")
                self.a = -1
            modified = textBuffer.get_modified()
            textStatusBar = "Tot. Caratteri = %s , Righe = %s, Limite= %s, Colonna=%s" %(char_count,line_count, colonne, self.a)
            context_id =  mleditor.multi_line_editor_statusbar.get_context_id("Multi Editor")
            mleditor.multi_line_editor_statusbar.push(context_id,textStatusBar)

        def on_ok_button_clicked(button):
            text = textBuffer.get_text(textBuffer.get_start_iter(),
                                    textBuffer.get_end_iter())

            self.descrizione_entry.set_text(text)
            vediamo = self.descrizione_entry.get_text()
            mleditor.multi_linea_editor.hide()
        button = mleditor.ok_button
        button.connect("clicked", on_ok_button_clicked)
        mleditor.multi_line_editor_textview.connect("key-press-event", test)

    def on_notebook_switch_page(self, notebook, page, page_num):

        if page_num == 2:
            self.calcolaTotale()

    def _refresh(self):
        self._loading = True

        self._tipoPersonaGiuridica = None
        self._operazione = None
        self._fonteValore = None
        self._segno = None
        self._variazioneListiniResponse = ''
        self._variazioneListiniShow = True

        self.data_documento_entry.set_sensitive(self.dao.id is None)
        self.edit_date_and_number_button.set_sensitive(self.dao.id is not None)
        self.numero_documento_entry.set_sensitive(False)

        self.id_operazione_combobox.set_sensitive(self.dao.id is None)

        self.id_persona_giuridica_customcombobox.set_sensitive(self.dao.id is None)

        self.id_operazione_combobox.set_active(-1)
        self.id_persona_giuridica_customcombobox.set_active(-1)

        self._operazione = self.dao.operazione
        findComboboxRowFromId(self.id_operazione_combobox, self.dao.operazione)
        self.on_id_operazione_combobox_changed(self.id_operazione_combobox)
        self.id_persona_giuridica_customcombobox.refresh(clear=True, filter=False)
        if self._tipoPersonaGiuridica == "fornitore":
            self.id_persona_giuridica_customcombobox.setId(self.dao.id_fornitore)
            self.id_destinazione_merce_customcombobox.combobox.clear()
            self.id_destinazione_merce_customcombobox.set_sensitive(False)
        elif self._tipoPersonaGiuridica == "cliente":
            self.id_persona_giuridica_customcombobox.setId(self.dao.id_cliente)
            fillComboboxDestinazioniMerce(self.id_destinazione_merce_customcombobox.combobox,
                    self.dao.id_cliente)
            findComboboxRowFromId(self.id_destinazione_merce_customcombobox.combobox,
                    (self.dao.id_destinazione_merce or -1))
            self.id_destinazione_merce_customcombobox.set_sensitive(True)

        self.data_documento_entry.set_text(dateToString(self.dao.data_documento))
        self.numero_documento_entry.set_text(str(self.dao.numero or '0'))
        self.showDatiMovimento()

        findComboboxRowFromId(self.id_pagamento_customcombobox.combobox, (self.dao.id_pagamento or -1))
        findComboboxRowFromId(self.id_banca_customcombobox.combobox, (self.dao.id_banca or -1) )
        findComboboxRowFromId(self.id_aliquota_iva_esenzione_customcombobox.combobox,
                (self.dao.id_aliquota_iva_esenzione or -1))
        self.id_agente_customcombobox.refresh(clear=True, filter=False)
        insertComboboxSearchAgente(self.id_agente_customcombobox,
                self.dao.id_agente)
        self.protocollo_entry1.set_text(self.dao.protocollo or '')
        self.note_pie_pagina_entry.set_text(self.dao.note_pie_pagina or '')
        textBuffer = self.note_interne_textview.get_buffer()
        if self.dao.note_interne is not None:
            textBuffer.set_text(self.dao.note_interne)
        else:
            textBuffer.set_text('')
        self.note_interne_textview.set_buffer(textBuffer)
        self.causale_trasporto_comboboxentry.child.set_text(self.dao.causale_trasporto or '')
        self.aspetto_esteriore_beni_comboboxentry.child.set_text(self.dao.aspetto_esteriore_beni or '')
        self.inizio_trasporto_entry.set_text(dateTimeToString(self.dao.inizio_trasporto))
        self.fine_trasporto_entry.set_text(dateTimeToString(self.dao.fine_trasporto))
        self.id_vettore_customcombobox.refresh(clear=True, filter=False)
        if self.dao.incaricato_trasporto == 'vettore':
            # Se l'incaricato e` un vettore, allora bisogna attivare il campo Porto
            self.vettore_radiobutton.set_active(True)
            insertComboboxSearchVettore(self.id_vettore_customcombobox,
                    self.dao.id_vettore)
            self.porto_combobox.set_sensitive(True)
        if self.dao.porto == 'Franco':
            self.porto_combobox.set_active(0)
        elif self.dao.porto == 'Assegnato':
            self.porto_combobox.set_active(1)
            self.id_vettore_customcombobox.set_sensitive(True)

        if self.dao.incaricato_trasporto == 'destinatario':
            self.destinatario_radiobutton.set_active(True)
            self.id_vettore_customcombobox.set_sensitive(False)
            self.porto_combobox.set_sensitive(False)
        elif self.dao.incaricato_trasporto == 'mittente':
            self.mittente_radiobutton.set_active(True)
            self.id_vettore_customcombobox.set_sensitive(False)
            self.porto_combobox.set_sensitive(False)

        self.importo_da_ripartire_entry.set_text(str(self.dao.costo_da_ripartire or 0))
        if (self.dao.ripartire_importo is not None):
            self.ripartire_importo_checkbutton.set_active(self.dao.ripartire_importo)


        self.totale_colli_entry.set_text(str(self.dao.totale_colli or 0))
        self.totale_peso_entry.set_text(str(self.dao.totale_peso or 0))
        self.sconti_testata_widget.setValues(self.dao.sconti, self.dao.applicazione_sconti)
        self.clearRows()

        for riga in self.dao.righe:
            self.azzeraRiga(0)
            j = self.dao.righe.index(riga) + 1
            magazzino = leggiMagazzino(riga.id_magazzino)
            articolo = leggiArticolo(riga.id_articolo)
            listino = leggiListino(riga.id_listino)
            multiplo = leggiMultiplo(riga.id_multiplo)
            (sconti, applicazione) = getScontiFromDao(
                    riga.sconti, riga.applicazione_sconti)
            if "SuMisura" in Environment.modulesList and riga.misura_pezzo:
                altezza = (riga.misura_pezzo[-1].altezza)
                larghezza = (riga.misura_pezzo[-1].larghezza)
                moltiplicatore_pezzi = riga.misura_pezzo[-1].moltiplicatore
            else:
                altezza = ''
                larghezza = ''
                moltiplicatore_pezzi = ''

            self._righe[0]["idRiga"] = riga.id
            self._righe[0]["idMagazzino"] = riga.id_magazzino
            self._righe[0]["magazzino"] = magazzino["denominazione"]
            self._righe[0]["idArticolo"] = riga.id_articolo
            self._righe[0]["codiceArticolo"] = articolo["codice"]
            self._righe[0]["descrizione"] = riga.descrizione
            self._righe[0]["percentualeIva"] = riga.percentuale_iva
            self._righe[0]["idUnitaBase"] = articolo["idUnitaBase"]
            self._righe[0]["unitaBase"] = articolo["unitaBase"]
            self._righe[0]["idMultiplo"] = riga.id_multiplo
            if multiplo["moltiplicatore"] != 0:
                self._righe[0]["multiplo"] = multiplo["denominazioneBreve"] + ' ( ' + str('%.2f' % multiplo["moltiplicatore"]) + ' X )'
            else:
                self._righe[0]["multiplo"] = ''
            self._righe[0]["idListino"] = riga.id_listino
            self._righe[0]["listino"] = listino["denominazione"]
            self._righe[0]["quantita"] = riga.quantita
            self._righe[0]["moltiplicatore"] = riga.moltiplicatore
            self._righe[0]["prezzoLordo"] = riga.valore_unitario_lordo
            self._righe[0]["sconti"] = sconti
            self._righe[0]["applicazioneSconti"] = applicazione
            self._righe[0]["prezzoNetto"] = riga.valore_unitario_netto
            self._righe[0]["prezzoNettoUltimo"] = riga.valore_unitario_netto
            self._righe[0]["totale"] = 0
            if "SuMisura" in Environment.modulesList:
                self._righe[0]["altezza"] = altezza
                self._righe[0]["larghezza"] = larghezza
                self._righe[0]["molt_pezzi"] = moltiplicatore_pezzi

            self.getTotaleRiga()
            self.unitaBaseLabel.set_text(self._righe[0]["unitaBase"])
            if self._tipoPersonaGiuridica == "fornitore":
                fornitura = leggiFornitura(riga.id_articolo, self.dao.id_fornitore, self.dao.data_documento, True)
                self._righe[0]["codiceArticoloFornitore"] = fornitura["codiceArticoloFornitore"]

            self._righe.append(self._righe[0])

            self.modelRiga.append((self._righe[j]["magazzino"],
                                    self._righe[j]["codiceArticolo"],
                                    self._righe[j]["descrizione"],
                                    '%5.2f' % float(self._righe[j]["percentualeIva"]),
                                    self._righe[j]["altezza"],
                                    self._righe[j]["larghezza"],
                                    self._righe[j]["molt_pezzi"],
                                    self._righe[j]["multiplo"],
                                    self._righe[j]["listino"],
                                    self._righe[j]["unitaBase"],
                                    '%9.3f' % float(self._righe[j]["quantita"]),
                                    ('%14.' + Environment.conf.decimals + 'f') % float(self._righe[j]["prezzoLordo"]),
                                    self._righe[j]["applicazioneSconti"] + ' ' + getStringaSconti(self._righe[j]["sconti"]),
                                    ('%14.' + Environment.conf.decimals + 'f') % float(self._righe[j]["prezzoNetto"]),
                                    ('%14.2f') % round(float(self._righe[j]["totale"]), 2)))

        self.righe_treeview.set_model(self.modelRiga)
        self._loading = False
        self.calcolaTotale()
        self.label_numero_righe.set_text(str(len(self.dao.righe)))
        self.notebook.set_current_page(0)
        self.nuovaRiga()
        if self.dao.id is None or self.numero_documento_entry.get_text() == '0':
            self.id_operazione_combobox.grab_focus()
        else:
            self.id_magazzino_combobox.grab_focus()
        if Environment.conf.hasPagamenti == True:
            self.Pagamenti.getScadenze()

    def setDao(self, dao):

        if dao is None:
            # Crea un nuovo Dao vuoto
            self.dao = TestataDocumento().getRecord()
            # Suggerisce la data odierna
            self.dao.data_documento = datetime.datetime.today()
            self._oldDaoRicreato = False #il dao è nuovo il controllo sul nuovo codice è necessario
        else:
            # Ricrea il Dao con una connessione al DBMS SQL
            self.dao = TestataDocumento(id=dao.id).getRecord()
            self._controllo_data_documento = dateToString(self.dao.data_documento)
            self._controllo_numero_documento = self.dao.numero
            self._oldDaoRicreato = True #il dao è nuovo il controllo sul nuovo codice non  è necessario

        self._refresh()


    def saveDao(self):
        scontiRigaDocumentoList = {}
        if not(len(self._righe) > 1):
            #print "ATTENZIONE, TENTATIVO DI SALVATAGGIO SENZA RIGHE?????"
            raise Exception, "ATTENZIONE, TENTATIVO DI SALVATAGGIO SENZA RIGHE?????"
            #return

        if (self.data_documento_entry.get_text() == ''):
            obligatoryField(self.dialogTopLevel,
                    self.data_documento_entry,
                    'Inserire la data del documento !')

        if (findIdFromCombobox(self.id_operazione_combobox) is None):
            obligatoryField(self.dialogTopLevel,
                    self.id_operazione_combobox,
                    'Inserire il tipo di documento !')

        if self.id_persona_giuridica_customcombobox.getId() is None:
            obligatoryField(self.dialogTopLevel,
                    self.id_persona_giuridica_customcombobox,
                    'Inserire l\'intestatario del documento !')

        self.dao.data_documento = stringToDate(self.data_documento_entry.get_text())
        if self.dao.id is not None and self.numero_documento_entry.get_text() != '0':

            #print "DATA DOCUMENTO :", self.data_documento_entry.get_text() == self._controllo_data_documento
            #print "NUMERO DOCUMENTO:", str(self.numero_documento_entry.get_text()) == str(self._controllo_numero_documento)

            if self.data_documento_entry.get_text() != self._controllo_data_documento or str(self.numero_documento_entry.get_text()) != str(self._controllo_numero_documento):
                numero = self.numero_documento_entry.get_text()
                idOperazione = findIdFromCombobox(self.id_operazione_combobox)
                daData, aData = getDateRange(self.data_documento_entry.get_text())
                docs = TestataDocumento(isList=True).select(daNumero=numero,
                                                    aNumero=numero,
                                                    daData=daData, aData=aData,
                                                    idOperazione=idOperazione, offset=None,
                                                    batchSize=None)
                if len(docs) > 0:
                    msg = """Attenzione!
Esiste già un documento numero %s per
l'anno di esercizio indicato nella data
del documento.
    Continuare comunque?""" % numero

                    dialog = gtk.MessageDialog(None, gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
                    gtk.MESSAGE_INFO, gtk.BUTTONS_OK_CANCEL, msg)
                    response = dialog.run()
                    dialog.destroy()
                    if response == gtk.RESPONSE_NONE or response == gtk.RESPONSE_CANCEL:
                        return
                    elif response == gtk.RESPONSE_OK:
                        #nothing to do about it.
                        print """si è deciso di salvare un documento il cui numero
                        è già stato usato per un altro. questo comporterà
                        l 'esistenza di due documenti con lo stesso numero!"""


                self.dao.numero = numero
        self.dao.operazione = self._operazione
        if self._tipoPersonaGiuridica == "fornitore":
            self.dao.id_fornitore = self.id_persona_giuridica_customcombobox.getId()
            self.dao.id_cliente = None
            self.dao.id_destinazione_merce = None
        elif self._tipoPersonaGiuridica == "cliente":
            self.dao.id_cliente = self.id_persona_giuridica_customcombobox.getId()
            self.dao.id_fornitore = None
            self.dao.id_destinazione_merce = findIdFromCombobox(self.id_destinazione_merce_customcombobox.combobox)

        self.dao.id_pagamento = findIdFromCombobox(self.id_pagamento_customcombobox.combobox)
        self.dao.id_banca = findIdFromCombobox(self.id_banca_customcombobox.combobox)
        self.dao.id_aliquota_iva_esenzione = findIdFromCombobox(self.id_aliquota_iva_esenzione_customcombobox.combobox)
        self.dao.id_agente = self.id_agente_customcombobox._id
        self.dao.protocollo = self.protocollo_entry1.get_text()
        self.dao.causale_trasporto = self.causale_trasporto_comboboxentry.child.get_text()
        self.dao.aspetto_esteriore_beni = self.aspetto_esteriore_beni_comboboxentry.child.get_text()
        self.dao.inizio_trasporto = stringToDateTime(self.inizio_trasporto_entry.get_text())
        self.dao.fine_trasporto = stringToDateTime(self.fine_trasporto_entry.get_text())

        if self.vettore_radiobutton.get_active():
            self.dao.id_vettore = self.id_vettore_customcombobox._id
            self.dao.incaricato_trasporto = 'vettore'
            if self.porto_combobox.get_active() == 0:
                self.dao.porto = 'Franco'
            elif self.porto_combobox.get_active() == 1:
                self.dao.porto = 'Assegnato'
        elif self.mittente_radiobutton.get_active():
            self.dao.id_vettore = None
            self.dao.incaricato_trasporto = 'mittente'
            self.dao.porto = 'Franco'
        elif self.destinatario_radiobutton.get_active():
            self.dao.id_vettore = None
            self.dao.incaricato_trasporto = 'destinatario'
            self.dao.porto = 'Assegnato'
        self.dao.totale_colli = self.totale_colli_entry.get_text()
        self.dao.totale_peso = self.totale_peso_entry.get_text()
        textBuffer = self.note_interne_textview.get_buffer()
        self.dao.note_interne = textBuffer.get_text(textBuffer.get_start_iter(), textBuffer.get_end_iter())
        self.dao.note_pie_pagina = self.note_pie_pagina_entry.get_text()
        self.dao.applicazione_sconti = self.sconti_testata_widget.getApplicazione()

        scontiSuTotale = {}
        res = self.sconti_testata_widget.getSconti()
        if res is not None:
            for k in range(0, len(res)):
                daoSconto = ScontoTestataDocumento().getRecord()
                daoSconto.valore = float(res[k]["valore"])
                daoSconto.tipo_sconto = res[k]["tipo"]
                scontiSuTotale[self.dao]=daoSconto
                #scontiSuTotale.append(daoSconto)

        #self.dao.sconti = scontiSuTotale
        scontiRigaDocumento={}
        righe = {}
        for i in range(1, len(self._righe)):
            daoRiga = RigaDocumento().getRecord()
            daoRiga.id_testata_documento = self.dao.id
            daoRiga.id_articolo = self._righe[i]["idArticolo"]
            daoRiga.id_magazzino = self._righe[i]["idMagazzino"]
            daoRiga.descrizione = self._righe[i]["descrizione"]
            daoRiga.codiceArticoloFornitore = self._righe[i]["codiceArticoloFornitore"]
            daoRiga.id_listino = self._righe[i]["idListino"]
            daoRiga.percentuale_iva = self._righe[i]["percentualeIva"]
            daoRiga.applicazione_sconti = self._righe[i]["applicazioneSconti"]
            daoRiga.quantita = self._righe[i]["quantita"]
            daoRiga.id_multiplo = self._righe[i]["idMultiplo"]
            daoRiga.moltiplicatore = self._righe[i]["moltiplicatore"]
            daoRiga.valore_unitario_lordo = self._righe[i]["prezzoLordo"]
            daoRiga.valore_unitario_netto = self._righe[i]["prezzoNetto"]

            sconti =[]
            listsco=[]
            if self._righe[i]["sconti"] is not None:
                for scon in self._righe[i]["sconti"]:
                    daoSconto = ScontoRigaDocumento().getRecord()
                    daoSconto.valore = float(scon["valore"])
                    daoSconto.tipo_sconto = scon["tipo"]
                    sconti.append(daoSconto)
            scontiRigaDocumento[daoRiga] = sconti
            sconti =[]

            if self._righe[i]["altezza"] != '' and self._righe[i]["larghezza"] != '' and "SuMisura" in Environment.modulesList:
                print "VEDIAMO SE ARRIVI A ISTANZIARE LA MISURA PEZZO EHHHHHH"
                from promogest.modules.SuMisura.dao.MisuraPezzo import MisuraPezzo
                daoMisura = MisuraPezzo().getRecord()
                daoMisura.altezza = float(self._righe[i]["altezza"] or 0)
                daoMisura.larghezza = float(self._righe[i]["larghezza"] or 0)
                daoMisura.moltiplicatore = float(self._righe[i]["molt_pezzi"] or 0)
                misure = daoMisura
                daoRiga.misura_pezzo = misure
            righe[i]=daoRiga
            #righe.append(daoRiga)

        #self.dao.righe = righe
        #FIXME : controllareee
        #self.dao.removeDividedCost()
        self.dao.costo_da_ripartire = self.importo_da_ripartire_entry.get_text()

        self.dao.ripartire_importo = self.ripartire_importo_checkbutton.get_active()
        if Environment.conf.hasPagamenti == True:
            self.Pagamenti.saveScadenze()

        tipoid = findIdFromCombobox(self.id_operazione_combobox)
        tipo = Operazione(id=tipoid).getRecord()
        if not self.dao.numero:
            valori = numeroRegistroGet(tipo=tipo.denominazione, date=self.data_documento_entry.get_text())
            self.dao.numero = valori[0]
            self.dao.registro_numerazione= valori[1]
        #porto in persist tre dizionari: uno per gli sconti sul totale, l'altro per gli sconti sulle righe e le righe stesse
        self.dao.persist(scontiRigaDocumento=scontiRigaDocumento,
                        scontiSuTotale=scontiSuTotale,
                        righe=righe)
        self.label_numero_righe.hide()
        text = str(len(self.dao.righe))
        self.label_numero_righe.set_text(text)
        self.label_numero_righe.show()

    def on_importo_da_ripartire_entry_changed(self, entry):
        self.dao.removeDividedCost()
        self.dao.ripartire_importo = False
        self.ripartire_importo_checkbutton.set_active(self.dao.ripartire_importo)
        self.dao.costo_da_ripartire = Decimal(self.importo_da_ripartire_entry.get_text())

        self.importo_sovrapprezzo_label.set_text(str('%.2f' % float(float(self.dao.costo_da_ripartire or 0)/self.dao.totalConfections)))

    def on_ripartire_importo_checkbutton_toggled(self, checkbutton):
        self.dao.ripartire_importo = self.ripartire_importo_checkbutton.get_active()
        if self.dao.ripartire_importo == True:
            self.dao.addDividedCost()
        else:
            self.dao.removeDividedCost()
        self._refresh()

    def on_righe_treeview_row_activated(self, treeview, path, column):
        """ riporta la riva selezionata in primo piano per la modifica """
        sel = treeview.get_selection()
        (model, self._iteratorRiga) = sel.get_selected()
        (selRow, ) = path
        self._numRiga = selRow + 1

        self.azzeraRiga(0)
        self._loading = True

        self._righe[0]["idRiga"] = self._righe[self._numRiga]["idRiga"]
        self._righe[0]["idMagazzino"] = self._righe[self._numRiga]["idMagazzino"]
        self._righe[0]["magazzino"] = self._righe[self._numRiga]["magazzino"]
        self._righe[0]["idArticolo"] = self._righe[self._numRiga]["idArticolo"]
        self._righe[0]["codiceArticolo"] = self._righe[self._numRiga]["codiceArticolo"]
        self._righe[0]["descrizione"] = self._righe[self._numRiga]["descrizione"]
        self._righe[0]["codiceArticoloFornitore"] = self._righe[self._numRiga]["codiceArticoloFornitore"]
        self._righe[0]["idUnitaBase"] = self._righe[self._numRiga]["idUnitaBase"]
        self._righe[0]["unitaBase"] = self._righe[self._numRiga]["unitaBase"]
        self._righe[0]["idMultiplo"] = self._righe[self._numRiga]["idMultiplo"]
        self._righe[0]["multiplo"] = self._righe[self._numRiga]["multiplo"]
        self._righe[0]["idListino"] = self._righe[self._numRiga]["idListino"]
        self._righe[0]["listino"] = self._righe[self._numRiga]["listino"]
        self._righe[0]["quantita"] = self._righe[self._numRiga]["quantita"]
        self._righe[0]["moltiplicatore"] = self._righe[self._numRiga]["moltiplicatore"]
        self._righe[0]["prezzoLordo"] = self._righe[self._numRiga]["prezzoLordo"]
        self._righe[0]["percentualeIva"] = self._righe[self._numRiga]["percentualeIva"]
        self._righe[0]["applicazioneSconti"] = self._righe[self._numRiga]["applicazioneSconti"]
        self._righe[0]["sconti"] = self._righe[self._numRiga]["sconti"]
        self._righe[0]["prezzoNetto"] = float(self._righe[self._numRiga]["prezzoNetto"])
        self._righe[0]["totale"] = self._righe[self._numRiga]["totale"]
        self._righe[0]["prezzoNettoUltimo"] = self._righe[self._numRiga]["prezzoNettoUltimo"]
        self._righe[0]["altezza"] = self._righe[self._numRiga]["altezza"]
        self._righe[0]["larghezza"] = self._righe[self._numRiga]["larghezza"]
        self._righe[0]["molt_pezzi"] = self._righe[self._numRiga]["molt_pezzi"]

        findComboboxRowFromId(self.id_magazzino_combobox, self._righe[0]["idMagazzino"])
        fillComboboxMultipli(self.id_multiplo_customcombobox.combobox, self._righe[0]["idArticolo"], True)
        findComboboxRowFromId(self.id_multiplo_customcombobox.combobox, self._righe[0]["idMultiplo"])
        self.refresh_combobox_listini()
        findComboboxRowFromId(self.id_listino_customcombobox.combobox, self._righe[0]["idListino"])

        self.articolo_entry.set_text(self._righe[0]["codiceArticolo"])
        self.descrizione_entry.set_text(self._righe[0]["descrizione"])
        self.codice_articolo_fornitore_entry.set_text(self._righe[0]["codiceArticoloFornitore"])
        self.percentuale_iva_entry.set_text('%-5.2f' % self._righe[0]["percentualeIva"])
        self.sconti_widget.setValues(self._righe[0]["sconti"], self._righe[0]["applicazioneSconti"], False)
        self.quantita_entry.set_text('%-9.3f' % float(self._righe[0]["quantita"]))
        self.prezzo_lordo_entry.set_text(Environment.conf.number_format % float(self._righe[0]["prezzoLordo"]))
        self.prezzo_netto_label.set_text(('%14.' + Environment.conf.decimals + 'f') % float(self._righe[0]["prezzoNetto"]))
        self.totale_riga_label.set_text(('%14.2f') % round(float(self._righe[0]["totale"]), 2))
        if "SuMisura" in Environment.modulesList:
            self.altezza_entry.set_text(str(self._righe[0]["altezza"]))
            self.larghezza_entry.set_text(str(self._righe[0]["larghezza"]))
            self.moltiplicatore_entry.set_text(str(self._righe[0]["molt_pezzi"]))

        self._loading = False
        self.articolo_entry.grab_focus()

    def on_new_row_button_clicked(self, widget):
        self.nuovaRiga()

    def on_confirm_row_withoutclean_button_clicked(self, widget):
        self.reuseDataRow = True
        self.on_confirm_row_button_clicked(widget)

    def on_confirm_row_button_clicked(self, widget,row=None):
        """
        Memorizza la riga inserita o modificata
        """

        self._righe[0]["idMagazzino"] = findIdFromCombobox(self.id_magazzino_combobox)
        magazzino = leggiMagazzino(self._righe[0]["idMagazzino"])
        self._righe[0]["magazzino"] = magazzino["denominazione"]

        if (self.data_documento_entry.get_text() == ''):
            self.showMessage('Inserire la data del documento !')
            return

        if (findIdFromCombobox(self.id_operazione_combobox) is None):
            self.showMessage('Inserire il tipo di documento !')
            return

        if (self.id_persona_giuridica_customcombobox.getId() is None):
            self.showMessage('Inserire l\'intestatario del documento !')
            return

        if ((self._righe[0]["idMagazzino"] is not None) and
                (self._righe[0]["idArticolo"] is None)):
            self.showMessage('Inserire l\'articolo !')
            return

        if ((self._righe[0]["idArticolo"] is not None) and
                (self._righe[0]["idMagazzino"] is None)):
            self.showMessage('Inserire il magazzino !')
            return

        costoVariato = (self._tipoPersonaGiuridica == "fornitore" and self._righe[0]["idArticolo"] is not None and
                (float(self._righe[0]["prezzoNetto"]) != float(self._righe[0]["prezzoNettoUltimo"])) and
                (self._segno is not None and self._segno != ''))

        if self._numRiga == 0:
            self._numRiga = len(self._righe)
            self._righe.append(self._righe[0])
            inserisci = True
        else:
            inserisci = False

        # memorizzazione delle parti descrittive (liberamente modificabili)
        self._righe[0]["descrizione"] = self.descrizione_entry.get_text()
        self._righe[0]["codiceArticoloFornitore"] = self.codice_articolo_fornitore_entry.get_text()

        if "SuMisura" in Environment.modulesList:
            self._righe[0]["altezza"] = self.altezza_entry.get_text()
            self._righe[0]["larghezza"] = self.larghezza_entry.get_text()
            self._righe[0]["molt_pezzi"] = self.moltiplicatore_entry.get_text()

        self._righe[self._numRiga]["idRiga"] = self._righe[0]["idRiga"]
        self._righe[self._numRiga]["idMagazzino"] = self._righe[0]["idMagazzino"]
        self._righe[self._numRiga]["magazzino"] = self._righe[0]["magazzino"]
        self._righe[self._numRiga]["idArticolo"] = self._righe[0]["idArticolo"]
        self._righe[self._numRiga]["codiceArticolo"] = self._righe[0]["codiceArticolo"]
        self._righe[self._numRiga]["descrizione"] = self._righe[0]["descrizione"]
        self._righe[self._numRiga]["codiceArticoloFornitore"] = self._righe[0]["codiceArticoloFornitore"]
        self._righe[self._numRiga]["percentualeIva"] = self._righe[0]["percentualeIva"]
        self._righe[self._numRiga]["idUnitaBase"] = self._righe[0]["idUnitaBase"]
        self._righe[self._numRiga]["unitaBase"] = self._righe[0]["unitaBase"]
        self._righe[self._numRiga]["idMultiplo"] = self._righe[0]["idMultiplo"]
        self._righe[self._numRiga]["multiplo"] = self._righe[0]["multiplo"]
        self._righe[self._numRiga]["idListino"] = self._righe[0]["idListino"]
        self._righe[self._numRiga]["listino"] = self._righe[0]["listino"]
        self._righe[self._numRiga]["quantita"] = float(self._righe[0]["quantita"])
        self._righe[self._numRiga]["moltiplicatore"] = float(self._righe[0]["moltiplicatore"])
        self._righe[self._numRiga]["prezzoLordo"] = float(self._righe[0]["prezzoLordo"])
        self._righe[self._numRiga]["applicazioneSconti"] = self._righe[0]["applicazioneSconti"]
        self._righe[self._numRiga]["sconti"] = self._righe[0]["sconti"]
        self._righe[self._numRiga]["prezzoNetto"] = float(self._righe[0]["prezzoNetto"])
        self._righe[self._numRiga]["totale"] = float(self._righe[0]["totale"])
        if "SuMisura" in Environment.modulesList:
            self._righe[self._numRiga]["altezza"] = self._righe[0]["altezza"]
            self._righe[self._numRiga]["larghezza"] = self._righe[0]["larghezza"]
            self._righe[self._numRiga]["molt_pezzi"] = self._righe[0]["molt_pezzi"]

        if not inserisci:
            if self._iteratorRiga is None:
                return
            self.modelRiga.set_value(self._iteratorRiga, 0, self._righe[self._numRiga]["magazzino"])
            self.modelRiga.set_value(self._iteratorRiga, 1, self._righe[self._numRiga]["codiceArticolo"])
            self.modelRiga.set_value(self._iteratorRiga, 2, self._righe[self._numRiga]["descrizione"])
            self.modelRiga.set_value(self._iteratorRiga, 3, '%5.2f' % float(self._righe[self._numRiga]["percentualeIva"]))
            if "SuMisura" in Environment.modulesList:
                self.modelRiga.set_value(self._iteratorRiga, 4, self._righe[self._numRiga][
                   "altezza"])
                self.modelRiga.set_value(self._iteratorRiga, 5, self._righe[self._numRiga][
                    "larghezza"])
                self.modelRiga.set_value(self._iteratorRiga, 6, self._righe[self._numRiga][
                    "molt_pezzi"])
            self.modelRiga.set_value(self._iteratorRiga, 7, self._righe[self._numRiga]["multiplo"])
            self.modelRiga.set_value(self._iteratorRiga, 8, self._righe[self._numRiga]["listino"])
            self.modelRiga.set_value(self._iteratorRiga, 9, self._righe[self._numRiga]["unitaBase"])
            self.modelRiga.set_value(self._iteratorRiga, 10, '%9.3f' % float(self._righe[self._numRiga]["quantita"]))
            self.modelRiga.set_value(self._iteratorRiga, 11, ('%14.' + Environment.conf.decimals + 'f') % float(
                self._righe[self._numRiga]["prezzoLordo"]))
            self.modelRiga.set_value(self._iteratorRiga, 12, self._righe[self._numRiga]["applicazioneSconti"] + (
                ' ' + getStringaSconti(self._righe[self._numRiga]["sconti"])))
            self.modelRiga.set_value(self._iteratorRiga, 13, ('%14.' + Environment.conf.decimals + 'f') % float(
                self._righe[self._numRiga]["prezzoNetto"]))
            self.modelRiga.set_value(self._iteratorRiga, 14, ('%14.2f') % round(
                float(self._righe[self._numRiga]["totale"]), 2))
        else:
            self.modelRiga.append((self._righe[self._numRiga]["magazzino"],
                self._righe[self._numRiga]["codiceArticolo"],
                self._righe[self._numRiga]["descrizione"],
                '%5.2f' % float(self._righe[self._numRiga]["percentualeIva"]),
                self._righe[self._numRiga]["altezza"],
                self._righe[self._numRiga]["larghezza"],
                self._righe[self._numRiga]["molt_pezzi"],
                self._righe[self._numRiga]["multiplo"],
                self._righe[self._numRiga]["listino"],
                self._righe[self._numRiga]["unitaBase"],
                '%9.3f' % float(self._righe[self._numRiga]["quantita"]),
                ('%14.' + Environment.conf.decimals + 'f') % float(self._righe[
                    self._numRiga]["prezzoLordo"]),
                self._righe[self._numRiga]["applicazioneSconti"] + ' ' + getStringaSconti(
                    self._righe[self._numRiga]["sconti"]),
                ('%14.' + Environment.conf.decimals + 'f') % float(self._righe[
                    self._numRiga]["prezzoNetto"]),


                ('%14.2f') % round(float(self._righe[self._numRiga]["totale"]), 2)))
        self.calcolaTotale()

        if costoVariato:
            if not(self._variazioneListiniResponse == 'all' or self._variazioneListiniResponse == 'none'):
                msg = 'Il prezzo di acquisto e\' stato variato:\n\n   si desidera aggiornare i listini di vendita ?'
                response = showComplexQuestion(self.dialogTopLevel, msg)
                if response == gtk.RESPONSE_YES:
                    self._variazioneListiniResponse = 'yes'
                    #la richiesta verra' riproposta per la successiva variante o articolo
                    self._variazioneListiniShow = True
                elif response == gtk.RESPONSE_NO:
                    self._variazioneListiniResponse = 'no'
                    #la richiesta verra' riproposta per la successiva variante o articolo
                    self._variazioneListiniShow = False
                elif response == gtk.RESPONSE_APPLY:
                    self._variazioneListiniResponse = 'all'
                    #la richiesta non verra' riproposta per la successiva variante o articolo
                    #ma per il prossimo articolo padre si'
                    self._variazioneListiniShow = True
                elif response == gtk.RESPONSE_REJECT:
                    self._variazioneListiniResponse = 'none'
                    #la richiesta non verra' riproposta per la successiva variante o articolo
                    #ma per il prossimo articolo padre si'
                    self._variazioneListiniShow = False

            if self._variazioneListiniShow:
                self.on_variazione_listini_button_clicked(self.variazione_listini_button)

        self._righe[self._numRiga]["prezzoNettoUltimo"] = float(self._righe[0]["prezzoNetto"])
        if self.reuseDataRow:
            rigatampone = self._righe[0]
            self.reuseDataRow=False
            self.nuovaRigaNoClean(rigatampone=rigatampone)
        else:
            self.nuovaRiga()

    def on_undo_row_button_clicked(self, widget):
        """ annulla l'inserimento o la modifica della riga in primo piano """
        self.nuovaRiga()

    def on_delete_row_button_clicked(self, widget):
        """ elimina la riga in primo piano """

        if not(self._numRiga == 0):
            del(self._righe[self._numRiga])
            self.modelRiga.remove(self._iteratorRiga)
        self.calcolaTotale()
        self.nuovaRiga()

    def on_ricerca_codice_button_clicked(self, widget):

        if self.ricerca_codice_button.get_active():
            self.ricercaArticolo()

    def on_ricerca_codice_a_barre_button_clicked(self, widget):

        if self.ricerca_codice_a_barre_button.get_active():
            self.ricercaArticolo()

    def on_ricerca_descrizione_button_clicked(self, widget):

        if self.ricerca_descrizione_button.get_active():
            self.ricercaArticolo()

    def on_ricerca_codice_articolo_fornitore_button_clicked(self, widget):

        if self.ricerca_codice_articolo_fornitore_button.get_active():
            self.ricercaArticolo()

    def on_articolo_entry_key_press_event(self, widget, event):

        keyname = gtk.gdk.keyval_name(event.keyval)
        if keyname == 'Return' or keyname == 'KP_Enter':
            self.ricercaArticolo()

    def on_search_row_button_clicked(self, widget):
        self.ricercaArticolo()

    def ricercaArticolo(self):

        def on_ricerca_articolo_hide(anagWindow, anag):
            if anag.dao is None:
                anagWindow.destroy()
                return

            anagWindow.destroy()
            self.mostraArticolo(anag.dao.id)


        if (self.data_documento_entry.get_text() == ''):
            self.showMessage('Inserire la data del documento !')
            return

        if (findIdFromCombobox(self.id_operazione_combobox) is None):
            self.showMessage('Inserire il tipo di documento !')
            return

        if (findIdFromCombobox(self.id_magazzino_combobox) is None):
            self.showMessage('Inserire il magazzino !')
            return

        codice = None
        codiceABarre = None
        denominazione = None
        codiceArticoloFornitore = None

        if self.ricerca_codice_button.get_active():
            codice = self.articolo_entry.get_text()
            orderBy = "codice"
        elif self.ricerca_codice_a_barre_button.get_active():
            codiceABarre = self.articolo_entry.get_text()
            orderBy = "codice_a_barre"
        elif self.ricerca_descrizione_button.get_active():
            denominazione = self.articolo_entry.get_text()
            orderBy = "denominazione"
        elif self.ricerca_codice_articolo_fornitore_button.get_active():
            codiceArticoloFornitore = self.articolo_entry.get_text()
            orderBy = "codice_articolo_fornitore"

        arts = Articolo(isList=True).select(orderBy=orderBy,
                                             denominazione=prepareFilterString(denominazione),
                                             codice=prepareFilterString(codice),
                                             codiceABarre=prepareFilterString(codiceABarre),
                                             codiceArticoloFornitore=prepareFilterString(codiceArticoloFornitore),
                                             idFamiglia=None,
                                             idCategoria=None,
                                             idStato=None,
                                             offset=None,
                                             batchSize=None)

        if (len(arts) == 1):

            self.mostraArticolo(arts[0].id)
        else:
            from RicercaComplessaArticoli import RicercaComplessaArticoli
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

    def on_promowear_manager_taglia_colore_togglebutton_toggled(self, togglebutton):
        active=self.promowear_manager_taglia_colore_togglebutton.get_active()
        if active:
            from promogest.modules.PromoWear.ui.ManageSizeAndColor import ManageSizeAndColor
            manag = ManageSizeAndColor(self, data=self.idArticoloWithVarianti)
            anagWindow = manag.getTopLevel()
            anagWindow.set_transient_for(self.dialogTopLevel)
        else:
            if Environment.tagliacoloretempdata[1]:
                for var in Environment.tagliacoloretempdata[1]:
                    self.mostraArticolo(var['id'],art=var)
            Environment.tagliacoloretempdata = (False,[])

    def mostraArticolo(self, id, art=None):
        self.articolo_entry.set_text('')
        self.descrizione_entry.set_text('')
        self.codice_articolo_fornitore_entry.set_text('')
        self.percentuale_iva_entry.set_text('0')
        self.id_multiplo_customcombobox.combobox.clear()
        self.id_listino_customcombobox.combobox.clear()
        self.prezzo_lordo_entry.set_text('0')
        self.quantita_entry.set_text('0')
        self.prezzo_netto_label.set_text('0')
        self.sconti_widget.clearValues()
        self.totale_riga_label.set_text('0')

        self._righe[0]["idArticolo"] = None
        self._righe[0]["codiceArticolo"] = ''
        self._righe[0]["descrizione"] = ''
        self._righe[0]["codiceArticoloFornitore"] = ''
        self._righe[0]["percentualeIva"] = 0
        self._righe[0]["idUnitaBase"] = None
        self._righe[0]["idMultiplo"] = None
        self._righe[0]["moltiplicatore"] = 1
        self._righe[0]["idListino"] = None
        self._righe[0]["prezzoLordo"] = 0
        self._righe[0]["quantita"] = 0
        self._righe[0]["prezzoNetto"] = 0
        self._righe[0]["sconti"] = []
        self._righe[0]["applicazioneSconti"] = 'scalare'
        self._righe[0]["totale"] = 0
        data = stringToDate(self.data_documento_entry.get_text())

        fillComboboxMultipli(self.id_multiplo_customcombobox.combobox, id, True)

        if id is not None:
            if "PromoWear" in Environment.modulesList:
                articolo = leggiArticolo(id,
                        idFornitore=self.id_persona_giuridica_customcombobox.getId(),
                        data=data)
                if articolo.has_key("varianti"):
                    self.promowear_manager_taglia_colore_togglebutton.set_property("visible", True)
                    self.promowear_manager_taglia_colore_togglebutton.set_sensitive(True)
                    self.idArticoloWithVarianti = articolo
                if art:
                    #print "ARTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT2", art
                    articolo = art
                    self._righe[0]["idArticolo"] = id
                    self._righe[0]["codiceArticolo"] = articolo["codice"]
                    self.articolo_entry.set_text(self._righe[0]["codiceArticolo"])
                    self._righe[0]["descrizione"] = articolo["denominazione"]
                    self.descrizione_entry.set_text(self._righe[0]["descrizione"])
                    self._righe[0]["percentualeIva"] = articolo["percentualeAliquotaIva"]
                    self.percentuale_iva_entry.set_text('%-5.2f' % self._righe[0]["percentualeIva"])
                    self._righe[0]["idUnitaBase"] = articolo["idUnitaBase"]
                    self._righe[0]["unitaBase"] = articolo["unitaBase"]
                    self.unitaBaseLabel.set_text(self._righe[0]["unitaBase"])
                    if ((self._fonteValore == "acquisto_iva") or  (self._fonteValore == "acquisto_senza_iva")):
                        costoLordo = articolo['fornitura']["prezzoLordo"]
                        if costoLordo:costoLordo = costoLordo.replace(',','.')
                        costoNetto = articolo['fornitura']["prezzoNetto"]
                        if costoNetto:costoNetto = costoNetto.replace(',','.')
                        if self._fonteValore == "acquisto_iva":
                            costoLordo = calcolaPrezzoIva(costoLordo, self._righe[0]["percentualeIva"])
                            costoNetto = calcolaPrezzoIva(costoNetto, self._righe[0]["percentualeIva"])
                        self._righe[0]["prezzoLordo"] = float(costoLordo)
                        self.prezzo_lordo_entry.set_text(Environment.conf.number_format % float(self._righe[0]["prezzoLordo"]))
                        self._righe[0]["prezzoNetto"] = float(costoNetto)
                        self.prezzo_netto_label.set_text(('%14.' + Environment.conf.decimals + 'f') % float(self._righe[0]["prezzoNetto"]))
                        self._righe[0]["prezzoNettoUltimo"] = float(costoNetto)
                        self._righe[0]["sconti"] = articolo['fornitura']["sconti"]
                        self._righe[0]["applicazioneSconti"] = articolo['fornitura']["applicazioneSconti"]
                        self.sconti_widget.setValues(self._righe[0]["sconti"], self._righe[0]["applicazioneSconti"], False)
                        self._righe[0]["codiceArticoloFornitore"] = articolo['fornitura']["codiceArticoloFornitore"]
                        self.codice_articolo_fornitore_entry.set_text(self._righe[0]["codiceArticoloFornitore"])
                        quantita =articolo["quantita"]
                        quantita = quantita.replace(',','.')
                        self._righe[0]["quantita"] = quantita
                        self.quantita_entry.set_text(self._righe[0]["quantita"])
                        if self._righe[0]["quantita"]:
                            self.calcolaTotaleRiga()

                    elif ((self._fonteValore == "vendita_iva") or
                        (self._fonteValore == "vendita_senza_iva")):
                        self.refresh_combobox_listini()
                    self.on_confirm_row_button_clicked(self.dialogTopLevel)
            else:
                articolo = leggiArticolo(id)
                self._righe[0]["idArticolo"] = id
                self._righe[0]["codiceArticolo"] = articolo["codice"]
                self.articolo_entry.set_text(self._righe[0]["codiceArticolo"])
                self._righe[0]["descrizione"] = articolo["denominazione"]
                self.descrizione_entry.set_text(self._righe[0]["descrizione"])
                self._righe[0]["percentualeIva"] = articolo["percentualeAliquotaIva"]
                self.percentuale_iva_entry.set_text('%-5.2f' % self._righe[0]["percentualeIva"])
                self._righe[0]["idUnitaBase"] = articolo["idUnitaBase"]
                self._righe[0]["unitaBase"] = articolo["unitaBase"]
                self.unitaBaseLabel.set_text(self._righe[0]["unitaBase"])
            self._righe[0]["idMultiplo"] = None
            self._righe[0]["moltiplicatore"] = 1
            self._righe[0]["prezzoLordo"] = 0
            self._righe[0]["prezzoNetto"] = 0
            self._righe[0]["sconti"] = []
            self._righe[0]["applicazioneSconti"] = 'scalare'
            self._righe[0]["codiceArticoloFornitore"] = ''

            if ((self._fonteValore == "acquisto_iva") or  (self._fonteValore == "acquisto_senza_iva")):
                fornitura = leggiFornitura(id, self.id_persona_giuridica_customcombobox.getId(), data)
                costoLordo = fornitura["prezzoLordo"]
                costoNetto = fornitura["prezzoNetto"]
                if self._fonteValore == "acquisto_iva":
                        costoLordo = calcolaPrezzoIva(costoLordo, self._righe[0]["percentualeIva"])
                        costoNetto = calcolaPrezzoIva(costoNetto, self._righe[0]["percentualeIva"])
                self._righe[0]["prezzoLordo"] = float(costoLordo)
                self.prezzo_lordo_entry.set_text(Environment.conf.number_format % float(self._righe[0]["prezzoLordo"]))
                self._righe[0]["prezzoNetto"] = float(costoNetto)
                self.prezzo_netto_label.set_text(('%14.' + Environment.conf.decimals + 'f') % float(self._righe[0]["prezzoNetto"]))
                self._righe[0]["prezzoNettoUltimo"] = float(costoNetto)
                self._righe[0]["sconti"] = fornitura["sconti"]
                self._righe[0]["applicazioneSconti"] = fornitura["applicazioneSconti"]
                self.sconti_widget.setValues(self._righe[0]["sconti"], self._righe[0]["applicazioneSconti"], False)
                self._righe[0]["codiceArticoloFornitore"] = fornitura["codiceArticoloFornitore"]
                self.codice_articolo_fornitore_entry.set_text(self._righe[0]["codiceArticoloFornitore"])
            elif ((self._fonteValore == "vendita_iva") or
                  (self._fonteValore == "vendita_senza_iva")):
                self.refresh_combobox_listini()

        if self._tipoPersonaGiuridica == "cliente":
            self.id_listino_customcombobox.combobox.grab_focus()
        elif self._tipoPersonaGiuridica == "fornitore":
            self.codice_articolo_fornitore_entry.grab_focus()
        else:
            self.descrizione_entry.grab_focus()


    def on_show_totali_riga(self, widget = None, event = None):
        """ calcola il prezzo netto """

        self._righe[0]["quantita"] = float(self.quantita_entry.get_text() or 0)
        self._righe[0]["prezzoLordo"] = float(self.prezzo_lordo_entry.get_text() or 0)
        self._righe[0]["percentualeIva"] = float(self.percentuale_iva_entry.get_text() or 0)
        self._righe[0]["applicazioneSconti"] = self.sconti_widget.getApplicazione()
        self._righe[0]["prezzoNetto"] = float(self._righe[0]["prezzoLordo"])
        self._righe[0]["sconti"] = self.sconti_widget.getSconti()
        self._righe[0]["applicazioneSconti"] = self.sconti_widget.getApplicazione()

        self.getPrezzoNetto()
        self.prezzo_netto_label.set_text(('%14.' + Environment.conf.decimals + 'f') % float(self._righe[0]["prezzoNetto"]))
        self.calcolaTotaleRiga()
        return False


    def calcolaTotaleRiga(self):
        """ calcola il totale riga """

        if self._righe[0]["prezzoNetto"] is None:
            self._righe[0]["prezzoNetto"] = 0
        if self._righe[0]["quantita"] is None:
            self._righe[0]["quantita"] = 0
        if self._righe[0]["moltiplicatore"] is None:
            self._righe[0]["moltiplicatore"] = 1
        elif float(self._righe[0]["moltiplicatore"]) == 0:
            self._righe[0]["moltiplicatore"] = 1

        self.getTotaleRiga()
        self.totale_riga_label.set_text(('%14.2f') % round(float(self._righe[0]["totale"]), 2))


    def calcolaTotale(self):
        """ calcola i totali documento """


        # FIXME: duplicated in TestataDocumenti.py
        totaleImponibile = float(0)
        totaleImposta = float(0)
        totaleNonScontato = float(0)

        totaleImpostaScontata = float(0)
        totaleImponibileScontato = float(0)
        totaleScontato = float(0)

        castellettoIva = {}

        for i in range(1, len(self._righe)):
            prezzoNetto = float(self._righe[i]["prezzoNetto"])
            quantita = float(self._righe[i]["quantita"])
            moltiplicatore = float(self._righe[i]["moltiplicatore"])
            percentualeIva = float(self._righe[i]["percentualeIva"])

            totaleRiga = prezzoNetto * quantita * moltiplicatore
            percentualeIvaRiga = percentualeIva

            if (self._fonteValore == "vendita_iva" or
                self._fonteValore == "acquisto_iva"):
                totaleImponibileRiga = calcolaPrezzoIva(totaleRiga, -1 * percentualeIvaRiga)
            else:
                totaleImponibileRiga = totaleRiga
                totaleRiga = calcolaPrezzoIva(totaleRiga, percentualeIvaRiga)

            totaleImpostaRiga = totaleRiga - totaleImponibileRiga
            totaleNonScontato += totaleRiga
            totaleImponibile += totaleImponibileRiga
            totaleImposta += totaleImpostaRiga

            if percentualeIvaRiga not in castellettoIva.keys():
                castellettoIva[percentualeIvaRiga] = {'imponibile': totaleImponibileRiga, 'imposta': totaleImpostaRiga, 'totale': totaleRiga}
            else:
                castellettoIva[percentualeIvaRiga]['imponibile'] += totaleImponibileRiga
                castellettoIva[percentualeIvaRiga]['imposta'] += totaleImpostaRiga
                castellettoIva[percentualeIvaRiga]['totale'] += totaleRiga

        totaleNonScontato = round(totaleNonScontato, 2)
        totaleImponibile = round(totaleImponibile, 2)
        totaleImposta = totaleNonScontato - totaleImponibile
        for percentualeIva in castellettoIva:
            castellettoIva[percentualeIva]['imponibile'] = round(castellettoIva[percentualeIva]['imponibile'], 2)
            castellettoIva[percentualeIva]['imposta'] = round(castellettoIva[percentualeIva]['imposta'], 2)
            castellettoIva[percentualeIva]['totale'] = round(castellettoIva[percentualeIva]['totale'], 2)

        totaleImponibileScontato = totaleImponibile
        totaleImpostaScontata = totaleImposta
        totaleScontato = totaleNonScontato
        scontiSuTotale = self.sconti_testata_widget.getSconti()
        applicazioneSconti = self.sconti_testata_widget.getApplicazione()

        if len(scontiSuTotale) > 0:
            for s in scontiSuTotale:
                if s["tipo"] == 'percentuale':
                    if applicazioneSconti == 'scalare':
                        totaleScontato = float(totaleScontato) * (1 - float(s["valore"]) / 100)
                    elif applicazioneSconti == 'non scalare':
                        totaleScontato = float(totaleScontato) - float(totaleNonScontato) * float(s["valore"]) / 100
                    else:
                        raise Exception, ('BUG! Tipo di applicazione sconto '
                                          'sconosciuto: %s' % s['tipo'])
                elif s["tipo"] == 'valore':
                    totaleScontato = float(totaleScontato) - float(s["valore"])

            # riporta l'insieme di sconti ad una percentuale globale
            percentualeScontoGlobale = (1 - totaleScontato / totaleNonScontato) * 100
            totaleImpostaScontata = 0
            totaleImponibileScontato = 0
            totaleScontato = 0
            # riproporzione del totale, dell'imponibile e dell'imposta
            for k in castellettoIva.keys():
                castellettoIva[k]['totale'] = round(float(castellettoIva[k]['totale']) * (1 - float(percentualeScontoGlobale) / 100), 2)
                castellettoIva[k]['imponibile'] = round(float(castellettoIva[k]['imponibile']) * (1 - float(percentualeScontoGlobale) / 100), 2)
                castellettoIva[k]['imposta'] = castellettoIva[k]['totale'] - castellettoIva[k]['imponibile']

                totaleImponibileScontato += castellettoIva[k]['imponibile']
                totaleImpostaScontata += castellettoIva[k]['imposta']

            totaleScontato = totaleImponibileScontato + totaleImpostaScontata

        self.totale_generale_label.set_text(('%14.2f') % float(totaleNonScontato))
        self.totale_generale_riepiloghi_label.set_text(('%14.2f') % float(totaleNonScontato))
        self.totale_imponibile_label.set_text(('%14.2f') % float(totaleImponibile))
        self.totale_imponibile_riepiloghi_label.set_text(('%14.2f') % float(totaleImponibile))
        self.totale_imposta_label.set_text(('%14.2f') % float(totaleImposta))
        self.totale_imposta_riepiloghi_label.set_text(('%14.2f') % float(totaleImposta))
        self.totale_imponibile_scontato_riepiloghi_label.set_text(('%14.2f') % float(totaleImponibileScontato))
        self.totale_imposta_scontata_riepiloghi_label.set_text(('%14.2f') % float(totaleImpostaScontata))
        self.totale_scontato_riepiloghi_label.set_text(('%14.2f') % float(totaleScontato))

        model = self.riepiloghi_iva_treeview.get_model()
        model.clear()
        for k in castellettoIva.keys():
            model.append(('%5.2f' % float(k),
                         ('%14.2f') % float(castellettoIva[k]['imponibile']),
                         ('%14.2f') % float(castellettoIva[k]['imposta'])))


    def showMessage(self, msg):

        dialog = gtk.MessageDialog(self.dialogTopLevel, gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
                                   gtk.MESSAGE_INFO, gtk.BUTTONS_OK, msg)
        dialog.run()
        dialog.destroy()


    def on_storico_costi_button_clicked(self, toggleButton):

        from StoricoForniture import StoricoForniture
        idArticolo = self._righe[0]["idArticolo"]
        if self._tipoPersonaGiuridica == "fornitore":
            idFornitore = self.id_persona_giuridica_customcombobox.getId()
        else:
            idFornitore = None
        anag = StoricoForniture(idArticolo, idFornitore)
        anagWindow = anag.getTopLevel()
        anagWindow.set_transient_for(self.dialogTopLevel)
        anagWindow.show_all()


    def on_storico_listini_button_clicked(self, toggleButton):

        from StoricoListini import StoricoListini
        idArticolo = self._righe[0]["idArticolo"]
        anag = StoricoListini(idArticolo)
        anagWindow = anag.getTopLevel()
        anagWindow.set_transient_for(self.dialogTopLevel)
        anagWindow.show_all()


    def on_variazione_listini_button_clicked(self, toggleButton):

        if self._righe[0]["idArticolo"] is None:
            self.showMessage('Selezionare un articolo !')
            return

        from VariazioneListini import VariazioneListini
        idArticolo = self._righe[0]["idArticolo"]
        costoNuovo = None
        costoUltimo = None
        if self._tipoPersonaGiuridica == "fornitore":
            costoNuovo = float(self._righe[0]["prezzoNetto"])
            costoUltimo = float(self._righe[0]["prezzoNettoUltimo"])
        anag = VariazioneListini(idArticolo, costoUltimo, costoNuovo)
        anagWindow = anag.getTopLevel()
        anagWindow.set_transient_for(self.dialogTopLevel)
        anagWindow.show_all()


    def on_edit_date_and_number_button_clicked(self, toggleButton):

        msg = 'Attenzione! Si sta per variare i riferimenti primari del documento.\n Continuare ?'
        dialog = gtk.MessageDialog(self.dialogTopLevel, gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
                                   gtk.MESSAGE_QUESTION, gtk.BUTTONS_YES_NO, msg)
        response = dialog.run()
        dialog.destroy()
        if response == gtk.RESPONSE_YES:
            self.data_documento_entry.set_sensitive(True)
            self.numero_documento_entry.set_sensitive(True)
            self.data_documento_entry.grab_focus()
            self.id_persona_giuridica_customcombobox.set_sensitive(True)


    def showDatiMovimento(self):

        stringLabel = '-'
        if self.dao.id is not None:
            res = TestataMovimento(isList=True).select(id_testata_documento= self.dao.id)
            if len(res) > 0:
                stringLabel = 'N.' + str(res[0].numero) + ' del ' + dateToString(res[0].data_movimento)

        self.rif_movimento_label.set_text(stringLabel)

    def on_larghezza_entry_key_press_event(self, entry, event):

        from promogest.modules.SuMisura.ui.SuMisura import CalcolaArea, CalcolaPerimetro

        altezza = float(self.altezza_entry.get_text() or 0)
        print "ALTEZZA!!!!!!!!!!!!!!!!!!!!!!!", altezza, self._righe[0]["unitaBase"]
        moltiplicatore = float(self.moltiplicatore_entry.get_text() or 1)
        if altezza != 0:
            larghezza = float(self.larghezza_entry.get_text() or 0)
            if larghezza != 0:
                if self._righe[0]["unitaBase"] == "Metri Quadri":
                    quantita = CalcolaArea(altezza, larghezza)
                    print "Ma cavolo " , quantita, altezza, larghezza
                elif self._righe[0]["unitaBase"] == "Metri":
                    quantita = CalcolaPerimetro(altezza, larghezza)
                else:
                    quantita = None
                if quantita is not None:
                    da_stamp = moltiplicatore * float(quantita)
                    self.quantita_entry.set_text(str(da_stamp))

    def on_altezza_entry_key_press_event(self, entry, event):

        from promogest.modules.SuMisura.ui.SuMisura import CalcolaArea, CalcolaPerimetro

        larghezza = float(self.larghezza_entry.get_text() or 0)
        moltiplicatore = float(self.moltiplicatore_entry.get_text() or 1)
        if larghezza != 0:
            altezza = float(self.altezza_entry.get_text())
            print "altezzaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa", altezza, self._righe[0]["unitaBase"]
            if altezza != 0:
                if self._righe[0]["unitaBase"] == "Metri Quadri":
                    quantita = CalcolaArea(altezza, larghezza)
                    print "Ma cavolo222 " , quantita, altezza, larghezza
                elif self._righe[0]["unitaBase"] == "Metri":
                    quantita = CalcolaPerimetro(altezza, larghezza)
                else:
                    quantita = None
                if quantita is not None:
                    da_stamp = float(quantita) * moltiplicatore
                    self.quantita_entry.set_text(str(da_stamp))

    def on_moltiplicatore_entry_key_press_event (self, entry, event):
        self.on_altezza_entry_key_press_event(entry, event)
        self.on_show_totali_riga()

    def on_quantita_entry_focus_out_event(self, entry, event):

        id = self._righe[0]["idArticolo"]
        if id is not None:
            articolo = leggiArticolo(id)
        else:
            return

        quantita = float(self.quantita_entry.get_text())
        quantita_minima = float(articolo["quantita_minima"])
        if (quantita < quantita_minima) :
            self.quantita_entry.set_text(str(quantita_minima))
