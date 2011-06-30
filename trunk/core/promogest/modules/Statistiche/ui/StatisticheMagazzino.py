# -*- coding: utf-8 -*-

#    Copyright (C) 2005, 2006, 2007 2008, 2009, 2010, 2011 by Promotux
#                        di Francesco Meloni snc - http://www.promotux.it/

#    Author: Francesco Meloni  <francesco@promotux.it>
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

import os
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
from promogest.ui.gtk_compat import *
from promogest.dao.DaoUtils import *


class StatisticheMagazzino(GladeWidget):

    def __init__(self, idMagazzino=None):

        GladeWidget.__init__(self, 'statistiche_magazzino_dialog',
                'Statistiche/gui/statistiche_magazzino_elements.glade',
                isModule=True)
        self.placeWindow(self.getTopLevel())
        self.da_data__entry.set_text('01/01/' + Environment.workingYear)
        self.a_data__entry.set_text(dateToString(datetime.datetime.now()))
        fillComboboxMagazzini(self.magazzino_combobox)
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
        folder = setconf("General", "cartella_predefinita") or ""
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
        self.filechooserdialog_stats.hide()

    def on_cancella_file_clicked(self, button):
        self.filechooserdialog_stats.hide()

    def exportss(self, filename):
        intervallo = ''
        self.res = []
        daData = stringToDate(self.da_data__entry.get_text())
        aData = stringToDate(self.a_data__entry.get_text())

        id = findIdFromCombobox(self.magazzino_combobox)
        if id :
            magazzini = [Magazzino().getRecord(id=id)]
        else:
            magazzini = Magazzino().select(batchSize=None)
        arti = []
        for mag in magazzini:
            idArticolo = None
            idArticoli = Environment.params["session"].query(Stoccaggio.id_articolo).filter(Stoccaggio.id_magazzino==mag.id).all()
            for idArticolo in idArticoli:
                artid = leggiArticolo(idArticolo)
                righeArticoloMovimentate= Environment.params["session"]\
                        .query(RigaMovimento,TestataMovimento)\
                        .filter(TestataMovimento.data_movimento.between(daData, aData))\
                        .filter(RigaMovimento.id_testata_movimento == TestataMovimento.id)\
                        .filter(Riga.id_articolo==idArticolo[0])\
                        .filter(Riga.id_magazzino ==mag.id)\
                        .all()

                arti= articoloStatistiche(arti=artid, righe=righeArticoloMovimentate)
                self.res.append(arti)
        c = csv.writer(open(filename, "wb"),dialect='excel',delimiter=';')
        rigga = ["ID","CODICE","DENOMINAZIONE","QUANTITA' VENDUTA", "QUANTITA' ACQUISTATA","DATA ULTIMO ACQUISTO",
                    "DATA ULTIMA VENDITA", "PREZZO ULTIMA VENDITA",  "PREZZO ULTIMO ACQUISTO",
                    "GIACENZA", "MEDIA PREZZO VENDITA", "MEDIA PREZZO ACQUISTO",
                    "UNITA' BASE", "IVA", "FAMIGLIA", "CATEGORIA"]
        if posso("PW"):
            rigga = rigga + ["COLORE","ANNO",
                    "GRUPPO TAGLIA","GENERE", "TAGLIA", "STAGIONE"]
        c.writerow(rigga)
        for i in self.res:
            if i["daoArticolo"]:
                id = i["id"][0]
                codice = i["codice"]
                denominazione = str(i["denominazione"]).replace(";"," ")
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
                if posso("PW"):
                    colore = i["colore"]
                    anno = i["anno"]
                    gruppoTaglia = i["gruppoTaglia"]
                    genere = i["genere"]
                    taglia = i["taglia"]
                    stagione = i["stagione"]
                paramRigga = [id, codice,denominazione, quantita_venduta, quantita_acquistata,
                            data_ultimo_acquisto,data_ultima_vendita, prezzo_ultima_vendita,
                             prezzo_ultimo_acquisto, giacenza, media_vendita, media_acquisto,
                            unita_base, denominazioneBreveAliquotaIva, famiglia, categoria]
                if posso("PW"):
                    paramRigga = paramRigga + [colore, anno, gruppoTaglia, genere, taglia,stagione]
                c.writerow(paramRigga)

        messageInfo(msg='\n\nEsportazione terminata !', transient=self.getTopLevel())
