# -*- coding: utf-8 -*-

# Promogest
#
# Copyright (C) 2007-2009 by Promotux Informatica - http://www.promotux.it/
# Author:  Francesco Meloni  "Vete" <francesco@promotux.it.com>

from decimal import *
import gtk
import os
from promogest import Environment
from promogest.ui.GladeWidget import GladeWidget
from promogest.ui.utils import *
from promogest.ui.utilsCombobox import *
from promogest.dao.DaoUtils import giacenzaArticolo
from promogest.dao.Articolo import Articolo
from promogest.dao.ListinoArticolo import ListinoArticolo
#from promogest.ui.AnagraficaComplessa import Anagrafica
from promogest.lib.sla2pdf.Sla2Pdf_ng import Sla2Pdf_ng
from promogest.lib.sla2pdf.SlaTpl2Sla import SlaTpl2Sla as SlaTpl2Sla_ng
from promogest.lib.SlaTpl2Sla import SlaTpl2Sla
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
        fillComboboxListini(self.listino_combobox, True)
        self.draw()

    def draw(self):
        """Creo una treeviewper la visualizzazione degli articoli che
            andranno poi in stampa
        """
        treeview = self.labels_treeview

        rendererSx = gtk.CellRendererText()
		# istanzia la gestione della TreeViewColumn
        column = gtk.TreeViewColumn("Codice", rendererSx, text=1)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(False)
        column.set_resizable(True)
        column.set_min_width(80)
        treeview.append_column(column)

        column = gtk.TreeViewColumn("Denominazione", rendererSx, text=2)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_resizable(True)
        column.set_expand(True)
        column.set_min_width(80)
        treeview.append_column(column)

        column = gtk.TreeViewColumn("codide a barre", rendererSx, text=3)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_resizable(True)
        column.set_expand(True)
        column.set_min_width(60)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Prezzo', rendererSx, text=4)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_resizable(True)
        column.set_expand(True)
        column.set_min_width(60)
        treeview.append_column(column)

        cellspin = gtk.CellRendererSpin()
        cellspin.set_property("editable", True)
        cellspin.set_property("visible", True)
        adjustment = gtk.Adjustment(1, 1, 1000,1,2)
        cellspin.set_property("adjustment", adjustment)
        #cellspin.set_property("digits",3)
        cellspin.set_property("climb-rate",3)
        cellspin.connect('edited', self.on_column_quantita_edited, treeview, True)
        column = gtk.TreeViewColumn('Quantità', cellspin, text=5)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_resizable(True)
        column.set_expand(True)
        column.set_min_width(40)
        treeview.append_column(column)
        if posso("PW"):
            self._treeViewModel = gtk.TreeStore(object,str,str,str,str,str)
        else:
            self._treeViewModel = gtk.ListStore(object,str,str,str,str,str)
        treeview.set_model(self._treeViewModel)
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
        self._folder = ''
#        self._pdfName = str(pdfGenerator.defaultFileName)
        if hasattr(Environment.conf,'Documenti'):
            self._folder = getattr(Environment.conf.Documenti,'cartella_predefinita','')
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
            d.resolveProperties()
            param.append(d.dictionary(complete=True))
            pbar(self.pbar,parziale=self.resultList.index(d), totale=len(self.resultList),text="GENERAZIONE DATI")
        if self.classic_radio.get_active():
            classic = True
        template_file= self.get_active_text(self.select_template_combobox)
        if template_file:
            slafile = Environment.labelTemplatesDir +template_file
        else:
            slafile = self._slaTemplate
        pbar(self.pbar,pulse=True,text="GENERAZIONE STAMPA ATTENDERE")
        stpl2sla = SlaTpl2Sla_ng(slafile=None,label=True,
                                    report=False,
                                    objects=param,
                                    daos=self.daos,
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
                                                str(dao.prezzo_dettaglio),
                                                "0",
                                                ))
                else:
                    ##for figlio in dao.arti.articoliVarianti:
                    self._treeViewModel.append(None,(dao,
                                            dao.codice_articolo,
                                            dao.articolo,
                                            dao.codice_a_barre,
                                            str(dao.prezzo_dettaglio),
                                            quantita,
                                            ))
            else:
                self._treeViewModel.append((dao,
                                            dao.codice_articolo,
                                            dao.articolo,
                                            dao.codice_a_barre,
                                            str(dao.prezzo_dettaglio),
                                            quantita,
                                            ))

    def on_search_row_button_clicked(self, button):
        print "OKOKOK"

    def on_add_button_clicked(self, button=None):
        idListino = findIdFromCombobox(self.listino_combobox)
        self.articolo_entry.set_text("")
        if self.articolo_matchato:
            artilist = ListinoArticolo().select(idListino=idListino, idArticolo=self.articolo_matchato.id)
            if artilist:
                self.daos.append(artilist[0])
                self.refresh()

    # Funzione utile. Gestione inserimento testo nella entry
    def on_articolo_entry_insert_text(self, text):
        # Assegna il testo della entri ad una variabile
        stringa = text.get_text()
#        print "AJAJAAJAJAJAJAJ", stringa, self.mattu,self.ricerca
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


    def on_column_quantita_edited(self, cell, path, value, treeview, editNext=True):
        """ Function ti set the value quantita edit in the cell"""
        model = treeview.get_model()
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
