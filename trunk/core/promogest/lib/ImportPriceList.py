# -*- coding: UTF-8 -*-

# Promogest
#
# Copyright (C) 2007 by Promotux Informatica - http://www.promotux.it/
# Author:  Marco Pinna "Dr astico" <zoccolodignu@gmail.com>
# Author:  Francesco Meloni  "Vete" <francesco@promotux.it.com>

import re, string, decimal
from decimal import *
import gtk, gobject, os
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


# possibleFieldsKeys is a global module list containing all visible fields that is possible to import from a price list
possibleFieldsKeys = ['Codice',
                      'Codice a barre',
                      'Codice articolo fornitore',
                      'Descrizione articolo',
                      'Aliquota iva',
                      'Famiglia',
                      'Categoria',
                      'Unita base',
                      'Produttore',
                      'Prezzo vendita ivato',
                      'Prezzo vendita NON ivato',
                      'Prezzo acquisto ivato',
                      'Prezzo acquisto NON ivato',
                      'Sconto Vendita Dettaglio',
                      'Sconto Vendita Ingrosso',
                      'Valore nullo']
# possibleFieldsValues is a global module list containing all real fields that is possible to import from a price list
possibleFieldsValues = ['codice_articolo',
                        'codice_barre_articolo',
                        'codice_fornitore',
                        'denominazione_articolo',
                        'aliquota_iva',
                        'famiglia_articolo',
                        'categoria_articolo',
                        'unita_base',
                        'produttore',
                        'prezzo_vendita_ivato',
                        'prezzo_vendita_non_ivato',
                        'prezzo_acquisto_ivato',
                        'prezzo_acquisto_non_ivato',
                        'sconto_vendita_dettaglio',
                        'sconto_vendita_ingrosso',
                        'chiave_nulla_']
# possibleFieldsDict is a global module dictionary containing all fields that is possible to import from a price list
possibleFieldsDict = dict(zip(possibleFieldsKeys, possibleFieldsValues))

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

class ImportPriceListModels(GladeWidget):
    """class ImportPriceList: manages all events from import_price_list_models"""

    def __init__(self, mainWindow, pathFile = None):
        GladeWidget.__init__(self, 'import_price_list_models_window')
        self._mainWindow = mainWindow
        self.window = self.import_price_list_models_window
        self.placeWindow(self.window)
        self.remove_null_field_button.set_sensitive(False)
        if pathFile is not None:
            self.priceListModel = PriceListModel(pathFile=pathFile)
        else:
            self.priceListModel = PriceListModel()
        self.priceListModel.setDefaultFields()
        self.draw()
        self.refresh(first_call=True)


    def draw(self):

        cbe_renderer = gtk.CellRendererText()
        self.model_name_comboboxentry.pack_start(cbe_renderer, True)
        self.model_name_comboboxentry.add_attribute(cbe_renderer, 'text', 0)

        #Creating fields treeview

        treeview = self.fields_treeview
        renderer = gtk.CellRendererText()

        column = gtk.TreeViewColumn('Campo', renderer, text=0)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_FIXED)
        column.set_clickable(True)
        column.set_resizable(True)
        column.set_expand(True)
        column.set_fixed_width(300)
        treeview.append_column(column)
        treeview.set_search_column(0)

        self._treeViewModel = gtk.ListStore(str)
        treeview.set_model(self._treeViewModel)

    def refresh(self, first_call=False):
        """fills all widgets in import_price_list_window window"""
        self.loading = True
        if not first_call:
            self.getCsvModelSyntax()
        fillModelCombobox(self.model_name_comboboxentry)
        self.model_name_comboboxentry.set_text_column(0)
        fillComboboxUnitaBase(self.default_unita_base_combobox)
        fillComboboxCategorieArticoli(self.default_categoria_combobox)
        fillComboboxFamiglieArticoli(self.default_famiglia_combobox)
        fillComboboxAliquoteIva(self.default_aliquotaiva_combobox)
        findComboboxRowFromStr(self.model_name_comboboxentry, self.priceListModel._name, 0)

        treeviewModel = self.fields_treeview.get_model()
        treeviewModel.clear()

        for f in self.priceListModel._fields:
            treeviewModel.append((f,))

        defaults = self.priceListModel._defaultAttributes
        self.skip_first_line_checkbutton.set_active(int(self.priceListModel._skipFirstLine ))
        self.skip_first_column_checkbutton.set_active(int(self.priceListModel._skipFirstColumn))
        mcolumn = 0
        if not(self.priceListModel._fieldsDelimiter is None or self.priceListModel._fieldsDelimiter == ''):
            model = self.fields_delimiter_combobox.get_model()
            for r in model:
                if r[mcolumn][0] == self.priceListModel._fieldsDelimiter:
                    self.fields_delimiter_combobox.set_active_iter(r.iter)
        if not(self.priceListModel._fieldsSeparator is None or self.priceListModel._fieldsSeparator == ''):
            model = self.fields_separator_combobox.get_model()
            for r in model:
                if r[mcolumn][0] == self.priceListModel._fieldsSeparator:
                    self.fields_separator_combobox.set_active_iter(r.iter)
        if not(self.priceListModel._decimalSymbol is None or self.priceListModel._decimalSymbol == ''):
            model = self.decimal_symbol_combobox.get_model()
            for r in model:
                if r[mcolumn][0] == self.priceListModel._decimalSymbol:
                    self.decimal_symbol_combobox.set_active_iter(r.iter)
        for f in self.priceListModel._fields:
            if f == 'Codice':
                    self.codice_articolo_cb.set_active(True)
            elif f == 'Codice a barre':
                    self.codice_barre_articolo_cb.set_active(True)
            elif f == 'Codice articolo fornitore':
                self.codice_fornitore_cb.set_active(True)
            elif f == 'Descrizione articolo':
                self.denominazione_articolo_cb.set_active(True)
            elif f == 'Aliquota iva':
                self.aliquota_iva_cb.set_active(True)
            elif f == 'Famiglia':
                self.famiglia_articolo_cb.set_active(True)
            elif f == 'Categoria':
                self.categoria_articolo_cb.set_active(True)
            elif f == 'Unita base':
                self.unita_base_cb.set_active(True)
            elif f == 'Produttore':
                self.produttore_cb.set_active(True)
            elif f == 'Prezzo vendita ivato':
                self.prezzo_vendita_ivato_cb.set_active(True)
            elif f == 'Prezzo vendita NON ivato':
                self.prezzo_vendita_non_ivato_cb.set_active(True)
            elif f == 'Prezzo acquisto ivato':
                self.prezzo_acquisto_ivato_cb.set_active(True)
            elif f == 'Prezzo acquisto NON ivato':
                self.prezzo_acquisto_non_ivato_cb.set_active(True)
            elif f == 'Sconto Vendita Dettaglio':
                self.sconto_vendita_dettaglio_cb.set_active(True)
            elif f == 'Sconto Vendita Ingrosso':
                self.sconto_vendita_ingrosso_cb.set_active(True)
        def_list = ['Aliquota iva','Famiglia','Categoria','Unita base']
        self.default_unita_base_combobox.set_sensitive(False)
        self.default_categoria_combobox.set_sensitive(False)
        self.categoria_togglebutton.set_sensitive(False)
        self.default_famiglia_combobox.set_sensitive(False)
        self.famiglia_togglebutton.set_sensitive(False)
        self.default_aliquotaiva_combobox.set_sensitive(False)
        self.aliquota_iva_togglebutton.set_sensitive(False)
        for k,val in defaults.iteritems():
            v =int(val or 0)
            if k == 'Unita base':
                self.default_unita_base_combobox.set_sensitive(True)
                self.default_unita_base_combobox.set_active(-1)
                findComboboxRowFromId(self.default_unita_base_combobox, v)
            elif k == 'Categoria':
                self.default_categoria_combobox.set_sensitive(True)
                self.categoria_togglebutton.set_sensitive(True)
                self.default_categoria_combobox.set_active(-1)
                findComboboxRowFromId(self.default_categoria_combobox, v)
            elif k == 'Famiglia':
                self.default_famiglia_combobox.set_sensitive(True)
                self.famiglia_togglebutton.set_sensitive(True)
                self.default_famiglia_combobox.set_active(-1)
                findComboboxRowFromId(self.default_famiglia_combobox, v)
            elif k == 'Aliquota iva':
                self.default_aliquotaiva_combobox.set_sensitive(True)
                self.aliquota_iva_togglebutton.set_sensitive(True)
                self.default_aliquotaiva_combobox.set_active(-1)
                findComboboxRowFromId(self.default_aliquotaiva_combobox, v)
        self.loading = False

    def clear(self):
        self.codice_articolo_cb.set_active(False)
        self.codice_barre_articolo_cb.set_active(False)
        self.codice_fornitore_cb.set_active(False)
        self.denominazione_articolo_cb.set_active(False)
        self.aliquota_iva_cb.set_active(False)
        self.famiglia_articolo_cb.set_active(False)
        self.categoria_articolo_cb.set_active(False)
        self.unita_base_cb.set_active(False)
        self.produttore_cb.set_active(False)
        self.prezzo_vendita_ivato_cb.set_active(False)
        self.prezzo_vendita_non_ivato_cb.set_active(False)
        self.prezzo_acquisto_ivato_cb.set_active(False)
        self.sconto_vendita_dettaglio_cb.set_active(False)
        self.sconto_vendita_ingrosso_cb.set_active(False)
        self.draw()

    def on_field_checkbutton_checked(self, checkbutton):
        if self.loading:
            return
        def_list =  ['Aliquota iva','Famiglia','Categoria','Unita base']
        _name = checkbutton.get_name()[:-3]
        for k in possibleFieldsKeys:
            if _name  == possibleFieldsDict[k]:
                status = checkbutton.get_active()
                if k in self.priceListModel._fields:
                    if not status:
                        self.priceListModel._fields.remove(k)
                        if k == def_list[0]:
                            self.default_aliquotaiva_combobox.set_sensitive(True)
                            self.aliquota_iva_togglebutton.set_sensitive(True)
                            break
                        elif k == def_list[1]:
                            self.default_famiglia_combobox.set_sensitive(True)
                            self.famiglia_togglebutton.set_sensitive(True)
                            break
                        elif k == def_list[2]:
                            self.default_categoria_combobox.set_sensitive(True)
                            self.categoria_togglebutton.set_sensitive(True)
                            break
                        elif k == def_list[3]:
                            self.default_unita_base_combobox.set_sensitive(True)
                            break
                    else:
                        if k == def_list[0]:
                            self.default_aliquotaiva_combobox.set_sensitive(False)
                            self.aliquota_iva_togglebutton.set_sensitive(False)
                            break
                        elif k == def_list[1]:
                            self.default_famiglia_combobox.set_sensitive(False)
                            self.famiglia_togglebutton.set_sensitive(False)
                            break
                        elif k == def_list[2]:
                            self.default_categoria_combobox.set_sensitive(False)
                            self.categoria_togglebutton.set_sensitive(False)
                            break
                        elif k == def_list[3]:
                            self.default_unita_base_combobox.set_sensitive(False)
                            break
                else:
                    if status:
                        self.priceListModel._fields.append(k)
                        if k == def_list[0]:
                            self.default_aliquotaiva_combobox.set_sensitive(False)
                            self.aliquota_iva_togglebutton.set_sensitive(False)
                            break
                        elif k == def_list[1]:
                            self.default_famiglia_combobox.set_sensitive(False)
                            self.famiglia_togglebutton.set_sensitive(False)
                            break
                        elif k == def_list[2]:
                            self.default_categoria_combobox.set_sensitive(False)
                            self.categoria_togglebutton.set_sensitive(False)
                            break
                        elif k == def_list[3]:
                            self.default_unita_base_combobox.set_sensitive(False)
                            break
        self.priceListModel.setDefaultFields()
        self.refresh()

    def on_remove_null_field_button_clicked(self, button):
        """Remove the selected null-field from treeview"""

        (model, iterator) = self.fields_treeview.get_selection().get_selected()
        nullFieldPattern= '^Valore nullo [0-9][0-9]?$'
        if bool(re.search(nullFieldPattern, model[iterator][0])):
            _field = model[iterator][0]
            self.priceListModel._fields.remove(_field)
            model.remove(iterator)
            self.remove_null_field_button.set_sensitive(False)
            self.refresh()

    def on_add_null_field_button_clicked(self, button):
        ind = 1
        pos = 0
        for n in self.priceListModel._fields:
            if bool(re.search('^Valore nullo [0-9][0-9]?$', n)):
                self.priceListModel._fields[pos] = 'Valore nullo '+str(ind)
                ind += 1
            pos +=1
        self.priceListModel._fields.append( 'Valore nullo '+str(ind))
        self.refresh()

    def on_save_button_clicked(self, button):
        """Calls the save method in PriceListModel class"""
        self.priceListModel.setDefaultFields()
        self.checkObligatoryFields()
        fileDialog = gtk.FileChooserDialog(title='Salvataggio modello',
                                           parent=self.getTopLevel(),
                                           action=gtk.FILE_CHOOSER_ACTION_SAVE,
                                           buttons=(gtk.STOCK_CANCEL,
                                                    gtk.RESPONSE_CANCEL,
                                                    gtk.STOCK_SAVE,
                                                    gtk.RESPONSE_OK),
                                           backend=None)
        folder = ''
        try:
            folder = modelsDir = Environment.documentsDir + 'modelli_listini'
        except:
            if os.name == 'posix':
                folder = os.environ['HOME']
            elif os.name == 'nt':
                folder = os.environ['USERPROFILE']
        fileDialog.set_current_folder(folder)

        f_name = self.model_name_comboboxentry_entry.get_text().replace(' ','_')
        fileDialog.set_current_name(f_name+'.pgx')

        response = fileDialog.run()

        if response == gtk.RESPONSE_OK:
            filename = fileDialog.get_filename()

            self.priceListModel
            self.priceListModel._name = self.model_name_comboboxentry.get_active_text()

            self.priceListModel._fields = []
            model = self.fields_treeview.get_model()
            for f in model:
                self.priceListModel._fields.append(f[0])
            self.getCsvModelSyntax()
            self.priceListModel.save(filename)
        fileDialog.destroy()
        self.window.destroy()

    def getCsvModelSyntax(self):
        self.priceListModel._fieldsSeparator = self.fields_separator_combobox.get_active_text()[0]
        self.priceListModel._fieldsDelimiter = self.fields_delimiter_combobox.get_active_text()[0]
        self.priceListModel._decimalSymbol = self.decimal_symbol_combobox.get_active_text()[0]
        self.priceListModel._skipFirstLine = self.skip_first_line_checkbutton.get_active()
        self.priceListModel._skipFirstColumn = self.skip_first_column_checkbutton.get_active()

    def checkObligatoryFields(self):
        """Checks if all obligatory fields have been inserted"""

        if self.model_name_comboboxentry.get_active_text() == '':
            obligatoryField(self.getTopLevel(),
                            self.model_name_comboboxentry,
                            'Inserire il nome del modello')

        model = self.fields_treeview.get_model()

        haskey = False
        for f in model:
            if f[0] == 'Codice' or f[0] == 'Codice a barre' or f[0] == 'Codice articolo fornitore':
                haskey = True
                break
        if not haskey:
            obligatoryField(self.getTopLevel(),
                            self.fields_treeview,
                            'Deve essere presente almeno una chiave')

        if not len(model):
            obligatoryField(self.getTopLevel(),
                            self.fields_treeview.get_model,
                            'Inserire almeno un campo nel modello')

        if self.fields_separator_combobox.get_active_text() is None:
            self.fields_separator_combobox.get_active_text()
            obligatoryField(self.getTopLevel(),
                            self.fields_separator_combobox,
                            'Selezionare il carattere di separazione dei campi del listino')

        if self.decimal_symbol_combobox.get_active_text() is None:
            obligatoryField(self.getTopLevel(),
                            self.decimalSymbol_combobox,
                            'Selezionare il simbolo decimale')

        for d in self.priceListModel._defaultAttributes.keys():
            if d == 'Aliquota Iva':
                if not findStrFromCombobox(self.default_aliquotaiva_combobox,2):
                    obligatoryField(self.getTopLevel(),
                            self.default_aliquotaiva_combobox,
                            'Attenzione! E\' necessario indicare il l\'aliquota iva associata\nal listino che si desidera importare')
            elif d == 'Famiglia':
                if not findStrFromCombobox(self.default_famiglia_combobox,2):
                    obligatoryField(self.getTopLevel(),
                            self.default_aliquotaiva_combobox,
                            'Attenzione! Indicare la famiglia di appartenenza\ndegli articoli del listino.')
            elif d == 'Categoria':
                if not findStrFromCombobox(self.default_categoria_combobox,2):
                    obligatoryField(self.getTopLevel(),
                            self.default_aliquotaiva_combobox,
                            'Attenzione! Indicare la categoria di appartenenza\ndegli articoli del listino.')
            elif d == 'Unita base':
                if not findStrFromCombobox(self.default_unita_base_combobox,2):
                    obligatoryField(self.getTopLevel(),
                            self.default_aliquotaiva_combobox,
                            'Attenzione! Indicare l\'unita\' di misura degli articoli del listino')
            else:
                return

    def on_refresh_button_clicked(self,comboboxentry):

        model = self.model_name_comboboxentry.get_model()
        active = self.model_name_comboboxentry.get_active()
        path = model[active][1]
        self.priceListModel = PriceListModel(pathFile=path)
        self.refresh()

    def on_fields_treeview_cursor_changed(self, treeview):
        if self.loading:
            return
        """catches the fields_treeview cursor changed event"""

        model = self.fields_treeview.get_model()
        self.priceListModel._fields = []
        for m in model:
            self.priceListModel._fields.append(m[0])

        self.remove_null_field_button.set_sensitive(True)

    def on_default_combobox_changed(self, combobox):
        if self.loading:
            return
        comboboxName = combobox.get_name()
        value = findStrFromCombobox(combobox,1) or ''
        if len(str(value)) > 0:
            if comboboxName == 'default_categoria_combobox':
                if  'Categoria' in self.priceListModel._defaultAttributes.keys():
                    if value == self.priceListModel._defaultAttributes['Categoria']:
                        return
                    else:
                        self.priceListModel._defaultAttributes['Categoria'] = value
            elif comboboxName == 'default_famiglia_combobox':
                if 'Famiglia' in self.priceListModel._defaultAttributes.keys():
                    if value == self.priceListModel._defaultAttributes['Famiglia']:
                        return
                    else:
                        self.priceListModel._defaultAttributes['Famiglia'] = value
            elif comboboxName == 'default_aliquotaiva_combobox':
                if 'Aliquota iva' in self.priceListModel._defaultAttributes.keys():
                    if value == self.priceListModel._defaultAttributes['Aliquota iva']:
                        return
                    else:
                        self.priceListModel._defaultAttributes['Aliquota iva'] = value
            elif comboboxName == 'default_unita_base_combobox':
                value = findStrFromCombobox(combobox,1)
                if 'Unita base' in self.priceListModel._defaultAttributes.keys():
                    if value == self.priceListModel._defaultAttributes['Unita base']:
                        return
                    else:
                        self.priceListModel._defaultAttributes['Unita base'] = value
        else:
            #FIXME:
            #we have to correct this mess
            print 'non so che sta succedendo.\
            segnalazione errori? per cosa? :D'
            pass

    def on_famiglia_togglebutton_toggled(self, toggleButton):
        if toggleButton.get_active():
            toggleButton.set_active(False)
            return
        anag = AnagraficaFamiglieArticoli()
        anagWindow = anag.getTopLevel()
        showAnagraficaRichiamata(self.getTopLevel(), anagWindow, toggleButton, self.refresh)


    def on_categoria_togglebutton_toggled(self, toggleButton):
        if toggleButton.get_active():
            toggleButton.set_active(False)
            return
        anag = AnagraficaCategorieArticoli()
        anagWindow = anag.getTopLevel()
        showAnagraficaRichiamata(self.getTopLevel(), anagWindow, toggleButton, self.refresh)

    def on_aliquota_iva_togglebutton_toggled(self, toggleButton):
        if toggleButton.get_active():
            toggleButton.set_active(False)
            return
        anag = AnagraficaAliquoteIva()
        anagWindow = anag.getTopLevel()
        showAnagraficaRichiamata(self.getTopLevel(), anagWindow, toggleButton, self.refresh)

    def on_import_price_list_models_window_close(self, widget, event=None):
        self.window.destroy()

class PriceListModel:
    """PriceListModel class manages model's structure"""
    def __init__(self, pathFile=None):
        self._file = pathFile
        self._fields = []
        self._defaultAttributes = {}
        myFieldsDict = {}
        if self._file is not None:
            root = self.parseFile('root')
            tree = self.parseFile('tree')
            if root.tag == 'model':
                self._name = root.attrib['name']
            parent_map = tree.getiterator()
            for p in parent_map:
                if p.tag == 'fieldsSeparator':
                    self._fieldsSeparator = p.attrib['value']
                elif p.tag == 'fieldsDelimiter':
                    self._fieldsDelimiter = p.attrib['value']
                elif p.tag == 'decimalSymbol':
                    self._decimalSymbol = p.attrib['value']
                elif p.tag == 'skipFirstLine':
                    if p.attrib['value'] == 'True':
                        self._skipFirstLine = True
                    else:
                        self._skipFirstLine = False
                elif p.tag == 'skipFirstColumn':
                    if p.attrib['value'] == 'True':
                        self._skipFirstColumn = True
                    else:
                        self._skipFirstColumn = False
                elif p.tag == 'field':
                    myFieldsDict[p.attrib['position']] = p.attrib['name']
                elif p.tag == 'default':
                    self._defaultAttributes[p.attrib['name']] = p.attrib['value']
            field_order = range(0, len(myFieldsDict.keys()))
            for p in field_order:
                self._fields.append(myFieldsDict[str(p)])

        else:
            self._name = 'Modello listino predefinito'
            self._fieldsSeparator = ','
            self._fieldsDelimiter = '"'
            self._decimalSymbol = '.'
            self._skipFirstColumn = False
            self._skipFirstLine = False
            self._fields = []
            self._defaultAttributes = {}

    def save(self, filename):
        """Saves the model into an xml file."""

        model_tag = Element("model")
        model_tag.attrib["name"] = self._name

        index = 0
        for n in self._fields:
            field_tag = SubElement(model_tag, "field")
            field_tag.attrib["name"] = n
            field_tag.attrib["position"] = str(index)
            index += 1

        fieldSeparatorTag = SubElement(model_tag, "fieldsSeparator")
        fieldSeparatorTag.attrib['value'] = str(self._fieldsSeparator)

        fieldsDelimiterTag = SubElement(model_tag, "fieldsDelimiter")
        fieldsDelimiterTag.attrib['value'] = str(self._fieldsDelimiter)

        decimalSymbolTag = SubElement(model_tag, "decimalSymbol")
        decimalSymbolTag.attrib['value'] = str(self._decimalSymbol)

        skipFirstLineTag = SubElement(model_tag,"skipFirstLine")
        skipFirstLineTag.attrib["value"] = str(self._skipFirstLine)

        skipFirstColumnTag = SubElement(model_tag,"skipFirstColumn")
        skipFirstColumnTag.attrib["value"] = str(self._skipFirstColumn)

        for d in self._defaultAttributes.keys():
            oneDefault = SubElement(model_tag,'default')
            oneDefault.attrib["name"] = str(d)
            oneDefault.attrib["value"] = str(self._defaultAttributes[d])
        ElementTree(model_tag).write(filename, encoding='utf-8')

    def parseFile(self,returnObject):
        """Parses xml file and returns, according to the value of returnObject,

        the entire tree or the root element of the tree"""
        file = open(self._file, 'r')
        tree = parse(file)
        if returnObject == 'root':
            root = tree.getroot()
            return root
        elif returnObject == 'tree':
            return tree

    def setDefaultFields(self):
        obbligatoryFields = ['Famiglia','Categoria','Aliquota iva','Unita base']
        for f in obbligatoryFields:
            if f not in self._fields:
                if f not in self._defaultAttributes.keys():
                    self._defaultAttributes[f] = None
            else:
                if f in self._defaultAttributes.keys():
                    try:
                        retVal = self._defaultAttributes.pop(f)
                    except:
                        print 'ATTENZIONE! si è cercato di rimuovere un campo inesistente da un modello di importazione listini.'
        return self._defaultAttributes.keys()

class ProductFromCsv:
    """Takes a product from a generic price list and "translates" it in a

    promogest-compatible dao product, ListinoArticolo and Fornitura"""
    def __init__(self, product, PLModel, promoPriceList, idfornitore,dataListino):
        self.PLModel = PLModel
        self.product = product
        self.promoPriceList = promoPriceList or None
        self.fornitore = idfornitore
        self.dataListino = dataListino
        self.daoArticolo = None
        if self.promoPriceList:
            liss = Listino(isList=True).select(idListino=self.promoPriceList,batchSize=None)
            if liss:
                self.price_list_id = liss[0].id
            del self.promoPriceList
        self.defaults = self.PLModel._defaultAttributes

    def save(self):
        """Gets the existing Dao"""
        for key in possibleFieldsDict.keys():
            if key not in self.product.keys():
                setattr(self, possibleFieldsDict[key], None)
            else:
                setattr(self, possibleFieldsDict[key], self.product[key])

        if self.codice_articolo:
            #self.daoArticolo = promogest.dao.Articolo.getByCodice(Environment.connection,
                                                             #codice=self.codice_articolo)
            try:
                self.daoArticolo = Articolo(isList=True).select(codice=self.codice_articolo)[0]
            except:
                pass

        elif self.codice_fornitore:
            daoFornitura =Fornitura(isList=True).select(codiceArticoloFornitore=self.codice_fornitore)
            if len(daoFornitura) == 1:
                self.daoArticolo = Articolo(id=daoFornitura[0].id_articolo).getRecord()

        elif self.codice_barre_articolo:
            daoCodiceABarre = CodiceABarreArticolo(isList=True).select(codice=self.codice_barre_articolo)
            if daoCodiceABarre:
                self.daoArticolo = Articolo(id=daoCodiceABarre.id_articolo).getRecord()
        else:
            self.daoArticolo = None
        self.fillDaos()

    def fillDaos(self):
        """fillDaos method fills all Dao related to daoArticolo"""
        if self.daoArticolo is None:
            self.daoArticolo = Articolo().getRecord()
        self.codice_articolo = str(self.codice_articolo)
        if self.codice_articolo is None:
            self.codice_articolo = promogest.dao.Articolo.getNuovoCodiceArticolo()

        self.denominazione_articolo = str(self.denominazione_articolo)
        self.daoArticolo.codice = self.codice_articolo
        self.daoArticolo.denominazione = self.denominazione_articolo


        #families
        id_famiglia = None
        if self.famiglia_articolo is None:
            self.famiglia_articolo_id = int(self.defaults['Famiglia'])
            self.famiglia_articolo = FamigliaArticolo(id=self.famiglia_articolo_id).getRecord()
            id_famiglia = self.famiglia_articolo.id

        else:
            self._families = FamigliaArticolo(isList=True).select(batchSize=None)
            code_list = []
            for f in self._families:
                code_list.append(f.codice)
                if self.famiglia_articolo in  (f.denominazione_breve, f.denominazione, f.codice, f.id):
                    id_famiglia = f.id

                    break
            if  id_famiglia is None:
                family_code = self.famiglia_articolo[:4]
                if len(self._families) > 0:
                    ind = 0
                    for code in code_list:
                        if family_code == code[:4]:
                            ind +=1
                    family_code = family_code+'/'+str(ind)

                daoFamiglia = FamigliaArticolo().getRecord()
                daoFamiglia.codice = family_code
                daoFamiglia.denominazione_breve = self.famiglia_articolo[:10]
                daoFamiglia.denominazione = self.famiglia_articolo
                daoFamiglia.id_padre = None
                daoFamiglia.persist()
                id_famiglia = daoFamiglia.id
                self._families.append(daoFamiglia)
        self.daoArticolo.id_famiglia_articolo = id_famiglia

        #categories
        id_categoria = None
        if self.categoria_articolo is None:
            self.categoria_articolo_id = self.defaults['Categoria']
            self.categoria_articolo = CategoriaArticolo(id=self.categoria_articolo_id).getRecord()
            id_categoria = self.categoria_articolo.id
        else:
            self._categories = CategoriaArticolo(isList=True).select(batchSize=None)
            category_list = []
            for c in self._categories:
                category_list.append(c.denominazione_breve)
                if self.categoria_articolo in (c.denominazione, c.denominazione_breve):
                    id_categoria = c.id
                    break
            if id_categoria == None:
                category_short_name = self.categoria_articolo[:7]
                if len(self._categories) > 0:
                    ind = 0
                    for category in category_list:
                        if category_short_name == category[:7]:
                            ind +=1
                    category_short_name = category_short_name+'/'+str(ind)
                daoCategoria = CategoriaArticolo().getRecord()
                daoCategoria.denominazione_breve = category_short_name
                daoCategoria.denominazione = self.categoria_articolo
                daoCategoria.persist()
                id_categoria = daoCategoria.id
                self._categories.append(daoCategoria)
        self.daoArticolo.id_categoria_articolo = id_categoria


        #VATs
        id_aliquota_iva = None
        if self.aliquota_iva is None:
            self.aliquota_iva_id = self.defaults['Aliquota iva']
            self.aliquota_iva = AliquotaIva(id=self.aliquota_iva_id).getRecord()
            id_aliquota_iva = self.aliquota_iva.id
        else:
            self._vats = AliquotaIva(isList=True).select(batchSize=None)
            for v in self._vats:
                if self.aliquota_iva.lower() in (v.denominazione_breve.lower(),v.denominazione.lower()) or\
                            int(str(self.aliquota_iva).replace('%','')) == int(v.percentuale):
                    id_aliquota_iva = v.id
                    break
            if id_aliquota_iva is None:
                self.aliquota_iva = str(self.aliquota_iva).replace('%','')
                daoAliquotaIva = AliquotaIva().getRecord()
                daoAliquotaIva.denominazione = 'ALIQUOTA '+ self.aliquota_iva +'%'
                daoAliquotaIva.denominazione_breve = self.aliquota_iva + '%'
                daoAliquotaIva.id_tipo = 1
                daoAliquotaIva.percentuale = Decimal(self.aliquota_iva)
                daoAliquotaIva.persist()
                id_aliquota_iva = daoAliquotaIva.id
                self._vats.append(daoAliquotaIva)
        self.daoArticolo.id_aliquota_iva = id_aliquota_iva


    #base units
        id_unita_base = None
        if  self.unita_base is None:
            self.unita_base_id = self.defaults['Unita base']
            #FIXME: promogest2 ----proviamo
            # La storedProcedure UnitaBaseGet NON esiste e la chiamta Dao qui sotto fallisce con un errore!!!
            self.unita_base = UnitaBase(id=self.unita_base_id).getRecord()
            id_unita_base = self.unita_base_id
        else:
            unis = UnitaBase(isList=True).select(batchSize=None)
            for u in unis:
                if self.unita_base.lower() in (u.denominazione.lower(),u.denominazione_breve.lower()):
                    id_unita_base = u.id
                    break
            if id_unita_base is None:
                self.unita_base = UnitaBase(isList=True).select(denominazione='Pezzi',
                                                                    batchSize=None)
                id_unita_base = self.unita_base.id
        self.daoArticolo.id_unita_base = id_unita_base
        self.daoArticolo.produttore = self.produttore or ''
        self.daoArticolo.cancellato = False
        self.daoArticolo.sospeso = False
        self.daoArticolo.persist()

        product_id = self.daoArticolo.id

        #barcode
        if self.codice_barre_articolo is not None:
            self.codice_barre_articolo = str(self.codice_barre_articolo)
            barCode = CodiceABarreArticolo(isList=True).select(codice=self.codice_barre_articolo,
                                                                batchSize=None)
            if len(barCode) > 0:
                daoBarCode = CodiceABarreArticolo(id=barCode[0].id).getRecord()
                daoBarCode.id_articolo = product_id
                daoBarCode.persist()
            else:
                daoBarCode = CodiceABarreArticolo().getRecord()
                daoBarCode.id_articolo = product_id
                daoBarCode.codice = self.codice_barre_articolo
                daoBarCode.primario = True
                daoBarCode.persist()

        #price-list--> product
        decimalSymbol = self.PLModel._decimalSymbol
        if (self.prezzo_vendita_non_ivato is not None or self.prezzo_acquisto_non_ivato is not None or self.prezzo_acquisto_ivato is not None or
            self.prezzo_vendita_ivato is not None):
            try:
                daoPriceListProduct = ListinoArticolo(isList=True).select(idListino=self.price_list_id,
                                                                    idArticolo=product_id,
                                                                    batchSize=None)[0]
            except:
                daoPriceListProduct = ListinoArticolo().getRecord()
                daoPriceListProduct.id_articolo = product_id
                daoPriceListProduct.id_listino = self.price_list_id
                daoPriceListProduct.data_listino_articolo = self.dataListino
                daoPriceListProduct.listino_attuale = False

            if self.prezzo_vendita_ivato is not None:
                prezzo = self.prezzo_vendita_ivato or '0'
                try:
                    daoPriceListProduct.prezzo_dettaglio = Decimal(prezzo)
                except:
                    prezzo = Decimal(self.checkDecimalSymbol(prezzo, decimalSymbol))
                    daoPriceListProduct.prezzo_dettaglio = prezzo
            else:
                daoPriceListProduct.prezzo_dettaglio = 0
            if self.prezzo_vendita_non_ivato is not None:
                prezzo = self.prezzo_vendita_non_ivato or 0
                try:
                    daoPriceListProduct.prezzo_ingrosso = Decimal(prezzo)
                except:
                    prezzo = Decimal(self.checkDecimalSymbol(prezzo, decimalSymbol))
                    daoPriceListProduct.prezzo_ingrosso = prezzo
            else:
                daoPriceListProduct.prezzo_ingrosso = Decimal('0')
            
                
            sconti_ingrosso = [ScontoVenditaIngrosso().getRecord(),]
            sconti_dettaglio = [ScontoVenditaDettaglio().getRecord(),]
            if self.sconto_vendita_ingrosso is not None:
                try:
                    sconti_ingrosso[0].valore = Decimal(self.sconto_vendita_ingrosso or 0)
                    sconti_ingrosso[0].tipo_sconto = 'percentuale'
                    daoPriceListProduct.sconto_vendita_ingrosso = sconti_ingrosso
                except:
                    sconti_ingrosso[0].valore = Decimal(self.checkDecimalSymbol(self.sconto_vendita_ingrosso, decimalSymbol))
                    sconti_ingrosso[0].tipo_sconto = 'percentuale'
                    daoPriceListProduct.sconto_vendita_ingrosso = sconti_ingrosso
            
            if self.sconto_vendita_dettaglio is not None:
                try:
                    sconti_dettaglio[0].valore = Decimal(self.sconto_vendita_dettaglio or 0)
                    sconti_dettaglio[0].tipo_sconto = 'percentuale'
                    daoPriceListProduct.sconto_vendita_dettaglio = sconti_dettaglio
                except:
                    sconti_dettaglio[0].valore = Decimal(self.checkDecimalSymbol(self.sconto_vendita_dettaglio, decimalSymbol))
                    sconti_dettaglio[0].tipo_sconto = 'percentuale'
                    daoPriceListProduct.sconto_vendita_dettaglio = sconti_dettaglio

            if self.prezzo_acquisto_non_ivato is not None:
                prezzo = self.prezzo_acquisto_non_ivato or '0'
                try:
                    daoPriceListProduct.ultimo_costo = Decimal(prezzo)
                except:
                    prezzo = Decimal(self.checkDecimalSymbol(prezzo, decimalSymbol))
                    daoPriceListProduct.ultimo_costo = prezzo
            elif self.prezzo_acquisto_ivato is not None:
                prezzo = self.prezzo_acquisto_ivato or '0'
                try:
                    daoPriceListProduct.ultimo_costo =  calcolaPrezzoIva(Decimal(prezzo), -1 * (Decimal(self.aliquota_iva.percentuale)))
                except:
                    prezzo = Decimal(self.checkDecimalSymbol(prezzo, decimalSymbol))
                    daoPriceListProduct.ultimo_costo =  calcolaPrezzoIva(prezzo, -1 * Decimal(str(self.aliquota_iva.percentuale)))
            daoPriceListProduct.persist()

        # Fornitura
        daoFornitura = Fornitura(isList=True).select(idFornitore=self.fornitore,
                                                    idArticolo=self.daoArticolo.id,
                                                    daDataPrezzo=self.dataListino,
                                                    aDataPrezzo=self.dataListino,
                                                    batchSize=None)
        if len(daoFornitura) == 0:
            daoFornitura = Fornitura().getRecord()
            daoFornitura.prezzo_netto = prezzo or 0
            daoFornitura.prezzo_lordo = prezzo or 0
            daoFornitura.id_fornitore = self.fornitore
            daoFornitura.id_articolo = self.daoArticolo.id
            daoFornitura.percentuale_iva = Decimal(str(self.aliquota_iva.percentuale))
            daoFornitura.data_prezzo = self.dataListino
            daoFornitura.codice_articolo_fornitore = self.codice_fornitore
            daoFornitura.fornitore_preferenziale = True
            daoFornitura.persist()

    def checkDecimalSymbol(self, number, symbol):
        """ adjust non decimal simbols """
        if number is None:
            return str(0)

        if symbol == '.':
            number = str(number).replace(',','')
        elif symbol == ',':
            number = str(number).replace('.','')
            number = str(number).replace(',','.')
        return number


class ImportPreview(GladeWidget):
    """create a preview window to check that import is being executed correctly"""

    # Table is the csv file data
    # Model is a priceListModel instance
    # ProductList is a list of dictionary that came from csv file
    # PromoPriceList is an existing "Listino" in the database. (what is it for?)
    def __init__(self, mainWindow, table, PLModel, productList, promoPriceList,Fornitore,data_listino):
        GladeWidget.__init__(self, 'import_preview_window')
        self.import_preview_window.set_title('Anteprima Importazione Dati')
        self._mainWindow = mainWindow
        self.window = self.getTopLevel()
        self.table = table
        self.PLModel = PLModel
        self.productList = productList
        self.promoPriceList = promoPriceList
        self.fornitore = Fornitore
        self.data_listino = data_listino
        self.draw()

    def draw(self):
        self.treeview = self.articoli_treeview
        rendererSx = gtk.CellRendererText()
        rendererDx = gtk.CellRendererText()
        rendererDx.set_property('xalign', 1)
        fields = self.PLModel._fields
        model = getDynamicStrListStore(len(fields))
        self.treeview.set_model(model)

        nc = 0
        for f in fields:
            column = gtk.TreeViewColumn(f, rendererSx, text=nc)
            column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
            column.set_clickable(False)
            column.set_resizable(True)
            column.set_expand(True)
            column.set_min_width(250)
            self.treeview.append_column(column)
            nc += 1
        remodel = self.treeview.get_model()

        for row in self.table:
            remodel.append(row)

    def on_import_preview_confirm_clicked(self, button):
        import csv
        savedlines = 0
        err_count = 0
        csvErrorFile = csv.DictWriter(file(Environment.documentsDir+'/import_error_list.csv', 'wb'), fieldnames=self.PLModel._fields,dialect='excel')
        for product in self.productList:
            productFromCsv = ProductFromCsv(product=product, PLModel=self.PLModel, promoPriceList=self.promoPriceList, idfornitore=self.fornitore, dataListino=self.data_listino)
            #try: #product data dictionary is transmitted to the method that will generate (or update) the corrispondent product
            productFromCsv.save()
            #except:
                #err_count += 1
                #csvErrorFile.writerow(product)
            savedlines += 1
        if err_count > 0:
            msg = """Si è verificato un errore nel salvataggio dei dati di qualche prodotto.
È stato creato un nuovo file CSV con questi prodotti nella cartella documenti.
Verificare gli errori nel file e ritentare l'importazione"""
            overDialog = gtk.MessageDialog(self.getTopLevel(),
                                                   gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
                                                   gtk.MESSAGE_ERROR,
                                                   gtk.BUTTONS_CANCEL, msg)
            response = overDialog.run()
            overDialog.destroy()
            savedlines = savedlines - err_count
        print u'Import Procedure completed.'
        print u'Articoli salvati: '+str(savedlines)
        print u'Articoli di cui è fallito l\'import (completamente): '+str(err_count)
        if savedlines > 0:
            msg = u'Operazione completata.\nsono stati importati/aggiornati '+str(savedlines)+' articoli.'

            overDialog = gtk.MessageDialog(self.getTopLevel(),
                                                                gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,\
                                                                gtk.MESSAGE_INFO,
                                                                gtk.BUTTONS_OK, msg)
            response = overDialog.run()
            overDialog.destroy()
            self.window.destroy()
            self._mainWindow.show_all()
        else:
            msg = u'Nessun articolo aggiornato/importato.'

            overDialog = gtk.MessageDialog(self.getTopLevel(),
                                                                gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,\
                                                                gtk.MESSAGE_INFO,
                                                                gtk.BUTTONS_OK, msg)
            response = overDialog.run()
            overDialog.destroy()
        if response == gtk.BUTTONS_OK:
            self.window.destroy()
            self._mainWindow.show_all()
        else:
            self.window.destroy()
            self._mainWindow.show_all()

    def on_import_preview_window_close(self, widget, event=None):
        self.window.destroy()
        self._mainWindow.show_all()
