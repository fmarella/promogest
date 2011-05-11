# -*- coding: utf-8 -*-

#    Copyright (C) 2005, 2006, 2007 2008, 2009, 2010
#by Promotux di Francesco Meloni snc - http://www.promotux.it/

# Author: Francesco Meloni <francesco@promotux.it>

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

from decimal import *
import gtk
import os
from promogest import Environment
from promogest.ui.GladeWidget import GladeWidget
from promogest.ui.utils import *
from promogest.ui.utilsCombobox import *
from promogest.dao.DaoUtils import giacenzaArticolo
from promogest.dao.Articolo import Articolo
from promogest.dao.Listino import Listino
from promogest.dao.ListinoArticolo import ListinoArticolo
from promogest.lib.sla2pdf.Sla2Pdf_ng import Sla2Pdf_ng
from promogest.lib.sla2pdf.SlaTpl2Sla import SlaTpl2Sla as SlaTpl2Sla_ng
#from promogest.lib.SlaTpl2Sla import SlaTpl2Sla
from promogest.ui.PrintDialog import PrintDialogHandler

class ManageLabelsToPrint(GladeWidget):

    def __init__(self, mainWindow=None,daos=None):
        """Widget di transizione per visualizzare e confermare gli oggetti
            preparati per la stampa ( Multi_dialog.glade tab 1)
        """
        GladeWidget.__init__(self, 'label_dialog',
                        fileName= 'Label/gui/label_dialog.glade',isModule=True)
        self.revert_button.destroy()
        self.apply_button.destroy()
        self.mainWindow = mainWindow
        self.completion = gtk.EntryCompletion()
        self.completion.set_match_func(self.match_func)
        self.completion.connect("match-selected",
                                            self.on_completion_match)
        listore = gtk.ListStore(str, object)
        self.completion.set_model(listore)
        self.completion.set_text_column(0)
        self.articolo_entry.set_completion(self.completion)
        self.mattu = False
        self.sepric = "  ~  " # separatore utile allo split
        self.articolo_matchato = None
        self.ricerca = "ricerca_codice_a_barre_button" # ATTENZIONE ...scorciatoia ... check non gestite
        self.daos = daos

#        fillComboboxListini(self.listino_combobox, True)
        self.draw()

    def draw(self):
        """Creo una treeviewper la visualizzazione degli articoli che
            andranno poi in stampa
        """
        if posso("PW"):
            self._treeViewModel = self.label_treestore # gtk.TreeStore(object,str,str,str,str,str)
        else:
            self._treeViewModel = self.label_liststore # gtk.ListStore(object,str,str,str,str,str)
        self.labels_treeview.set_model(self._treeViewModel)
        fillComboboxMagazzini(self.id_magazzino_label_combobox, True)
        self.id_magazzino_label_combobox.set_active(0)
        modek = self.select_template_combobox.get_model()
        path=Environment.labelTemplatesDir  # insert the path to the directory of interest
        # preleva i file .sla dalla cartella
        dirList=os.listdir(path)
        for fname in dirList:
            if os.path.splitext(fname)[1] ==".sla":
                modek.append([fname],)
        self.refresh()

    def selectFilter(self, model, path, iter):
        #lista = []
        check = model.get_value(iter, 1)
        fatherPath = model.get_path(iter)
        if check:
            if len(fatherPath) ==1:
                return
            oggetto = model.get_value(iter, 0)
            quantita = model.get_value(iter, 5)
            for ogg in range(0,int(quantita)):
                oggetto.codice_a_barre = model.get_value(iter, 4)
                self.resultList.append(oggetto)

    def get_active_text(self, combobox):
        model = combobox.get_model()
        active = combobox.get_active()
        if active < 0:
            return None
        return model[active][0]

    def on_ok_button_clicked(self,button):
        self._folder = setconf("General", "cartella_predefinita") or ""
        if self._folder == '':
            if os.name == 'posix':
                self._folder = os.environ['HOME']
            elif os.name == 'nt':
                self._folder = os.environ['USERPROFILE']
        self.resultList= []
        for row in self._treeViewModel:
            if row[5] == "0" or row[5] == "":
                continue
            else:
                for v in range(0,int(row[5])):
                    self.resultList.append(row[0])
        classic = False
        param = []
        for d in self.resultList:
#            d.resolveProperties()
            a = d.dictionary(complete=True)
            a["prezzo_dettaglio"] = str(self.prezzoVenditaDettaglio(d))
            param.append(a)
            pbar(self.pbar,parziale=self.resultList.index(d), totale=len(self.resultList),text="GENERAZIONE DATI")
        if self.classic_radio.get_active():
            classic = True
        template_file= self.get_active_text(self.select_template_combobox)
        if template_file:
            slafile = Environment.labelTemplatesDir +template_file
        else:
            messageInfo(msg="NESSUN TEMPLATE LABEL SELEZIONATO?")
            return
        pbar(self.pbar,pulse=True,text="GENERAZIONE STAMPA ATTENDERE")
        stpl2sla = SlaTpl2Sla_ng(slafile=None,label=True,
                                    report=False,
                                    objects=param,
                                    daos=[], #self.daos,
                                    slaFileName=slafile,
                                    pdfFolder=self._folder,
                                    classic=classic,
                                    template_file=template_file,
                                    pbar=self.pbar)
        pbar(self.pbar,pulse=True,text="GENERAZIONE STAMPA ATTENDERE")
        ecco= Sla2Pdf_ng(slafile=self._folder+"_temppp.sla", pbar=self.pbar).translate()
        g = file(Environment.tempDir+".temp.pdf", "wb")
        g.write(ecco)
        g.close()
        pbar(self.pbar,stop=True)
        anag = PrintDialogHandler(self,g)

    def refresh(self):
        # Aggiornamento TreeView
        self._treeViewModel.clear()
        #print(dir(self.daos[0]))
        quantita ="1"
        for dao in self.daos:
            if posso("PW"):
                if articleType(dao.arti) == "father":
                    parent = self._treeViewModel.append(None,(dao,
                                                dao.codice_articolo,
                                                dao.articolo,
                                                dao.codice_a_barre,
                                                str(self.prezzoVenditaDettaglio(dao)),
                                                "0",
                                                ))
                else:
                    ##for figlio in dao.arti.articoliVarianti:
                    self._treeViewModel.append(None,(dao,
                                            dao.codice_articolo,
                                            dao.articolo,
                                            dao.codice_a_barre,
                                            str(self.prezzoVenditaDettaglio(dao)),
                                            str(quantita),
                                            ))
            else:
                self._treeViewModel.append((dao,
                                            dao.codice_articolo,
                                            dao.articolo,
                                            dao.codice_a_barre,
                                            str(self.prezzoVenditaDettaglio(dao)),
                                            quantita,
                                            ))

    def ricercaListino(self):
        """ check if there is a priceList like setted on configure file
        """
        try:
            pp = Environment.conf.VenditaDettaglio.listino
        except:
            pp = None
        if pp:
            pricelist = Listino().select(denominazione = pp ,
                                        offset = None,
                                        batchSize = None)
        else:
            return None

        if pricelist:
            id_listino = pricelist[0].id
        else:
            id_listino = None
        return id_listino


    def prezzoVenditaDettaglio(self, dao):
        """Funzione importante perchè restituisce
            il prezzo scontato per il dettaglio"""
        if self.listino_vendita_dettaglio.get_active() and self.ricercaListino():
            listino = leggiListino(self.ricercaListino(), dao.id_articolo)
        else:
            listino = leggiListino(dao.id_listino, dao.id_articolo)

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
        return prezzoScontato

    def on_search_row_button_clicked(self, button):
        print "OKOKOK"

    def on_add_button_clicked(self, button=None):
        if self.articolo_entry.get_text() =="":
            return
        idListino = findIdFromCombobox(self.listino_combobox)
        self.articolo_entry.set_text("")
        if self.articolo_matchato:
            artilist = ListinoArticolo().select(idListino=idListino, idArticolo=self.articolo_matchato.id)
            if artilist:
                self.daos.append(artilist[0])
                self.articolo_matchato = None
                self.refresh()

    # Funzione utile. Gestione inserimento testo nella entry
    def on_articolo_entry_insert_text(self, text):
        # Assegna il testo della entri ad una variabile
        stringa = text.get_text()
        if self.mattu:
            text.set_text(stringa.split(self.sepric)[0])
        model = gtk.ListStore(str,object)
        #vediamo = self.completion.get_model()
        #vediamo.clear()
        art = []
        if stringa ==[] or len(stringa)<2:
            return
        if self.ricerca == "ricerca_codice_button":
            if len(text.get_text()) <3:
                art = Articolo().select(codice=stringa, batchSize=20)
            else:
                art = Articolo().select(codice=stringa, batchSize=50)
        elif self.ricerca == "ricerca_descrizione_button":
            if len(text.get_text()) <3:
                art = Articolo().select(denominazione=stringa, batchSize=20)
            else:
                art = Articolo().select(denominazione=stringa, batchSize=50)
        elif self.ricerca == "ricerca_codice_a_barre_button":
            if len(text.get_text()) <7:
                art = Articolo().select(codiceABarre=stringa, batchSize=10)
            else:
                art = Articolo().select(codiceABarre=stringa, batchSize=40)
        elif self.ricerca == "ricerca_codice_articolo_fornitore_button":
            if len(text.get_text()) <3:
                art = Articolo().select(codiceArticoloFornitore=stringa, batchSize=10)
            else:
                art = Articolo().select(codiceArticoloFornitore=stringa, batchSize=40)
#        print "MMMM",art
        for m in art:
            codice_art = m.codice
            den = m.denominazione
            bloccoInformazioni = codice_art+self.sepric+den
            compl_string = bloccoInformazioni
            if self.ricerca == "ricerca_codice_articolo_fornitore_button":
                caf = m.codice_articolo_fornitore
                compl_string = bloccoInformazioni+self.sepric+caf
            if self.ricerca == "ricerca_codice_a_barre_button":
                cb = m.codice_a_barre
                compl_string = bloccoInformazioni+self.sepric+cb
            model.append([compl_string,m])
        self.completion.set_model(model)
        if len(art) == 1:
            self.mattu = True
            self.articolo_matchato = art[0]
            self.articolo_entry.set_position(-1)
#            self.on_add_button_clicked()

    def match_func(self, completion, key, iter):
        model = self.completion.get_model()
        self.mattu = False
        self.articolo_matchato = None
#        print "MODELLLLLLLLLLLLLLLLLL", model[iter][0], key, completion.get_text_column()
        if model[iter][0] and self.articolo_entry.get_text().lower() in model[iter][0].lower():
            return model[iter][0]
        else:
            return None

    def on_completion_match(self, completion=None, model=None, iter=None):
        self.mattu = True
        self.articolo_matchato = model[iter][1]
        self.articolo_entry.set_position(-1)


    def on_column_quantita_edited(self, treeview, path, value):
        """ Function ti set the value quantita edit in the cell"""
        model = self.labels_treeview.get_model()
        #model[path][0]["quantita"] = value
        model[path][5] = value

    def on_calculate_button_clicked(self, button):
        idMagazzino = findIdFromCombobox(self.id_magazzino_label_combobox)
        if self.manuale_radio.get_active():
            quantitagenerale = self.quantita_entry.get_text()
            for row in self._treeViewModel:
                row[5] = quantitagenerale
        elif self.giacenza_radio.get_active():
            for row in self._treeViewModel:
                pbar(self.pbar,parziale=row.path[0]+1,totale=len(self._treeViewModel))
                if idMagazzino:
                    giacenza = giacenzaArticolo(year=Environment.workingYear,
                                            idMagazzino=idMagazzino,
                                            idArticolo=row[0].id_articolo)
                else:
                    giacenza = giacenzaArticolo(year=Environment.workingYear,
                                            idArticolo=row[0].id_articolo,
                                            allMag=True)
                if int(giacenza) <= 0:
                    row[5] = "1"
                else:
                    row[5] = str(int(giacenza))
                pbar(self.pbar,stop=True)
        elif self.movimento_radio.get_active():
            from promogest.dao.TestataMovimento import TestataMovimento
#            from promogest.dao.TestataDocumento import TestataDocumento
            for row in self._treeViewModel:
                pbar(self.pbar,parziale=row.path[0]+1,totale=len(self._treeViewModel))
                docu = TestataMovimento().select(idArticolo=row[0].id_articolo, batchSize=None)
#                docu = TestataDocumento().select(idArticolo=row[0].id_articolo, batchSize=None)
                if docu:
                    doc = docu[-1]
                    for riga in doc.righe:
                        if riga.codice_articolo == row[1]:
                            quanti = riga.quantita
                            if int(quanti) <= 0:
                                row[5] = "1"
                            else:
                                row[5] = str(int(quanti))
            pbar(self.pbar,stop=True)

    def on_manuale_radio_toggled(self, radiobutton):
        if not self.manuale_radio.get_active():
            self.quantita_entry.set_property("sensitive",False)
        else:
            self.quantita_entry.set_property("sensitive",True)

    def on_quantita_entry_icon_press(self,entry,button,secondary):
        self.quantita_entry.set_text("")


    def on_discard_button_clicked(self, button):
        self.getTopLevel().destroy()
