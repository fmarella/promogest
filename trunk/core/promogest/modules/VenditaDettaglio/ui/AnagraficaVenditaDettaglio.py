# -*- coding: utf-8 -*-

# Promogest
#
# Copyright (C) 2005 by Promotux Informatica - http://www.promotux.it/
# Author: Alessandro Scano <alessandro@promotux.it>
# Author: Francesco Meloni <francescoo@promotux.it>

from promogest.ui.utils import *
import gtk, gobject
import os, popen2
import gtkhtml2
from promogest.dao.DaoUtils import giacenzaSel
from datetime import datetime, timedelta
from promogest import Environment
from promogest.ui.GladeWidget import GladeWidget
from promogest.dao.TestataMovimento import TestataMovimento
from promogest.dao.RigaMovimento import RigaMovimento
from promogest.dao.ScontoRigaMovimento import ScontoRigaMovimento
from promogest.modules.VenditaDettaglio.dao.TestataScontrino import TestataScontrino
from promogest.modules.VenditaDettaglio.dao.RigaScontrino import RigaScontrino
from promogest.modules.VenditaDettaglio.dao.ScontoRigaScontrino import ScontoRigaScontrino
from promogest.modules.VenditaDettaglio.dao.ChiusuraFiscale import ChiusuraFiscale
from promogest.dao.Articolo import Articolo
from promogest.dao.CodiceABarreArticolo import CodiceABarreArticolo
from promogest.dao.AliquotaIva import AliquotaIva
from promogest.dao.Magazzino import Magazzino
from promogest.dao.Listino import Listino
from promogest.dao.ListinoArticolo import ListinoArticolo
from promogest.ui.widgets.FilterWidget import FilterWidget
from GestioneScontrini import GestioneScontrini
from GestioneChiusuraFiscale import GestioneChiusuraFiscale

class AnagraficaVenditaDettaglio(GladeWidget):
    """ Frame per la gestione delle vendite a dettaglio """

    def __init__(self):
        GladeWidget.__init__(self, 'vendita_dettaglio_window',
                        fileName='promogest/modules/VenditaDettaglio/gui/vendita_dettaglio_window.glade',
                        isModule=True)
        self.placeWindow(self.getTopLevel())
        self._currentRow = {}
        self._simboloPercentuale = '%'
        self._simboloEuro = '€'
        textStatusBar = "     *****   PromoGest2 - Vendita Dettaglio - by PromoTUX Informatica - 800 034561 - www.PromoTUX.it - info@PromoTUX.it  *****     "
        context_id =  self.vendita_dettaglio_statusbar.get_context_id("vendita_dettaglio_window")
        self.vendita_dettaglio_statusbar.push(context_id,textStatusBar)
        azienda = Azienda().getRecord(id=Environment.params["schema"])
        self.logo_articolo.set_from_file(azienda.percorso_immagine)
        self.createPopupMenu()
        #nascondo i dati riga e le info aggiuntive
        self.dati_riga_frame.destroy()
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
        self.modelRiga = gtk.ListStore(int,str, str, str, str, str, str, str, str, str)

        treeview = self.scontrino_treeview
        rendererSx = gtk.CellRendererText()
        rendererDx = gtk.CellRendererText()
        rendererDx.set_property('xalign', 1)

        self.lsmodel = gtk.ListStore(int,str)
        cellcombo1= gtk.CellRendererCombo()
        cellcombo1.set_property("editable", True)
        cellcombo1.set_property("visible", True)
        cellcombo1.set_property("text-column", 1)
        cellcombo1.set_property("editable", True)
        cellcombo1.set_property("has-entry", False)
        cellcombo1.set_property("model", self.lsmodel)
        cellcombo1.connect('edited', self.on_column_listinoRiga_edited, treeview, True)
        column = gtk.TreeViewColumn('List.', cellcombo1, text=1)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        column.set_resizable(True)
        column.set_expand(False)
        column.set_min_width(20)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Codice a barre', rendererSx, text=2)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(False)
        column.set_resizable(True)
        column.set_expand(False)
        column.set_min_width(90)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Codice', rendererSx, text=3)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(False)
        column.set_resizable(True)
        column.set_expand(False)
        column.set_min_width(70)
        treeview.append_column(column)

        cellrendererDescrizione = gtk.CellRendererText()
        cellrendererDescrizione.set_property("editable", True)
        cellrendererDescrizione.set_property("visible", True)
        cellrendererDescrizione.connect('edited', self.on_column_descrizione_edited, treeview, True)
        column = gtk.TreeViewColumn('Descrizione', cellrendererDescrizione, text=4)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        rendererSx.connect('edited', self.on_column_descrizione_edited, treeview, True)
        column.set_resizable(True)
        column.set_expand(True)
        column.set_min_width(50)
        treeview.append_column(column)

        cellspin = gtk.CellRendererSpin()
        cellspin.set_property("editable", True)
        cellspin.set_property("visible", True)
        adjustment = gtk.Adjustment(1, 1, 1000,0.500,2)
        cellspin.set_property("adjustment", adjustment)
        cellspin.set_property("digits",3)
        cellspin.set_property("climb-rate",3)
        #cellspin.set_property("foreground", "orange")

        cellspin.connect('edited', self.on_column_prezzo_edited, treeview, True)
        column = gtk.TreeViewColumn('Prezzo', cellspin, text=5,foreground=4, background=2)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        #column.set_clickable(False)
        column.set_resizable(True)
        column.set_expand(False)
        column.set_min_width(80)
        treeview.append_column(column)

        cellspinsconto = gtk.CellRendererSpin()
        cellspinsconto.set_property("editable", True)
        cellspinsconto.set_property("visible", True)
        adjustment = gtk.Adjustment(1, 1, 1000,1,2)
        cellspinsconto.set_property("adjustment", adjustment)
        #cellspin.set_property("digits",3)
        #cellspin.set_property("climb-rate",3)
        cellspinsconto.connect('edited', self.on_column_sconto_edited, treeview, True)
        column = gtk.TreeViewColumn('Sconto', cellspinsconto, text=6)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        column.set_resizable(True)
        column.set_expand(False)
        column.set_min_width(50)
        treeview.append_column(column)


        lsmodel = gtk.ListStore(str)
        lsmodel.append(["%"])
        lsmodel.append(["€"])
        cellcombo= gtk.CellRendererCombo()
        cellcombo.set_property("editable", True)
        cellcombo.set_property("visible", True)
        cellcombo.set_property("text-column", 0)
        cellcombo.set_property("editable", True)
        cellcombo.set_property("has-entry", False)
        cellcombo.set_property("model", lsmodel)
        cellcombo.connect('edited', self.on_column_tipo_edited, treeview, True)
        column = gtk.TreeViewColumn('Tipo', cellcombo, text=7)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        column.set_resizable(True)
        column.set_expand(False)
        column.set_min_width(20)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Pr.Scont', rendererDx, text=8)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(False)
        column.set_resizable(True)
        column.set_expand(False)
        column.set_min_width(50)
        treeview.append_column(column)

        cellspin = gtk.CellRendererSpin()
        cellspin.set_property("editable", True)
        cellspin.set_property("visible", True)
        adjustment = gtk.Adjustment(1, 1, 1000,0.500,2)
        cellspin.set_property("adjustment", adjustment)
        cellspin.set_property("digits",3)
        cellspin.set_property("climb-rate",3)
        cellspin.connect('edited', self.on_column_quantita_edited, treeview, True)
        column = gtk.TreeViewColumn('Quantità', cellspin, text=9)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        #column.set_clickable(False)
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

        self.codice_a_barre_entry.grab_focus()
        self._loading = False

        # Segnali
        treeViewSelection = self.scontrino_treeview.get_selection()
        self.scontrino_treeview.set_property('rules-hint',True)
        treeViewSelection.connect('changed', self.on_scontrino_treeview_selection_changed)

        # Ricerca listino
        self.id_listino = self.ricercaListino()

        # Ricerca magazzino
        magalist = Magazzino().select(denominazione = Environment.conf.VenditaDettaglio.magazzino,
                                        offset = None,
                                        batchSize = None)

        if len(magalist) > 0:
            self.id_magazzino = magalist[0].id
        else:
            self.id_magazzino = None

        #self.prezzo_entry.connect('key_press_event',
                                  #self.on_prezzo_entry_key_press_event)
        #self.prezzo_scontato_entry.connect('key_press_event',
                                           #self.on_prezzo_scontato_entry_key_press_event)
        #self.quantita_entry.connect('key_press_event',
                                    #self.on_quantita_entry_key_press_event)
        #self.sconti_scontrino_widget.button.connect('toggled',
                #self.on_sconti_scontrino_widget_button_toggled)

        # Vado in stato di ricerca
        self._state = 'search'
        self.empty_current_row()

    def on_column_prezzo_edited(self, cell, path, value, treeview, editNext=True):
        """ Function to set the value prezzo edit in the cell"""
        model = treeview.get_model()
        value=value.replace(",",".")
        value = mN(value)
        model[path][5] = value
        if model[path][7] == '%':
            tipoSconto = "percentuale"
        else:
            tipoSconto = "valore"
        if model[path][6]== 0 or not model[path][5]:
            tipoSconto = None
            model[path][8] = model[path][5]
        else:
            if tipoSconto == "percentuale":
                prezzoscontato = mN(model[path][5]) - (mN(model[path][5]) * mN(model[path][6])) / 100
            else:
                prezzoscontato = mN(model[path][5]) -mN(model[path][6])
            if not prezzoscontato:
                prezzoscontato = "0.00"
            model[path][8] = prezzoscontato
        self.refreshTotal()
        self.on_cancel_button_clicked(self.getTopLevel)

    def on_column_sconto_edited(self, cell, path, value, treeview, editNext=True):
        model = treeview.get_model()
        model[path][6] = value
        prez = model[path][5]
        self.on_column_prezzo_edited(cell, path, prez, treeview)

    def on_column_listinoRiga_edited(self, cell, path, value, treeview, editNext=True):
        #rivedere assolutamente .....
        model = treeview.get_model()
        model[path][1] = value
        listin = {}
        for l in self.lsmodel:
            if l[1] == value:
                idlisti=l[0]
                listin = leggiListino(l[0],model[path][0] )
                break
        prez = str(listin['prezzoDettaglio'])
        if listin.has_key('scontiDettaglio'):
                if  len(listin["scontiDettaglio"]) > 0:
                    model[path][6]= listin['scontiDettaglio'][0].valore or 0
                else:
                    model[path][6] = 0
        self.on_column_prezzo_edited(cell, path, prez, treeview)

    def on_column_quantita_edited(self, cell, path, value, treeview, editNext=True):
        """ Function ti set the value quantita edit in the cell """
        model = treeview.get_model()
        value=value.replace(",",".")
        value = mN(value)
        model[path][9] = value
        self.refreshTotal()
        self.on_cancel_button_clicked(self.getTopLevel)

    def on_column_descrizione_edited(self, cell, path, value, treeview, editNext=True):
        """ Function ti set the value quantita edit in the cell """
        model = treeview.get_model()
        model[path][4] = value
        self.on_cancel_button_clicked(self.getTopLevel)

    def on_column_tipo_edited(self, cell, path, value, treeview, editNext=True):
        """ Function ti set the value quantita edit in the cell"""
        model = treeview.get_model()
        model[path][7] = value
        scont = model[path][6]
        self.on_column_sconto_edited(cell, path, scont, treeview)

    def on_vendita_dettaglio_window_key_press_event(self,widget, event):
        """ jolly key è F9, richiama ed inserisce l'articolo definito nel configure"""
        keyname = gtk.gdk.keyval_name(event.keyval)
        if keyname == 'F9':
            try:
                codice = Environment.conf.VenditaDettaglio.jolly
                self.search_item(codice=codice)
            except:
                print "ARTICOLO JOLLY NON SETTATO NEL CONFIGURE NELLA SEZIONE [VenditaDettaglio]"

    def search_item(self, codiceABarre=None, codice=None, descrizione=None):
        # Ricerca articolo per barcode
        if codiceABarre is not None:
            arts = Articolo().select( codiceABarre = codiceABarre,
                                                 offset = None,
                                                 batchSize = None)
        elif codice is not None:
            arts = Articolo().select( codice = codice,
                                                 offset = None,
                                                 batchSize = None)
        elif descrizione is not None:
            arts = Articolo().select( denominazione = descrizione,
                                                 offset = None,
                                                 batchSize = None)
        if len(arts) == 1:
            idArticolo = arts[0].id
            codice = arts[0].codice or ''
            codiceABarre = arts[0].codice_a_barre or ''
            descrizione = arts[0].descrizione_etichetta or arts[0].denominazione or ''
            # Ricerca listino_articolo
            listino = leggiListino(self.id_listino, idArticolo)
            prezzo = mN(listino["prezzoDettaglio"])
            listinoRiga = (self.id_listino,listino['denominazione'])
            prezzoScontato = prezzo
            valoreSconto = 0
            tipoSconto = None
            if listino.has_key('scontiDettaglio'):
                if  len(listino["scontiDettaglio"]) > 0:
                    valoreSconto = listino['scontiDettaglio'][0].valore or 0
                    if valoreSconto == 0:
                        tipoSconto = None
                        prezzoScontato = prezzo
                    else:
                        tipoSconto = listino['scontiDettaglio'][0].tipo_sconto
                        if tipoSconto == "percentuale":
                            prezzoScontato = mN(mN(prezzo) - (mN(prezzo) * mN(valoreSconto)) / 100)
                        else:
                            prezzoScontato = mN(mN(prezzo) -mN(valoreSconto))
            quantita = 1

            self.codice_a_barre_entry.set_text(codiceABarre)
            self.codice_entry.set_text(codice)
            self.activate_item(idArticolo, listinoRiga, codiceABarre,codice,
                               descrizione, prezzo, valoreSconto,tipoSconto,
                               prezzoScontato, quantita)
            self.confirm_button.grab_focus()
            try:
                if Environment.conf.VenditaDettaglio.direct_confirm == "yes":
                    self.on_confirm_button_clicked(self.getTopLevel())
                    self.refreshTotal()
            except:
                pass
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

    def on_descrizione_entry_activate(self,text_entry):
        if self.descrizione_entry.get_text() != '':
            self.search_item(descrizione = prepareFilterString(self.descrizione_entry.get_text()))
        return True

    def setDao(self, dao):
        if dao is None:
            # Crea un nuovo Dao vuoto
            self.dao = ListinoArticolo()
        else:
            # Ricrea il Dao con una connessione al DBMS SQL
            self.dao = ListinoArticolo().select(idListino=dao.id_listino,
                                                    idArticolo=dao.id_articolo,
                                                    orderBy="id_articolo")[0]
        self._refresh()

    def empty_current_row(self):
        self._currentRow['idArticolo'] = None
        self._currentRow['listinoRiga'] = (None,None)
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
        self.descrizione_entry.set_text('')
        self.descrizione_label.set_text('')
        self.prezzo_entry.set_text('')
        self.sconto_entry.set_text('')
        self.prezzo_scontato_entry.set_text('')
        self.quantita_entry.set_text('')
        self.listini_combobox.clear()
        self.id_listino = self.ricercaListino()
        self.giacenza_label.set_text('-')


    def activate_item(self, idArticolo,listinoRiga,codiceABarre,codice,denominazione,
                        prezzo,valoreSconto,tipoSconto,prezzoScontato,quantita):
        self._loading = True
        self.lsmodel.clear()

        #fillComboboxListiniFiltrati(self.listini_combobox,
                                    #idArticolo=idArticolo,
                                    #idMagazzino=None,
                                    #idCliente=None,
                                    #filter=False)
        listiniList= listinoCandidateSel(idArticolo=idArticolo,
                                        idMagazzino=self.id_magazzino ,
                                        idCliente=None)
        if listiniList:
            for l in listiniList:
                self.lsmodel.append([l.id,l.denominazione])
        if self.id_listino is not None:
            findComboboxRowFromId(self.listini_combobox, self.id_listino)
        else:
            self.listini_combobox.set_active(1)
            try:
                self.id_listino = findIdFromCombobox(self.listini_combobox)
                if prezzo == 0:
                    listino = leggiListino(self.id_listino, idArticolo)
                    prezzo = mN(listino["prezzoDettaglio"])
                    prezzoScontato = prezzo
                    valoreSconto = 0
            except:
                pass

        self._loading = False
        if tipoSconto == "percentuale":
            tipoSconto = "%"
        elif tipoSconto == "valore":
            tipoSconto = "€"
        else:
            tipoSconto = ""

        self.rhesus_button.set_sensitive(True)
        self.annulling_button.set_sensitive(True)
        self._currentRow = {'idArticolo' : idArticolo,
                            'listinoRiga' : listinoRiga,
                            'codiceABarre' : codiceABarre,
                            'codice' : codice,
                            'descrizione' : denominazione,
                            'prezzo' : prezzo,
                            'valoreSconto' : valoreSconto,
                            'tipoSconto' : tipoSconto,
                            'prezzoScontato':prezzoScontato,
                            'quantita' : quantita}


    def on_scontrino_treeview_selection_changed(self, treeSelection):
        (model, iterator) = treeSelection.get_selected()
        if iterator is not None:
            self.delete_button.set_sensitive(True)
            #self.confirm_button.set_sensitive(True)
            self.rhesus_button.set_sensitive(True)
            self.annulling_button.set_sensitive(True)
            self.search_button.set_sensitive(False)
            self.codice_a_barre_entry.set_sensitive(False)
            self.codice_entry.set_sensitive(False)
            self.descrizione_entry.set_sensitive(False)
            # Vado in editing
            self._state = 'editing'
            treeview = self.scontrino_treeview
            model = treeview.get_model()
            self.currentIteratorRow = iterator
            listinoRiga = model.get_value(self.currentIteratorRow, 1)
            idArticolo = model.get_value(self.currentIteratorRow, 0)
            self.lsmodel.clear()
            listiniList = listinoCandidateSel(idArticolo=idArticolo,
                                                idMagazzino=self.id_magazzino)
            listinoPref = Listino().select(idListino=self.id_listino)[0]
            self.lsmodel.append([listinoPref.id,listinoPref.denominazione])
            if listiniList:
                for l in listiniList:
                    if l.denominazione != listinoPref.denominazione:
                        self.lsmodel.append([l.id,l.denominazione])
            self.descrizione_label.set_markup('<b><span foreground="black" size="12000">'\
                                            +model.get_value(self.currentIteratorRow, 2)\
                                            + " - " \
                                            + model.get_value(self.currentIteratorRow, 3)\
                                            +" - " \
                                            +model.get_value(self.currentIteratorRow, 4)\
                                            +'</span></b>')


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
                        self._currentRow['listinoRiga'][1][0:10],
                        self._currentRow['codiceABarre'],
                        self._currentRow['codice'],
                        self._currentRow['descrizione'],
                        mN(self._currentRow['prezzo']),
                        mN(self._currentRow['valoreSconto']),
                        self._currentRow['tipoSconto'],
                        mN(self._currentRow['prezzoScontato']),
                        Decimal(self._currentRow['quantita'])))
        elif self._state == 'editing':
            model.set_value(self.currentIteratorRow, 0, self._currentRow['idArticolo'])
            model.set_value(self.currentIteratorRow, 1, self._currentRow['listinoRiga'][1][0:10])
            model.set_value(self.currentIteratorRow, 2, self._currentRow['codiceABarre'])
            model.set_value(self.currentIteratorRow, 3, self._currentRow['codice'])
            model.set_value(self.currentIteratorRow, 4, self._currentRow['descrizione'])
            model.set_value(self.currentIteratorRow, 5, mN(self._currentRow['prezzo']))
            model.set_value(self.currentIteratorRow, 6, mN(self._currentRow['valoreSconto']))
            model.set_value(self.currentIteratorRow, 7, self._currentRow['tipoSconto'])
            model.set_value(self.currentIteratorRow, 8, mN(self._currentRow['prezzoScontato']))
            model.set_value(self.currentIteratorRow, 9, Decimal(self._currentRow['quantita']))

        self.marginevalue_label.set_text('')
        self.ultimocostovalue_label.set_text('')
        self.empty_current_row()
        self.scontrino_treeview.scroll_to_cell(str(len(model)-1))
        self.righe_label.set_markup('<b>'+ " [ "+str(len(model)) +" ] Righe scontrino"+'</b>')
        # Disabilito cancella e conferma e abilito ricerca barcode
        self.delete_button.set_sensitive(False)
        self.confirm_button.set_sensitive(False)
        self.rhesus_button.set_sensitive(False)
        self.annulling_button.set_sensitive(False)
        self.codice_a_barre_entry.set_sensitive(True)
        self.codice_entry.set_sensitive(True)
        self.descrizione_entry.set_sensitive(True)

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


    def on_scontrino_treeview_cursor_changed(self,treeview):
        print "PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP"

    def on_cancel_button_clicked(self, button):
        self.empty_current_row()

        # Disabilito cancella e conferma e abilito ricerca barcode
        self.delete_button.set_sensitive(False)
        self.confirm_button.set_sensitive(False)
        self.rhesus_button.set_sensitive(False)
        self.annulling_button.set_sensitive(False)
        self.codice_a_barre_entry.set_sensitive(True)
        self.codice_entry.set_sensitive(True)
        self.descrizione_entry.set_sensitive(True)
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
        quantita = Decimal(self.quantita_entry.get_text())
        self._currentRow['quantita'] = (quantita * -1)
        self.quantita_entry.set_text(str(Decimal(self._currentRow['quantita'])))
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
        self.descrizione_entry.set_sensitive(True)
        self.search_button.set_sensitive(True)
        self.empty_current_row()

        # Calcolo totali
        self.refreshTotal()

        # vado in search
        self._state = 'search'
        self.codice_a_barre_entry.grab_focus()


    def refreshTotal(self):
        total = 0
        model = self.scontrino_treeview.get_model()
        for row in model:
            prezzo = mN(row[5]) or 0
            valoreSconto = mN(row[6]) or 0
            prezzoScontato = mN(row[8]) or 0
            quantita = Decimal(row[9])
            if valoreSconto == 0: #sconto
                total = total + (prezzo * quantita)
            else:
                total = total + (prezzoScontato * quantita)
        if not total:
            total = "0.00"
        self.label_totale.set_markup('<b><span foreground="black" size="38000">' + str(mN(total)) +'</span></b>')
        return total

    def on_empty_button_clicked(self, button):
        self.scontrino_treeview.get_model().clear()
        self.empty_current_row()
        self.label_totale.set_markup('<b><span foreground="black" size="38000">0.00</span></b>')
        self.label_resto.set_markup('<b><span foreground="black" size="24000">0.00</span></b>')
        self.empty_button.set_sensitive(False)
        self.total_button.set_sensitive(False)
        self.setPagamento(enabled = False)
        self.codice_a_barre_entry.grab_focus()

    def on_total_button_clicked(self, button):
        totale_scontrino = mN(self.refreshTotal())
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
        dao = TestataScontrino()

        dao.totale_scontrino = totale_scontrino
        totale_contanti = 0
        totale_assegni = 0
        totale_carta_di_credito = 0

        if self.contanti_entry.get_text() != '':
            totale_contanti = mN(self.contanti_entry.get_text())
            resto = totale_contanti - dao.totale_scontrino
            self.label_resto.set_markup('<b><span foreground="black" size="24000">' + str(resto) +'</span></b>')
        if self.non_contanti_entry.get_text() != '':
            if self.assegni_radio_button.get_active():
                totale_assegni = mN(self.non_contanti_entry.get_text())
            else:
                totale_carta_di_credito = mN(self.non_contanti_entry.get_text())

        dao.totale_contanti = totale_contanti
        dao.totale_assegni = totale_assegni
        dao.totale_carta_credito = totale_carta_di_credito

        # Creo righe
        righe = []
        model = self.scontrino_treeview.get_model()
        for row in model:
            idArticolo = row[0]
            descrizione = row[4]
            prezzo = mN(row[5])
            valoreSconto = mN(row[6])
            tipoSconto = row[7]
            prezzoScontato = mN(row[8])
            quantita = Decimal(row[9])

            # Nuova riga
            daoRiga = RigaScontrino()
            daoRiga.id_testata_scontrino = dao.id
            daoRiga.id_articolo = idArticolo
            daoRiga.descrizione = descrizione
            daoRiga.prezzo = prezzo
            daoRiga.prezzo_scontato = prezzoScontato
            daoRiga.quantita = quantita
            listarighesconto = []
            if valoreSconto > 0:
                daoScontoRigaScontrino = ScontoRigaScontrino()
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
        self.descrizione_entry.set_sensitive(True)
        self.confirm_button.set_sensitive(False)
        self.rhesus_button.set_sensitive(False)
        self.annulling_button.set_sensitive(False)
        self.delete_button.set_sensitive(False)
        self.on_empty_button_clicked(self.empty_button)
        self.righe_label.set_markup('<b>'+ " [ 0 ] Righe scontrino"+'</b>')
        self._state = 'search'

    def on_chiusura_fiscale_activate(self, widget):
        # Chiedo conferma
        GestioneChiusuraFiscale(self).chiusuraDialog(widget, self.id_magazzino)

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

        #stringa = '10                %09.2f00\r\n' % (totale_contanti)
        #f.write(stringa)
        #stringa='70                00000000000..\r\n'
        #f.write(stringa)
        stringa = '10                %09.2f00\r\n' % (totale_contanti)
        f.write(stringa)
        #stringa='71      Francesco Meloni     ..\r\n'
        #f.write(stringa)
        #stringa='71 CIAO A TUTTI              ..\r\n'
        #f.write(stringa)
        #stringa='71ARRIVEDERCI ALLA PROSSIMA  ..\r\n'
        #f.write(stringa)
        #stringa='72                00000000000..\r\n'
        #f.write(stringa)
        f.close()
        return filename


    def on_stampa_del_giornale_breve_activate(self, widget):
        filename = Environment.conf.VenditaDettaglio.export_path + 'stampa_del_giornale_breve_' + datetime.date.today().strftime('%d_%m_%Y_%H_%M_%S')
        f = file(filename,'w')
        stringa = '52                00000000002..\r\n'
        f.write(stringa)
        f.close()
        self.sendToPrint(filename)

    def on_stampa_del_periodico_cassa_activate(self, widget):
        filename = Environment.conf.VenditaDettaglio.export_path + 'stampa_del_periodico_cassa_' + datetime.date.today().strftime('%d_%m_%Y_%H_%M_%S')
        f = file(filename,'w')
        stringa = '52                00000000004..\r\n'
        f.write(stringa)
        f.close()
        self.sendToPrint(filename)

    def on_stampa_del_periodico_reparti_activate(self, widget):
        filename = Environment.conf.VenditaDettaglio.export_path + 'stampa_del_periodico_reparti_' + datetime.date.today().strftime('%d_%m_%Y_%H_%M_%S')
        f = file(filename,'w')
        stringa = '52                00000000006..\r\n'
        f.write(stringa)
        f.close()
        self.sendToPrint(filename)

    def on_stampa_del_periodico_articoli_activate(self, widget):
        filename = Environment.conf.VenditaDettaglio.export_path + 'stampa_del_periodico_articoli_' + datetime.date.today().strftime('%d_%m_%Y_%H_%M_%S')
        f = file(filename,'w')
        stringa = '52                00000000008..\r\n'
        f.write(stringa)
        f.close()
        self.sendToPrint(filename)

    def on_stampa_della_affluenza_oraria_activate(self, widget):
        filename = Environment.conf.VenditaDettaglio.export_path + 'stampa_della_affluenza_oraria_' + datetime.date.today().strftime('%d_%m_%Y_%H_%M_%S')
        f = file(filename,'w')
        stringa = '52                00000000009..\r\n'
        f.write(stringa)
        f.close()
        self.sendToPrint(filename)

    def sendToPrint(self, filesToSend):
        # Mando comando alle casse
        program_launch = Environment.conf.VenditaDettaglio.driver_command
        program_params = (' ' + filesToSend + ' ' +
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

        # Elimino il file
        os.remove(filesToSend)
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

    def ricercaArticolo(self):

        def on_ricerca_articolo_hide(anagWindow, anag):
            if anag.dao is None:
                anagWindow.destroy()
                return
            valoreSconto = 0
            tipoSconto = 'percentuale'
            anagWindow.destroy()
            idArticolo = anag.dao.id
            codiceABarre = anag.dao.codice_a_barre or ''
            codice = anag.dao.codice or ''
            descrizione = anag.dao.descrizione_etichetta or anag.dao.denominazione or ''
            # Ricerca listino_articolo
            listino = leggiListino(self.id_listino, idArticolo)
            #prezzo = listino["prezzoDettaglio"]
            listinoRiga = (self.id_listino, listino['denominazione'][0:10])
            prezzo = mN(listino["prezzoDettaglio"])
            prezzoScontato = prezzo
            tipoSconto = None
            if listino.has_key('scontiDettaglio'):
                if  len(listino["scontiDettaglio"]) > 0:
                    valoreSconto = listino['scontiDettaglio'][0].valore or 0
                    if valoreSconto == 0:
                        tipoSconto = None
                        prezzoScontato = prezzo
                    else:
                        tipoSconto = listino['scontiDettaglio'][0].tipo_sconto
                        if tipoSconto == "percentuale":
                            prezzoScontato = mN(mN(prezzo) - (mN(prezzo) * mN(valoreSconto)) / 100)
                        else:
                            prezzoScontato = mN(mN(prezzo) -mN(valoreSconto))
            quantita = 1

            self.activate_item(idArticolo,
                                listinoRiga,
                               codiceABarre,
                               codice or '',
                               descrizione,
                               prezzo,
                               valoreSconto,
                               tipoSconto,
                               prezzoScontato,
                               quantita)

            self.prezzo_entry.grab_focus()
            try:
                if Environment.conf.VenditaDettaglio.direct_confirm == "yes":
                    self.on_confirm_button_clicked(self.getTopLevel())
                    self.refreshTotal()
            except:
                pass

        from promogest.ui.RicercaComplessaArticoli import RicercaComplessaArticoli
        codiceABarre = self.codice_a_barre_entry.get_text()
        codice = self.codice_entry.get_text()
        descrizione = self.descrizione_entry.get_text()
        anag = RicercaComplessaArticoli(codiceABarre = codiceABarre,
                                        codice = codice,
                                        denominazione=descrizione)
        anag.setTreeViewSelectionType(gtk.SELECTION_SINGLE)
        anagWindow = anag.getTopLevel()
        anagWindow.connect("hide",
                           on_ricerca_articolo_hide, anag)
        anagWindow.set_transient_for(self.getTopLevel())
        anagWindow.show_all()


    def on_new_button_clicked(self, button):
        """
            open the anagraficaArticolo Semplice to add a new article
        """
        from promogest.ui.AnagraficaArticoliSemplice import AnagraficaArticoliSemplice
        anag = AnagraficaArticoliSemplice()
        anagWindow = anag.getTopLevel()
        showAnagraficaRichiamata(self.getTopLevel(), anagWindow, button)

    def ricercaListino(self):
        """
            check if there is a priceList like setted on configure file
        """
        pricelist = Listino().select(denominazione = Environment.conf.VenditaDettaglio.listino,
                                    offset = None,
                                    batchSize = None)
        if len(pricelist) > 0:
            id_listino = pricelist[0].id
        else:
            id_listino = None
        return id_listino

    def on_total_button_grab_focus(self, button):
        totale_scontrino = mN(self.label_totale.get_text())
        if self.contanti_entry.get_text() != '':
            totale_pagamento = mN(self.contanti_entry.get_text())
        elif self.non_contanti_entry.get_text() != '':
            totale_pagamento = mN(self.non_contanti_entry.get_text())
        else:
            totale_pagamento = 0
        resto = totale_pagamento - totale_scontrino
        self.label_resto.set_markup('<b><span size="xx-large">' + str(resto) + '</span></b>')

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
            self.non_contanti_entry.set_text(str(self.refreshTotal()))
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

        ts = TestataScontrino().getRecord(id=self.idRhesusSource[0])
        for r in ts.righe:
            idArticolo = r.id_articolo
            codiceArticolo = r.codice_articolo or ''
            codiceABarre = r.codice_a_barre or ''
            descrizione = r.descrizione or ''
            prezzo = mN(r.prezzo or 0)
            quantita = -1 * mN(r.quantita or 0)
            tipoSconto = None
            sconto = mN(r.valore_sconto or 0)
            prezzoScontato = mN(r.prezzo_scontato or 0)
            if sconto != 0:
                if r.tipo_sconto == 'percentuale':
                    tipoSconto = self._simboloPercentuale
                else:
                    tipoSconto = self._simboloEuro
            listinoRiga = ""
            model.append((idArticolo,
                            listinoRiga,
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
        #FIXME: attenzione funzioen da rifareeeeeeeeeeeeeeeee
        #movs = Environment.connection.execStoredProcedure('ScaricoScontrinoSel', (None, Environment.conf.workingYear, idArticolo, idMagazzino, False))
        #for m in movs:
            #totGiacenza += ((m['scarico_qta'] or 0 ) * -1)
        return totGiacenza

    def on_scontrino_treeview_button_press_event(self, treeview, event):
        if event.button == 3:
                x = int(event.x)
                y = int(event.y)
                time = event.time
                pthinfo = treeview.get_path_at_pos(x, y)
                if pthinfo is not None:
                    path, col, cellx, celly = pthinfo
                    treeview.grab_focus()
                    treeview.set_cursor( path, col, 0)
                    self.file_menu.popup( None, None, None, event.button, time)
                return 1

    def createPopupMenu(self):
        self.file_menu = gtk.Menu()    # Don't need to show menus
        # Create the menu items
        open_item = gtk.MenuItem("Conferma")
        #save_item = gtk.MenuItem("Cancella")
        quit_item = gtk.MenuItem("Annulla")
        # Add them to the menu
        self.file_menu.append(open_item)
        #self.file_menu.append(save_item)
        self.file_menu.append(quit_item)
        # Attach the callback functions to the activate signal
        open_item.connect_object("activate", self.on_confirm_button_clicked, "file.open")
        #save_item.connect_object("activate", self.on_empty_button_clicked, "file.save")
        quit_item.connect_object ("activate", self.on_cancel_button_clicked, "file.quit")

        # We do need to show menu items
        open_item.show()
        #save_item.show()
        quit_item.show()

    def on_sconti_scontrino_widget_button_toggled(self, button):
        pippo = self.sconti_scontrino_widget.getSconti()
        return


















    #def on_prezzo_entry_focus_out_event(self, entry, event):
        #prezzo = mN(self.prezzo_entry.get_text().strip())
        #self._currentRow['prezzo'] = prezzo
        #if self._currentRow['valoreSconto'] == 0:
            #self._currentRow['prezzoScontato'] = prezzo
            #self.prezzo_scontato_entry.set_text(str(mN(self._currentRow['prezzoScontato'])).strip())
            ##self.marginevalue_label.set_markup('<b>'+'%-6.3f' % calcolaMargine(float(self.fornitura["prezzoNetto"]),
                                                                   ##float(self._currentRow['prezzoScontato']),
                                                                   ##float(self.art["percentualeAliquotaIva"]))+ '</b>')
            #self.marginevalue_label.set_text('')
        #else:
            #if self._currentRow['tipoSconto'] == self._simboloPercentuale:
                #self._currentRow['prezzoScontato'] = prezzo - ((prezzo) * (mN(self._currentRow['valoreSconto']) / 100))
                #self.prezzo_scontato_entry.set_text(str( self._currentRow['prezzoScontato']))
                #self.marginevalue_label.set_text('')
            #else:
                #self._currentRow['prezzoScontato'] = prezzo - mN(self._currentRow['valoreSconto'])
                #self.prezzo_scontato_entry.set_text(str(mN(self._currentRow['prezzoScontato'])))
                #self.marginevalue_label.set_text('')

    #def on_prezzo_entry_key_press_event(self, widget, event):
        #keyname = gtk.gdk.keyval_name(event.keyval)
        #if keyname == 'Return' or keyname == 'KP_Enter':
            #self.quantita_entry.grab_focus()

    #def on_prezzo_scontato_entry_focus_out_event(self, entry, event):
        #prezzoScontato = mN(self.prezzo_scontato_entry.get_text())
        #self._currentRow['prezzoScontato'] = prezzoScontato
        #if abs(mN(self._currentRow['prezzo']) - self._currentRow['prezzoScontato']) > 0:
            #if self._currentRow['tipoSconto'] == self._simboloPercentuale:
                #self._currentRow['valoreSconto'] = 100 * (1 - mN(self._currentRow['prezzoScontato']) / mN(self._currentRow['prezzo']))
                #self.sconto_entry.set_text(str(mN(self._currentRow['valoreSconto'])))
                #self.sconto_entry.tipoSconto = 'percentuale'
                #self.marginevalue_label.set_markup('<b>'+"%s" % str(calcolaMargine(mN(self.fornitura["prezzoNetto"]),
                                                                   #mN(self._currentRow['prezzoScontato']),
                                                                   #mN(str(self.art["percentualeAliquotaIva"]))))+ '</b>')
            #else:
                #self._currentRow['valoreSconto'] = mN(self._currentRow['prezzo']) - mN(self._currentRow['prezzoScontato'])
                #self.sconto_entry.set_text(str(mN(self._currentRow['valoreSconto'])))
                #self.sconto_entry.tipoSconto = 'valore'
                #self.marginevalue_label.set_markup('<b>'+'%s' % str(calcolaMargine(mN(self.fornitura["prezzoNetto"]),
                                                                   #mN(self._currentRow['prezzoScontato']),
                                                                   #mN(self.art["percentualeAliquotaIva"])))+ '</b>')

    #def on_prezzo_scontato_entry_key_press_event(self, widget, event):
        #keyname = gtk.gdk.keyval_name(event.keyval)
        #if keyname == 'Return' or keyname == 'KP_Enter':
            #self.confirm_button.grab_focus()

    #def on_sconto_entry_focus_out_event(self, entry, event):
        #self._currentRow['valoreSconto'] = mN(self.sconto_entry.get_text())
        #if self.sconto_entry.tipoSconto == 'percentuale':
            #self._currentRow['tipoSconto'] = self._simboloPercentuale
        #else:
            #self._currentRow['tipoSconto'] = self._simboloEuro
        #if self._currentRow['valoreSconto'] == 0:
            #self._currentRow['tipoSconto'] = None
            #self._currentRow['prezzoScontato'] = mN(self._currentRow['prezzo'])
            #self.prezzo_scontato_entry.set_text(str(mN(self._currentRow['prezzoScontato'])))
            #self.marginevalue_label.set_markup('<b>'+'%s' % str(calcolaMargine(mN(self.fornitura["prezzoNetto"]),
                                                                   #mN(self._currentRow['prezzoScontato']),
                                                                   #mN(self.art["percentualeAliquotaIva"])))+ '</b>')
        #else:
            #if self._currentRow['tipoSconto'] == self._simboloPercentuale:
                #self._currentRow['prezzoScontato'] = mN(self._currentRow['prezzo']) - (mN(self._currentRow['prezzo']) * mN(self._currentRow['valoreSconto'])) / 100
                #self.prezzo_scontato_entry.set_text(str(mN(self._currentRow['prezzoScontato'])).strip())
                #self.marginevalue_label.set_markup('<b>'+'%s' % str(calcolaMargine(mN(self.fornitura["prezzoNetto"]),
                                                                   #mN(self._currentRow['prezzoScontato']),
                                                                   #Decimal(str(self.art["percentualeAliquotaIva"]))))+ '</b>')
            #else:
                #self._currentRow['prezzoScontato'] = mN(self._currentRow['prezzo']) - mN(self._currentRow['valoreSconto'])
                #self.prezzo_scontato_entry.set_text(str(mN(self._currentRow['prezzoScontato'])))
                #self.marginevalue_label.set_markup('<b>'+'%s' % str(calcolaMargine(mN(self.fornitura["prezzoNetto"]),
                                                                   #mN(self._currentRow['prezzoScontato']),
                                                                   #Decimal(str(self.art["percentualeAliquotaIva"]))))+ '</b>')

    #def on_quantita_entry_focus_out_event(self, entry, event):
        #self._currentRow['quantita'] = Decimal(self.quantita_entry.get_text().strip())

    #def on_quantita_entry_key_press_event(self, widget, event):
        #keyname = gtk.gdk.keyval_name(event.keyval)
        #if keyname == 'Return' or keyname == 'KP_Enter':
            #self.confirm_button.grab_focus()


        #listino = ListinoArticolo()
        #self.art = leggiArticolo(idArticolo)
        #if listino.ultimo_costo is None:
            #self.fornitura = leggiFornitura(idArticolo)
            #self.ultimocostovalue_label.set_markup('<b>' + str(mN(self.fornitura["prezzoNetto"])) + '</b>')
        #else:
            #self.ultimocostovalue_label.set_markup('<b>' + str(mN(listino.ultimo_costo or 0)) + '</b>')

        #if prezzoScontato == prezzo:
            #self.marginevalue_label.set_markup('<b>'+ "%s" % str(calcolaMargine(mN(self.fornitura["prezzoNetto"]),
                                                                   #mN(prezzo),
                                                                   #mN(self.art["percentualeAliquotaIva"])))+ '</b>')
        #else:
            #self.marginevalue_label.set_markup('<b>'+"%s" % str(calcolaMargine(mN(self.fornitura["prezzoNetto"]),
                                                                   #mN(prezzoScontato),
                                                                   #mN(self.art["percentualeAliquotaIva"])))+ '</b>')
        #giacenza = self.getGiacenzaArticolo(idArticolo=idArticolo)
        #self.giacenza_label.set_markup('<b>' + str(mN(giacenza)) + '</b>')