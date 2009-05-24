# -*- coding: utf-8 -*-

# Promogest
#
# Copyright (C) 2007 by Promotux Informatica - http://www.promotux.it/
# Author:  Marco Pinna "Dr astico" <zoccolodignu@gmail.com>
# Author:  Francesco Meloni  "Vete" <francesco@promotux.it.com>

import string
from decimal import *
import gtk
from datetime import datetime
import xml.etree.cElementTree as ElementTree
from promogest import Environment
from promogest.ui.GladeWidget import GladeWidget
from promogest.dao.Articolo import Articolo
from promogest.dao.AliquotaIva import AliquotaIva
from promogest.dao.CodiceABarreArticolo import CodiceABarreArticolo
from promogest.dao.FamigliaArticolo import FamigliaArticolo
from promogest.dao.CategoriaArticolo import CategoriaArticolo
from promogest.dao.Fornitura import Fornitura
from promogest.dao.Listino import Listino
from promogest.dao.ListinoArticolo import ListinoArticolo
from promogest.dao.UnitaBase import UnitaBase
from promogest.dao.ScontoVenditaDettaglio import ScontoVenditaDettaglio
from promogest.dao.ScontoVenditaIngrosso import ScontoVenditaIngrosso
import promogest.ui.AnagraficaListini
import promogest.ui.Main
from promogest.ui.Main import *
from promogest.ui.AnagraficaListini import AnagraficaListini
from promogest.ui.AnagraficaAliquoteIva import AnagraficaAliquoteIva
from promogest.ui.AnagraficaCategorieArticoli import AnagraficaCategorieArticoli
from promogest.ui.AnagraficaFamiglieArticoli import AnagraficaFamiglieArticoli
from promogest.ui.AnagraficaFornitori import AnagraficaFornitori
from promogest.ui.utils import *
from promogest.ui.utilsCombobox import fillModelCombobox,fillComboboxListini
import promogest.ui.Login
from promogest.modules.ImportPriceList.ui.ImportPriceListPreview import ImportPreview
from fieldsDict import *
from promogest.modules.ImportPriceList.ui.ImportPriceListModels import ImportPriceListModels
from promogest.modules.ImportPriceList.ui.PriceListModel import PriceListModel

class ImportPriceList(GladeWidget):
    """Does price-list importation"""

    def __init__(self, mainWindow):
        GladeWidget.__init__(self, 'import_price_list_window')
        self._mainWindow = mainWindow
        #self._mainWindow.hide()
        if self._mainWindow in Login.windowGroup:
            Login.windowGroup.remove(self._mainWindow)
        self.window = self.getTopLevel()
        self.placeWindow(self.window)

        self.file_name = None
        self.promoPriceList = None
        self.mod_name = None
        self.fornitore = None
        self.modelsDir = Environment.documentsDir + 'modelli_listini'
        self.draw()

    def draw(self):
        """draw method draws and fills all widgets in import_price_list_window """

        if self.file_name:
            self.path_file_entry.set_text(self.file_name)
        fillModelCombobox(self.model_combobox)
        if self.mod_name is not None:
            findComboboxRowFromStr(self.model_combobox, self.mod_name,0)
        else:
            self.model_combobox.set_active(0)
        fillComboboxListini(self.price_list_name_combobox)
        if self.promoPriceList is not None:
            findComboboxRowFromStr(self.price_list_name_combobox, self.promoPriceList, 1)
        else:
            self.price_list_name_combobox.set_active(0)
        fillComboboxFornitori(self.fornitore_combobox)
        if self.fornitore is not None:
            findComboboxRowFromStr(self.fornitore_combobox, self.fornitore,1)
        else:
            self.fornitore_combobox.set_active(0)

    def on_path_file_entry_changed(self, gtkentry):
        self.file_name = self.path_file_entry.get_text()

    def on_model_combobox_changed(self, combobox):
        self.mod_name = findStrFromCombobox(self.model_combobox, 0)

    def on_fornitore_combobox_changed(self, combobox):
        self.fornitore = findStrFromCombobox(self.fornitore_combobox,1)

    def on_import_button_clicked(self, button):
        """begin price-list importation procedure"""

        self.checkObligatoryFields()
        self.promoPriceList = findStrFromCombobox(self.price_list_name_combobox, 1)
        if self.promoPriceList is None:
            self.promoPriceList = findStrFromCombobox(self.price_list_name_combobox, 2)

        self.data_listino = stringToDate(self.data_listino_entry.get_text())


        model = self.model_combobox.get_model()
        active = self.model_combobox.get_active()
        path = model[active][1]

        priceListModel = PriceListModel(pathFile = path)
        try:
            csvPriceListFile = open(self.file_name,'r')
        except:
            msg = 'Impossibile aprire il file CSV selezionato.'
            overDialog = gtk.MessageDialog(self.getTopLevel(),
                                                       gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
                                                       gtk.MESSAGE_ERROR,
                                                       gtk.BUTTONS_CANCEL, msg)
            response = overDialog.run()
            overDialog.destroy()
            return
        self.modelFields = priceListModel._fields
        startFromRow = int(priceListModel._skipFirstLine)
        try:
            lines = csvPriceListFile.readlines()
        except:
            msg = 'Impossibile leggere il file "'+self.file_name+'".\nIl file potrebbe essere corrotto'
            overDialog = gtk.MessageDialog(self.getTopLevel(),
                                                       gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
                                                       gtk.MESSAGE_ERROR,
                                                       gtk.BUTTONS_CANCEL, msg)
            response = overDialog.run()
            overDialog.destroy()
            return
        if priceListModel._skipFirstColumn:
            modelFields = []
            modelFields.append('Valore nullo 0')
            for f in self.modelFields:
                modelFields.append(f)

        row = []
        table=[]
        product = {}


        # Create a bi-dimensional list from the lines of the file (excluding fields separators and fields delimiters)
        if startFromRow:
            lines = lines[1:]
        ind = 0
        for line in lines:
            line.encode('utf-8','replace')
            fields = string.split(line[:-1], priceListModel._fieldsSeparator)
            for i in range(len(fields)):
                if len(fields[i]) > 0:
                    if fields[i][0]  == priceListModel._fieldsDelimiter:
                        fields[i] = fields[i][1:]
                    if fields[i][-1] == priceListModel._fieldsDelimiter:
                        fields[i] = fields[i][:-1]
            table.insert(ind, fields)
            ind += 1
        print "Done. We are ready to start, There are "+str(ind)+" products"


        #create a 'product' dictionary for every line of the price list file and generate a list of 'products'.
        _priceList = []
        rowcount = 0
        width = len(self.modelFields)

        for row in table:
            if len(row) == width:
                product= dict(zip(self.modelFields,row))
                _priceList.append(product)
                rowcount += 1
            else:
                msg = """Attenzione!
I campi indicati nel modello non coincidono (in numero)
con quelli realmente presenti nel documento alla
riga %s Verificare il modello definito o la validità
del formato del file e riprovare""" % str(rowcount+1)
                overDialog = gtk.MessageDialog(self.getTopLevel(),
                                                   gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
                                                   gtk.MESSAGE_ERROR,
                                                   gtk.BUTTONS_CANCEL, msg)
                response = overDialog.run()
                overDialog.destroy()
                return
        self.window.hide()
        anag = ImportPreview(self.window, table, priceListModel, _priceList, self.promoPriceList, self.fornitore, self.data_listino)
        anagWindow = anag.getTopLevel()
        showAnagraficaRichiamata(self.window, anagWindow)
##        self.on_import_price_list_window_close(widget=None)

    def on_models_button_clicked(self, button):
        """opens price_list_models_window with path_file parameter if any model
        is specified in model_combobox"""
        model = self.model_combobox.get_model()
        active = self.model_combobox.get_active()
        if model[active] is not None:
            _path = model[active][1]
            anag = ImportPriceListModels(self.window, pathFile=_path)
        else:
            anag = importPriceListModels(self.window, pathFile=None)
        anagWindow = anag.getTopLevel()

        showAnagraficaRichiamata(self.window, anagWindow, button,self.refresh)

    def on_browse_button_clicked(self, button):
        """on_browse_button_clicked method opens a FileChooserDialog to choose the price-list file"""
        fileDialog = gtk.FileChooserDialog(title='Importazione listino',
                                           parent=self.getTopLevel(),
                                           action=gtk.FILE_CHOOSER_ACTION_OPEN,
                                           buttons=(gtk.STOCK_CANCEL,
                                                    gtk.RESPONSE_CANCEL,
                                                    gtk.STOCK_OK,
                                                    gtk.RESPONSE_OK),
                                           backend=None)
        fltr = gtk.FileFilter()
        #fltr.add_mime_type('application/csv')
        fltr.add_pattern('*.csv')
        fltr.set_name('File CSV (*.csv)')
        fileDialog.add_filter(fltr)
        fltr = gtk.FileFilter()
        fltr.add_pattern('*')
        fltr.set_name('Tutti i file')
        fileDialog.add_filter(fltr)

        response = fileDialog.run()
        if response == gtk.RESPONSE_OK:
            filename = fileDialog.get_filename()
            self.path_file_entry.set_text(filename)
        fileDialog.destroy()


    def on_anagrafica_listini_button_clicked(self, button):
        anag = AnagraficaListini()
        anagWindow = anag.getTopLevel()
        showAnagraficaRichiamata(self.window, anagWindow, button, self.refresh)


    def on_fornitori_button_clicked(self, button):
        anag = AnagraficaFornitori()
        anagWindow = anag.getTopLevel()
        showAnagraficaRichiamata(self.window, anagWindow, button, self.refresh)

    def refresh(self):
        """refresh method refreshes this window"""
        self._existingModels = getModelsName()
        self.file_name = self.path_file_entry.get_text()
        self.mod_name = findStrFromCombobox(self.model_combobox, 0)
        self.promoPriceList = findStrFromCombobox(self.price_list_name_combobox,2)
        self.draw()



    def checkObligatoryFields(self):
        """checkObligatoryFields method checks if all obligatory fields has been inserted"""
        if not self.path_file_entry.get_text():
            obligatoryField(self.getTopLevel(),
                            self.path_file_entry,
                            'Inserire il file del listino da importare')

        if not self.model_combobox.get_active_text():
            obligatoryField(self.getTopLevel(),
                            self.model_combobox,
                            'Selezionare un modello')

        if findStrFromCombobox(self.price_list_name_combobox, 1) == '':
            obligatoryField(self.getTopLevel(),
                            self.price_list_name_combobox,
                            'Selezionare il listino di destinazione')

        if findStrFromCombobox(self.fornitore_combobox, 1) == '':
            obbligatoryField(self.getTopLevel(),
                                self.fornitore_combobox,
                                'Selezionare un Fornitore')

        if self.data_listino_entry.get_text() == '':
            obbligatoryField(self.getTopLevel(),
                                self.data_listino_entry,
                                'indicare la data del listino che si intende importare')

    def on_import_price_list_window_close(self, widget, event=None):
        self.window.destroy()
        self.destroy()
        if self._mainWindow not in Login.windowGroup:
            Login.windowGroup.append(self._mainWindow)
        self._mainWindow.show_all()
