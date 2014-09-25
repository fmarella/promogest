# -*- coding: utf-8 -*-

#    Copyright (C) 2005-2012 by Promotux
#                        di Francesco Meloni snc - http://www.promotux.it/

#    Author: Marco Pinna "Dr astico" <zoccolodignu@gmail.com>
#    Author: Francesco Meloni <francesco@promotux.it>
#    Author: Francesco Marella <francesco.marella@anche.no>

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


import re
from decimal import *
import os
from promogest import Environment
import promogest.ui.AnagraficaListini
import promogest.ui.Main
import promogest.ui.Login
from promogest.ui.GladeWidget import GladeWidget
from promogest.ui.Main import *
from promogest.ui.AnagraficaAliquoteIva import AnagraficaAliquoteIva
from promogest.ui.AnagraficaCategorieArticoli import AnagraficaCategorieArticoli
from promogest.ui.AnagraficaFamiglieArticoli import AnagraficaFamiglieArticoli
from promogest.lib.utils import *
from promogest.ui.utilsCombobox import fillModelCombobox
from promogest.ui.gtk_compat import *

from fieldsDict import *
from PriceListModel import PriceListModel


class ImportPriceListModels(GladeWidget):
    """ImportPriceList  manages all events from import_price_list_models"""

    def __init__(self, mainWindow, pathFile = None):
        GladeWidget.__init__(self, root='import_price_list_models_window',
                        path='ImportPriceList/gui/import_price_list_models_window.glade',
                        isModule=True)
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

        #cbe_renderer = gtk.CellRendererText()
        #self.model_name_comboboxentry.pack_start(cbe_renderer, True)
        #self.model_name_comboboxentry.add_attribute(cbe_renderer, 'text', 0)

        #Creating fields treeview

        treeview = self.fields_treeview
        renderer = gtk.CellRendererText()

        column = gtk.TreeViewColumn('Campo', renderer, text=0)
        column.set_sizing(GTK_COLUMN_FIXED)
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
        #self.model_name_comboboxentry.set_text_column(0)
        fillComboboxUnitaBase(self.default_unita_base_combobox)
        fillComboboxCategorieArticoli(self.default_categoria_combobox)
        fillComboboxFamiglieArticoli(self.default_famiglia_combobox)
        fillComboboxAliquoteIva(self.default_aliquotaiva_combobox)
        findComboboxRowFromStr(self.model_name_comboboxentry, self.priceListModel._name, 0)

        treeviewModel = self.fields_treeview.get_model()
        treeviewModel.clear()

        for f in self.priceListModel._fields:
            treeviewModel.append((f, ))

        defaults = self.priceListModel._defaultAttributes
        self.skip_first_line_checkbutton.set_active(int(self.priceListModel._skipFirstLine))
        self.skip_first_column_checkbutton.set_active(int(self.priceListModel._skipFirstColumn))
        mcolumn = 0
        if not(self.priceListModel._fieldsDelimiter is None or self.priceListModel._fieldsDelimiter == ''):
            model = self.fields_delimiter_combobox.get_model()
            for r in model:
                if r[mcolumn] == self.priceListModel._fieldsDelimiter:
                    self.fields_delimiter_combobox.set_active_iter(r.iter)
        if not(self.priceListModel._fieldsSeparator is None or self.priceListModel._fieldsSeparator == ''):
            model = self.fields_separator_combobox.get_model()
            for r in model:
                if r[mcolumn] == self.priceListModel._fieldsSeparator:
                    self.fields_separator_combobox.set_active_iter(r.iter)
        if not(self.priceListModel._decimalSymbol is None or self.priceListModel._decimalSymbol == ''):
            model = self.decimal_symbol_combobox.get_model()
            for r in model:
                if r[mcolumn] == self.priceListModel._decimalSymbol:
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
            elif posso("PW") and f == "Anno":
                self.anno_cb.set_active(True)
            elif posso("PW") and f == "Modello":
                self.modello_cb.set_active(True)
            elif posso("PW") and f == "Genere":
                self.genere_cb.set_active(True)
            elif posso("PW") and f == "Taglia":
                self.taglia_cb.set_active(True)
            elif posso("PW") and f == "Colore":
                self.colore_cb.set_active(True)
            elif posso("PW") and f == "Codice Padre":
                self.codice_padre_cb.set_active(True)
            elif posso("PW") and f == "Stagione":
                self.stagione_cb.set_active(True)
            elif posso("PW") and f == "Gruppo Taglia":
                self.gruppo_taglia_cb.set_active(True)
        def_list = ['Aliquota iva', 'Famiglia', 'Categoria', 'Unita base']

        self.default_unita_base_combobox.set_sensitive(False)
        self.default_categoria_combobox.set_sensitive(False)
        self.categoria_togglebutton.set_sensitive(False)
        self.default_famiglia_combobox.set_sensitive(False)
        self.famiglia_togglebutton.set_sensitive(False)
        self.default_aliquotaiva_combobox.set_sensitive(False)
        self.aliquota_iva_togglebutton.set_sensitive(False)

        for k, val in defaults.iteritems():
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
        if posso("PW"):
            self.modello_cb.set_active(False)
            self.anno_cb.set_active(False)
            self.taglia_cb.set_active(False)
            self.gruppo_taglia_cb.set_active(False)
            self.codice_padre_cb.set_active(False)
            self.genere_cb.set_active(False)
            self.stagione_cb.set_active(False)
            self.colore_cb.set_active(False)
        self.draw()

    def on_field_checkbutton_checked(self, checkbutton):
        if self.loading:
            return
        def_list = ['Aliquota iva', 'Famiglia', 'Categoria', 'Unita base']
#        _name = checkbutton.get_name()[:-3]
        _name = gtk.Buildable.get_name(checkbutton)[:-3]
        for k in possibleFieldsKeys:
            if _name == possibleFieldsDict[k]:
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
        """
        Remove the selected null-field from treeview
        """

        (model, iterator) = self.fields_treeview.get_selection().get_selected()
        nullFieldPattern= '^Valore nullo [0-9][0-9]?$'
        if bool(re.search(nullFieldPattern, model[iterator][0])):
            _field = model[iterator][0]
            self.priceListModel._fields.remove(_field)
            model.remove(iterator)
            self.remove_null_field_button.set_sensitive(False)
            self.refresh()

    def on_add_null_field_button_clicked(self, button):
        """
        aggiunge un valore nullo alla ricostruzione del modello
        """
        ind = 1
        pos = 0
        for n in self.priceListModel._fields:
            if bool(re.search('^Valore nullo [0-9][0-9]?$', n)):
                self.priceListModel._fields[pos] = 'Valore nullo '+str(ind)
                ind += 1
            pos +=1
        self.priceListModel._fields.append('Valore nullo '+str(ind))
        self.refresh()

    def on_save_button_clicked(self, button):
        """Calls the save method in PriceListModel class"""
        self.priceListModel.setDefaultFields()
        self.checkObligatoryFields()
        fileDialog = gtk.FileChooserDialog(title='Salvataggio modello',
                                           parent=self.getTopLevel(),
                                           action=GTK_FILE_CHOOSER_ACTION_SAVE,
                                           buttons=(gtk.STOCK_CANCEL,
                                                    GTK_RESPONSE_CANCEL,
                                                    gtk.STOCK_SAVE,
                                                    GTK_RESPONSE_OK),
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
        #print "FDFDFDSFSDFSDFSDFSDFSDFSD", dir(self.model_name_comboboxentry)
        f_name = self.model_name_comboboxentry.child.get_text().replace(' ', '_')

        fileDialog.set_current_name(f_name+'.pgx')

        response = fileDialog.run()

        if response == GTK_RESPONSE_OK:
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
                if not findStrFromCombobox(self.default_aliquotaiva_combobox, 2):
                    obligatoryField(self.getTopLevel(),
                            self.default_aliquotaiva_combobox,
                            'Attenzione! E\' necessario indicare il l\'aliquota iva associata\nal listino che si desidera importare')
            elif d == 'Famiglia':
                if not findStrFromCombobox(self.default_famiglia_combobox, 2):
                    obligatoryField(self.getTopLevel(),
                            self.default_aliquotaiva_combobox,
                            'Attenzione! Indicare la famiglia di appartenenza\ndegli articoli del listino.')
            elif d == 'Categoria':
                if not findStrFromCombobox(self.default_categoria_combobox, 2):
                    obligatoryField(self.getTopLevel(),
                            self.default_aliquotaiva_combobox,
                            'Attenzione! Indicare la categoria di appartenenza\ndegli articoli del listino.')
            elif d == 'Unita base':
                if not findStrFromCombobox(self.default_unita_base_combobox, 2):
                    obligatoryField(self.getTopLevel(),
                            self.default_aliquotaiva_combobox,
                            'Attenzione! Indicare l\'unita\' di misura degli articoli del listino')
            else:
                return

    def on_refresh_button_clicked(self, comboboxentry):

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
#        comboboxName = combobox.get_name()
        comboboxName = gtk.Buildable.get_name(combobox)
        value = findStrFromCombobox(combobox, 1) or ''

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
                value = findStrFromCombobox(combobox, 1)
                if 'Unita base' in self.priceListModel._defaultAttributes.keys():
                    if value == self.priceListModel._defaultAttributes['Unita base']:
                        return
                    else:
                        self.priceListModel._defaultAttributes['Unita base'] = value
        else:
            #FIXME:
            #we have to correct this mess
            print """non so che sta succedendo.
    segnalazione errori? per cosa? :D"""
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
        """
        on_aliquota_iva_togglebutton_toggled
        """
        if toggleButton.get_active():
            toggleButton.set_active(False)
            return
        anag = AnagraficaAliquoteIva()
        anagWindow = anag.getTopLevel()
        showAnagraficaRichiamata(self.getTopLevel(), anagWindow, toggleButton, self.refresh)

    def on_import_price_list_models_window_close(self, widget, event=None):
        """
        close the windows
        """
        self.window.destroy()
