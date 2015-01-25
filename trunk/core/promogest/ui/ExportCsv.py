# -*- coding: utf-8 -*-

#    Copyright (C) 2005-2012 by Promotux
#                        di Francesco Meloni snc - http://www.promotux.it/

#    Author: Francesco Meloni  <francesco@promotux.it>
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
from shutil import copy2
import xml.etree.ElementTree as ET
from promogest.ui.GladeWidget import GladeWidget
from promogest import Environment
from promogest.lib.utils import messageInfo, obligatoryField, pbar
from promogest.ui.gtk_compat import *


class ExportCsv(GladeWidget):
    """ Anagrafica aziende """

    def __init__(self, mainWindow, dao=None):
        self._mainWindow = mainWindow
        GladeWidget.__init__(self, root='export_csv',
                        path='export_csv.glade')
        self.getTopLevel()
        self.placeWindow(self.getTopLevel())
        self.dao = dao
        self.draw()


    def draw(self):

        treeview = self.modello_treeview
        cellspin = gtk.CellRendererToggle()
        cellspin.set_property('activatable', True)
        cellspin.connect('toggled', self.on_selected, treeview, True)
        column = gtk.TreeViewColumn('Attiva', cellspin)
        column.add_attribute( cellspin, "active", 0)
#        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_resizable(False)
        column.set_expand(False)
        column.set_min_width(70)
        treeview.append_column(column)
        rendererSx =gtk.CellRendererText()
        column = gtk.TreeViewColumn('campo', rendererSx, text=1)
        #column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_resizable(True)
        column.set_expand(True)
        treeview.append_column(column)
        model = gtk.ListStore(bool, str)
        treeview.set_model(model)
        self.fillmodellocombo()
        self.modello_csv_scrolledwindow.set_sensitive(False)
        self.hbox2.set_sensitive(False)
        self.nome_entry.hide()
        self.separatore_combobox.set_active(0)
        self.stringa_combobox.set_active(0)
#        self._refresh()


    def fillmodellocombo(self):
        modek = self.selezione_modello_combobox.get_model()
        modek.clear()
        path=Environment.templatesDir
        # preleva i file .pge dalla cartella
        dirList=os.listdir(path)
        for fname in dirList:
            if os.path.splitext(fname)[1] ==".pge":
                file_ = open(path+fname, "r")
                doc = ET.parse(file_)
                file_.close()
                elem = doc.getroot()
                dao = elem.get("dao")
                if dao == self.dao.__class__.__name__:
                    modek.append([fname],)

    def on_selezione_modello_combobox_changed(self, combobox):
        nomefile= combobox.get_active_text()
        pathFile = Environment.templatesDir
        d = self._loadPgxAttributes(nomefile)
        self.modello_csv_scrolledwindow.set_sensitive(True)
        self.hbox2.set_sensitive(True)
        self._refresh(diz=d)

    def on_nuovo_button_clicked(self, button):
        self.modello_csv_scrolledwindow.set_sensitive(True)
        self.hbox2.set_sensitive(True)
        self.selezione_modello_combobox.hide()
        self.nome_entry.show()
        self._refresh()

    def on_selected(self, cell, path, treeview,value,):
        model = treeview.get_model()
        model[path][0] = not model[path][0]
        return

    def _refresh(self, diz=None):
        model = self.modello_treeview.get_model()
        model.clear()

        if self.dao is None:
            return

        dic = self.dao.dictionary(complete=True)

        if not diz:
            for k,v in dic.items():
                if "_" != k[0]:
                    if k !="session" and k !="metadata" and k !="DaoModule" :
                        model.append((False,k))
            return True
        else:
            cic=[]
            for k,v in diz.items():
                if k == "CSVSCHEMA":
                    for a in v:
                        for m,n in a.items():
                            if m =="campo":
                                model.append((True,n))
                                cic.append(n)
                elif k =="separatore":
                    mode = self.separatore_combobox.get_model()
                    for m in mode:
                        if m[0] == v:
                            self.separatore_combobox.set_active_iter(m.iter)
#                    self.separatore_combobox.set_text(k)
                elif k=="stringa":
                    mode = self.stringa_combobox.get_model()
                    for m in mode:
                        if m[0] == v:
                            self.stringa_combobox.set_active_iter(m.iter)
                elif k == "prima_riga":
                    if v == "True": g = 1
                    else: g = 0
                    self.primariga_check.set_active(g)
            for o,p in dic.items():

                if "_" != o[0]:
                    if o !="session" and o !="metadata" and o !="DaoModule" and o != "campi":
                        if  o not in cic:
                            model.append((False,o))


    def on_salva_modello_button_clicked(self, button):
        """ bottone di salvataggio del modello xml pge"""
        model = self.modello_treeview.get_model()
        self.campi=[]
        for m in model:
            if m[0] ==True:
                self.campi.append((m[1], m.path[0]))
        if self.nome_entry.get_text() =="" and self.selezione_modello_combobox.get_active_text() ==None:
            obligatoryField(self.getTopLevel(), self.nome_entry)
        self._savePgxAttributes()
        nome = self.nome_entry.get_text()
        if not nome:
            nome = self.selezione_modello_combobox.get_active_text().split(".")[0]
        temNome = Environment.tempDir+"tempPGE"
        copy2(temNome, Environment.templatesDir+nome+".pge")
#        self.modello_csv_scrolledwindow.set_sensitive(False)
#        self.hbox2.set_sensitive(False)
        self.nome_entry.hide()
        self.fillmodellocombo()
        self.selezione_modello_combobox.show()


    def on_esporta_button_clicked(self, button):
        """Esporta il file csv dopo averlo creato"""
        if self.selezione_modello_combobox.get_active_text() =="":
            obligatoryField(self.getTopLevel(), self.selezione_modello_combobox)
        if self.selezione_radio.get_active():
            print "SOLO SELEZIONATO"
            record = [self.dao]
            print "self.dao", self.dao
        elif self.filtrati_radio.get_active():
            print "SOLO FILTRATI"
            try:
                #semplice
                record = self._mainWindow.runFilter()
            except:
                #complessa
                record = self._mainWindow.filter.runFilter()
        elif self.tutti_radio.get_active():
            print "TUTTI"
            try:
                #semplice
                record = self._mainWindow.runFilter(offset=None, batchSize=None)
            except:
                #complessa
                record = self._mainWindow.filter.runFilter(offset=None, batchSize=None)
#            print "RECORD TUTTI", record
        self.recordToCSV(record)
        self.salvaFile()

    def salvaFile(self):
        fileDialog = gtk.FileChooserDialog(title='Salva il file',
                                           parent=self.getTopLevel(),
                                           action=gtk.FILE_CHOOSER_ACTION_SAVE,
                                           buttons=(gtk.STOCK_CANCEL,
                                                    gtk.RESPONSE_CANCEL,
                                                    gtk.STOCK_SAVE,
                                                    gtk.RESPONSE_OK),
                                           backend=None)
        fileDialog.set_current_name(self.dao.__class__.__name__+".csv")
        fileDialog.set_current_folder(Environment.documentsDir)

        response = fileDialog.run()
        # FIXME: handle errors here
        if ( (response == gtk.RESPONSE_CANCEL) or ( response == gtk.RESPONSE_DELETE_EVENT)) :
            fileDialog.destroy()
        elif response == gtk.RESPONSE_OK:
            filename = fileDialog.get_filename()
            if not filename:
                messageInfo(msg="Nessun nome scelto per il file")
            else:
                fileDialog.destroy()
                copy2(Environment.tempDir+"tempCSV", filename)

    def recordToCSV(self, record):
        """ TODO: Aggiungere i campi obbligatori"""
        if self.separatore_combobox.get_active_text() =="" or self.separatore_combobox.get_active_text() == None:
            obligatoryField(self.getTopLevel(), self.separatore_combobox, msg="Separatatore Campo obbligatorio")
        if self.stringa_combobox.get_active_text() =="" or self.stringa_combobox.get_active_text() ==None:
            obligatoryField(self.getTopLevel(), self.stringa_combobox,msg="Separatatore Testo obbligatorio")
        tempFileCsv = Environment.tempDir+"tempCSV"
        separatore = self.separatore_combobox.get_active_text()
        print("SEPARATORE: ", separatore)
        Environment.pg2log.info("SEPARATORE: "+ (separatore or ""))
        stringa = self.stringa_combobox.get_active_text()
        print("STRINGA: ", stringa)
        Environment.pg2log.info("STRINGA: "+ (stringa or ""))
        spamWriter = csv.writer(open(tempFileCsv, 'wb'), delimiter=separatore or ";",
                                quotechar=stringa or '"', quoting=csv.QUOTE_MINIMAL)
        model = self.modello_treeview.get_model()
        campilist = []
        for m in model:
            if m[0] == True:
                campilist.append(m[1])
        if self.primariga_check.get_active():
            spamWriter.writerow(campilist)
        for r in record:
            row = []
            for camp in campilist:
                row.append(getattr(r,camp))
            spamWriter.writerow(row)
            pbar(self.generic_progressbar,parziale=record.index(r)+1,totale=len(record))
        pbar(self.generic_progressbar,stop=True)

    def on_ripristina_button_clicked(self, button):
        """ riporta l'interfaccia al momento dell'aoertura"""
        print "DA FARE RISPRISTINA"

    def on_elimina_modello_button_clicked(self, button):
        """ cancella il modello pgx dall'hd"""
        print " elimino"


    def on_close_button_clicked(self, button):
        self.getTopLevel().destroy()


    def _loadPgxAttributes(self, nome):
        """ Imports size and position of the window """
        if nome:
            file_ = open(Environment.templatesDir+nome, "r")
            d = {}
            doc = ET.parse(file_)
            file_.close()
            elem = doc.getroot()
            d["separatore"] = elem.get("separatore")
            d["stringa"] = elem.get("stringa")
            d["dao"] = elem.get("dao")
            d["prima_riga"] = elem.get("prima_riga")
            l = []
            for obj in elem.findall("CSVSCHEMA"):
                c = {}
                c["position"] = int(obj.get('position'))
                c["campo"] = str(obj.get('campo'))
                l.append(c)
            d["CSVSCHEMA"] = l
            return d

    def _savePgxAttributes(self):
        """
        """
        if self.separatore_combobox.get_active_text() =="":
            obligatoryField(self.getTopLevel(), self.separatore_combobox)
        if self.stringa_combobox.get_active_text() =="":
            obligatoryField(self.getTopLevel(), self.stringa_combobox)
        tempFile = Environment.tempDir+"tempPGE"
        root = ET.Element("CSVOPTIONS")
        tree = ET.ElementTree(root)
        separatore = self.separatore_combobox.get_active_text() or ";"
        root.set("separatore",separatore)
        stringa = self.stringa_combobox.get_active_text() or '"'
        root.set("stringa",stringa)
        root.set("dao",self.dao.__class__.__name__)
        root.set("prima_riga",str(self.primariga_check.get_active()))

        for a in self.campi:
            obj = ET.SubElement(root,"CSVSCHEMA")
            obj.set("campo", str(a[0]))
            obj.set("position", str(a[1]))

        tree.write(tempFile)

    def on_chiudi_button_clicked(self, button):
        self.destroy()
        return None
