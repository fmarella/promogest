# -*- coding: iso-8859-15 -*-

# Promogest
#
# Copyright (C) 2005 by Promotux Informatica - http://www.promotux.it/
# Author: Alessandro Scano <alessandro@promotux.it>
# Author: Francesco Meloni <francescoo@promotux.it>


from promogest.ui.utils import *

import gtk, gobject
import os, popen2
import gtkhtml2
import genshi
from genshi.template import TemplateLoader
from promogest.dao.DaoUtils import giacenzaSel
from datetime import datetime, timedelta
from promogest import Environment
from promogest.ui.GladeWidget import GladeWidget
import promogest.dao.TestataMovimento
from promogest.dao.TestataMovimento import TestataMovimento
import promogest.dao.RigaMovimento
from promogest.dao.RigaMovimento import RigaMovimento
import promogest.dao.ScontoRigaMovimento
from promogest.dao.ScontoRigaMovimento import ScontoRigaMovimento
#import promogest.modules.VenditaDettaglio.dao.TestataScontrino
from promogest.modules.VenditaDettaglio.dao.TestataScontrino import TestataScontrino
#import promogest.modules.VenditaDettaglio.dao.RigaScontrino
from promogest.modules.VenditaDettaglio.dao.RigaScontrino import RigaScontrino
#import promogest.modules.VenditaDettaglio.dao.ScontoRigaScontrino
from promogest.modules.VenditaDettaglio.dao.ScontoRigaScontrino import ScontoRigaScontrino
#import promogest.modules.VenditaDettaglio.dao.ChiusuraFiscale
from promogest.modules.VenditaDettaglio.dao.ChiusuraFiscale import ChiusuraFiscale
import promogest.dao.Articolo
from promogest.dao.Articolo import Articolo
import promogest.dao.CodiceABarreArticolo
from promogest.dao.CodiceABarreArticolo import CodiceABarreArticolo
import promogest.dao.AliquotaIva
from promogest.dao.AliquotaIva import AliquotaIva
#import promogest.dao.Listino
from promogest.dao.Magazzino import Magazzino
from promogest.dao.Listino import Listino
from promogest.dao.ListinoArticolo import ListinoArticolo
from promogest.ui.widgets.FilterWidget import FilterWidget
from promogest.dao.Dao import Dao

class AnagraficaVenditaDettaglio(GladeWidget):
    """ Frame per la gestione delle vendite a dettaglio """

    def __init__(self):
        GladeWidget.__init__(self, 'vendita_dettaglio_window',
                        fileName='promogest/modules/VenditaDettaglio/gui/vendita_dettaglio_window.glade',
                        isModule=True)
        self.placeWindow(self.getTopLevel())
        self._currentRow = {}
        self._simboloPercentuale = '%'
        self._simboloEuro = ''
        textStatusBar = "     *****   Promogest2 - Modulo Vendita Dettaglio - by Promotux Informatica - 800034561 - www.promotux.it - promogest.promotux.it  *****     "
        context_id =  self.vendita_dettaglio_statusbar.get_context_id("vendita_dettaglio_window")
        self.vendita_dettaglio_statusbar.push(context_id,textStatusBar)
        azienda = Azienda(id=Environment.params["schema"]).getRecord()
        self.logo_articolo.set_from_file(azienda.percorso_immagine)
        self.draw()



    def draw(self):
        accelGroup = gtk.AccelGroup()
        self.getTopLevel().add_accel_group(accelGroup)
        self.contanti_radio_button.add_accelerator('clicked', accelGroup, gtk.keysyms.F1, 0, gtk.ACCEL_VISIBLE)
        self.assegni_radio_button.add_accelerator('clicked', accelGroup, gtk.keysyms.F2, 0, gtk.ACCEL_VISIBLE)
        self.carta_di_credito_radio_button.add_accelerator('clicked', accelGroup, gtk.keysyms.F3, 0, gtk.ACCEL_VISIBLE)
        self.total_button.add_accelerator('grab_focus', accelGroup, gtk.keysyms.F5, 0, gtk.ACCEL_VISIBLE)
        self.total_button.set_focus_on_click(False)

        # Costruisco treeview scontrino
        self.modelRiga = gtk.ListStore(int, str, str, str, float, float, str, float, float)

        treeview = self.scontrino_treeview
        rendererSx = gtk.CellRendererText()
        rendererDx = gtk.CellRendererText()
        rendererDx.set_property('xalign', 1)

        column = gtk.TreeViewColumn('Codice a barre', rendererSx, text=1)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(False)
        column.set_resizable(True)
        column.set_expand(False)
        column.set_min_width(90)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Codice', rendererSx, text=2)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(False)
        column.set_resizable(True)
        column.set_expand(False)
        column.set_min_width(70)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Descrizione', rendererSx, text=3)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(False)
        column.set_resizable(True)
        column.set_expand(True)
        column.set_min_width(50)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Prezzo', rendererDx, text=4)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(False)
        column.set_resizable(True)
        column.set_expand(False)
        column.set_min_width(50)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Sconto', rendererDx, text=5)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(False)
        column.set_resizable(True)
        column.set_expand(False)
        column.set_min_width(50)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Tipo', rendererDx, text=6)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(False)
        column.set_resizable(True)
        column.set_expand(False)
        column.set_min_width(20)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Prezzo scontato', rendererDx, text=7)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(False)
        column.set_resizable(True)
        column.set_expand(False)
        column.set_min_width(50)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Quantita\'', rendererDx, text=8)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(False)
        column.set_resizable(True)
        column.set_expand(False)
        column.set_min_width(50)
        treeview.append_column(column)

        treeview.set_model(self.modelRiga)

        # Disabilito bottoni e text entry
        self.confirm_button.set_sensitive(False)
        self.delete_button.set_sensitive(False)
        self.rhesus_button.set_sensitive(False)
        self.annulling_button.set_sensitive(False)
        self.total_button.set_sensitive(False)
        self.empty_button.set_sensitive(False)

        self.setPagamento(enabled = False)


        #if Environment.taglia_colore:
            #self.new_button.set_no_show_all(True)
            #self.new_button.set_property('visible', False)

        self.codice_a_barre_entry.grab_focus()
        self._loading = False

        # Segnali
        treeViewSelection = self.scontrino_treeview.get_selection()
        treeViewSelection.connect('changed', self.on_scontrino_treeview_selection_changed)

        # Ricerca listino
        self.id_listino = self.ricercaListino()

        # Ricerca magazzino
        magalist = Magazzino(isList=True).select(denominazione = Environment.conf.VenditaDettaglio.magazzino,
                                                  offset = None,
                                                  batchSize = None)

        if len(magalist) > 0:
            self.id_magazzino = magalist[0].id
        else:
            self.id_magazzino = None

        self.prezzo_entry.connect('key_press_event',
                                  self.on_prezzo_entry_key_press_event)
        self.prezzo_scontato_entry.connect('key_press_event',
                                           self.on_prezzo_scontato_entry_key_press_event)
        self.quantita_entry.connect('key_press_event',
                                    self.on_quantita_entry_key_press_event)

        # Vado in stato di ricerca
        self._state = 'search'
        self.empty_current_row()


    def search_item(self, codiceABarre=None, codice=None):
        # Ricerca articolo per barcode

        if codiceABarre is not None:
            arts = Articolo(isList=True).select( codiceABarre = codiceABarre,
                                                 offset = None,
                                                 batchSize = None)
        else:
            arts = Articolo(isList=True).select( codice = codice,
                                                 offset = None,
                                                 batchSize = None)

        if len(arts) == 1:
            idArticolo = arts[0].id
            codice = arts[0].codice or ''
            codiceABarre = arts[0].codice_a_barre or ''
            descrizione = arts[0].descrizione_etichetta or arts[0].denominazione or ''
            # Ricerca listino_articolo
            listino = leggiListino(self.id_listino, idArticolo)
            prezzo = listino["prezzoDettaglio"]
            valoreSconto = 0
            tipoSconto = None
            prezzoScontato = prezzo
            quantita = 1

            self.codice_a_barre_entry.set_text(codiceABarre)
            self.codice_entry.set_text(codice)
            self.activate_item(idArticolo,
                               codiceABarre,
                               codice,
                               descrizione,
                               prezzo,
                               valoreSconto,
                               tipoSconto,
                               prezzoScontato,
                               quantita)
            self.confirm_button.grab_focus()
        else:
            self.ricercaArticolo()


    def on_search_button_clicked(self, button):
        self.ricercaArticolo()


    def on_codice_a_barre_entry_activate(self, text_entry):
        if self.codice_a_barre_entry.get_text() != '':
            self.search_item(codiceABarre = prepareFilterString(self.codice_a_barre_entry.get_text()))
        return True


    def on_codice_entry_activate(self,text_entry):
        if self.codice_entry.get_text() != '':
            self.search_item(codice = prepareFilterString(self.codice_entry.get_text()))
        return True

    def setDao(self, dao):
        if dao is None:
            # Crea un nuovo Dao vuoto
            self.dao = ListinoArticolo().getRecord()
        else:
            # Ricrea il Dao con una connessione al DBMS SQL
            self.dao = ListinoArticolo(isList=True).select(idListino=dao.id_listino,
                                                    idArticolo=dao.id_articolo,
                                                    orderBy="id_articolo")[0]
        self._refresh()

    def empty_current_row(self):
        self._currentRow['idArticolo'] = None
        self._currentRow['codiceABarre'] = None
        self._currentRow['codice'] = None
        self._currentRow['descrizione'] = None
        self._currentRow['prezzo'] = 0
        self._currentRow['valoreSconto'] = 0
        self._currentRow['tipoSconto'] = None
        self._currentRow['prezzoScontato'] = 0
        self._currentRow['quantita'] = 0

        self.codice_a_barre_entry.set_text('')
        self.codice_entry.set_text('')
        self.descrizione_label.set_text('')
        self.prezzo_entry.set_text('')
        self.sconto_entry.set_text('')
        self.prezzo_scontato_entry.set_text('')
        self.quantita_entry.set_text('')
        self.listini_combobox.clear()
        self.id_listino = self.ricercaListino()
        self.giacenza_label.set_text('-')


    def activate_item(self, idArticolo, codiceABarre, codice, denominazione, prezzo, valoreSconto, tipoSconto, prezzoScontato, quantita):
        self._loading = True

        fillComboboxListiniFiltrati(self.listini_combobox, idArticolo=idArticolo, idMagazzino=None, idCliente=None, filter=False)

        if self.id_listino is not None:
            findComboboxRowFromId(self.listini_combobox, self.id_listino)
        else:
            self.listini_combobox.set_active(1)
            try:
                self.id_listino = findIdFromCombobox(self.listini_combobox)
                if prezzo == 0:
                    listino = leggiListino(self.id_listino, idArticolo)
                    prezzo = listino["prezzoDettaglio"]
                    prezzoScontato = prezzo
                    valoreSconto = 0
            except:
                pass

        self._loading = False

        self.codice_a_barre_entry.set_text(codiceABarre)
        self.codice_entry.set_text(codice)
        self.descrizione_label.set_markup('<b>' + denominazione + '</b>')
        self.prezzo_entry.set_text(Environment.conf.number_format % prezzo)
        self.sconto_entry.tipoSconto = tipoSconto
        tipoScontoString = self.sconto_entry.getTipoScontoString()
        self.sconto_entry.set_text(Environment.conf.number_format % valoreSconto)
        if not(valoreSconto > 0):
            tipoScontoString = ''
        self.prezzo_scontato_entry.set_text(Environment.conf.number_format % prezzoScontato)
        self.quantita_entry.set_text(Environment.conf.number_format % quantita)
        self.confirm_button.set_sensitive(True)
        self.rhesus_button.set_sensitive(True)
        self.annulling_button.set_sensitive(True)
        listino = ListinoArticolo(Environment.connection)
        self.art = leggiArticolo(idArticolo)
        if listino.ultimo_costo is None:
            self.fornitura = leggiFornitura(idArticolo)
            self.ultimocostovalue_label.set_markup('<b>' + Environment.conf.number_format % float(self.fornitura["prezzoNetto"]) + '</b>')
        else:
            self.ultimocostovalue_label.set_markup('<b>' + Environment.conf.number_format % float(listino.ultimo_costo or 0) + '</b>')

        if prezzoScontato == prezzo:
            self.marginevalue_label.set_markup('<b>'+'%-6.3f' % calcolaMargine(float(self.fornitura["prezzoNetto"]),
                                                                   float(prezzo),
                                                                   float(self.art["percentualeAliquotaIva"]))+ '</b>')
        else:
            self.marginevalue_label.set_markup('<b>'+'%-6.3f' % calcolaMargine(float(self.fornitura["prezzoNetto"]),
                                                                   float(prezzoScontato),
                                                                   float(self.art["percentualeAliquotaIva"]))+ '</b>')
        giacenza = self.getGiacenzaArticolo(idArticolo=idArticolo)
        self.giacenza_label.set_markup('<b>' + Environment.conf.number_format % giacenza + '</b>')

        self._currentRow = {'idArticolo' : idArticolo
                           ,'codiceABarre' : codiceABarre
                           ,'codice' : codice
                           ,'descrizione' : denominazione
                           ,'prezzo' : prezzo
                           ,'valoreSconto' : valoreSconto
                           ,'tipoSconto' : tipoScontoString
                           ,'prezzoScontato':prezzoScontato
                           ,'quantita' : quantita}


    def on_listini_combobox_changed(self, combobox):
        if self._loading:
            return

        self.id_listino = findIdFromCombobox(self.listini_combobox)
        listino = leggiListino(self.id_listino, self._currentRow['idArticolo'])
        prezzo_dettaglio = listino["prezzoDettaglio"]
        self._currentRow['prezzo'] = prezzo_dettaglio
        self.prezzo_entry.set_text(Environment.conf.number_format % prezzo_dettaglio)


    def on_scontrino_treeview_selection_changed(self, treeSelection):
        (model, iterator) = treeSelection.get_selected()

        if iterator is not None:
            idArticolo = model.get_value(iterator, 0)
            codiceABarre = model.get_value(iterator, 1)
            codice = model.get_value(iterator, 2)
            denominazione = model.get_value(iterator, 3)
            prezzo = model.get_value(iterator, 4)
            valoreSconto = model.get_value(iterator, 5)
            tipoSconto = model.get_value(iterator, 6)
            if tipoSconto != self._simboloPercentuale:
                tipoSconto = 'valore'
            else:
                tipoSconto = 'percentuale'
            prezzoScontato = model.get_value(iterator, 7)
            quantita = model.get_value(iterator, 8)
            self.activate_item(idArticolo, codiceABarre, codice, denominazione, prezzo, valoreSconto, tipoSconto, prezzoScontato, quantita)

            # Abilito bottoni e text entry
            self.delete_button.set_sensitive(True)
            self.confirm_button.set_sensitive(True)
            self.rhesus_button.set_sensitive(True)
            self.annulling_button.set_sensitive(True)
            self.search_button.set_sensitive(False)
            self.codice_a_barre_entry.set_sensitive(False)
            self.codice_entry.set_sensitive(False)

            # Vado in editing
            self._state = 'editing'
            self.currentIteratorRow = iterator


    def on_confirm_button_clicked(self, button):
        # controllo che il prezzo non sia nullo
        if self._currentRow['prezzo'] == 0:
            dialog = gtk.MessageDialog(self.getTopLevel(),
                                       gtk.DIALOG_MODAL
                                       | gtk.DIALOG_DESTROY_WITH_PARENT,
                                       gtk.MESSAGE_WARNING, gtk.BUTTONS_OK)
            dialog.set_markup("<b>ATTENZIONE:\n</b>Inserire un prezzo all'articolo")
            response = dialog.run()
            dialog.destroy()
            self.prezzo_entry.grab_focus()
            return

        treeview = self.scontrino_treeview
        model = treeview.get_model()

        if self._state == 'search':
            model.append((self._currentRow['idArticolo'],
                          self._currentRow['codiceABarre'],
                          self._currentRow['codice'],
                          self._currentRow['descrizione'],
                          round(self._currentRow['prezzo'], int(Environment.conf.decimals)),
                          round(self._currentRow['valoreSconto'], int(Environment.conf.decimals)),
                          self._currentRow['tipoSconto'],
                          round(self._currentRow['prezzoScontato'], int(Environment.conf.decimals)),
                          round(self._currentRow['quantita'], int(Environment.conf.decimals))))
        elif self._state == 'editing':
            model.set_value(self.currentIteratorRow, 0, self._currentRow['idArticolo'])
            model.set_value(self.currentIteratorRow, 1, self._currentRow['codiceABarre'])
            model.set_value(self.currentIteratorRow, 2, self._currentRow['codice'])
            model.set_value(self.currentIteratorRow, 3, self._currentRow['descrizione'])
            model.set_value(self.currentIteratorRow, 4, round(self._currentRow['prezzo'],int(Environment.conf.Numbers.decimals)))
            model.set_value(self.currentIteratorRow, 5, round(self._currentRow['valoreSconto'],int(Environment.conf.Numbers.decimals)))
            model.set_value(self.currentIteratorRow, 6, self._currentRow['tipoSconto'])
            model.set_value(self.currentIteratorRow, 7, round(self._currentRow['prezzoScontato'],int(Environment.conf.Numbers.decimals)))
            model.set_value(self.currentIteratorRow, 8, round(self._currentRow['quantita'],int(Environment.conf.Numbers.decimals)))

        self.marginevalue_label.set_text('')
        self.ultimocostovalue_label.set_text('')
        self.empty_current_row()

        # Disabilito cancella e conferma e abilito ricerca barcode
        self.delete_button.set_sensitive(False)
        self.confirm_button.set_sensitive(False)
        self.rhesus_button.set_sensitive(False)
        self.annulling_button.set_sensitive(False)
        self.codice_a_barre_entry.set_sensitive(True)
        self.codice_entry.set_sensitive(True)

        self.search_button.set_sensitive(True)
        # Abilito pulsante totale e annulla
        notEmpty = (len(model) > 0)
        self.total_button.set_sensitive(notEmpty)
        self.empty_button.set_sensitive(notEmpty)
        self.setPagamento(enabled = notEmpty)

        # Calcolo totali
        self.refreshTotal()

        treeview.get_selection().unselect_all()

        # vado in search
        self._state = 'search'
        self.codice_a_barre_entry.grab_focus()


    def on_cancel_button_clicked(self, button):
        self.empty_current_row()

        # Disabilito cancella e conferma e abilito ricerca barcode
        self.delete_button.set_sensitive(False)
        self.confirm_button.set_sensitive(False)
        self.rhesus_button.set_sensitive(False)
        self.annulling_button.set_sensitive(False)
        self.codice_a_barre_entry.set_sensitive(True)
        self.codice_entry.set_sensitive(True)
        self.search_button.set_sensitive(True)

        treeview = self.scontrino_treeview
        model = treeview.get_model()

        # Abilito pulsante totale e annulla
        notEmpty = (len(model) > 0)
        self.total_button.set_sensitive(notEmpty)
        self.empty_button.set_sensitive(notEmpty)
        self.setPagamento(enabled = notEmpty)

        treeview.get_selection().unselect_all()

        # vado in search
        self._state = 'search'
        self.codice_a_barre_entry.grab_focus()


    def on_rhesus_button_clicked(self, button):
        quantita = float(self.quantita_entry.get_text())
        self._currentRow['quantita'] = (quantita * -1)
        self.quantita_entry.set_text(Environment.conf.number_format % self._currentRow['quantita'])
        self.confirm_button.grab_focus()


    def on_delete_button_clicked(self, button):
        treeview = self.scontrino_treeview
        model = treeview.get_model()
        model.remove(self.currentIteratorRow)

        # Se era l'ultima riga disabilito text box e pulsanti per totali
        notEmpty = (len(model) > 0)
        self.total_button.set_sensitive(notEmpty)
        self.empty_button.set_sensitive(notEmpty)
        self.setPagamento(enabled = notEmpty)

        # Disabilito cancella e conferma e abilito ricerca barcode
        self.delete_button.set_sensitive(False)
        self.confirm_button.set_sensitive(False)
        self.rhesus_button.set_sensitive(False)
        self.annulling_button.set_sensitive(False)
        self.codice_a_barre_entry.set_sensitive(True)
        self.codice_entry.set_sensitive(True)
        self.search_button.set_sensitive(True)
        self.empty_current_row()

        # Calcolo totali
        self.refreshTotal()

        # vado in search
        self._state = 'search'
        self.codice_a_barre_entry.grab_focus()


    def on_prezzo_entry_focus_out_event(self, entry, event):
        prezzo = float(self.prezzo_entry.get_text())
        self._currentRow['prezzo'] = prezzo
        if self._currentRow['valoreSconto'] == 0:
            self._currentRow['prezzoScontato'] = prezzo
            self.prezzo_scontato_entry.set_text(Environment.conf.number_format % self._currentRow['prezzoScontato'])
            #self.marginevalue_label.set_markup('<b>'+'%-6.3f' % calcolaMargine(float(self.fornitura["prezzoNetto"]),
                                                                   #float(self._currentRow['prezzoScontato']),
                                                                   #float(self.art["percentualeAliquotaIva"]))+ '</b>')
            self.marginevalue_label.set_text('')

        else:
            if self._currentRow['tipoSconto'] == self._simboloPercentuale:
                self._currentRow['prezzoScontato'] = Decimal(str(prezzo)) - (Decimal(str(prezzo)) * self._currentRow['valoreSconto']) / 100
                self.prezzo_scontato_entry.set_text(str( self._currentRow['prezzoScontato']))
                self.marginevalue_label.set_text('')

            else:
                self._currentRow['prezzoScontato'] = prezzo - self._currentRow['valoreSconto']
                self.prezzo_scontato_entry.set_text(Environment.conf.number_format % self._currentRow['prezzoScontato'])
                self.marginevalue_label.set_text('')



    def on_prezzo_entry_key_press_event(self, widget, event):
        keyname = gtk.gdk.keyval_name(event.keyval)
        if keyname == 'Return' or keyname == 'KP_Enter':
            self.quantita_entry.grab_focus()


    def on_prezzo_scontato_entry_focus_out_event(self, entry, event):
        prezzoScontato = float(self.prezzo_scontato_entry.get_text())
        self._currentRow['prezzoScontato'] = prezzoScontato
        if abs(self._currentRow['prezzo'] - self._currentRow['prezzoScontato']) > 0:
            if self._currentRow['tipoSconto'] == self._simboloPercentuale:
                self._currentRow['valoreSconto'] = 100 * (1 - self._currentRow['prezzoScontato'] / self._currentRow['prezzo'])
                self.sconto_entry.set_text(Environment.conf.number_format % self._currentRow['valoreSconto'])
                self.sconto_entry.tipoSconto = 'percentuale'
                self.marginevalue_label.set_markup('<b>'+'%-6.3f' % calcolaMargine(float(self.fornitura["prezzoNetto"]),
                                                                   float(self._currentRow['prezzoScontato']),
                                                                   float(self.art["percentualeAliquotaIva"]))+ '</b>')
            else:
                self._currentRow['valoreSconto'] = self._currentRow['prezzo'] - self._currentRow['prezzoScontato']
                self.sconto_entry.set_text(Environment.conf.number_format % self._currentRow['valoreSconto'])
                self.sconto_entry.tipoSconto = 'valore'
                self.marginevalue_label.set_markup('<b>'+'%-6.3f' % calcolaMargine(float(self.fornitura["prezzoNetto"]),
                                                                   float(self._currentRow['prezzoScontato']),
                                                                   float(self.art["percentualeAliquotaIva"]))+ '</b>')


    def on_prezzo_scontato_entry_key_press_event(self, widget, event):
        keyname = gtk.gdk.keyval_name(event.keyval)
        if keyname == 'Return' or keyname == 'KP_Enter':
            self.confirm_button.grab_focus()


    def on_sconto_entry_focus_out_event(self, entry, event):
        self._currentRow['valoreSconto'] = float(self.sconto_entry.get_text())
        if self.sconto_entry.tipoSconto == 'percentuale':
            self._currentRow['tipoSconto'] = self._simboloPercentuale
        else:
            self._currentRow['tipoSconto'] = self._simboloEuro
        if self._currentRow['valoreSconto'] == 0:
            self._currentRow['tipoSconto'] = None
            self._currentRow['prezzoScontato'] = self._currentRow['prezzo']
            self.prezzo_scontato_entry.set_text(Environment.conf.number_format % self._currentRow['prezzoScontato'])
            self.marginevalue_label.set_markup('<b>'+'%-6.3f' % calcolaMargine(float(self.fornitura["prezzoNetto"]),
                                                                   float(self._currentRow['prezzoScontato']),
                                                                   float(self.art["percentualeAliquotaIva"]))+ '</b>')
        else:
            if self._currentRow['tipoSconto'] == self._simboloPercentuale:
                self._currentRow['prezzoScontato'] = self._currentRow['prezzo'] - (self._currentRow['prezzo'] * self._currentRow['valoreSconto']) / 100
                self.prezzo_scontato_entry.set_text(Environment.conf.number_format % self._currentRow['prezzoScontato'])
                self.marginevalue_label.set_markup('<b>'+'%-6.3f' % calcolaMargine(float(self.fornitura["prezzoNetto"]),
                                                                   float(self._currentRow['prezzoScontato']),
                                                                   float(self.art["percentualeAliquotaIva"]))+ '</b>')
            else:
                self._currentRow['prezzoScontato'] = self._currentRow['prezzo'] - self._currentRow['valoreSconto']
                self.prezzo_scontato_entry.set_text(Environment.conf.number_format % self._currentRow['prezzoScontato'])
                self.marginevalue_label.set_markup('<b>'+'%-6.3f' % calcolaMargine(float(self.fornitura["prezzoNetto"]),
                                                                   float(self._currentRow['prezzoScontato']),
                                                                   float(self.art["percentualeAliquotaIva"]))+ '</b>')


    def on_quantita_entry_focus_out_event(self, entry, event):
        self._currentRow['quantita'] = float(self.quantita_entry.get_text())


    def on_quantita_entry_key_press_event(self, widget, event):
        keyname = gtk.gdk.keyval_name(event.keyval)
        if keyname == 'Return' or keyname == 'KP_Enter':
            self.confirm_button.grab_focus()


    def refreshTotal(self):
        total = 0.0
        model = self.scontrino_treeview.get_model()
        for row in model:
            prezzo = row[4]
            valoreSconto = float(row[5])
            prezzoScontato = float(row[7])
            quantita = float(row[8])

            if valoreSconto == 0: #sconto
                total = total + (prezzo * quantita)
            else:
                total = total + (prezzoScontato * quantita)
        self.label_totale.set_markup('<b><span size="xx-large">' + Environment.conf.number_format % total + '</span></b>')
        return total


    def on_empty_button_clicked(self, button):
        self.scontrino_treeview.get_model().clear()
        self.empty_current_row()
        self.label_totale.set_markup('<b><span size="xx-large">0.00</span></b>')
        self.label_resto.set_markup('<b><span size="xx-large">0.00</span></b>')
        self.empty_button.set_sensitive(False)
        self.total_button.set_sensitive(False)
        self.setPagamento(enabled = False)
        self.codice_a_barre_entry.grab_focus()


    def on_total_button_clicked(self, button):
        totale_scontrino = float(Environment.conf.number_format % self.refreshTotal())
        if totale_scontrino < 0:
            msg = 'Attenzione!\n\nIl totale non puo\' essere negativo !'
            dialog = gtk.MessageDialog(self.getTopLevel(),
                                       gtk.DIALOG_MODAL
                                       | gtk.DIALOG_DESTROY_WITH_PARENT,
                                       gtk.MESSAGE_ERROR, gtk.BUTTONS_OK,
                                       msg)
            response = dialog.run()
            dialog.destroy()
            return

        # Creo dao testata_scontrino
        dao = TestataScontrino().getRecord()

        dao.totale_scontrino = totale_scontrino
        totale_contanti = 0
        totale_assegni = 0
        totale_carta_di_credito = 0

        if self.contanti_entry.get_text() != '':
            totale_contanti = float(Environment.conf.number_format % float(self.contanti_entry.get_text()))
            resto = totale_contanti - dao.totale_scontrino
            self.label_resto.set_markup('<b><span size="xx-large">' + Environment.conf.number_format % resto + '</span></b>')
        if self.non_contanti_entry.get_text() != '':
            if self.assegni_radio_button.get_active():
                totale_assegni = float(Environment.conf.number_format % float(self.non_contanti_entry.get_text()))
            else:
                totale_carta_di_credito = float(Environment.conf.number_format % float(self.non_contanti_entry.get_text()))

        dao.totale_contanti = totale_contanti
        dao.totale_assegni = totale_assegni
        dao.totale_carta_credito = totale_carta_di_credito

        # Creo righe
        righe = []
        model = self.scontrino_treeview.get_model()
        for row in model:
            idArticolo = row[0]
            descrizione = row[3]
            prezzo = float(row[4])
            valoreSconto = float(row[5])
            tipoSconto = row[6]
            prezzoScontato = float(row[7])
            quantita = row[8]

            # Nuova riga
            daoRiga = RigaScontrino().getRecord()
            daoRiga.id_testata_scontrino = dao.id
            daoRiga.id_articolo = idArticolo
            daoRiga.descrizione = descrizione
            daoRiga.prezzo = prezzo
            daoRiga.prezzo_scontato = prezzoScontato
            daoRiga.quantita = quantita
            listarighesconto = []
            if valoreSconto > 0:
                daoScontoRigaScontrino = ScontoRigaScontrino().getRecord()
                daoScontoRigaScontrino.valore = valoreSconto
                if tipoSconto == self._simboloPercentuale:
                    daoScontoRigaScontrino.tipo_sconto = 'percentuale'
                else:
                    daoScontoRigaScontrino.tipo_sconto = 'valore'
                listarighesconto.append(daoScontoRigaScontrino)
            daoRiga.sconti=listarighesconto
            righe.append(daoRiga)

        # Aggiungo righe e salvo dao
        dao.righe = righe
        dao.persist()

        # Rileggo dao
        dao.update()

        # Creo il file
        filescontrino = self.create_export_file(dao)
        # Mando comando alle casse

        if not(hasattr(Environment.conf.VenditaDettaglio,'disabilita_stampa') and Environment.conf.VenditaDettaglio.disabilita_stampa == 'yes'):
            program_launch = Environment.conf.VenditaDettaglio.driver_command
            program_params = (' ' + filescontrino + ' ' +
                              Environment.conf.VenditaDettaglio.serial_device)

            if os.name == 'nt':
                exportingProcessPid = os.spawnl(os.P_NOWAIT, program_launch, program_params)
                id, ret_value = os.waitpid(exportingProcessPid, 0)
                ret_value = ret_value >> 8
            else:
                command = program_launch + program_params
                process = popen2.Popen3(command, True)
                message = process.childerr.readlines()
                ret_value = process.wait()
        else:
            ret_value = 0

        # Elimino il file
        os.remove(filescontrino)
        if ret_value != 0:
            string_message = ''
            for s in message:
                string_message = string_message + s + "\n"

            # Mostro messaggio di errore
            dialog = gtk.MessageDialog(self.getTopLevel(),
                                       gtk.DIALOG_MODAL
                                       | gtk.DIALOG_DESTROY_WITH_PARENT,
                                       gtk.MESSAGE_ERROR, gtk.BUTTONS_OK,
                                       string_message)
            response = dialog.run()
            dialog.destroy()
            # Elimino lo scontrino
            dao.delete()

        # Svuoto transazione e mi rimetto in stato di ricerca
        self.search_button.set_sensitive(True)
        self.codice_a_barre_entry.set_sensitive(True)
        self.codice_entry.set_sensitive(True)
        self.confirm_button.set_sensitive(False)
        self.rhesus_button.set_sensitive(False)
        self.annulling_button.set_sensitive(False)
        self.delete_button.set_sensitive(False)
        self.on_empty_button_clicked(self.empty_button)
        self._state = 'search'


    def close_day(self):
        # Seleziono scontrini della giornata
        datefirst = datetime.today().date()
        aData= stringToDateBumped(datetime.today().date())
        scontrini = TestataScontrino(isList=True).select( daData = datefirst,
                                                          aData = aData,  # Scontrini prodotti nella giornata odierna
                                                          offset = None,
                                                          batchSize = None)

        # Creo nuovo movimento
        daoMovimento = TestataMovimento().getRecord()
        daoMovimento.operazione = Environment.conf.VenditaDettaglio.operazione
        daoMovimento.data_movimento = datefirst
        daoMovimento.note_interne = 'Movimento chiusura fiscale'
        righeMovimento = []
        for scontrino in scontrini:
            for riga in scontrino.righe:
                # Istanzio articolo
                art = Articolo(id=riga.id_articolo).getRecord()
                # Cerco IVA
                iva = AliquotaIva(id=art.id_aliquota_iva).getRecord()

                daoRiga = RigaMovimento().getRecord()
                daoRiga.valore_unitario_lordo = riga.prezzo
                daoRiga.valore_unitario_netto = riga.prezzo_scontato
                daoRiga.quantita = riga.quantita
                daoRiga.moltiplicatore = 1
                daoRiga.descrizione = riga.descrizione
                daoRiga.id_magazzino = self.id_magazzino
                daoRiga.id_articolo = riga.id_articolo
                daoRiga.percentuale_iva = iva.percentuale
                daoRiga.sconti = []
                if riga.sconti:
                    for s in riga.sconti:
                        daoScontoRigaMovimento = ScontoRigaMovimento().getRecord()
                        daoScontoRigaMovimento.valore = s.valore
                        daoScontoRigaMovimento.tipo_sconto = s.tipo_sconto
                        daoRiga.sconti.append(daoScontoRigaMovimento)
                righeMovimento.append(daoRiga)

        daoMovimento.righe = righeMovimento
        daoMovimento.persist()
        #daoMovimento.update()

        # Creo nuova chiusura
        daoChiusura = ChiusuraFiscale().getRecord()
        daoChiusura.data_chiusura = datefirst
        daoChiusura.persist()
        #daoChiusura.update()

        # Creo il file
        filechiusura = self.create_fiscal_close_file()
        # Mando comando alle casse
        if not(hasattr(Environment.conf.VenditaDettaglio,'disabilita_stampa_chiusura') and Environment.conf.VenditaDettaglio.disabilita_stampa_chiusura == 'yes'):
            program_launch = Environment.conf.VenditaDettaglio.driver_command
            program_params = (' ' + filechiusura + ' ' +
                              Environment.conf.VenditaDettaglio.serial_device)

            if os.name == 'nt':
                exportingProcessPid = os.spawnl(os.P_NOWAIT, program_launch, program_params)
                id, ret_value = os.waitpid(exportingProcessPid, 0)
                ret_value = ret_value >> 8
            else:
                command = program_launch + program_params
                process = popen2.Popen3(command, True)
                message = process.childerr.readlines()
                ret_value = process.wait()
        else:
            ret_value = 0

        # Elimino il file
        #os.remove(filechiusura)
        if ret_value != 0:
            string_message = ''
            for s in message:
                string_message = string_message + s + "\n"

            # Mostro messaggio di errore
            dialog = gtk.MessageDialog(self.getTopLevel(),
                                       gtk.DIALOG_MODAL
                                       | gtk.DIALOG_DESTROY_WITH_PARENT,
                                       gtk.MESSAGE_ERROR, gtk.BUTTONS_OK,
                                       string_message)
            response = dialog.run()
            dialog.destroy()
            # Elimino il movimento e la chiusura
            daoChiusura.delete()
            daoChiusura = None
            daoMovimento.delete()
            daoMovimento = None

        if daoMovimento is not None:
            # Associo movimento agli scontrini
            for scontrino in scontrini:
                daoScontrino = TestataScontrino(id=scontrino.id).getRecord()
                daoScontrino.id_testata_movimento = daoMovimento.id
                daoScontrino.persist(chiusura=True)

        # Svuoto transazione
        self.on_empty_button_clicked(self.empty_button)


    def on_chiusura_fiscale_activate(self, widget):
        # Chiedo conferma
        dialog = gtk.MessageDialog(self.getTopLevel(),
                                   gtk.DIALOG_MODAL
                                   | gtk.DIALOG_DESTROY_WITH_PARENT,
                                   gtk.MESSAGE_QUESTION, gtk.BUTTONS_YES_NO)
        dialog.set_markup('<b>ATTENZIONE</b>: Chiusura fiscale! Confermi?')
        response = dialog.run()
        dialog.destroy()
        if response ==  gtk.RESPONSE_YES:
            # controllo se vi e` gia` stata una chiusura
            datefirst = datetime.today().date()
            chiusure = ChiusuraFiscale(isList=True).select( dataChiusura = datefirst,
                                                            offset = None,
                                                            batchSize = None)
            if len(chiusure) != 0:
                dialog = gtk.MessageDialog(self.getTopLevel(),
                                           gtk.DIALOG_MODAL
                                           | gtk.DIALOG_DESTROY_WITH_PARENT,
                                           gtk.MESSAGE_ERROR, gtk.BUTTONS_OK)
                dialog.set_markup("<b>ATTENZIONE:\n La chiusura odierna e` gia' stata effettuata</b>")
                response = dialog.run()
                dialog.destroy()
                return
            self.close_day()
        else:
            return


    def create_export_file(self, daoScontrino):
        # Genero nome file
        filename = Environment.conf.VenditaDettaglio.export_path + str(daoScontrino.id) + datetime.today().strftime('%d_%m_%Y_%H_%M_%S')
        f = file(filename,'w')

        # nel file scontrino i resi vengono vengono messi alla fine (limitazione cassa) DITRON
        righe = []
        for riga in daoScontrino.righe:
            if riga.quantita < 0:
                righe.append(riga)
            else:
                righe.insert(0, riga)

        for riga in righe:
            quantita = abs(riga.quantita)
            if quantita != 1:
                # quantita' non unitaria
                stringa = '000000000000000000%09d00\r\n' % (quantita * 1000)
                f.write(stringa)
            if riga.quantita < 0:
                # riga reso
                stringa = '020000000000000000%09d00\r\n' % (0)
                f.write(stringa)

            reparto = getattr(Environment.conf.VenditaDettaglio,'reparto_default',1)
            art = leggiArticolo(riga.id_articolo)
            repartoIva = 'reparto_' + art["denominazioneBreveAliquotaIva"].lower()
            if hasattr(Environment.conf.VenditaDettaglio, repartoIva):
                reparto = getattr(Environment.conf.VenditaDettaglio,repartoIva,reparto)
            reparto = str(reparto).zfill(2)

            if not(riga.quantita < 0):
                stringa = '01%-16s%09.2f%2s\r\n' % (riga.descrizione[:16], riga.prezzo, reparto)
                f.write(stringa)
                for sconto in riga.sconti:
                    if sconto.valore != 0:
                        if sconto.tipo_sconto == 'percentuale':
                            stringa = '07%-16s%09.2f00\r\n' % ('sconto', sconto.valore)
                        else:
                            stringa = '06%-16s%09.2f00\r\n' % ('sconto', sconto.valore * quantita)
                        f.write(stringa)
            else:
                # per i resi, nello scontrino, si scrive direttamente il prezzo scontato (limitazione cassa)
                stringa = '01%-16s%09.2f%2s\r\n' % (riga.descrizione[:16], riga.prezzo_scontato, reparto)
                f.write(stringa)

        if daoScontrino.totale_contanti is None or daoScontrino.totale_contanti == 0:
            totale_contanti = daoScontrino.totale_scontrino
        else:
            totale_contanti = daoScontrino.totale_contanti

        if daoScontrino.totale_assegni is not None and daoScontrino.totale_assegni != 0:
            stringa = '20                %09d00\r\n' % (daoScontrino.totale_assegni * 100)
            f.write(stringa)

        if daoScontrino.totale_carta_credito is not None and daoScontrino.totale_carta_credito != 0:
            stringa = '30                %09d00\r\n' % (daoScontrino.totale_carta_credito * 100)
            f.write(stringa)

        stringa = '10                %09.2f00\r\n' % (totale_contanti)
        f.write(stringa)
        f.close()
        return filename


    def create_fiscal_close_file(self):
        # Genero nome file
        filename = Environment.conf.VenditaDettaglio.export_path + 'fiscal_close_' + datetime.today().strftime('%d_%m_%Y_%H_%M_%S')

        f = file(filename,'w')
        stringa = '51                00000000002..\r\n'
        f.write(stringa)
        f.close()
        return filename


    def ricercaArticolo(self):

        def on_ricerca_articolo_hide(anagWindow, anag):
            if anag.dao is None:
                anagWindow.destroy()
                return

            anagWindow.destroy()
            idArticolo = anag.dao.id
            codiceABarre = anag.dao.codice_a_barre or ''
            codice = anag.dao.codice or ''
            descrizione = anag.dao.descrizione_etichetta or anag.dao.denominazione or ''
            # Ricerca listino_articolo
            listino = leggiListino(self.id_listino, idArticolo)
            prezzo = listino["prezzoDettaglio"]
            if  len(listino["scontiDettaglio"]) > 0:
                valoreSconto = listino["scontiDettaglio"][0].valore
                tipoSconto = listino["scontiDettaglio"][0].tipo_sconto
            else:
                valoreSconto = 0
                tipoSconto = 'percentuale'
            prezzoScontato = prezzo - prezzo * valoreSconto / 100
            quantita = 1

            self.activate_item(idArticolo,
                               codiceABarre,
                               codice or '',
                               descrizione,
                               prezzo,
                               valoreSconto,
                               tipoSconto,
                               prezzoScontato,
                               quantita)

            self.prezzo_entry.grab_focus()

        from promogest.ui.RicercaComplessaArticoli import RicercaComplessaArticoli
        codiceABarre = self.codice_a_barre_entry.get_text()
        codice = self.codice_entry.get_text()
        anag = RicercaComplessaArticoli(codiceABarre = codiceABarre,
                                        codice = codice)
        anag.setTreeViewSelectionType(gtk.SELECTION_SINGLE)
        anagWindow = anag.getTopLevel()
        anagWindow.connect("hide",
                           on_ricerca_articolo_hide, anag)
        anagWindow.set_transient_for(self.getTopLevel())
        anagWindow.show_all()


    def on_new_button_clicked(self, button):
        from promogest.ui.AnagraficaArticoliSemplice import AnagraficaArticoliSemplice
        anag = AnagraficaArticoliSemplice()
        anagWindow = anag.getTopLevel()
        showAnagraficaRichiamata(self.getTopLevel(), anagWindow, button)


    def ricercaListino(self):
        pricelist = Listino(isList=True).select(denominazione = Environment.conf.VenditaDettaglio.listino,
                                                                                            offset = None,
                                                                                            batchSize = None)
        if len(pricelist) > 0:
            id_listino = pricelist[0].id
        else:
            id_listino = None

        return id_listino


    def on_total_button_grab_focus(self, button):
        totale_scontrino = float(self.label_totale.get_text())
        if self.contanti_entry.get_text() != '':
            totale_pagamento = float(self.contanti_entry.get_text())
        elif self.non_contanti_entry.get_text() != '':
            totale_pagamento = float(self.non_contanti_entry.get_text())
        else:
            totale_pagamento = 0
        resto = totale_pagamento - totale_scontrino
        self.label_resto.set_markup('<b><span size="xx-large">' + Environment.conf.number_format % resto + '</span></b>')

        if self.total_button.is_focus():
            self.on_total_button_clicked(button)


    def on_contanti_radio_button_clicked(self, button):
        #predisposizione per il pagamento con contanti
        if self.total_button.get_property('sensitive'):
            self.contanti_entry.set_sensitive(True)
            self.contanti_entry.grab_focus()
            self.non_contanti_entry.set_text('')
            self.non_contanti_entry.set_sensitive(False)
        else:
            self.contanti_entry.set_sensitive(False)
            self.non_contanti_entry.set_sensitive(False)


    def on_non_contanti_clicked(self):
        #predisposizione per il pagamento non in contanti
        if self.total_button.get_property('sensitive'):
            self.non_contanti_entry.set_sensitive(True)
            self.non_contanti_entry.grab_focus()
            self.non_contanti_entry.set_text(Environment.conf.number_format % self.refreshTotal())
            self.contanti_entry.set_text('')
            self.contanti_entry.set_sensitive(False)
        else:
            self.contanti_entry.set_sensitive(False)
            self.non_contanti_entry.set_sensitive(False)


    def on_assegni_radio_button_clicked(self, button):
        #predisposizione per il pagamento con assegni
        self.on_non_contanti_clicked()


    def on_carta_di_credito_radio_button_clicked(self, button):
        #predisposizione per il pagamento con carta di credito
        self.on_non_contanti_clicked()


    def setPagamento(self, enabled = False):
        self.contanti_radio_button.set_active(True)
        self.contanti_entry.set_text('')
        self.non_contanti_entry.set_text('')
        self.non_contanti_entry.set_sensitive(False)
        self.contanti_entry.set_sensitive(enabled)


    def on_vendita_dettaglio_window_close(self, widget, event=None):
        self.destroy()
        return None


    def on_list_button_clicked(self, widget):
        self.idRhesusSource = []
        gest = GestioneScontrini(daData=None, aData=None, righe=self.idRhesusSource)
        gestWnd = gest.getTopLevel()
        showAnagraficaRichiamata(self.getTopLevel(), gestWnd, None, self.creaScontrinoReso)


    def creaScontrinoReso(self):
        treeview = self.scontrino_treeview
        model = treeview.get_model()

        if not(len(self.idRhesusSource) > 0):
            return

        ts = TestataScontrino(id=self.idRhesusSource[0]).getRecord()
        for r in ts.righe:
            idArticolo = r.id_articolo
            codiceArticolo = r.codice_articolo or ''
            codiceABarre = r.codice_a_barre or ''
            descrizione = r.descrizione or ''
            prezzo = round(r.prezzo or 0, int(Environment.conf.decimals))
            quantita = -1 * round(r.quantita or 0, int(Environment.conf.decimals))
            tipoSconto = None
            sconto = round(r.valore_sconto or 0, int(Environment.conf.decimals))
            prezzoScontato = round(r.prezzo_scontato or 0, int(Environment.conf.decimals))
            if sconto != 0:
                if r.tipo_sconto == 'percentuale':
                    tipoSconto = self._simboloPercentuale
                else:
                    tipoSconto = self._simboloEuro

            model.append((idArticolo,
                          codiceABarre,
                          codiceArticolo,
                          descrizione,
                          prezzo,
                          sconto,
                          tipoSconto,
                          prezzoScontato,
                          quantita))

        notEmpty = (len(model) > 0)
        self.total_button.set_sensitive(notEmpty)
        self.empty_button.set_sensitive(notEmpty)
        self.setPagamento(enabled = notEmpty)

        self.search_button.set_sensitive(True)

        # Calcolo totali
        self.refreshTotal()
        # vado in search
        self.empty_current_row()
        self._state = 'search'
        self.codice_a_barre_entry.grab_focus()


    def getGiacenzaArticolo(self, idArticolo):
        idMagazzino = self.id_magazzino
        totGiacenza = 0
        movs = giacenzaSel(year=Environment.workingYear, idMagazzino= self.id_magazzino, idArticolo=idArticolo)
        #movs = Environment.connection.execStoredProcedure('GiacenzaSel', (None, Environment.conf.workingYear, idMagazzino, idArticolo))
        for m in movs:
            totGiacenza += m['giacenza'] or 0

        # FIXME: attenzione funzioen da rifareeeeeeeeeeeeeeeee
        #movs = Environment.connection.execStoredProcedure('ScaricoScontrinoSel', (None, Environment.conf.workingYear, idArticolo, idMagazzino, False))
        #for m in movs:
            #totGiacenza += ((m['scarico_qta'] or 0 ) * -1)

        return totGiacenza



class GestioneScontrini(GladeWidget):
    """ Classe per la gestione degli scontrini emessi """

    def __init__(self, idArticolo = None,
                       daData = None,
                       aData = None,
                       righe = []):
        self._idArticolo = idArticolo
        self._daData = daData
        self._aData = aData
        self._righe = righe

        self._htmlTemplate = None
        self.dao = None

        GladeWidget.__init__(self, 'generic_dialog',
                fileName="promogest/modules/VenditaDettaglio/gui/generic_dialog.glade", isModule=True)
        self._window = self.generic_dialog

        self.placeWindow(self._window)
        self.draw()


    def draw(self):
        self._window.set_title('Scontrini emessi')
        rhesus_button = gtk.Button(stock=gtk.STOCK_REDO)
        alignment = rhesus_button.get_children()[0]
        hbox = alignment.get_children()[0]
        image, label = hbox.get_children()
        label.set_text('_Reso')
        label.set_use_underline(True)
        quit_button = gtk.Button(stock=gtk.STOCK_QUIT)
        self.main_hbuttonbox.pack_start(rhesus_button)
        self.main_hbuttonbox.pack_end(quit_button)
        #self._window.add_action_widget(rhesus_button, gtk.RESPONSE_APPLY)
        #self._window.add_action_widget(quit_button, gtk.RESPONSE_CANCEL)

        rhesus_button.connect('clicked',
                              self.on_rhesus_button_clicked)
        quit_button.connect('clicked',
                            self.on_scontrini_window_close)

        main_hpaned = gtk.HPaned()
        self.main_vbox.add(main_hpaned)

        self.filterss = FilterWidget(owner=self, filtersElement=GladeWidget(rootWidget='scontrini_filter_table',
            fileName="promogest/modules/VenditaDettaglio/gui/_scontrini_emessi_elements.glade", isModule=True))
        self.filters = self.filterss.filtersElement
        self.filterTopLevel = self.filterss.getTopLevel()
        main_hpaned.pack1(self.filterTopLevel)
        self.detail = GladeWidget(rootWidget = 'scontrini_detail_vbox',
            fileName="promogest/modules/VenditaDettaglio/gui/_scontrini_emessi_elements.glade", isModule=True)
        self.detailTopLevel = self.detail.getTopLevel()
        main_hpaned.pack2(self.detailTopLevel)

        self.filterss.filter_scrolledwindow.set_policy(hscrollbar_policy = gtk.POLICY_AUTOMATIC,
                                                     vscrollbar_policy = gtk.POLICY_AUTOMATIC)
        self.filterss.filter_body_label.set_markup('<b>Elenco scontrini</b>')
        self.filterss.filter_body_label.set_property('visible', True)


        # Colonne della Treeview per il filtro
        treeview = self.filterss.resultsElement
        model = self.filterss._treeViewModel = gtk.ListStore(object, str, str, str, str, str, str, str)

        rendererSx = gtk.CellRendererText()
        rendererDx = gtk.CellRendererText()
        rendererDx.set_property('xalign', 1)

        column = gtk.TreeViewColumn('Data', rendererSx, text=1)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        column.connect("clicked", self.filterss._changeOrderBy, 'data_inserimento, id')
        column.set_resizable(True)
        column.set_expand(True)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Totale', rendererDx, text=2)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(False)
        column.set_resizable(True)
        column.set_expand(False)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Contanti', rendererDx, text=3)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(False)
        column.set_resizable(True)
        column.set_expand(False)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Assegni', rendererDx, text=4)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(False)
        column.set_resizable(True)
        column.set_expand(False)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Carta di credito', rendererDx, text=5)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(False)
        column.set_resizable(True)
        column.set_expand(False)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Data mov. mag.', rendererSx, text=6)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        column.connect("clicked", self.filterss._changeOrderBy, 'data_movimento')
        column.set_resizable(True)
        column.set_expand(False)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Numero mov. mag.', rendererSx, text=7)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        column.connect("clicked", self.filterss._changeOrderBy, 'numero_movimento')
        column.set_resizable(True)
        column.set_expand(False)
        treeview.append_column(column)

        treeview.set_model(model)

        self.filters.id_articolo_filter_customcombobox.setId(self._idArticolo)

        if self._daData is None:
            self.filters.da_data_filter_entry.setNow()
        else:
            self.filters.da_data_filter_entry.set_text(self_daData)
        if self._aData is None:
            self.filters.a_data_filter_entry.setNow()
        else:
            self.filters.a_data_filter_entry.set_text(self_aData)
        self.defaultFileName = "scontrino.html"
        self._htmlTemplate = "promogest/modules/VenditaDettaglio/templates"
        self.refreshHtml()

        self.refresh()


    def clear(self):
        # Annullamento filtro
        self.filters.id_articolo_filter_customcombobox.set_active(0)
        self.filters.da_data_filter_entry.set_text('')
        self.filters.a_data_filter_entry.set_text('')
        self.refresh()


    def refresh(self):
        # Aggiornamento TreeView
        idArticolo = self.filters.id_articolo_filter_customcombobox.getId()
        daData = stringToDate(self.filters.da_data_filter_entry.get_text())
        aData = stringToDateBumped(self.filters.a_data_filter_entry.get_text())
        self.filterss.numRecords = TestataScontrino(isList=True).count(idArticolo=idArticolo,
                                                                      daData=daData,
                                                                      aData=aData)

        self.filterss._refreshPageCount()

        scos = TestataScontrino(isList=True).select( orderBy=self.filterss.orderBy,
                                                     idArticolo=idArticolo,
                                                     daData=daData,
                                                     aData=aData,
                                                     offset=self.filterss.offset,
                                                     batchSize=self.filterss.batchSize)

        self.filterss._treeViewModel.clear()

        for s in scos:
            totale = '%14.2f' % (s.totale_scontrino or 0)
            contanti = '%14.2f' % (s.totale_contanti or 0)
            assegni = '%14.2f' % (s.totale_assegni or 0)
            carta = '%14.2f' % (s.totale_carta_credito or 0)
            self.filterss._treeViewModel.append((s, dateToString(s.data_inserimento), totale,
                                               contanti, assegni, carta,
                                               dateToString(s.data_movimento), str(s.numero_movimento or '')))


    def on_filter_treeview_cursor_changed(self, treeview):
        sel = self.filterss.resultsElement.get_selection()
        (model, iterator) = sel.get_selected()

        if iterator is None:
            print 'on_filter_treeview_cursor_changed(): FIXME: iterator is None!'
            return

        self.dao = model.get_value(iterator, 0)
        self.refreshHtml(self.dao)


    def on_filter_treeview_row_activated(self, treeview, path, column):
        # Not used here
        pass


    def on_filter_treeview_selection_changed(self, treeSelection):
        # Not used here
        pass


    def refreshHtml(self, dao=None):
        document =gtkhtml2.Document()
        if self.dao is None:
            html = '<html></html>'
        else:
            templates_dir = self._htmlTemplate
            loader = TemplateLoader([templates_dir])
            tmpl = loader.load(self.defaultFileName)
            stream = tmpl.generate(dao=self.dao)
            html = stream.render('xhtml')
        document.open_stream('text/html')
        document.write_stream(html)
        document.close_stream()
        self.detail.detail_html.set_document(document)


    def on_scontrini_window_close(self, widget, event=None):
        self.destroy()
        return None


    def on_rhesus_button_clicked(self, widget):
        if self.dao is not None:
            self._righe.append(self.dao.id)
            self.on_scontrini_window_close(widget)
