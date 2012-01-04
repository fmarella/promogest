# -*- coding: utf-8 -*-

#    Copyright (C) 2005-2012 by Promotux
#                        di Francesco Meloni snc - http://www.promotux.it/

#    Author: Francesco Meloni <francesco@promotux.it>
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

import datetime
from promogest.ui.AnagraficaComplessaEdit import AnagraficaEdit
from promogest.ui.anagDocumenti.AnagraficaDocumentiEditUtils import *
from promogest import Environment
from promogest.dao.TestataMovimento import TestataMovimento
from promogest.dao.TestataDocumento import TestataDocumento
from promogest.dao.RigaMovimento import RigaMovimento
from promogest.dao.ScontoRigaMovimento import ScontoRigaMovimento
from promogest.dao.Articolo import Articolo
from promogest.dao.Fornitore import Fornitore
from promogest.ui.utils import *
from promogest.ui.utilsCombobox import *
from promogest.ui.gtk_compat import *

if posso("PW"):
    from promogest.modules.PromoWear.ui import AnagraficaDocumentiEditPromoWearExt


class AnagraficaMovimentiEdit(AnagraficaEdit):

    def __init__(self, anagrafica):
        """
        Modifica un record dei movimenti
        """
        AnagraficaEdit.__init__(self,
                                anagrafica,
                                'anagrafica_movimenti_detail_vbox',
                                'Dati movimento',
                                gladeFile='_anagrafica_movimenti_elements.glade')
        self._widgetFirstFocus = self.data_movimento_entry
        #try:
            #if Environment.conf.Documenti.rosas =="yes":
                #pass
        #except:
        self.totale_spinbutton.destroy()
        self.prz_totale_label.destroy()
        self.id_multiplo_customcombobox.destroy()
        self.unita_derivate_label.destroy()

        # contenitore (dizionario) righe (riga 0 riservata per
        # variazioni in corso)
        self._righe = []
        self._righe.append({})
        # numero riga corrente
        self._numRiga = 0
        # modello righe: magazzino, codice articolo,
        # descrizione, percentuale iva, unita base, multiplo, listino,
        # quantita, prezzo lordo, sconti, prezzo netto, totale
        self.modelRiga = gtk.ListStore(str, str, str, str, str, str, str,
                                       str, str, str, str, str)
        # iteratore riga corrente
        self._iteratorRiga = None
        # cliente o fornitore ?
        self._tipoPersonaGiuridica = None
        self._operazione = None
        # prezzo vendita/acquisto, ivato/non ivato
        self._fonteValore = None
        # carico (+) o scarico (-) o novita ( = )
        self._segno = None
        # caricamento movimento (interrompe l'azione degli eventi on_changed nelle combobox)
        self._loading = False
        self.mattu = False
        self.completion = self.ricerca_articolo_entrycompletition
        if Environment.pg3:
            self.completion.set_match_func(self.match_func,None)
        else:
            self.completion.set_match_func(self.match_func)
        self.completion.set_text_column(0)
        self.articolo_entry.set_completion(self.completion)
        self.sepric = "  ~  "
        self.articolo_matchato = None
        if posso("PW"):
            self.promowear_manager_taglia_colore_togglebutton.set_property("visible", True)
            self.promowear_manager_taglia_colore_togglebutton.set_sensitive(False)
        else:
            hidePromoWear(self)


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
                               "idAliquotaIva":None,
                               "idUnitaBase": None,
                               "unitaBase": '',
                               "idMultiplo": None,
                               "multiplo": '',
                               "idListino": None,
                               "listino": '',
                               "quantita": 0,
                               "moltiplicatore": 0,
                               "prezzoLordo": 0,
                               "applicazioneSconti": '',
                               "sconti": [],
                               "prezzoNetto": 0,
                               "totale": 0,
                               "codiceArticoloFornitore": '',
                               "prezzoNettoUltimo": 0}


    def nuovaRiga(self):
        """
        prepara per l'inserimento di una nuova riga
        """
        self._numRiga = 0
        self.azzeraRiga(0)

        self.articolo_entry.set_text('')
        self.descrizione_entry.set_text('')
        self.codice_articolo_fornitore_entry.set_text('')
        #self.percentuale_iva_entry.set_text('0')
        self.id_iva_customcombobox.combobox.set_active(-1)
        self.id_multiplo_customcombobox.combobox.clear()
        self.id_listino_customcombobox.combobox.clear()
        self.prezzo_lordo_entry.set_text('0')
        self.quantita_entry.set_text('0')
        self.prezzo_netto_label.set_text('0')
        self.sconti_widget.clearValues()
        self.totale_riga_label.set_text('0')

        if len(self._righe) > 1:
            self.data_movimento_entry.set_sensitive(False)
            self.id_operazione_combobox.set_sensitive(False)
            self.id_persona_giuridica_customcombobox.set_sensitive(False)
            self.articolo_entry.grab_focus()
        else:
            self.data_movimento_entry.set_sensitive(True)
            self.id_persona_giuridica_customcombobox.set_sensitive(self.id_operazione_combobox.get_active() != -1)
            self.id_operazione_combobox.set_sensitive(True)
            if self._anagrafica._magazzinoFissato:
                findComboboxRowFromId(self.id_magazzino_combobox, self._anagrafica._idMagazzino)
            else:
                self.id_magazzino_combobox.set_active(-1)
            self.id_magazzino_combobox.grab_focus()


    def clearRows(self):
        """
        Pulisce i campi per il trattamento e la conservazione delle righe
        """
        self._righe = []
        self._righe.append({})
        self._numRiga = 0
        self.modelRiga.clear()
        self._iteratorRiga = None
        self.nuovaRiga()


    def draw(self, cplx=False):
        """
        Costruisce la treevew e gli altri widget dell'interfaccia
        """
        treeview = self.righe_treeview
        rendererSx = gtk.CellRendererText()
        rendererDx = gtk.CellRendererText()
        rendererDx.set_property('xalign', 1)

        column = gtk.TreeViewColumn('Magazzino', rendererSx, text=0)
        column.set_sizing(GTK_COLUMN_GROWN_ONLY)
        column.set_clickable(False)
        column.set_resizable(True)
        column.set_expand(False)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Codice articolo', rendererSx, text=1)
        column.set_sizing(GTK_COLUMN_GROWN_ONLY)
        column.set_clickable(False)
        column.set_resizable(True)
        column.set_expand(False)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Descrizione', rendererSx, text=2)
        column.set_sizing(GTK_COLUMN_GROWN_ONLY)
        column.set_clickable(False)
        column.set_resizable(True)
        column.set_expand(True)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('% IVA', rendererDx, text=3)
        column.set_sizing(GTK_COLUMN_GROWN_ONLY)
        column.set_clickable(False)
        column.set_resizable(True)
        column.set_expand(False)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('U.M.', rendererSx, text=4)
        column.set_sizing(GTK_COLUMN_GROWN_ONLY)
        column.set_clickable(False)
        column.set_resizable(True)
        column.set_expand(False)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Multiplo', rendererSx, text=5)
        column.set_sizing(GTK_COLUMN_GROWN_ONLY)
        column.set_clickable(False)
        column.set_resizable(True)
        column.set_expand(False)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Listino', rendererSx, text=6)
        column.set_sizing(GTK_COLUMN_GROWN_ONLY)
        column.set_clickable(False)
        column.set_resizable(True)
        column.set_expand(False)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Quantita''', rendererDx, text=7)
        column.set_sizing(GTK_COLUMN_GROWN_ONLY)
        column.set_clickable(False)
        column.set_resizable(True)
        column.set_expand(False)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Prezzo lordo', rendererDx, text=8)
        column.set_sizing(GTK_COLUMN_GROWN_ONLY)
        column.set_clickable(False)
        column.set_resizable(True)
        column.set_expand(False)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Sconti', rendererSx, text=9)
        column.set_sizing(GTK_COLUMN_GROWN_ONLY)
        column.set_clickable(False)
        column.set_resizable(True)
        column.set_expand(False)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Prezzo netto', rendererDx, text=10)
        column.set_sizing(GTK_COLUMN_GROWN_ONLY)
        column.set_clickable(False)
        column.set_resizable(True)
        column.set_expand(False)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Totale', rendererDx, text=11)
        column.set_sizing(GTK_COLUMN_GROWN_ONLY)
        column.set_clickable(False)
        column.set_resizable(True)
        column.set_expand(False)
        treeview.append_column(column)

        fillComboboxOperazioni(self.id_operazione_combobox, 'movimento')
        fillComboboxMagazzini(self.id_magazzino_combobox)

        self.nuovaRiga()

        crit = setconf("Documenti", "ricerca_per")
        self.ricerca = crit
        if crit == 'codice':
            self.ricerca_criterio_combobox.set_active(0)
        elif crit == 'codice_a_barre':
            self.ricerca_criterio_combobox.set_active(1)
        elif crit == 'descrizione':
            self.ricerca_criterio_combobox.set_active(2)
        elif crit == 'codice_articolo_fornitore':
            self.ricerca_criterio_combobox.set_active(3)
        if not self.ricerca:
            self.ricerca_criterio_combobox.set_active(2)

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
        self.variazione_listini_button.connect('clicked',
                                               self.on_variazione_listini_button_clicked)
        self.storico_costi_button.connect('clicked',
                                          self.on_storico_costi_button_clicked)
        self.storico_listini_button.connect('clicked',
                                            self.on_storico_listini_button_clicked)
        self.edit_date_and_number_button.connect('clicked',
                                                 self.on_edit_date_and_number_button_clicked)

        #Castelletto iva
        rendererText = gtk.CellRendererText()

        column = gtk.TreeViewColumn('Aliquota I.V.A.', rendererText, text=0)
        column.set_sizing(GTK_COLUMN_GROWN_ONLY)
        column.set_clickable(False)
        column.set_resizable(True)
        column.set_expand(True)
        self.riepiloghi_iva_treeview.append_column(column)

        rendererText = gtk.CellRendererText()
        rendererText.set_property('xalign', 1)

        column = gtk.TreeViewColumn('Imponibile', rendererText, text=1)
        column.set_sizing(GTK_COLUMN_GROWN_ONLY)
        column.set_clickable(False)
        column.set_resizable(True)
        column.set_expand(True)
        self.riepiloghi_iva_treeview.append_column(column)

        column = gtk.TreeViewColumn('Imposta', rendererText, text=2)
        column.set_sizing(GTK_COLUMN_GROWN_ONLY)
        column.set_clickable(False)
        column.set_resizable(True)
        column.set_expand(True)
        self.riepiloghi_iva_treeview.append_column(column)

        model = gtk.ListStore(str, str, str)
        self.riepiloghi_iva_treeview.set_model(model)
        fillComboboxAliquoteIva(self.id_iva_customcombobox.combobox)
        self.id_iva_customcombobox.connect('clicked',
                                on_id_aliquota_iva_customcombobox_clicked)

    def on_id_operazione_combobox_changed(self, combobox):
        """
        Setta l'operazione sul movimento corrente
        """
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
        elif self._tipoPersonaGiuridica == "cliente":
            self.persona_giuridica_label.set_text('Cliente')
            self.id_persona_giuridica_customcombobox.setType(self._tipoPersonaGiuridica)
            self.id_persona_giuridica_customcombobox.set_sensitive(True)
            self.label_listino.set_property('visible', True)
            self.id_listino_customcombobox.set_property('visible', True)
            self.prz_lordo_label.set_text('Prezzo')
            self.prz_netto_label.set_text('Prezzo netto')
            self.codice_articolo_fornitore_label.set_property('visible', False)
            self.codice_articolo_fornitore_entry.set_property('visible', False)
        elif self._tipoPersonaGiuridica == "magazzino":
            fillComboboxMagazzini(self.id_magazzino_combobox_trasferimento)
            self.persona_giuridica_label.set_sensitive(False)
            self.id_persona_giuridica_customcombobox.set_sensitive(False)
            self.magazzino_label.set_property('visible', True)
            self.id_magazzino_combobox_trasferimento.set_property('visible', True)
            self.label_listino.set_property('visible', True)
            self.id_listino_customcombobox.set_property('visible', True)
            self.prz_lordo_label.set_text('Prezzo')
            self.prz_netto_label.set_text('Prezzo netto')
            self.codice_articolo_fornitore_label.set_property('visible', False)
            self.codice_articolo_fornitore_entry.set_property('visible', False)
        else:
            self.persona_giuridica_label.set_text('Cliente/Fornitore ?')
            self.id_persona_giuridica_customcombobox.set_sensitive(False)
            self.label_listino.set_property('visible', True)
            self.id_listino_customcombobox.set_property('visible', True)
            self.prz_lordo_label.set_text('Prezzo')
            self.prz_netto_label.set_text('Prezzo netto')
            self.codice_articolo_fornitore_label.set_property('visible', False)
            self.codice_articolo_fornitore_entry.set_property('visible', False)
        self.persona_giuridica_changed()
        self.data_movimento_entry.grab_focus()


    def persona_giuridica_changed(self):
        """
        Gestisce il cambiamento di persona giuridica
        """
        if self._tipoPersonaGiuridica == "cliente":
            self.refresh_combobox_listini()


    def on_id_magazzino_combobox_changed(self, combobox):
        """
        Gestisce il cambiamento di magazzino nella combobox
        """
        if self._loading:
            return

        self._righe[0]["idMagazzino"] = findIdFromCombobox(self.id_magazzino_combobox)
        magazzino = leggiMagazzino(self._righe[0]["idMagazzino"])
        self._righe[0]["magazzino"] = magazzino["denominazione"]
        self.refresh_combobox_listini()


    def refresh_combobox_listini(self):
        """
        Gestisce i listini nella combobox
        """
        if self._righe[0]["idArticolo"] is None:
            self.id_listino_customcombobox.combobox.clear
        else:
            fillComboboxListiniFiltrati(self.id_listino_customcombobox.combobox,
                                        self._righe[0]["idArticolo"],
                                        self._righe[0]["idMagazzino"],
                                        self.id_persona_giuridica_customcombobox.getId())

    def on_id_multiplo_customcombobox_button_clicked(self, widget, toggleButton):
        """
        FIXME
        """
        on_id_multiplo_customcombobox_clicked(widget, toggleButton, self._righe[0]["idArticolo"])

    def on_id_multiplo_customcombobox_changed(self, combobox):
        """
        FIXME
        """
        if self._loading:
            return

        self._righe[0]["idMultiplo"] = findIdFromCombobox(self.id_multiplo_customcombobox.combobox)
        multiplo = leggiMultiplo(self._righe[0]["idMultiplo"])
        self._righe[0]["multiplo"] = multiplo["denominazioneBreve"] + ' ( ' + str('%.2f' % multiplo["moltiplicatore"]) + ' X )'
        self._righe[0]["moltiplicatore"] = multiplo["moltiplicatore"]
        self.calcolaTotaleRiga()

    def on_id_listino_customcombobox_button_clicked(self, widget, toggleButton):
        """
        FIXME
        """
        on_id_listino_customcombobox_clicked(widget, toggleButton, self._righe[0]["idArticolo"], None)

    def on_id_listino_customcombobox_button_toggled(self, button):
        """
        FIXME
        """
        if button.get_property('active') is True:
            return

        self.refresh_combobox_listini()

    def on_id_listino_customcombobox_changed(self, combobox):
        """
        Gestisce la combo ( custom ) dei listini
        """
        if self._loading:
            return

        idListino = findIdFromCombobox(self.id_listino_customcombobox.combobox)
        idArticolo = self._righe[0]["idArticolo"]
        self.getPrezzoVenditaLordo(idListino, idArticolo)
        self.prezzo_lordo_entry.set_text(str(mN(self._righe[0]["prezzoLordo"])))
        self.on_show_totali_riga()

    def getPrezzoVenditaLordo(self, idListino, idArticolo):
        """
        Cerca il prezzo di vendita
        """
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
        """
        Calcola il prezzo netto dal prezzo lordo e dagli sconti
        """
        prezzoLordo = Decimal(str(self._righe[0]["prezzoLordo"]))
        prezzoNetto = Decimal(str(self._righe[0]["prezzoLordo"]))
        applicazione = self._righe[0]["applicazioneSconti"]
        sconti = self._righe[0]["sconti"]
        for s in sconti:
            if s["tipo"] == 'percentuale':
                if applicazione == 'scalare':
                    prezzoNetto = prezzoNetto * (1 - Decimal(s["valore"]) / 100)
                elif applicazione == 'non scalare':
                    prezzoNetto = prezzoNetto - prezzoLordo * Decimal(s["valore"]) / 100
            elif s["tipo"] == 'valore':
                prezzoNetto = prezzoNetto - Decimal(s["valore"])
        self._righe[0]["prezzoNetto"] = prezzoNetto

    def getTotaleRiga(self):
        """
        Calcola il totale della riga
        FIXME: verificare i float e portarlo ai Decimal
        """
        segnoIva = 1
        percentualeIva = Decimal(self._righe[0]["percentualeIva"])
        prezzoNetto = Decimal(self._righe[0]["prezzoNetto"])
        quantita = Decimal(self._righe[0]["quantita"])
        moltiplicatore = Decimal(self._righe[0]["moltiplicatore"])
        self._righe[0]["totale"] = prezzoNetto * quantita * moltiplicatore

    def on_sconti_widget_button_toggled(self, button):
        """
        Apre il custom widget degli sconti
        """
        if button.get_property('active') is True:
            return

        self._righe[0]["sconti"] = self.sconti_widget.getSconti()
        self._righe[0]["applicazioneSconti"] = self.sconti_widget.getApplicazione()
        self.on_show_totali_riga()

    def on_notebook_switch_page(self, notebook, page, page_num):
        """
        Gestisce il cambio di pagina nel notebook
        """
        if page_num == 2:
            self.calcolaTotale()

    def _refresh(self):
        """
        Riporta i valori corretti, carica all'inizio e rinfresca dopo alcune
        operazioni
        """
        self._loading = True
        self._tipoPersonaGiuridica = None
        self._operazione = None
        self._fonteValore = None
        self._segno = None

        self.data_movimento_entry.set_sensitive(self.dao.id is None)
        self.edit_date_and_number_button.set_sensitive(self.dao.id is not None)
        self.numero_movimento_entry.set_sensitive(False)

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
        elif self._tipoPersonaGiuridica == "cliente":
            self.id_persona_giuridica_customcombobox.setId(self.dao.id_cliente)
        elif self._tipoPersonaGiuridica == "magazzino":
            findComboboxRowFromId(self.id_magazzino_combobox_trasferimento, self.dao.id_to_magazzino)
        self.data_movimento_entry.set_text(dateToString(self.dao.data_movimento))
        self.numero_movimento_entry.set_text(str(self.dao.numero or '0'))
        self.showDatiDocumento()

        textBuffer = self.note_interne_textview.get_buffer()
        if self.dao.note_interne is not None:
            textBuffer.set_text(self.dao.note_interne)
        else:
            textBuffer.set_text('')
        self.note_interne_textview.set_buffer(textBuffer)

        self.clearRows()

        for riga in self.dao.righe:
            self.azzeraRiga(0)
            j = self.dao.righe.index(riga) + 1
            magazzino = leggiMagazzino(riga.id_magazzino)
            articolo = leggiArticolo(riga.id_articolo)
            listino = leggiListino(riga.id_listino)
            multiplo = leggiMultiplo(riga.id_multiplo)
            (sconti, applicazione) = getScontiFromDao(riga.sconti, riga.applicazione_sconti)

            self._righe[0]["idRiga"] = riga.id
            self._righe[0]["idMagazzino"] = riga.id_magazzino
            self._righe[0]["magazzino"] = magazzino["denominazione"]
            self._righe[0]["idArticolo"] = riga.id_articolo
            self._righe[0]["codiceArticolo"] = articolo["codice"]
            self._righe[0]["descrizione"] = riga.descrizione


            idiva = None
            if riga.id_iva == None:
                if riga.id_articolo is not None:
                    #siamo di fronte ad un articolo "vecchio"
                    art = Articolo().getRecord(id=riga.id_articolo)
                    ivaart = art.id_aliquota_iva
                    daoiva = AliquotaIva().select(percentuale=riga.percentuale_iva)
                    if daoiva:
                        idiva = daoiva[0].id
                else:
                    if riga.percentuale_iva != 0:
                        #riga descrittiva
                        daoiva = AliquotaIva().select(percentuale=riga.percentuale_iva)
                        if daoiva:
                            idiva = daoiva[0].id
            else:
                idiva = riga.id_iva
            self._righe[0]["idAliquotaIva"] = idiva


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
            self.getTotaleRiga()
            if self._tipoPersonaGiuridica == "fornitore":
                fornitura = leggiFornitura(riga.id_articolo, self.dao.id_fornitore, self.dao.data_movimento, True)
                self._righe[0]["codiceArticoloFornitore"] = fornitura["codiceArticoloFornitore"]
            self._righe.append(self._righe[0])
            rigatomodel = self._righe[j]
            self.modelRiga.append((rigatomodel["magazzino"],
                                   rigatomodel["codiceArticolo"],
                                   rigatomodel["descrizione"],
                                   str(mN(rigatomodel["percentualeIva"],2)),
                                   rigatomodel["unitaBase"],
                                   rigatomodel["multiplo"],
                                   rigatomodel["listino"],
                                   str(mN(rigatomodel["quantita"],3)),
                                   str(mN(rigatomodel["prezzoLordo"])),
                                   self._righe[j]["applicazioneSconti"] + ' ' + getStringaSconti(rigatomodel["sconti"]),
                                   str(mN((rigatomodel["prezzoNetto"]))),
                                   str(mN(rigatomodel["totale"],2))))
        self.righe_treeview.set_model(self.modelRiga)
        self._loading = False
        self.calcolaTotale()
        self.label_numero_righe.set_text(str(len(self.dao.righe)))
        self.notebook.set_current_page(0)
        self.nuovaRiga()
        if self.dao.id is None or self.numero_movimento_entry.get_text() == '0':
            self.id_operazione_combobox.grab_focus()
        else:
            self.id_magazzino_combobox.grab_focus()

    def setDao(self, dao):
        """
        Inizializza un Dao nuovo se None o usa quello passato Dalla anag Filter
        """
        if dao is None:
            # Crea un nuovo Dao vuoto
            self.dao = TestataMovimento()
            # Suggerisce la data odierna
            self.dao.data_movimento = datetime.datetime.today()
            try:
                cli = setconf("Documenti", "cliente_predefinito")
                if cli:
                    self.dao.id_cliente = int(cli)
                    self.oneshot = True
                    self.articolo_entry.grab_focus()
            except:
                pass
            try:
                forn = setconf("Documenti", "fornitore_predefinito")
                if forn:
                    self.dao.id_fornitore = int(forn)
                    self.oneshot = True
                    self.articolo_entry.grab_focus()
            except:
                pass
        else:
            # Ricrea il Dao con una connessione al DBMS SQL
            self.dao = TestataMovimento().getRecord(id=dao.id)
        self._refresh()
        return self.dao

    def saveDao(self, tipo=None):
        """
        Salva il Dao nel Database
        """
        if not(len(self._righe) > 1):
            return

        if (self.data_movimento_entry.get_text() == ''):
            obligatoryField(self.dialogTopLevel,
                            self.data_movimento_entry,
                            'Inserire la data del documento !')

        if (findIdFromCombobox(self.id_operazione_combobox) is None):
            obligatoryField(self.dialogTopLevel,
                            self.id_operazione_combobox,
                            'Inserire il tipo di documento !')

        self.dao.data_movimento = stringToDate(self.data_movimento_entry.get_text())
        if self.dao.id is not None and self.numero_movimento_entry.get_text() != '0':
            self.dao.numero = self.numero_movimento_entry.get_text()

        self.dao.operazione = self._operazione
        pbar(self.dialog.pbar,parziale=1, totale=4)
        if self._tipoPersonaGiuridica == "fornitore":
            self.dao.id_fornitore = self.id_persona_giuridica_customcombobox.getId()
            self.dao.id_cliente = None
            self.dao.id_to_magazzino = None
        elif self._tipoPersonaGiuridica == "cliente":
            self.dao.id_cliente = self.id_persona_giuridica_customcombobox.getId()
            self.dao.id_fornitore = None
            self.dao.id_to_magazzino = None
        elif self._tipoPersonaGiuridica == "magazzino":
            self.dao.id_cliente = None
            self.dao.id_fornitore = None
            self.dao.id_to_magazzino = findIdFromCombobox(self.id_magazzino_combobox_trasferimento)
        textBuffer = self.note_interne_textview.get_buffer()
        self.dao.note_interne = textBuffer.get_text(textBuffer.get_start_iter(), textBuffer.get_end_iter(),True)
        righeMovimento = []
        scontiRigheMovimento= []
        #righe = []
        pbar(self.dialog.pbar,parziale=2, totale=4)
        for i in range(1, len(self._righe)):
            daoRiga = RigaMovimento()
            daoRiga.id_testata_movimento = self.dao.id
            daoRiga.id_articolo = self._righe[i]["idArticolo"]
            daoRiga.id_magazzino = self._righe[i]["idMagazzino"]
            daoRiga.descrizione = self._righe[i]["descrizione"]
            daoRiga.codiceArticoloFornitore = self._righe[i]["codiceArticoloFornitore"]
            daoRiga.id_listino = self._righe[i]["idListino"]
            daoRiga.id_iva = self._righe[i]["idAliquotaIva"]


            daoRiga.percentuale_iva = self._righe[i]["percentualeIva"]
            daoRiga.applicazione_sconti = self._righe[i]["applicazioneSconti"]
            daoRiga.quantita = self._righe[i]["quantita"]
            daoRiga.id_multiplo = self._righe[i]["idMultiplo"]
            daoRiga.moltiplicatore = self._righe[i]["moltiplicatore"]
            daoRiga.valore_unitario_lordo = self._righe[i]["prezzoLordo"]
            daoRiga.valore_unitario_netto = self._righe[i]["prezzoNetto"]

            sconti = []
            if self._righe[i]["sconti"] is not None:
                for j in range(0, len(self._righe[i]["sconti"])):
                    daoSconto = ScontoRigaMovimento()
                    daoSconto.valore = Decimal(self._righe[i]["sconti"][j]["valore"])
                    daoSconto.tipo_sconto = self._righe[i]["sconti"][j]["tipo"]
                    scontiRigheMovimento.append(daoSconto)
            #scontiRigheMovimento[daoRiga] = sconti

            daoRiga.scontiRigheMovimento = scontiRigheMovimento
            #righeMovimento[i] = daoRiga
            righeMovimento.append(daoRiga)
        pbar(self.dialog.pbar,parziale=3, totale=4)
        self.dao.righeMovimento = righeMovimento
        self.dao.persist()
        pbar(self.dialog.pbar,parziale=4, totale=4)
        self.label_numero_righe.hide()
        text = str(len(self.dao.righe))
        self.label_numero_righe.set_text(text)
        self.label_numero_righe.show()
        pbar(self.dialog.pbar,stop=True)

    def on_righe_treeview_row_activated(self, treeview, path, column):
        """
        Riporta la riga selezionata in primo piano per la modifica
        """
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
        self._righe[0]["quantita"] = mN(self._righe[self._numRiga]["quantita"],3)
        self._righe[0]["moltiplicatore"] = mN(self._righe[self._numRiga]["moltiplicatore"],2)
        self._righe[0]["prezzoLordo"] = mN(self._righe[self._numRiga]["prezzoLordo"])
        self._righe[0]["percentualeIva"] = mN(self._righe[self._numRiga]["percentualeIva"],2)
        self._righe[0]["idAliquotaIva"] = self._righe[self._numRiga]["idAliquotaIva"]
        self._righe[0]["applicazioneSconti"] = self._righe[self._numRiga]["applicazioneSconti"]
        self._righe[0]["sconti"] = self._righe[self._numRiga]["sconti"]
        self._righe[0]["prezzoNetto"] = mN(self._righe[self._numRiga]["prezzoNetto"])
        self._righe[0]["totale"] = mN(self._righe[self._numRiga]["totale"],2)
        self._righe[0]["prezzoNettoUltimo"] = mN(self._righe[self._numRiga]["prezzoNettoUltimo"])

        findComboboxRowFromId(self.id_magazzino_combobox, self._righe[0]["idMagazzino"])
        fillComboboxMultipli(self.id_multiplo_customcombobox.combobox, self._righe[0]["idArticolo"], True)
        findComboboxRowFromId(self.id_multiplo_customcombobox.combobox, self._righe[0]["idMultiplo"])
        self.refresh_combobox_listini()
        findComboboxRowFromId(self.id_listino_customcombobox.combobox, self._righe[0]["idListino"])
        self.articolo_entry.set_text(self._righe[0]["codiceArticolo"])
        self.descrizione_entry.set_text(self._righe[0]["descrizione"])
        self.codice_articolo_fornitore_entry.set_text(self._righe[0]["codiceArticoloFornitore"])
        findComboboxRowFromId(self.id_iva_customcombobox.combobox, self._righe[0]["idAliquotaIva"])
        #self.percentuale_iva_entry.set_text(str(mN(self._righe[0]["percentualeIva"],2)))
        self.sconti_widget.setValues(self._righe[0]["sconti"], self._righe[0]["applicazioneSconti"], False)
        self.quantita_entry.set_text(str(mN(self._righe[0]["quantita"],3)))
        self.prezzo_lordo_entry.set_text(str(mN(self._righe[0]["prezzoLordo"])))
        self.prezzo_netto_label.set_text(str(mN(self._righe[0]["prezzoNetto"])))
        self.totale_riga_label.set_text(str(mN(self._righe[0]["totale"],2)))

        self._loading = False
        self.articolo_entry.grab_focus()


    def on_new_row_button_clicked(self, widget):
        """
        Gestisce l'evento di creazione di una nuova riga
        """
        self.nuovaRiga()


    def on_confirm_row_button_clicked(self, widget):
        """
        Memorizza la riga inserita o modificata
        """
        self._righe[0]["idMagazzino"] = findIdFromCombobox(self.id_magazzino_combobox)
        magazzino = leggiMagazzino(self._righe[0]["idMagazzino"])
        self._righe[0]["magazzino"] = magazzino["denominazione"]

        if (self.data_movimento_entry.get_text() == ''):
            self.showMessage('Inserire da data del movimento !')
            return

        if (findIdFromCombobox(self.id_operazione_combobox) is None):
            self.showMessage('Inserire il tipo di movimento !')
            return

        if ((self._righe[0]["idMagazzino"] is not None) and
            (self._righe[0]["idArticolo"] is None)):
            self.showMessage('Inserire l''articolo !')
            return

        if ((self._righe[0]["idArticolo"] is not None) and
            (self._righe[0]["idMagazzino"] is None)):
            self.showMessage('Inserire il magazzino !')
            return
        self.on_show_totali_riga()
        costoVariato = (self._tipoPersonaGiuridica == "fornitore" and self._righe[0]["idArticolo"] is not None and
                        (Decimal(self._righe[0]["prezzoNetto"]) != Decimal(self._righe[0]["prezzoNettoUltimo"])))

        if self._numRiga == 0:
            self._numRiga = len(self._righe)
            self._righe.append(self._righe[0])
            inserisci = True
        else:
            inserisci = False

        # memorizzazione delle parti descrittive (liberamente modificabili)
        self._righe[0]["descrizione"] = self.descrizione_entry.get_text()
        self._righe[0]["codiceArticoloFornitore"] = self.codice_articolo_fornitore_entry.get_text()

        self._righe[self._numRiga]["idRiga"] = self._righe[0]["idRiga"]
        self._righe[self._numRiga]["idMagazzino"] = self._righe[0]["idMagazzino"]
        self._righe[self._numRiga]["magazzino"] = self._righe[0]["magazzino"]
        self._righe[self._numRiga]["idArticolo"] = self._righe[0]["idArticolo"]
        self._righe[self._numRiga]["codiceArticolo"] = self._righe[0]["codiceArticolo"]
        self._righe[self._numRiga]["descrizione"] = self._righe[0]["descrizione"]
        self._righe[self._numRiga]["codiceArticoloFornitore"] = self._righe[0]["codiceArticoloFornitore"]
        self._righe[self._numRiga]["percentualeIva"] = mN(self._righe[0]["percentualeIva"],2)
        self._righe[self._numRiga]["idAliquotaIva"] = self._righe[0]["idAliquotaIva"]
        self._righe[self._numRiga]["idUnitaBase"] = self._righe[0]["idUnitaBase"]
        self._righe[self._numRiga]["unitaBase"] = self._righe[0]["unitaBase"]
        self._righe[self._numRiga]["idMultiplo"] = self._righe[0]["idMultiplo"]
        self._righe[self._numRiga]["multiplo"] = self._righe[0]["multiplo"]
        self._righe[self._numRiga]["idListino"] = self._righe[0]["idListino"]
        self._righe[self._numRiga]["listino"] = self._righe[0]["listino"]
        self._righe[self._numRiga]["quantita"] = mN(self._righe[0]["quantita"],3)
        self._righe[self._numRiga]["moltiplicatore"] = mN(self._righe[0]["moltiplicatore"],2)
        self._righe[self._numRiga]["prezzoLordo"] = mN(self._righe[0]["prezzoLordo"])
        self._righe[self._numRiga]["applicazioneSconti"] = self._righe[0]["applicazioneSconti"]
        self._righe[self._numRiga]["sconti"] = self._righe[0]["sconti"]
        self._righe[self._numRiga]["prezzoNetto"] = mN(self._righe[0]["prezzoNetto"])
        self._righe[self._numRiga]["totale"] = mN(self._righe[0]["totale"],2)
        if not inserisci:
            if self._iteratorRiga is None:
                return
            self.modelRiga.set_value(self._iteratorRiga, 0, self._righe[self._numRiga]["magazzino"])
            self.modelRiga.set_value(self._iteratorRiga, 1, self._righe[self._numRiga]["codiceArticolo"])
            self.modelRiga.set_value(self._iteratorRiga, 2, self._righe[self._numRiga]["descrizione"])
            self.modelRiga.set_value(self._iteratorRiga, 3, mN(self._righe[self._numRiga]["percentualeIva"],2))
            self.modelRiga.set_value(self._iteratorRiga, 4, self._righe[self._numRiga]["unitaBase"])
            self.modelRiga.set_value(self._iteratorRiga, 5, self._righe[self._numRiga]["multiplo"])
            self.modelRiga.set_value(self._iteratorRiga, 6, self._righe[self._numRiga]["listino"])
            self.modelRiga.set_value(self._iteratorRiga, 7, mN(self._righe[self._numRiga]["quantita"],3))
            self.modelRiga.set_value(self._iteratorRiga, 8, mN(self._righe[self._numRiga]["prezzoLordo"]))
            self.modelRiga.set_value(self._iteratorRiga, 9, self._righe[self._numRiga]["applicazioneSconti"] + ' ' + getStringaSconti(self._righe[self._numRiga]["sconti"]))
            self.modelRiga.set_value(self._iteratorRiga, 10, mN(self._righe[self._numRiga]["prezzoNetto"]))
            self.modelRiga.set_value(self._iteratorRiga, 11, mN(self._righe[self._numRiga]["totale"],2))
        else:
            self.modelRiga.append((self._righe[self._numRiga]["magazzino"],
                                   self._righe[self._numRiga]["codiceArticolo"],
                                   self._righe[self._numRiga]["descrizione"],
                                   str(mN(self._righe[self._numRiga]["percentualeIva"],2)),
                                   self._righe[self._numRiga]["unitaBase"],
                                   self._righe[self._numRiga]["multiplo"],
                                   self._righe[self._numRiga]["listino"],
                                   str(mN(self._righe[self._numRiga]["quantita"],3)),
                                   str(mN(self._righe[self._numRiga]["prezzoLordo"])),
                                   self._righe[self._numRiga]["applicazioneSconti"] + ' ' + getStringaSconti(self._righe[self._numRiga]["sconti"]),
                                   str(mN(self._righe[self._numRiga]["prezzoNetto"])),
                                   str(mN(self._righe[self._numRiga]["totale"],2))))
        self.calcolaTotale()

        if costoVariato:
            msg = "Il prezzo di acquisto e' stato variato:\n si desidera aggiornare i listini di vendita ?"
            if YesNoDialog(msg=msg, transient=self.dialogTopLevel):
                self.on_variazione_listini_button_clicked(self.variazione_listini_button)
        self._righe[self._numRiga]["prezzoNettoUltimo"] = mN(self._righe[0]["prezzoNetto"])
        self.nuovaRiga()


    def on_undo_row_button_clicked(self, widget):
        """
        Annulla l'inserimento o la modifica della riga in primo piano
        """
        self.nuovaRiga()


    def on_delete_row_button_clicked(self, widget):
        """
        Elimina la riga in primo piano
        """
        if not(self._numRiga == 0):
            del(self._righe[self._numRiga])
            self.modelRiga.remove(self._iteratorRiga)
        self.calcolaTotale()
        self.nuovaRiga()

    def on_ricerca_codice_button_clicked(self, widget):
        """
        Imposta la ricerca per codice Articolo
        """
        if self.ricerca_codice_button.get_active():
            self.ricercaArticolo()


    def on_ricerca_codice_a_barre_button_clicked(self, widget):
        """
        Imposta la ricerca per codice a barre
        """
        if self.ricerca_codice_a_barre_button.get_active():
            self.ricercaArticolo()


    def on_ricerca_descrizione_button_clicked(self, widget):
        """
        Imposta la ricerca per Descrizione
        """
        if self.ricerca_descrizione_button.get_active():
            self.ricercaArticolo()


    def on_ricerca_codice_articolo_fornitore_button_clicked(self, widget):
        """
        Imposta la ricerca per codice Articolo fornitore
        """
        if self.ricerca_codice_articolo_fornitore_button.get_active():
            self.ricercaArticolo()



    def on_search_row_button_clicked(self, widget):
        """
        FIXME
        """
        self.ricercaArticolo()


    def ricercaArticolo(self):
        def on_ricerca_articolo_hide(anagWindow, anag):
            if anag.dao is None:
                anagWindow.destroy()
                return

            anagWindow.destroy()
            self.mostraArticolo(anag.dao.id)

        if (self.data_movimento_entry.get_text() == ''):
            messageInfo(_('Inserire la data del documento !'))
            return

        if findIdFromCombobox(self.id_operazione_combobox) is None:
            messageInfo(_('Inserire il tipo di documento !'))
            return

        if (findIdFromCombobox(self.id_magazzino_combobox) is None):
            messageInfo(_('Inserire il magazzino !'))
            return

        codice = None
        codiceABarre = None
        denominazione = None
        codiceArticoloFornitore = None
        join = None
        orderBy = None
        if self.ricerca_criterio_combobox.get_active() == 0:
            codice = self.articolo_entry.get_text()
            if Environment.tipo_eng =="sqlite":
                orderBy = "articolo.codice"
            else:
                orderBy = Environment.params["schema"]+".articolo.codice"
                batchSize = setconf("Numbers", "batch_size")
        elif self.ricerca_criterio_combobox.get_active() == 1:
            codiceABarre = self.articolo_entry.get_text()
            join= Articolo.cod_barre
            if Environment.tipo_eng =="sqlite":
                orderBy = "codice_a_barre_articolo.codice"
            else:
                orderBy = Environment.params["schema"]+".codice_a_barre_articolo.codice"
            batchSize = setconf("Numbers", "batch_size")
        elif self.ricerca_criterio_combobox.get_active() == 2:
            denominazione = self.articolo_entry.get_text()
            if Environment.tipo_eng =="sqlite":
                orderBy = "articolo.denominazione"
            else:
                orderBy = Environment.params["schema"]+".articolo.denominazione"
            batchSize = setconf("Numbers", "batch_size")
        elif self.ricerca_criterio_combobox.get_active() == 3:
            codiceArticoloFornitore = self.articolo_entry.get_text()
            join= Articolo.fornitur
            if Environment.tipo_eng =="sqlite":
                orderBy = "fornitura.codice_articolo_fornitore"
            else:
                orderBy = Environment.params["schema"]+".fornitura.codice_articolo_fornitore"
        batchSize = setconf("Numbers", "batch_size")
        if self.articolo_matchato:
            arts = [self.articolo_matchato]
        else:
            arts = Articolo().select(codiceEM=prepareFilterString(codice),
                                        orderBy=orderBy,
                                        join = join,
                                        denominazione=prepareFilterString(denominazione),
                                        codiceABarre=prepareFilterString(codiceABarre),
                                        codiceArticoloFornitore=prepareFilterString(codiceArticoloFornitore),
                                        idFamiglia=None,
                                        idCategoria=None,
                                        idStato=None,
                                        offset=None,
                                        batchSize=None)
        if (len(arts) == 1):
            self.mostraArticolo(arts[0].id)
            self.articolo_matchato = None
        else:
            from promogest.ui.RicercaComplessaArticoli import RicercaComplessaArticoli
            anag = RicercaComplessaArticoli(denominazione=denominazione,
                                            codice=codice,
                                            codiceABarre=codiceABarre,
                                            codiceArticoloFornitore=codiceArticoloFornitore)
            anag.setTreeViewSelectionType(GTK_SELECTIONMODE_SINGLE)

            anagWindow = anag.getTopLevel()
            anagWindow.connect("hide",
                               on_ricerca_articolo_hide,
                               anag)
            anagWindow.set_transient_for(self.dialogTopLevel)
            anag.show_all()
        self.cplx=False





    def mostraArticolo(self, id):
        """
        Riempie l'interfaccia con i dati relativi all'articolo
        """
        self.articolo_entry.set_text('')
        self.descrizione_entry.set_text('')
        self.codice_articolo_fornitore_entry.set_text('')
        #self.percentuale_iva_entry.set_text('')
        self.id_iva_customcombobox.combobox.set_active(-1)
        self.id_multiplo_customcombobox.combobox.clear()
        self.id_listino_customcombobox.combobox.clear()
        self.prezzo_lordo_entry.set_text('0')
        self.quantita_entry.set_text('0')
        self.prezzo_netto_label.set_text('0')
        self.sconti_widget.clearValues()

        self._righe[0]["idArticolo"] = None
        self._righe[0]["codiceArticolo"] = ''
        self._righe[0]["descrizione"] = ''
        self._righe[0]["codiceArticoloFornitore"] = ''
        self._righe[0]["percentualeIva"] = 0
        self._righe[0]["idAliquotaIva"] = None
        self._righe[0]["idUnitaBase"] = None
        self._righe[0]["idMultiplo"] = None
        self._righe[0]["moltiplicatore"] = 1
        self._righe[0]["idListino"] = None
        self._righe[0]["prezzoLordo"] = 0
        self._righe[0]["prezzoNetto"] = 0
        self._righe[0]["sconti"] = []
        self._righe[0]["applicazioneSconti"] = 'scalare'
        data = stringToDate(self.data_movimento_entry.get_text())

        fillComboboxMultipli(self.id_multiplo_customcombobox.combobox, id, True)

        if id is not None:
            articolo = leggiArticolo(id)
            self._righe[0]["idArticolo"] = id
            self._righe[0]["codiceArticolo"] = articolo["codice"]
            self._righe[0]["descrizione"] = articolo["denominazione"]
            self._righe[0]["percentualeIva"] = mN(articolo["percentualeAliquotaIva"],2)
            self._righe[0]["idAliquotaIva"] = articolo["idAliquotaIva"]
            findComboboxRowFromId(self.id_iva_customcombobox.combobox,self._righe[0]["idAliquotaIva"])
            self._righe[0]["idUnitaBase"] = articolo["idUnitaBase"]
            self._righe[0]["unitaBase"] = articolo["unitaBase"]
            self._righe[0]["idMultiplo"] = None
            self._righe[0]["moltiplicatore"] = 1
            self._righe[0]["prezzoLordo"] = 0
            self._righe[0]["prezzoNetto"] = 0
            self._righe[0]["sconti"] = []
            self._righe[0]["applicazioneSconti"] = 'scalare'
            self._righe[0]["codiceArticoloFornitore"] = ''

            if ((self._fonteValore == "acquisto_iva") or
                (self._fonteValore == "acquisto_senza_iva")):
                fornitura = leggiFornitura(id, self.id_persona_giuridica_customcombobox.getId(), data)
                costoLordo = fornitura["prezzoLordo"]
                costoNetto = fornitura["prezzoNetto"]
                if self._fonteValore == "acquisto_iva":
                    costoLordo = calcolaPrezzoIva(costoLordo, self._righe[0]["percentualeIva"])
                    costoNetto = calcolaPrezzoIva(costoNetto, self._righe[0]["percentualeIva"])
                self._righe[0]["prezzoLordo"] = costoLordo
                self._righe[0]["prezzoNettoUltimo"] = costoNetto
                self._righe[0]["sconti"] = fornitura["sconti"]
                self._righe[0]["applicazioneSconti"] = fornitura["applicazioneSconti"]
                self._righe[0]["codiceArticoloFornitore"] = fornitura["codiceArticoloFornitore"]
            elif ((self._fonteValore == "vendita_iva") or
                  (self._fonteValore == "vendita_senza_iva")):
                self.refresh_combobox_listini()

        self.articolo_entry.set_text(self._righe[0]["codiceArticolo"])
        self.descrizione_entry.set_text(self._righe[0]["descrizione"])

        #self.percentuale_iva_entry.set_text(str(self._righe[0]["percentualeIva"]))
        #self._righe[0]["percentualeIva"] = mN(articolo["percentualeAliquotaIva"],2)

        self._righe[0]["idAliquotaIva"] = articolo["idAliquotaIva"]
        findComboboxRowFromId(self.id_iva_customcombobox.combobox,self._righe[0]["idAliquotaIva"])
        self.codice_articolo_fornitore_entry.set_text(self._righe[0]["codiceArticoloFornitore"])
        self.prezzo_lordo_entry.set_text(str(self._righe[0]["prezzoLordo"]))
        self.on_show_totali_riga()
        if self._tipoPersonaGiuridica == "cliente":
            self.id_listino_customcombobox.combobox.grab_focus()
        elif self._tipoPersonaGiuridica == "fornitore":
            self.codice_articolo_fornitore_entry.grab_focus()
        else:
            self.descrizione_entry.grab_focus()

    def on_totale_spinbutton_focus_out_event(self, spinbutton, event):
        """
        Gestisce il totale Arbitrario per modifica "rosas"
        """
        self.quantita_entry.grab_focus()
        self.quantita_entry.set_text("")

    def on_show_totali_riga(self, widget = None, event = None):
        """
        Calcola il prezzo netto
        """
        quantita = mN(self.quantita_entry.get_text(),3) or 0
        self._righe[0]["quantita"] = quantita
        self._righe[0]["prezzoLordo"] = float(self.prezzo_lordo_entry.get_text() or 0)
        iva = findStrFromCombobox(self.id_iva_customcombobox.combobox,0)
        if iva and type(iva) != type("CIAO"):
            self._righe[0]["percentualeIva"] = mN(iva.percentuale,0) or 0
            self._righe[0]["idAliquotaIva"] = iva.id or None
        else:
            self._righe[0]["percentualeIva"] =  0
            self._righe[0]["idAliquotaIva"] = None


        #self._righe[0]["percentualeIva"] = mN(self.percentuale_iva_entry.get_text(),2) or 0
        self._righe[0]["applicazioneSconti"] = self.sconti_widget.getApplicazione()
        self._righe[0]["prezzoNetto"] = self._righe[0]["prezzoLordo"]
        self._righe[0]["sconti"] = self.sconti_widget.getSconti()
        self._righe[0]["applicazioneSconti"] = self.sconti_widget.getApplicazione()

        self.getPrezzoNetto()
        self.prezzo_netto_label.set_text(str(mN(self._righe[0]["prezzoNetto"])))
        self.calcolaTotaleRiga()
        return False


    def calcolaTotaleRiga(self):
        """
        Calcola il totale riga
        """
        if self._righe[0]["prezzoNetto"] is None:
            self._righe[0]["prezzoNetto"] = 0
        if self._righe[0]["quantita"] is None:
            self._righe[0]["quantita"] = 0
        if self._righe[0]["moltiplicatore"] is None:
            self._righe[0]["moltiplicatore"] = 1
        elif mN(self._righe[0]["moltiplicatore"],2) == 0:
            self._righe[0]["moltiplicatore"] = 1

        self.getTotaleRiga()
        self.totale_riga_label.set_text(str(mN(self._righe[0]["totale"],2)))


    def calcolaTotale(self):
        """
        Calcola i totali movimento
        """
        totaleImponibile = Decimal(0)
        totaleImposta = Decimal(0)
        totaleNonScontato = Decimal(0)

        castellettoIva = {}

        for riga in self._righe[1:]:
            prezzoNetto = mN(riga["prezzoNetto"])
            quantita = mN(riga["quantita"],3)
            moltiplicatore = Decimal(riga["moltiplicatore"])
            percentualeIva = Decimal(riga["percentualeIva"])
            idAliquotaIva = riga["idAliquotaIva"]
            daoiva=None
            if idAliquotaIva:
                daoiva = AliquotaIva().getRecord(id=idAliquotaIva)
            totaleRiga = prezzoNetto * quantita * moltiplicatore

            percentualeIvaRiga = percentualeIva

            if (self._fonteValore == "vendita_iva" or
                self._fonteValore == "acquisto_iva"):
                totaleImponibileRiga = calcolaPrezzoIva(totaleRiga, -1 * percentualeIvaRiga)
            else:
                totaleImponibileRiga = mN(totaleRiga,2)
                totaleRiga = calcolaPrezzoIva(totaleRiga, percentualeIvaRiga)

            totaleRiga = mN(totaleRiga, 2)
            totaleImponibileRiga = mN(totaleImponibileRiga, 2)

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

        self.totale_generale_label.set_text(str(mN(totaleNonScontato,2)))
        self.totale_generale_riepiloghi_label.set_text(str(mN(totaleNonScontato,2)))
        self.totale_imponibile_label.set_text(str(mN(totaleImponibile,2)))
        self.totale_imponibile_riepiloghi_label.set_text(str(mN(totaleImponibile,2)))
        self.totale_imposta_label.set_text(str(mN(totaleImposta,2)))
        self.totale_imposta_riepiloghi_label.set_text(str(mN(totaleImposta,2)))

        model = self.riepiloghi_iva_treeview.get_model()
        model.clear()
        for k in castellettoIva.keys():
            model.append((str(mN(k,2)),
                         str(mN(castellettoIva[k]['imponibile'],2)),
                         str(mN(castellettoIva[k]['imposta'],2))))


    def showMessage(self, msg):
        """
        Generico dialog di messaggio
        """
        messageInfo(msg=msg, transient=self.dialogTopLevel)


    def on_storico_costi_button_clicked(self, toggleButton):
        """
        FIXME
        """
        from promogest.ui.StoricoForniture import StoricoForniture
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
        """
        FIXME
        """
        from promogest.ui.StoricoListini import StoricoListini
        idArticolo = self._righe[0]["idArticolo"]

        anag = StoricoListini(idArticolo)

        anagWindow = anag.getTopLevel()
        anagWindow.set_transient_for(self.dialogTopLevel)
        anagWindow.show_all()


    def on_variazione_listini_button_clicked(self, toggleButton):
        """
        Apre l'interfaccia di variazione listino
        """
        if self._righe[0]["idArticolo"] is None:
            self.showMessage('Selezionare un articolo !')
            return

        from promogest.ui.VariazioneListini import VariazioneListini
        idArticolo = self._righe[0]["idArticolo"]
        costoNuovo = None
        costoUltimo = None
        if self._tipoPersonaGiuridica == "fornitore":
            costoNuovo = mN(self._righe[0]["prezzoNetto"])
            costoUltimo = mN(self._righe[0]["prezzoNettoUltimo"])
        anag = VariazioneListini(idArticolo, costoUltimo, costoNuovo)
        anagWindow = anag.getTopLevel()
        anagWindow.set_transient_for(self.dialogTopLevel)
        anagWindow.show_all()


    def on_edit_date_and_number_button_clicked(self, toggleButton):
        """
        FIXME
        """
        msg = 'Attenzione! Si sta per variare i riferimenti primari del movimento.\n Continuare ?'
        if YesNoDialog(msg=msg, transient=self.dialogTopLevel):
            self.data_movimento_entry.set_sensitive(True)
            self.numero_movimento_entry.set_sensitive(True)
            self.data_movimento_entry.grab_focus()
            self.id_persona_giuridica_customcombobox.set_sensitive(True)

    def showDatiDocumento(self):
        """
        Mostra ', se presente una eventuale relazione con un Documento in archivio
        """
        stringLabel = '-'
        if self.dao.id_testata_documento is not None:
            res = TestataDocumento().getRecord(id = self.dao.id_testata_documento)
            if res:
                stringLabel = 'N.' + str(res.numero) + ' del ' + dateToString(res.data_documento)

        self.rif_documento_label.set_text(stringLabel)

    def on_articolo_entry_insert_text(self, text):
        # assegna il valore della casella di testo alla variabile
        stringa = text.get_text()
        if self.mattu:
            text.set_text(stringa.split(self.sepric)[0])
        #model = gtk.ListStore(str,object)
        #vediamo = self.completion.get_model()
        #vediamo.clear()
        self.ricerca_art_listore.clear()
        art = []
        # evita la ricerca per stringhe vuote o più corte di due caratteri
        if stringa ==[] or len(stringa)<2:
            return
        if self.ricerca == "codice":
            if len(text.get_text()) <3:
                art = Articolo().select(codice=stringa,cancellato=True, batchSize=20)
            else:
                art = Articolo().select(codice=stringa,cancellato=True, batchSize=50)
        elif self.ricerca == "descrizione":
            if len(text.get_text()) <3:
                art = Articolo().select(denominazione=stringa,cancellato=True, batchSize=20)
            else:
                art = Articolo().select(denominazione=stringa,cancellato=True, batchSize=50)
        elif self.ricerca == "codice_a_barre":
            if len(text.get_text()) <7:
                art = Articolo().select(codiceABarre=stringa,cancellato=True, batchSize=10)
            else:
                art = Articolo().select(codiceABarre=stringa,cancellato=True, batchSize=40)
        elif self.ricerca == "codice_articolo_fornitore_button":
            if len(text.get_text()) <3:
                art = Articolo().select(codiceArticoloFornitore=stringa,cancellato=True, batchSize=10)
            else:
                art = Articolo().select(codiceArticoloFornitore=stringa,cancellato=True, batchSize=40)
        for m in art:
            codice_art = m.codice
            den = m.denominazione
            bloccoInformazioni = codice_art+self.sepric+den
            compl_string = bloccoInformazioni
            if self.ricerca == "codice_articolo_fornitore":
                caf = m.codice_articolo_fornitore
                compl_string = bloccoInformazioni+self.sepric+caf
            if self.ricerca == "codice_a_barre":
                cb = m.codice_a_barre
                compl_string = bloccoInformazioni+self.sepric+cb
            self.ricerca_art_listore.append([compl_string,m])
        #self.completion.set_model(model)


    def match_func(self, completion, key, iter):
        model = self.completion.get_model()
        self.mattu = False
        self.articolo_matchato = None
        if model[iter][0] and self.articolo_entry.get_text().lower() in model[iter][0].lower():
            return model[iter][0]
        else:
            return None

    def on_completion_match(self, completion=None, model=None, iter=None):
        self.mattu = True
        self.articolo_matchato = model[iter][1]
        self.articolo_entry.set_position(-1)

    def on_ricerca_criterio_combobox_changed(self, combobox):
        if combobox.get_active() ==0:
            self.ricerca = "codice"
        elif combobox.get_active() ==1:
            self.ricerca = "codice_a_barre"
        elif combobox.get_active() ==2:
            self.ricerca = "descrizione"
        elif combobox.get_active() == 3:
            self.ricerca = "codice_articolo_fornitore"

    def on_articolo_entry_key_press_event(self, widget, event):
        """ """
        keyname = gdk_keyval_name(event.keyval)
        if self.mattu and keyname == 'Return' or keyname == 'KP_Enter':
            self.ricercaArticolo()
        if keyname == 'F3':
            self.ricercaArticolo()
