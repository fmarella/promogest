# -*- coding: utf-8 -*-

# Promogest
#
# Copyright (C) 2005 by Promotux Informatica - http://www.promotux.it/
# Author: Andrea Argiolas <andrea@promotux.it>
# Author: Francesco Meloni  <francesco@promotux.it>

import os
import gtk
import csv
import datetime
from promogest.ui.GladeWidget import GladeWidget
from promogest import Environment
from promogest.dao.TestataMovimento import TestataMovimento
from promogest.dao.RigaMovimento import RigaMovimento
from promogest.dao.Riga import Riga
from promogest.dao.Magazzino import Magazzino
from promogest.dao.Stoccaggio import Stoccaggio
from promogest.ui.utils import *
from promogest.ui.utilsCombobox import *
from promogest.dao.DaoUtils import *


class StatisticheMagazzino(GladeWidget):

    def __init__(self, idMagazzino=None):

        GladeWidget.__init__(self, 'statistiche_magazzino_dialog',
                'Statistiche/gui/statistiche_magazzino_elements.glade',
                isModule=True)
        self.placeWindow(self.getTopLevel())
        self.da_data__entry.set_text('01/01/' + Environment.workingYear)
        self.a_data__entry.set_text(dateToString(datetime.datetime.now()))
        self._idMagazzino = idMagazzino
        self.da_data__entry.show_all()
        self.a_data__entry.show_all()

    def on_statistiche_magazzino_dialog_destroy(self, widget):
        self.a_data__entry.destroy()
        self.da_data__entry.destroy()
        self.getTopLevel().destroy()
        #return

    def on_ok_buttonn_clicked(self, button):

        self.filechooserdialog_stats.show()
        folder = ''
        if hasattr(Environment.conf,'Documenti'):
            folder = getattr(Environment.conf.Documenti,'cartella_predefinita','')
        if folder == '':
            if os.name == 'posix':
                folder = os.environ['HOME']
            elif os.name == 'nt':
                folder = os.environ['USERPROFILE']
        self.filechooserdialog_stats.set_current_folder(folder)

        fltr = gtk.FileFilter()
        fltr.add_mime_type('application/csv')
        fltr.set_name('File CSV (*.csv)')
        self.filechooserdialog_stats.add_filter(fltr)

        self.filechooserdialog_stats.set_current_name('stat_mag.csv')

        response = self.filechooserdialog_stats.run()

    def on_salva_file_clicked(self, button):
        filename = self.filechooserdialog_stats.get_filename()
        self.exportss(filename)
        self.filechooserdialog_stats.destroy()

    def on_cancella_file_clicked(self, button):
        self.filechooserdialog_stats.destroy()

    def exportss(self, filename):
        intervallo = ''
        self.res = []
        daData = stringToDate(self.da_data__entry.get_text())
        aData = stringToDate(self.a_data__entry.get_text())
        if self.allmag_checkbutton:
            magazzini = Environment.params["session"].query(Magazzino.id).all()
        else:
            magazzini = [1]
        idArticolo=None
        idArticoli = Environment.params["session"].query(Stoccaggio.id_articolo).filter(Stoccaggio.id_magazzino==magazzini[0][0]).all()

        for idArticolo in idArticoli:
            arti = leggiArticolo(idArticolo)
            righeArticoloMovimentate= Environment.params["session"]\
                    .query(RigaMovimento,TestataMovimento)\
                    .filter(TestataMovimento.data_movimento.between(daData, aData))\
                    .filter(RigaMovimento.id_testata_movimento == TestataMovimento.id)\
                    .filter(Riga.id_articolo==idArticolo[0])\
                    .filter(Riga.id_magazzino.in_(magazzini[0]))\
                    .all()

            arti= articoloStatistiche(arti=arti, righe=righeArticoloMovimentate)

            self.res.append(arti)
        c = csv.writer(open(filename, "wb"),dialect='excel',delimiter=';')
        c.writerow(["ID","CODICE","DENOMINAZIONE","QUANTITA' VENDUTA", "QUANTITA' ACQUISTATA","DATA ULTIMO ACQUISTO",
                    "DATA ULTIMA VENDITA", "PREZZO ULTIMA VENDITA",  "PREZZO ULTIMO ACQUISTO",
                    "GIACENZA", "MEDIA PREZZO VENDITA", "MEDIA PREZZO ACQUISTO",
                    "UNITA' BASE", "IVA", "FAMIGLIA", "CATEGORIA","COLORE","ANNO",
                    "GRUPPO TAGLIA","GENERE", "TAGLIA", "STAGIONE"])
        for i in self.res:
            id = i["id"][0]
            codice = i["codice"]
            denominazione = str(i["denominazione"]).replace(";"," ")
            colore = i["colore"]
            anno = i["anno"]
            gruppoTaglia = i["gruppoTaglia"]
            genere = i["genere"]
            taglia = i["taglia"]
            stagione = i["stagione"]
            data_ultima_vendita = dateTimeToString(i["data_ultima_vendita"])
            data_ultimo_acquisto = dateTimeToString(i["data_ultimo_acquisto"])
            prezzo_ultimo_acquisto = str(mN(i["prezzo_ultimo_acquisto"]))
            prezzo_ultima_vendita = str(mN(i["prezzo_ultima_vendita"]))
            giacenza = abs(i["giacenza"])
            media_acquisto = str(mN(i["media_acquisto"]))
            media_vendita = str(mN(i["media_vendita"]))
            quantita_venduta = abs(i["quantita_venduta"])
            quantita_acquistata = abs(i["quantita_acquistata"])
            unita_base = i["unitaBase"]
            denominazioneBreveAliquotaIva = i["denominazioneBreveAliquotaIva"]
            famiglia = i["daoArticolo"].denominazione_breve_famiglia
            categoria = i["daoArticolo"].denominazione_breve_categoria

            c.writerow([id, codice,denominazione, quantita_venduta, quantita_acquistata,
                        data_ultimo_acquisto,data_ultima_vendita, prezzo_ultima_vendita,
                         prezzo_ultimo_acquisto, giacenza, media_vendita, media_acquisto,
                        unita_base, denominazioneBreveAliquotaIva, famiglia, categoria,
                        colore, anno, gruppoTaglia, genere, taglia,stagione])

        dialog = gtk.MessageDialog(self.getTopLevel(), gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
                                   gtk.MESSAGE_INFO, gtk.BUTTONS_OK, '\n\nEsportazione terminata !')
        dialog.run()
        dialog.destroy()
