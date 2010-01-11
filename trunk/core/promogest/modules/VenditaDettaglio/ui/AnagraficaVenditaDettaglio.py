# -*- coding: utf-8 -*-

# Promogest
#
# Copyright (C) 2005 by Promotux Informatica - http://www.promotux.it/
# Author: Alessandro Scano <alessandro@promotux.it>
# Author: Francesco Meloni <francescoo@promotux.it>

from promogest.ui.utils import *
import gtk
from  subprocess import *
from datetime import datetime
from promogest import Environment
from promogest.ui.GladeWidget import GladeWidget
from promogest.modules.VenditaDettaglio.dao.TestataScontrino import TestataScontrino
from promogest.modules.VenditaDettaglio.dao.RigaScontrino import RigaScontrino
from promogest.modules.VenditaDettaglio.dao.ScontoRigaScontrino import ScontoRigaScontrino
from promogest.modules.VenditaDettaglio.dao.ScontoTestataScontrino import ScontoTestataScontrino
from promogest.dao.Articolo import Articolo
from promogest.dao.Listino import Listino
from promogest.dao.ListinoArticolo import ListinoArticolo
from GestioneScontrini import GestioneScontrini
from GestioneChiusuraFiscale import GestioneChiusuraFiscale
from venditaDettaglioUiPart import drawPart

if hasattr(Environment.conf.VenditaDettaglio,"backend") and\
    Environment.conf.VenditaDettaglio.backend.upper() =="OLIVETTI" and\
    Environment.conf.VenditaDettaglio.disabilita_stampa == 'no':
    from promogest.modules.VenditaDettaglio.lib.olivetti import ElaExecute
#    print "DRIVER OLIVETTI ANCORA DA FARE"
    DRIVER = "E"
elif hasattr(Environment.conf.VenditaDettaglio,"backend") and\
    Environment.conf.VenditaDettaglio.backend.capitalize() == "DITRON" and\
    Environment.conf.VenditaDettaglio.disabilita_stampa == 'no':
    from promogest.modules.VenditaDettaglio.lib.ditron import Ditron
    DRIVER = "D"
elif Environment.conf.VenditaDettaglio.disabilita_stampa == 'yes':
    DRIVER = None
else:
    print "ERRORE NELLA DEFINIZIONE DEL BACKEND"
    from promogest.modules.VenditaDettaglio.lib.ditron import Ditron
    DRIVER = "D"

class AnagraficaVenditaDettaglio(GladeWidget):
    """ Frame per la gestione delle vendite a dettaglio """

    def __init__(self):
        GladeWidget.__init__(self, 'vendita_dettaglio_window',
                        fileName='VenditaDettaglio/gui/vendita_dettaglio_window.glade',
                        isModule=True)
        self.placeWindow(self.getTopLevel())
        self._currentRow = {}
        self._simboloPercentuale = '%'
        self._simboloEuro = '€'
        textStatusBar = "     PromoGest2 - Vendita Dettaglio - by PromoTUX Informatica - 800 034561 - www.PromoTUX.it - info@PromoTUX.it      "
        context_id = self.vendita_dettaglio_statusbar.get_context_id("vendita_dettaglio_window")
        self.vendita_dettaglio_statusbar.push(context_id, textStatusBar)
        azienda = Azienda().getRecord(id=Environment.params["schema"])
        self.logo_articolo.set_from_file(azienda.percorso_immagine)
        self.createPopupMenu()
        #nascondo i dati riga e le info aggiuntive
        self.dati_riga_frame.destroy()
        self.shop = Environment.shop
        self.draw()

    def draw(self):
        drawPart(self)

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
                listin = leggiListino(l[0],model[path][0])
                break
        prez = str(listin['prezzoDettaglio'])
        if listin.has_key('scontiDettaglio'):
                if  len(listin["scontiDettaglio"]) > 0:
                    model[path][6]= listin['scontiDettaglio'][0].valore or 0
                else:
                    model[path][6] = 0
        self.on_column_prezzo_edited(cell, path, prez, treeview)

    def on_column_quantita_edited(self, cell, path, value, treeview, editNext=True):
        """ Set the value "quantita" edit in the cell """
        model = treeview.get_model()
        value=value.replace(",",".")
        value = mN(value)
        model[path][9] = value
        self.refreshTotal()
        self.on_cancel_button_clicked(self.getTopLevel)

    def on_column_descrizione_edited(self, cell, path, value, treeview, editNext=True):
        """ Set the value descrizione edit in the cell """
        model = treeview.get_model()
        model[path][4] = value
        self.on_cancel_button_clicked(self.getTopLevel)

    def on_column_tipo_edited(self, cell, path, value, treeview, editNext=True):
        """ Set the value tipo_sconto edit in the cell"""
        model = treeview.get_model()
        model[path][7] = value
        scont = model[path][6]
        self.on_column_sconto_edited(cell, path, scont, treeview)

    def on_vendita_dettaglio_window_key_press_event(self, widget, event):
        """ jolly key è F9, richiama ed inserisce l'articolo definito nel configure"""
        keyname = gtk.gdk.keyval_name(event.keyval)
        if keyname == 'F9':
            try:
                codice = Environment.conf.VenditaDettaglio.jolly
                self.search_item(codice=codice, fnove=True)
            except:
                Environment.pg2log.info("ARTICOLO JOLLY NON SETTATO NEL CONFIGURE NELLA SEZIONE [VenditaDettaglio]")

    def fnovewidget(self,codice=None, destroy=None):
        if destroy:
            prezzo1 = self.prezzo_f9_entry.get_text()
            quantita1 = self.quantita_f9_entry.get_text()
            self.articolo_generico_dialogo.hide()
            self.search_item(codice=self.codi,fnove=True,valorigenerici=(quantita1,prezzo1) )
        else:
            self.codi =  codice
            self.prezzo_f9_entry.set_text("")
            self.quantita_f9_entry.set_text("1")
            self.dialog_genrico_vbox.show_all()
            self.articolo_generico_dialogo.show_all()

    def on_generico_ok_button_clicked(self, button):
        self.fnovewidget(destroy=True)

    def on_annulla_generico_button_clicked(self, button):
        self.articolo_generico_dialogo.hide()

    def on_minus_button_clicked(self, button):
        valore = int(abs(float(self.prezzo_f9_entry.get_text())))
        self.prezzo_f9_entry.set_text(str(valore-1))

    def on_plus_button_clicked(self, button):
        valore = int(abs(float(self.prezzo_f9_entry.get_text())))
        self.prezzo_f9_entry.set_text(str(valore+1))

    def on_minus2_button_clicked(self, button):
        valore = int(abs(float(self.quantita_f9_entry.get_text())))
        self.quantita_f9_entry.set_text(str(valore-1))

    def on_plus2_button_clicked(self, button):
        valore = int(abs(float(self.quantita_f9_entry.get_text())))
        self.quantita_f9_entry.set_text(str(valore+1))

    def search_item(self, codiceABarre=None, codice=None,
                                valorigenerici=[], descrizione=None,
                                fnove=False):
        # Ricerca articolo per barcode
        if codiceABarre is not None:
            arts = Articolo().select(codiceABarre = codiceABarre,
                                                 offset = None,
                                                 batchSize = None)
        elif codice is not None:
            arts = Articolo().select(codice = codice,
                                                 offset = None,
                                                 batchSize = None)
        elif descrizione is not None:
            arts = Articolo().select(denominazione = descrizione,
                                                 offset = None,
                                                 batchSize = None)
        if len(arts) == 1:
            idArticolo = arts[0].id
            codice = arts[0].codice or ''
            codiceABarre = arts[0].codice_a_barre or ''
            descrizione = arts[0].descrizione_etichetta or arts[0].denominazione or ''
            # Ricerca listino_articolo
            listino = leggiListino(self.id_listino, idArticolo)
            if fnove and not valorigenerici:
                self.fnovewidget(codice=codice)
            elif fnove and valorigenerici:
                quantita = valorigenerici[0] or 1
                prezzo = mN(valorigenerici[1]) or 0
            else:
                prezzo = mN(listino["prezzoDettaglio"])
                quantita = 1
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


            self.codice_a_barre_entry.set_text(codiceABarre)
            self.codice_entry.set_text(codice)
            self.activate_item(idArticolo, listinoRiga, codiceABarre,codice,
                               descrizione, prezzo, valoreSconto,tipoSconto,
                               prezzoScontato, quantita)
            #self.confirm_button.grab_focus()
            #if not fnove:
            self.on_confirm_button_clicked(self.getTopLevel())
            self.refreshTotal()
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
        #self.annulling_button.set_sensitive(True)
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
            #self.annulling_button.set_sensitive(True)
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
            self._quantita = model.get_value(self.currentIteratorRow, 9)
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
            self.refreshTotal()

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
            #self.prezzo_entry.grab_focus()
            self._state == 'editing'
            #return

        treeview = self.scontrino_treeview
        model = treeview.get_model()

        if self._state == 'search':
            model.append((self._currentRow['idArticolo'],
                        self._currentRow['listinoRiga'][1],
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
            model.set_value(self.currentIteratorRow, 1, self._currentRow['listinoRiga'][1])
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
        self.righe_label.set_markup('<b>[ '+str(len(model)) +' ] Righe scontrino</b>')
        # Disabilito cancella e conferma e abilito ricerca barcode
        self.delete_button.set_sensitive(False)
        #self.confirm_button.set_sensitive(False)
        self.rhesus_button.set_sensitive(False)
        #self.annulling_button.set_sensitive(False)
        self.codice_a_barre_entry.set_sensitive(True)
        self.codice_entry.set_sensitive(True)
        self.descrizione_entry.set_sensitive(True)

        self.search_button.set_sensitive(True)
        # Abilito pulsante totale e annulla
        notEmpty = (len(model) > 0)
        self.total_button.set_sensitive(notEmpty)
        self.subtotal_button.set_sensitive(notEmpty)
        self.empty_button.set_sensitive(notEmpty)
        self.setPagamento(enabled = notEmpty)
        self.sconto_hbox.set_sensitive(notEmpty)

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
        self.rhesus_button.set_sensitive(False)
        self.codice_a_barre_entry.set_sensitive(True)
        self.codice_entry.set_sensitive(True)
        self.descrizione_entry.set_sensitive(True)
        self.search_button.set_sensitive(True)

        treeview = self.scontrino_treeview
        model = treeview.get_model()

        # Abilito pulsante totale e annulla
        notEmpty = (len(model) > 0)
        self.total_button.set_sensitive(notEmpty)
        self.subtotal_button.set_sensitive(notEmpty)
        self.empty_button.set_sensitive(notEmpty)
        self.setPagamento(enabled = notEmpty)
        self.sconto_hbox.set_sensitive(notEmpty)
        treeview.get_selection().unselect_all()
        # vado in search
        self._state = 'search'
        self.codice_a_barre_entry.grab_focus()

    def on_rhesus_button_clicked(self, button):
        selection = self.scontrino_treeview.get_selection()
        (model, iter) = selection.get_selected()
        quantita = model.get_value(iter, 9)
        model[iter][9]= Decimal(quantita)* -1
        self.refreshTotal()
        self.on_cancel_button_clicked(self.getTopLevel)

    def on_delete_button_clicked(self, button):
        treeview = self.scontrino_treeview
        model = treeview.get_model()
        model.remove(self.currentIteratorRow)

        # Se era l'ultima riga disabilito text box e pulsanti per totali
        notEmpty = (len(model) > 0)
        self.total_button.set_sensitive(notEmpty)
        self.subtotal_button.set_sensitive(notEmpty)
        self.empty_button.set_sensitive(notEmpty)
        self.setPagamento(enabled = notEmpty)
        self.sconto_hbox.set_sensitive(notEmpty)

        # Disabilito cancella e conferma e abilito ricerca barcode
        self.delete_button.set_sensitive(False)
        self.rhesus_button.set_sensitive(False)
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
        """ Here we can calculate subTotals and Totals of the sales
        """
        total = 0
        totale_scontato = "0.00"
        totale_sconto = "0.00"
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
            totale_scontato = "0.00"
            totale_sconto = "0.00"
        else:
            self.sconto = self.sconto_totale_entry.get_text()
            if self.tipo_sconto_euro.get_active():
                self.tipo_sconto_scontrino = "valore"
                totale_sconto = Decimal(self.sconto or 0)
                totale_scontato = total-totale_sconto
            else:
                self.tipo_sconto_scontrino = "percentuale"
                if not self.sconto:
                    totale_scontato = total
                else:
                    totale_sconto = total*(Decimal(self.sconto)/100)
                    totale_scontato = total-totale_sconto

        self.label_totale.set_markup('<b><span foreground="black" size="40000">' + str(mN(totale_scontato)) +'</span></b>')
        self.label_sconto.set_markup('<b><span foreground="#338000" size="24000">' + str(mN(totale_sconto)) +'</span></b>')
        self.label_subtotale.set_markup('<b><span foreground="#338000" size="26000">' + str(mN(total)) +'</span></b>')

        return (totale_scontato,total,totale_sconto, self.sconto)

    def on_empty_button_clicked(self, button):
        self.scontrino_treeview.get_model().clear()
        self.empty_current_row()
        self.label_totale.set_markup('<b><span foreground="black" size="40000">0.00</span></b>')
        self.label_resto.set_markup('<b><span foreground="black" size="24000">0.00</span></b>')
        self.label_subtotale.set_markup('<b><span foreground="black" size="24000">0.00</span></b>')
        self.label_sconto.set_markup('<b><span foreground="black" size="26000">0.00</span></b>')
        self.empty_button.set_sensitive(False)
        self.total_button.set_sensitive(False)
        self.subtotal_button.set_sensitive(False)
        self.setPagamento(enabled = False)
        self.sconto_totale_entry.set_text("")
        self.sconto_hbox.set_sensitive(False)
        self.codice_a_barre_entry.grab_focus()

    def on_total_button_clicked(self, button):
        self.refreshTotal()

        dao = TestataScontrino()
        dao.data_inserimento = datetime.now()
        dao.totale_scontrino = mN(self.label_totale.get_text())
        dao.totale_sconto = mN(self.sconto_totale_entry.get_text())
        dao.totale_subtotale = mN(self.label_subtotale.get_text())
        dao.tipo_sconto_scontrino = self.tipo_sconto_scontrino

        #print "TOTALI",totale_scontrino,  totale_sconto, totale_subtotale

        if dao.totale_scontrino < 0:
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
        scontiSuTotale = []
        #res = self.sconti_testata_widget.getSconti()
        if dao.totale_sconto:
            daoSconto = ScontoTestataScontrino()
            daoSconto.valore = dao.totale_sconto
            daoSconto.tipo_sconto = dao.tipo_sconto_scontrino
            scontiSuTotale.append(daoSconto)
        dao.scontiSuTotale = scontiSuTotale

        #dao.totale_scontrino = totale_scontrino
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

        # Creo il file e lo stampo
        if DRIVER:
            filescontrino = self.createFileToPos(dao)

        # Svuoto transazione e mi rimetto in stato di ricerca
        self.search_button.set_sensitive(True)
        self.codice_a_barre_entry.set_sensitive(True)
        self.codice_entry.set_sensitive(True)
        self.descrizione_entry.set_sensitive(True)
        #self.confirm_button.set_sensitive(False)
        self.rhesus_button.set_sensitive(False)
        #self.annulling_button.set_sensitive(False)
        self.delete_button.set_sensitive(False)
        self.on_empty_button_clicked(self.empty_button)
        self.righe_label.set_markup('<b> [ 0 ] Righe scontrino</b>')
        self.codice_a_barre_entry.grab_focus()
        self._state = 'search'

    def on_chiusura_fiscale_activate(self, widget):
        if DRIVER=="D":
            GestioneChiusuraFiscale(self).chiusuraDialog(widget, self.id_magazzino)

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
            listinoRiga = (self.id_listino, listino['denominazione'])
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
        """ open the anagraficaArticolo Semplice to add a new article
        """
        return
        from promogest.ui.AnagraficaArticoliSemplice import AnagraficaArticoliSemplice
        anag = AnagraficaArticoliSemplice()
        anagWindow = anag.getTopLevel()
        showAnagraficaRichiamata(self.getTopLevel(), anagWindow, button)

    def ricercaListino(self):
        """ check if there is a priceList like setted on configure file
        """
        pricelist = Listino().select(denominazione = Environment.conf.VenditaDettaglio.listino,
                                    offset = None,
                                    batchSize = None)

        if pricelist and len(pricelist) > 0:
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
        self.label_resto.set_markup('<b><span size="xx-large">'+ str(resto) +'</span></b>')

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
        self.refreshTotal()

    def on_non_contanti_clicked(self):
        #predisposizione per il pagamento non in contanti
        if self.total_button.get_property('sensitive'):
            self.non_contanti_entry.set_sensitive(True)
            self.non_contanti_entry.grab_focus()
            self.non_contanti_entry.set_text(str(self.refreshTotal()[0]))
            self.contanti_entry.set_text('')
            self.contanti_entry.set_sensitive(False)
        else:
            self.contanti_entry.set_sensitive(False)
            self.non_contanti_entry.set_sensitive(False)
        self.refreshTotal()

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
        if self.shop:
            dialog = gtk.MessageDialog(self.getTopLevel(),
                                   gtk.DIALOG_MODAL
                                   | gtk.DIALOG_DESTROY_WITH_PARENT,
                                   gtk.MESSAGE_QUESTION, gtk.BUTTONS_YES_NO,
                                   'Confermi la chiusura?')
            response = dialog.run()
            dialog.destroy()
            if response ==  gtk.RESPONSE_YES:
                self.hide()
                Environment.pg2log.info("CHIUDO IL MODULO DI GESTIONE NEGOZIO APERTO CON SHOP")
                gtk.main_quit()
            else:
                return
        else:
            self.destroy()
            return None

    def createFileToPos(self, dao):
        if DRIVER == "E":
            print "DRIVER OLIVETTI"
            filescontrino = ElaExecute().create_export_file(daoScontrino=dao)
        elif DRIVER =="D":
            print "DRIVER DITRON"
            filescontrino = Ditron().create_export_file(daoScontrino=dao)
            Ditron().sendToPrint(filescontrino)
            return True
        else:
            print " WHAT ELSE?"

    def on_chiusura_fiscale_activate(self, widget):
        if DRIVER=="D":
            GestioneChiusuraFiscale(self).chiusuraDialog(widget, self.id_magazzino)

    def on_stampa_del_giornale_breve_activate(self, widget):
        if DRIVER =="D":
            Ditron().stampa_del_giornale_breve()

    def on_stampa_del_periodico_cassa_activate(self, widget):
        if DRIVER =="D":
            Ditron().stampa_del_periodico_cassa()

    def on_stampa_del_periodico_reparti_activate(self, widget):
        if DRIVER =="D":
            Ditron().stampa_del_periodico_reparti()

    def on_stampa_del_periodico_articoli_activate(self, widget):
        if DRIVER =="D":
            Ditron().stampa_del_periodico_articoli()

    def on_stampa_della_affluenza_oraria_activate(self, widget):
        if DRIVER =="D":
            Ditron().stampa_della_affluenza_oraria()

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

    def on_scontrino_treeview_button_press_event(self, treeview, event):
        if event.button == 3:
                x = int(event.x)
                y = int(event.y)
                time = event.time
                pthinfo = treeview.get_path_at_pos(x, y)
                if pthinfo is not None:
                    path, col, cellx, celly = pthinfo
                    treeview.grab_focus()
                    treeview.set_cursor(path, col, 0)
                    self.file_menu.popup(None, None, None, event.button, time)
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
        quit_item.connect_object("activate", self.on_cancel_button_clicked, "file.quit")

        # We do need to show menu items
        open_item.show()
        #save_item.show()
        quit_item.show()

    def on_subtotal_button_clicked(self, button):
        self.refreshTotal()

    def on_list_button_clicked(self, widget):
        self.idRhesusSource = []
        gest = GestioneScontrini(daData=None, aData=None, righe=self.idRhesusSource)
        gestWnd = gest.getTopLevel()
        showAnagraficaRichiamata(self.getTopLevel(), gestWnd, None, self.creaScontrinoReso)
