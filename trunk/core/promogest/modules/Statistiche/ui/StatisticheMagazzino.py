# -*- coding: utf-8 -*-

# Promogest
#
# Copyright (C) 2005 by Promotux Informatica - http://www.promotux.it/
# Author: Andrea Argiolas <andrea@promotux.it>
# Author: Francesco Meloni  <francesco@promotux.it>

import os
import gtk
import time
import datetime
from promogest.ui.GladeWidget import GladeWidget
from promogest import Environment
from promogest.dao.TestataMovimento import TestataMovimento
from promogest.dao.RigaMovimento import RigaMovimento
from promogest.dao.Riga import Riga
from promogest.dao.Magazzino import Magazzino
from promogest.dao.Operazione import Operazione
from promogest.dao.Stoccaggio import Stoccaggio
from sqlalchemy import or_
from promogest.ui.utils import *
from promogest.ui.utilsCombobox import *
import csv

class StatisticheMagazzino(GladeWidget):

    def __init__(self, idMagazzino=None):

        GladeWidget.__init__(self, 'statistiche_magazzino_dialog',
                'Statistiche/gui/statistiche_magazzino_elements.glade',
                isModule=True)
        self.placeWindow(self.getTopLevel())

        self._idMagazzino = idMagazzino
        self._orderingOrder = []
        self._groupingOrder = []

        self.giacenze_radiobutton.set_active(True)
        self.set_radiobutton_states()
        self.year_combobox.set_active(3)

    def on_window_close(self, widget, event):
        self.destroy()


    def set_radiobutton_states(self, button=None):
        self.active_giacenze_buttons(self.giacenze_radiobutton.get_active())
        self.active_venduti_buttons(self.venduto_radiobutton.get_active())


    def active_giacenze_buttons(self, val):
        self.ultimo_prezzo_acquisto_radiobutton.set_sensitive(val)
        self.ultimo_prezzo_vendita_radiobutton.set_sensitive(val)
        self.prezzo_medio_acquisto_radiobutton.set_sensitive(val)
        self.prezzo_medio_vendita_radiobutton.set_sensitive(val)
        self.ordinamento_famiglia_checkbutton.set_sensitive(val)
        self.ordinamento_categoria_checkbutton.set_sensitive(val)
        self.ordinamento_genere_checkbutton.set_sensitive(val)
        self.ordinamento_fornitore_checkbutton.set_sensitive(val)


    def active_venduti_buttons(self, val):
        self.da_data_entry.set_sensitive(val)
        self.a_data_entry.set_sensitive(val)
        self.raggruppamento_famiglia_checkbutton.set_sensitive(val)
        self.raggruppamento_categoria_checkbutton.set_sensitive(val)
        self.raggruppamento_genere_checkbutton.set_sensitive(val)
        self.raggruppamento_fornitore_checkbutton.set_sensitive(val)


    def on_any_checkbutton_giacenze_clicked(self, button):
        element = None
        if button == self.ordinamento_famiglia_checkbutton:
            element = 'famiglia'
        elif button == self.ordinamento_categoria_checkbutton:
            element = 'categoria'
        elif button == self.ordinamento_genere_checkbutton:
            element = 'genere'
        elif button == self.ordinamento_fornitore_checkbutton:
            element = 'fornitore'

        if element is None:
            return

        if button.get_active():
            self._orderingOrder.append(element)
        else:
            for s in range(len(self._orderingOrder)):
                if self._orderingOrder[s] == element:
                    self._orderingOrder.pop(s)
                    break


    def on_any_checkbutton_venduto_clicked(self, button):
        element = None
        if button == self.raggruppamento_famiglia_checkbutton:
            element = 'famiglia'
        elif button == self.raggruppamento_categoria_checkbutton:
            element = 'categoria'
        elif button == self.raggruppamento_genere_checkbutton:
            element = 'genere'
        elif button == self.raggruppamento_fornitore_checkbutton:
            element = 'fornitore'

        if element is None:
            return

        if button.get_active():
            self._groupingOrder.append(element)
        else:
            for s in range(len(self._groupingOrder)):
                if self._groupingOrder[s] == element:
                    self._groupingOrder.pop(s)
                    break


    def on_ok_button_clicked(self, button):
        fileDialog = gtk.FileChooserDialog(title='Salva la statistica ',
                                           parent=self.getTopLevel(),
                                           action=gtk.FILE_CHOOSER_ACTION_SAVE,
                                           buttons=(gtk.STOCK_CANCEL,
                                                    gtk.RESPONSE_CANCEL,
                                                    gtk.STOCK_SAVE,
                                                    gtk.RESPONSE_OK),
                                           backend=None)


        folder = ''
        if hasattr(Environment.conf,'Documenti'):
            folder = getattr(Environment.conf.Documenti,'cartella_predefinita','')
        if folder == '':
            if os.name == 'posix':
                folder = os.environ['HOME']
            elif os.name == 'nt':
                folder = os.environ['USERPROFILE']
        fileDialog.set_current_folder(folder)

        fltr = gtk.FileFilter()
        fltr.add_mime_type('application/csv')
        fltr.set_name('File CSV (*.csv)')
        fileDialog.add_filter(fltr)

        fileDialog.set_current_name('stat_mag.csv')

        response = fileDialog.run()
        if response == gtk.RESPONSE_OK:
            filename = fileDialog.get_filename()
            fileDialog.destroy()

            self.export(filename)
        else:
            fileDialog.destroy()
            return

    def calcolaUltimoPrezzoAcquisto(self, arti=None, righe=None):

        prezzo_ultimo_vendita = 0
        prezzo_ultimo_acquisto = 0
        data_ultimo_acquisto = "Nessuna"
        data_ultima_vendita = "Nessuna"
        prezzo_vendita = []
        prezzo_acquisto = []
        if righe:
            new_data =datetime.datetime(2003, 7, 14, 12, 30)
            for riga in righe:
                rm = riga[0]
                tm = riga[1]
                data_movimento=tm.data_movimento
                if data_movimento >= new_data:
                    new_data = data_movimento
                    if tm.segnoOperazione == "-":
                        prezzo_ultimo_vendita = rm.valore_unitario_netto
                        data_ultima_vendita = new_data
                    else:
                        prezzo_ultimo_acquisto = rm.valore_unitario_netto
                        data_ultimo_acquisto = new_data
                if tm.segnoOperazione == "-":
                    prezzo_vendita.append(rm.valore_unitario_netto)
                else:
                    prezzo_acquisto.append(rm.valore_unitario_netto)

                quantita_acquistata= 0
                quantita_venduta = 0
                if tm.segnoOperazione == "-":
                    quantita_venduta += rm.quantita *rm.moltiplicatore
                else:
                    quantita_acquistata += rm.quantita *rm.moltiplicatore
                giacenza = abs(quantita_acquistata-quantita_venduta)

            if prezzo_acquisto:
                media_acquisto = sum(prezzo_acquisto) / len(prezzo_acquisto)
            else:
                media_acquisto = 0
            if prezzo_vendita:
                media_vendita = sum(prezzo_vendita) / len(prezzo_vendita)
            else:
                media_vendita = 0
            arti.update(prezzo_ultima_vendita = prezzo_ultimo_vendita,
                        data_ultima_vendita = data_ultima_vendita,
                        prezzo_ultimo_acquisto = prezzo_ultimo_acquisto,
                        data_ultimo_acquisto = data_ultimo_acquisto,
                        media_acquisto = media_acquisto,
                        media_vendita = media_vendita,
                        quantita_venduta = quantita_venduta,
                        quantita_acquistata = quantita_acquistata,
                        giacenza = giacenza,
)
        else:
            arti.update(prezzo_ultima_vendita = 0,
                    data_ultima_vendita = data_ultima_vendita,
                    prezzo_ultimo_acquisto = 0,
                    data_ultimo_acquisto = data_ultimo_acquisto,
                    media_acquisto = 0,
                    media_vendita = 0,
                    quantita_venduta = 0,
                    quantita_acquistata = 0,
                    giacenza = 0,
)
        return arti
            


    def export(self, filename):
        intervallo = ''
        self.res = []
        year = self.year_combobox.get_active_text()
        if not year:
            year="2009"
        if self.allmag_checkbutton:
            magazzini = Environment.params["session"].query(Magazzino.id).all()
            #print "PASSA QUIIIIIIIIIIIIII", year
        else:
            magazzini = [1]
        idArticolo=None
        idArticoli = Environment.params["session"].query(Stoccaggio.id_articolo).filter(Stoccaggio.id_magazzino==magazzini[0][0]).all()
        #print "ARTICOLI NL MAGAZZINO", len(idArticoli)

        for idArticolo in idArticoli:
            arti = leggiArticolo(idArticolo)
            #print arti["daoArticolo"].denominazione
            #print "ID ARTICOLO", idArticolo
            righeArticoloMovimentate= Environment.params["session"]\
                    .query(RigaMovimento,TestataMovimento)\
                    .filter(TestataMovimento.data_movimento.between(datetime.date(int(year), 1, 1), datetime.date(int(year) + 1, 1, 1)))\
                    .filter(RigaMovimento.id_testata_movimento == TestataMovimento.id)\
                    .filter(Riga.id_articolo==idArticolo[0])\
                    .filter(Riga.id_magazzino.in_(magazzini[0]))\
                    .all()

            arti= self.calcolaUltimoPrezzoAcquisto(arti=arti, righe=righeArticoloMovimentate)

            self.res.append(arti)
        c = csv.writer(open(filename, "wb"))
        c.writerow(["ID","CODICE","DENOMINAZIONE","COLORE","ANNO","GRUPPO TAGLIA","GENERE", "TAGLIA", "STAGIONE" ,
                    "DATA ULTIMA VENDITA", "PREZZO ULTIMA VENDITA", "DATA ULTIMO ACQUISTO", "PREZZO ULTIMO ACQUISTO",
                    "GIACENZA", "MEDIA PREZZO VENDITA", "MEDIA PREZZO ACQUISTO", "QUANTITA' VENDUTA", "QUANTITA' ACQUISTATA",
                    "UNITA' BASE", "IVA", "FAMIGLIA", "CATEGORIA"]
)
        for i in self.res:
            #print "IIIIIIIIIIIIIII", i
            id = i["id"][0]
            codice = i["codice"]
            denominazione = i["denominazione"]
            colore = i["colore"]
            anno = i["anno"]
            gruppoTaglia = i["gruppoTaglia"]
            genere = i["genere"]
            taglia = i["taglia"]
            stagione = i["stagione"]
            data_ultima_vendita = dateTimeToString(i["data_ultima_vendita"])
            data_ultimo_acquisto = dateTimeToString(i["data_ultimo_acquisto"])
            prezzo_ultimo_acquisto = mN(i["prezzo_ultimo_acquisto"])
            prezzo_ultima_vendita = mN(i["prezzo_ultima_vendita"])
            giacenza = mN(i["giacenza"])
            media_acquisto = mN(i["media_acquisto"])
            media_vendita = mN(i["media_vendita"])
            quantita_venduta = mN(i["quantita_venduta"])
            quantita_acquistata = mN(i["quantita_acquistata"])
            unita_base = i["unitaBase"]
            denominazioneBreveAliquotaIva = i["denominazioneBreveAliquotaIva"]
            famiglia = i["daoArticolo"].denominazione_breve_famiglia
            categoria = i["daoArticolo"].denominazione_breve_categoria
            c.writerow([id,codice,denominazione, colore, anno, gruppoTaglia, genere, taglia,
                        stagione, data_ultima_vendita, prezzo_ultima_vendita,
                        data_ultimo_acquisto, prezzo_ultimo_acquisto, giacenza,
                        media_vendita, media_acquisto,quantita_venduta,quantita_acquistata,
                        unita_base, denominazioneBreveAliquotaIva, famiglia, categoria]
)
 

        dialog = gtk.MessageDialog(self.getTopLevel(), gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
                                   gtk.MESSAGE_INFO, gtk.BUTTONS_OK, '\n\nEsportazione terminata !')
        dialog.run()
        dialog.destroy()

