# -*- coding: utf-8 -*-

#    Copyright (C) 2005-2012 by Promotux
#                        di Francesco Meloni snc - http://www.promotux.it/

# Author: Alceste Scalas <alceste@promotux.it>
# Author: Andrea Argiolas <andrea@promotux.it>
# Author: Francesco Meloni <francesco@promotux.it

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

import time
from promogest.ui.gtk_compat import *
import os
import sys
import threading
import os.path
from promogest.Environment import conf
from promogest.ui.GladeWidget import GladeWidget
from promogest.ui.widgets.FilterWidget import FilterWidget
from promogest.lib.XmlGenerator import XlsXmlGenerator
from promogest.lib.CsvGenerator import CsvFileGenerator
from promogest.ui.utils import *
import subprocess
import shlex
from promogest import Environment
from calendar import Calendar
#if Environment.new_print_enjine:
from promogest.lib.sla2pdf.Sla2Pdf_ng import Sla2Pdf_ng
from promogest.lib.sla2pdf.SlaTpl2Sla import SlaTpl2Sla as SlaTpl2Sla_ng
from promogest.lib.SlaTpl2Sla import SlaTpl2Sla
#else:
from promogest.lib.GtkPrintDialog import GtkPrintDialog
from promogest.ui.SendEmail import SendEmail
from promogest.lib.HtmlHandler import createHtmlObj, renderTemplate, renderHTML
from promogest.dao.Azienda import Azienda
from hashlib import md5

if not Environment.pg3:
    try:
        import gtkunixprint
        gtkunixprint # pyflakes
    except ImportError:
        gtkunixprint = None
else:
    gtkunixprint = None



class Anagrafica(GladeWidget):
    """ Classe base per le anagrafiche di Promogest """

    def __init__(self, windowTitle, recordMenuLabel,
            filterElement, htmlHandler, reportHandler,
            editElement, labelHandler = None,
            gladeFile=None, aziendaStr=None):
        GladeWidget.__init__(self, 'anagrafica_complessa_window',
                            fileName=gladeFile)
        if aziendaStr is not None:
            self.anagrafica_complessa_window.set_title(windowTitle[:12]+' su ('+aziendaStr+') - '+windowTitle[11:])
        else:
            self.anagrafica_complessa_window.set_title(windowTitle)
        self.record_menu.get_child().set_label(recordMenuLabel)
        if self.anagrafica_complessa_window not in Environment.windowGroup:
            Environment.windowGroup.append(self.anagrafica_complessa_window)

        self.html = createHtmlObj(self)
        self.anagrafica_detail_scrolledwindow.add(self.html)
        self._setFilterElement(filterElement)
        self._setHtmlHandler(htmlHandler)
        self._setReportHandler(reportHandler)
        self._setEditElement(editElement)
        self._setLabelHandler(labelHandler)
        self._selectedDao = None
        if self.__class__.__name__ == 'AnagraficaDocumenti':
            for tracciato in tracciati_disponibili():
                if tracciato == 'conad':
                    self.esporta_conad_menuitem.show()
                elif tracciato == 'buffetti':
                    self.esporta_buffetti_menuitem.show()
                else:
                    pass
            self.records_file_export.set_menu(self.menu3)
        # Initial (in)sensitive widgets
        textStatusBar = "     *****   PromoGest - 070 8649705 - www.promogest.me - assistenza@promotux.it  *****     "
        context_id =  self.pg2_statusbar.get_context_id("anagrafica_complessa_windows")
        self.pg2_statusbar.push(context_id,textStatusBar)
        self.record_delete_button.set_sensitive(False)
        self.record_delete_menu.set_sensitive(False)
        self.duplica_button.set_sensitive(False)
        self.record_edit_button.set_sensitive(False)
        self.record_edit_menu.set_sensitive(False)
        self.duplica_in_cliente.set_sensitive(False)
        self.duplica_in_fornitore.set_sensitive(False)
#        self.record_duplicate_menu.set_property('visible', False)
#        self.record_duplicate_menu.set_no_show_all(True)
        self.record_duplicate_menu.set_sensitive(False)
        self.duplica_button.set_sensitive(False)
        self.selected_record_print_button.set_sensitive(False)
        self.selected_record_print_menu.set_sensitive(False)
        if self.__class__.__name__ != 'AnagraficaListiniArticoli':
            self.modifiche_menu.destroy()
        if self.__class__.__name__ != 'AnagraficaDocumenti':
            self.strumenti_menu.destroy()
        self.placeWindow(self.anagrafica_complessa_window)
        self.filter.draw()
        self.editElement.draw(cplx=True)
        self.email = ""
        if self.__class__.__name__ !="AnagraficaPrimaNota":
            self.info_anag_complessa_label.destroy()
        self.setFocus()

    def _setFilterElement(self, gladeWidget):
        self.bodyWidget = FilterWidget(owner=gladeWidget, filtersElement=gladeWidget)

        self.filter = self.bodyWidget.filtersElement
        self.filterTopLevel = self.filter.getTopLevel()

        filterElement = self.bodyWidget.filter_frame
        filterElement.unparent()
        self.anagrafica_filters_viewport.add(filterElement)
        self.anagrafica_hpaned.set_position(350)

        resultElement = self.bodyWidget.filter_list_vbox
        resultElement.unparent()
        self.anagrafica_results_viewport.add(resultElement)

        self.anagrafica_filter_treeview = self.bodyWidget.resultsElement

        gladeWidget.build()

        accelGroup = gtk.AccelGroup()
        self.getTopLevel().add_accel_group(accelGroup)
        self.bodyWidget.filter_clear_button.add_accelerator('clicked',
                            accelGroup, GDK_KEY_ESCAPE, 0, GTK_ACCEL_VISIBLE)
        self.bodyWidget.filter_search_button.add_accelerator('clicked',
                            accelGroup, GDK_KEY_F3, 0, GTK_ACCEL_VISIBLE)
#        self.bodyWidget.filter_search_button.add_accelerator('clicked',
#                            accelGroup, gtk.keysyms.KP_Enter, 0, gtk.ACCEL_VISIBLE)
#        self.bodyWidget.filter_search_button.add_accelerator('clicked',
#                            accelGroup, gtk.keysyms.Return, 0, gtk.ACCEL_VISIBLE)

    def _setHtmlHandler(self, htmlHandler):
        self.htmlHandler = htmlHandler
        html = """<html><body></body></html>"""
        renderHTML(self.html,html)

    def _setLabelHandler(self, labelHandler):
        self.labelHandler = labelHandler

    def _setReportHandler(self, reportHandler):
        self.reportHandler = reportHandler

    def _setEditElement(self, gladeWidget):
        self.editElement = gladeWidget

    def placeWindow(self, window):
        GladeWidget.placeWindow(self, window)
        if (self.width is None and self.height is None and
            self.left is None and self.top is None):
            window.maximize()

    def show_all(self):
        """ Visualizza/aggiorna tutta la struttura dell'anagrafica """
        self.anagrafica_complessa_window.show_all()

    def on_esporta_conad_menuitem_activate(self, menuitem):
        from promogest.dao.TestataDocumento import TestataDocumento
        from promogest.dao.InformazioniFatturazioneDocumento import InformazioniFatturazioneDocumento
        from promogest.lib.parser import myparse
        from promogest.dao.Azienda import Azienda

        def dati_file_conad(testata):
            """ 
            """
            if testata:
                #Scriviamo la testata della fattura
                dati_differita = InformazioniFatturazioneDocumento().select(id_fattura = testata.id)
                azienda = Azienda().getRecord(id=Environment.azienda)
                codice_fornitore = ''
                if azienda:
                    codice_fornitore = azienda.matricola_inps
                if dati_differita:
                    for ddtt in dati_differita:
                        ddt = TestataDocumento().getRecord(id=ddtt.id_ddt)
        
                        dati = {
                            'testata': {
                                'numero_progressivo': str(dati_differita.index(ddtt) + 1),
                                'numero_fattura': str(testata.numero),
                                'data_fattura': testata.data_documento,
                                'numero_bolla': str(ddt.numero),
                                'data_bolla': ddt.data_documento,
                                'codice_fornitore': codice_fornitore,
                                'codice_cliente': ddt.ragione_sociale_cliente,
                            },
                            'dettaglio': []
                        }
                        
        
                        for riga in ddt.righe:
                            if riga.id_articolo:
                                art = leggiArticolo(riga.id_articolo)
                                dati['dettaglio'].append(
                                    {
                                        'numero_progressivo':str(dati_differita.index(ddtt) + 1),
                                        'codice_articolo': str(art["codice"]),
                                        'descrizione': str(art["denominazione"].replace("à", "a")),
                                        'unita_misura': str(art["unitaBase"]).upper(),
                                        'qta_fatturata': str(mN(Decimal(riga.quantita * (riga.moltiplicatore or 1)), 2)),
                                        'prezzo_unitario': str(mN(Decimal(riga.valore_unitario_netto), 3)),
                                        'importo_totale': str(mN(Decimal(riga.quantita or 0) * Decimal(riga.moltiplicatore or 1) * Decimal(riga.valore_unitario_netto or 0), 3)),
                                        'aliquota_iva': str(mN(riga.percentuale_iva,0))
                                    })
                    return dati
        # Otteniamo il documento
        dao = self.filter.getSelectedDao()
        self._selectedDao = dao
        # Generiamo i dati utili dal documento
        dati = dati_file_conad(dao)
        xml_file = open(os.path.join(Environment.tracciatiDir, 'conad.xml'))
        
        def get_save_filename():
            dialog = gtk.FileChooserDialog("Inserisci il nome del file",
                                           None,
                                           GTK_FILE_CHOOSER_ACTION_SAVE,
                                           (gtk.STOCK_CANCEL, GTK_RESPONSE_CANCEL,
                                            gtk.STOCK_SAVE, GTK_RESPONSE_OK))
            dialog.set_default_response(GTK_RESPONSE_OK)
            
            self.__homeFolder = setconf("General", "cartella_predefinita") or None
            if self.__homeFolder is None:
                if os.name == 'posix':
                    self.__homeFolder = os.environ['HOME']
                elif os.name == 'nt':
                    self.__homeFolder = os.environ['USERPROFILE']
            dialog.set_current_folder(self.__homeFolder)
            
            response = dialog.run()
          
            if response == GTK_RESPONSE_OK:
                save_filename = dialog.get_filename()
                dialog.destroy()
                return save_filename
            else:
                dialog.destroy()
                return None

        save_filename = get_save_filename()
        if save_filename is None:
            return
        file_out = open(save_filename, 'wb')

        try:
            myparse(xml_file, dati, file_out)
        except Exception as e:
            messageError("Si è verificato un problema durante l'esportazione.")
        else:
            messageInfo("Esportazione eseguita con successo")

    def on_esporta_buffetti_menuitem_activate(self, menuitem):
        pass

    def on_records_file_export_clicked(self, widget):
        dao = self.editElement.setDao(None)
        #print "DAOO", dao
#        data = self.set_export_data()
#        data_export = self.filter.xptDaoList

#        values = self.set_data_list(data_export)

        from ExportCsv import ExportCsv
        anag = ExportCsv(self, dao=dao)
        dao=None
        return

        data = self.set_export_data()
        saveDialog = gtk.FileChooserDialog("export in a file...",
                                            None,
                                            gtk.FILE_CHOOSER_ACTION_SAVE,
                                            (gtk.STOCK_CANCEL,
                                                GTK_RESPONSE_CANCEL,
                                                gtk.STOCK_SAVE,
                                            GTK_RESPONSE_OK))
        saveDialog.set_default_response(GTK_RESPONSE_OK)

        self.__homeFolder = setconf("General", "cartella_predefinita") or ""
        if self.__homeFolder == '':
            if os.name == 'posix':
                self.__homeFolder = os.environ['HOME']
            elif os.name == 'nt':
                self.__homeFolder = os.environ['USERPROFILE']
        saveDialog.set_current_folder(self.__homeFolder)
        folder = self.__homeFolder

        filter = gtk.FileFilter()
        filter.set_name("All files")
        filter.add_pattern("*")
        saveDialog.add_filter(filter)

        filter1 = gtk.FileFilter()
        filter1.set_name("XML files")
        filter1.add_pattern("*.xml")
        filter1.add_pattern("*.XML")
        saveDialog.add_filter(filter1)

        filter2 = gtk.FileFilter()
        filter2.set_name("CSV files")
        filter2.add_pattern("*.csv")
        filter2.add_pattern("*.CSV")
        saveDialog.add_filter(filter2)

        currentName = data['currentName']
        saveDialog.set_filter(filter1)
        saveDialog.set_current_name(currentName)
        cb_typeList = [['CSV','Csv compatibile Excel'],
                                            ['XML','MS Excel 2003 Xml format']]
        typeComboBox = insertFileTypeChooser(filechooser=saveDialog,
                                                            typeList=cb_typeList)
        typeComboBox.connect('changed', on_typeComboBox_changed,
                                                        saveDialog, currentName)
        typeComboBox.set_active(1)
        xmlMarkup = data['XmlMarkup']

        data_export = self.filter.xptDaoList

        values = self.set_data_list(data_export)
        saveDialog.show_all()
        response = saveDialog.run()
        if response == GTK_RESPONSE_OK:
            (fileType,file_name) = on_typeComboBox_changed(typeComboBox,
                                                            saveDialog,
                                                            currentName,
                                                            isEvent=False)
            if fileType == "CSV":
                csvFile = CsvFileGenerator(file_name)
                csvFile.setAttributes(head=xmlMarkup[0],
                                        cols=xmlMarkup[2],
                                        data=values,
                                        totColumns=xmlMarkup[1])
                csvFile.createFile(wtot=True)
            elif fileType == "XML":
                xmlFile = XlsXmlGenerator(file_name)
                xmlFile.setAttributes(head=xmlMarkup[0], cols=xmlMarkup[2], data=values, totColumns=xmlMarkup[1])
                # wtot is to tell the function if it can close the worksheet after filling it with data.
                xmlFile.createFile(wtot=True)
                #the previous function by default closes automatically the worksheet
                #xmlFile.close_sheet()
                xmlFile.XlsXmlFooter()
            saveDialog.destroy()
        elif response == GTK_RESPONSE_CANCEL:
            saveDialog.destroy()

    def on_credits_menu_activate(self, widget):
        creditsDialog = GladeWidget('credits_dialog', callbacks_proxy=self)
        creditsDialog.getTopLevel().set_transient_for(self.getTopLevel())
        creditsDialog.getTopLevel().show_all()
        response = creditsDialog.credits_dialog.run()
        if response == GTK_RESPONSE_OK:
            creditsDialog.credits_dialog.destroy()

    def on_send_Email_activate(self, widget):
        sendemail = SendEmail()

    def on_licenza_menu_activate(self, widget):
        licenzaDialog = GladeWidget('licenza_dialog', callbacks_proxy=self)
        licenzaDialog.getTopLevel().set_transient_for(self.getTopLevel())
        licenseText = ''
        try:
            lines = open('./LICENSE').readlines()
            for l in lines:
                licenseText += l
        except:
            licenseText = 'Lavori in corso ....'
            print 'License file not found (LICENSE).'
        textBuffer = licenzaDialog.licenza_textview.get_buffer()
        textBuffer.set_text(licenseText)
        licenzaDialog.licenza_textview.set_buffer(textBuffer)
        licenzaDialog.getTopLevel().show_all()
        response = licenzaDialog.licenza_dialog.run()
        if response == GTK_RESPONSE_OK:
            licenzaDialog.licenza_dialog.destroy()

    def on_seriale_menu_activate(self, widget):
        try:
            fileName = Environment.conf.guiDir + 'logo_promogest.png'
            f = open(fileName,'rb')
            content = f.read()
            f.close()
            msg = 'Codice installazione:\n\n' + str(md5.new(content).hexdigest().upper())
        except:
            msg = 'Impossibile generare il codice !!!'
        messageInfo(msg=msg)

    def on_anagrafica_filter_treeview_cursor_changed(self, treeview=None):
        sel = self.anagrafica_filter_treeview.get_selection()
        if sel.get_mode() == GTK_SELECTIONMODE_MULTIPLE:
            return
        elif sel.get_mode() == GTK_SELECTIONMODE_SINGLE:
            (model, iterator) = sel.get_selected()
            if iterator is not None:
                self.dao = model.get_value(iterator, 0)
            else:
                self.dao = None
        if self.dao is not None:
            self.htmlHandler.setDao(self.dao)

        self.record_edit_button.set_sensitive(self.dao is not None)
        self.record_edit_menu.set_sensitive(self.dao is not None)
        if self.dao.__class__.__name__ in ["TestataDocumento", "Articolo", "TestataMovimento", "Listino"]:
            self.duplica_button.set_sensitive(self.dao is not None)
            self.record_duplicate_menu.set_sensitive(self.dao is not None)

        self.record_delete_button.set_sensitive(self.dao is not None)
        self.record_delete_menu.set_sensitive(self.dao is not None)

        self.selected_record_print_button.set_sensitive(self.dao is not None)
        self.selected_record_print_menu.set_sensitive(self.dao is not None)
        return self.dao or False

    def on_anagrafica_filter_treeview_row_activated(self, widget, path, column):
        self.on_record_edit_activate(widget, path, column)

    def on_anagrafica_filter_treeview_selection_changed(self, treeSelection):
        sel = treeSelection
        self.daoSelection = []
        self.dao = None
        if sel.get_mode() == GTK_SELECTIONMODE_MULTIPLE:
            model, iterator = sel.get_selected_rows()
            count = sel.count_selected_rows()
            if count > 1:
                for iter in iterator:
                    self.daoSelection.append(model[iter][0])
                self.dao = None
            elif count == 1:
                self.dao = model[iterator[0]][0]
            else:
                iterator = None
                # No items are currently selected
                self.dao = None
        else:
            return
        if self.dao is not None:
            self.htmlHandler.setDao(self.dao)

        self.record_edit_button.set_sensitive(self.dao is not None)
        self.record_edit_menu.set_sensitive(self.dao is not None)
        if self.dao.__class__.__name__ in ["TestataDocumento", "Articolo", "TestataMovimento", "Listino"]:
            self.duplica_button.set_sensitive(self.dao is not None)
            self.record_duplicate_menu.set_sensitive(self.dao is not None)
            
        if self.dao.__class__.__name__ == 'TestataDocumento':
            self.esporta_conad_menuitem.set_sensitive(self.dao is not None)
            self.esporta_buffetti_menuitem.set_sensitive(self.dao is not None)

        self.record_delete_button.set_sensitive(self.dao is not None)
        self.record_delete_menu.set_sensitive(self.dao is not None)

        self.selected_record_print_button.set_sensitive(self.dao is not None)
        self.selected_record_print_menu.set_sensitive(self.dao is not None)
        return self.daoSelection or self.dao or False

    def on_record_new_activate(self, widget=None, from_other_dao=None):
        self.editElement.setVisible(True)
        if self.__class__.__name__=="AnagraficaUtenti":
            self.editElement.setDao(None, from_other_dao=from_other_dao)
        else:
            self.editElement.setDao(None)
        self.setFocus()

    def on_record_delete_activate(self, widget):
        if not YesNoDialog(msg='Confermi l\'eliminazione ?', transient=self.getTopLevel()):
            return
        dao = self.filter.getSelectedDao()
        if dao:
            dao.delete()
        self.filter.refresh()
        self.htmlHandler.setDao(None)
        self.setFocus()

    def on_record_edit_activate(self, widget=None, path=None, column=None, dao=None):
        if not dao:
            dao = self.filter.getSelectedDao()
        self._selectedDao = dao
        self.editElement.setVisible(True)
        self.editElement.setDao(dao)
        self.setFocus()

    def on_record_duplicate_menu_activate(self, widget, path=None, column=None):
        dao = self.filter.getSelectedDao()
        self._selectedDao = dao
        self.duplicate(dao)

    def duplicate(self):
        """ Duplica il dao corrente """
        raise NotImplementedError

    def on_records_print_activate(self, widget):
        self._handlePrinting(pdfGenerator=self.reportHandler, report=True)

    def on_Stampa_Frontaline_clicked(self, widget):
        if posso("LA"):
            results = self.filter.runFilter(offset=None, batchSize=None)
            self.manageLabels(results)
        else:
            fenceDialog()

    def on_selected_record_print_activate(self, widget):
        self._handlePrinting(daos=[self.filter.getSelectedDao()],
                             pdfGenerator=self.htmlHandler,
                             report=True)

    def manageLabels(self, results):
        from promogest.modules.Label.ui.ManageLabelsToPrint import ManageLabelsToPrint
        a = ManageLabelsToPrint(mainWindow=self,daos=results)
        anagWindow = a.getTopLevel()
        returnWindow = self.getTopLevel().get_toplevel()
        anagWindow.set_transient_for(returnWindow)
        anagWindow.show_all()

    def _handlePrinting(self, pdfGenerator, report,
                        daos=None, label=None,
                        returnResults=None,classic=False, template_file=False):
        # FIXME: refactor this mess!!!

        # tiro su la finestrella con la progress bar
        progressDialog = GladeWidget('records_print_progress_dialog',
                                     callbacks_proxy=self)
        progressDialog.getTopLevel().set_transient_for(self.getTopLevel())
        progressDialog.getTopLevel().show_all()
        pbar = progressDialog.records_print_progress_bar
        pbar.set_text('Lettura dati')

        self.__pulseSourceTag = None
        self.__cancelOperation = False
        self.__pdfGenerator = pdfGenerator
        self.__returnResults = returnResults
        self.__pdfReport = None
        self._reportType = report
        self._template_file = template_file
        self._classic = classic
        self.label = label # tipo report ma anche opzione label
        self._pdfName = str(pdfGenerator.defaultFileName)
        self._folder = setconf("General", "cartella_predefinita") or ""
        if self._folder == '':
            if os.name == 'posix':
                self._folder = os.environ['HOME']
            elif os.name == 'nt':
                self._folder = os.environ['USERPROFILE']

        def showPrintingDialog():
            if self.__cancelOperation:
                # Operation has been cancelled, do nothing
                return

            progressDialog.getTopLevel().destroy()
            gobject.source_remove(self.__pulseSourceTag)

            printDialog = GladeWidget('records_print_dialog',
                                      callbacks_proxy=self)
            printDialog.getTopLevel().set_transient_for(self.getTopLevel())

            printDialog.records_print_dialog_description_label.set_text(self._pdfName)
            printDialog.email_destinatario_entry.set_text(self.email)
            printDialog.records_print_dialog_size_label.set_text(str(len(self.__pdfReport) / 1024) + ' Kb')
            printDialog.placeWindow(printDialog.getTopLevel())
            printDialog.getTopLevel().show_all()
            self.printDialog = printDialog
            return False

        def progressCB(results, prevLen, totalLen):
            if self.__cancelOperation:
                raise Exception, 'Operation cancelled, thread killed'

            # Let's schedule progress bar update from the main thread
            def updateProgressBarIdle():
                if self.__cancelOperation:
                    # Progress bar is being destroyed, do nothing
                    return
                if results:
                    frac = len(results) / float(totalLen)
                    pbar.set_fraction(frac)
                return False
            gobject.idle_add(updateProgressBarIdle)

            if len(results) == totalLen:
                # We're done: let's switch progress bar type from the
                # main thread

                def renewProgressBarIdle():
                    pbar.set_pulse_step(0.07)
                    pbar.set_text('Creazione della stampa')

                    # Let's also schedule the progress bar pulsing from
                    # the main thread
                    def pulsePBar():
                        pbar.pulse()
                        return True
                    self.__pulseSourceTag = gobject.timeout_add(33, pulsePBar)

                    return False
                gobject.idle_add(renewProgressBarIdle)

                # In the end, let's launch the template rendering thread
                def renderingThread():
                    """ Questo è il thread di conversione e generazione della stampa"""
                    operationName = ""

                    pdfGenerator.setObjects(results)
                    self._pdfName = str(pdfGenerator.defaultFileName)

                    if pdfGenerator.defaultFileName == 'documento':
                        dao = self.filter.getSelectedDao()
                        data = dao.data_documento
                        operationName = dao.operazione
                        if dao.id_cliente:
                            self.email = leggiCliente(dao.id_cliente)['email']
                        elif dao.id_fornitore:
                            self.email = leggiFornitore(dao.id_fornitore)['email']
                        else:
                            self.email = ''
                        intestatario = permalinkaTitle(dao.intestatario)[0:15] or ""
                        #intestatario = dao.intestatario[0:15].replace(" ","_").replace("\\n","") or ""
                        self._pdfName = operationName + \
                                        '_' +\
                                        str(dao.numero) +\
                                        '_' +\
                                        intestatario + \
                                        '_' +\
                                        data.strftime('%d-%m-%Y')
                    elif pdfGenerator.defaultFileName == 'promemoria':
                        dao = self.filter.getSelectedDao()
                        self._pdfName = self.__pdfGenerator.defaultFileName +\
                                        '_' + \
                                        str(dao.id)
                    elif pdfGenerator.defaultFileName == 'label':

                        self._pdfName = pdfGenerator.defaultFileName +\
                                        '_' + \
                                        time.strftime('%d-%m-%Y')
                        operationName = "label"
                    self.__pdfReport = pdfGenerator.pdf(operationName,
                                                classic=self._classic,
                                                template_file=self._template_file)

                    # When we're done, let's schedule the printing
                    # dialog (going back to the main GTK loop)
                    gobject.idle_add(showPrintingDialog)
                if pdfGenerator.defaultFileName == 'label' and self.__returnResults == None:
                    progressDialog.getTopLevel().destroy()
                    #gobject.idle_add(self.manageLabels,results)
                    self.manageLabels(results)
                else:
                    if Environment.tipo_eng =="sqlite":
                        renderingThread()
                    else:
                        t = threading.Thread(group=None, target=renderingThread,
                                            name='Data rendering thread', args=(),
                                            kwargs={})
                        #t.setDaemon(True) # FIXME: are we sure?
                        t.start()

        def fetchingThread(daos=None):
            """ funzione di prelievo dei risultati """
            if daos is None:
                # Let's fetch the data
                self.unused = self.filter.runFilter(offset=None, batchSize=None,
                                               progressCB=progressCB,
                                               progressBatchSize=5)
                progressCB(results=self.unused, prevLen=0, totalLen=len(self.unused))
            else:
                # We've got all the data we need, let's jump to the
                # callback directly
                progressCB(results=daos, prevLen=0, totalLen=len(daos))

        # Qui c'è il cuore della funzione di stampa con il lancio del thread separato
        if Environment.tipo_eng =="sqlite":
            fetchingThread(daos=daos)
        else:
            t = threading.Thread(group=None, target=fetchingThread,
                                name='Data fetching thread', args=(),
                                kwargs={'daos' : daos})
            #t.setDaemon(True) # FIXME: are we sure?
            t.start()

    def on_records_print_on_screen_activate(self, widget):
        """ Questo segnale rimanda a AnagraficaComplessaReport
        che a sua volta rimanda a AnagraficaComplessaPrinterPreview che
        si occupa della visualizzazione e della stampa"""
        previewDialog = self.reportHandler.buildPreviewWidget()

    def on_report_farmacia_veterinaria_activate(self, widget):
        previewDialog = self.reportHandler.buildPreviewWidget(veter=True)

    def on_records_print_progress_dialog_response(self, dialog, responseId):
        if responseId == GTK_RESPONSE_CANCEL:
            self.__cancelOperation = True

            #self.__pdfGenerator.cancelOperation()

            if self.__pulseSourceTag is not None:
                gobject.source_remove(self.__pulseSourceTag)

            self.on_records_print_dialog_close(dialog)
#            del self.__pdfReport
#            del self.__pdfGenerator


    def on_records_print_progress_dialog_close(self, dialog, event=None):
        # FIXME: we're leaving the threads running!
        dialog.destroy()

    def on_cerca_contatto_button_clicked(self, widget):
        from promogest.modules.Contatti.ui.RicercaContatti import RicercaContatti
        
        def aggiorna_email(anagWindow, tipo):
            if anag.dao is None:
                id = None
            else:
                id = anag.dao.id
            if tipo == 'fornitore':
                res = leggiFornitore(id)
            elif tipo == 'cliente':
                res = leggiCliente(id)
            elif tipo == 'contatto':
                res = leggiContatto(id)
            self.printDialog.email_destinatario_entry.set_text(res["email"])
            self.email = res["email"]
            anagWindow.destroy()
        
        anag = RicercaContatti()
        anagWindow = anag.getTopLevel()
        anagWindow.connect("hide", aggiorna_email, 'contatto')
        anagWindow.set_transient_for(self.printDialog.getTopLevel())
        anag.show_all()

    def tryToSavePdf(self, pdfFile):
        try:
        ##trying to save the file with the right name
            f = file(pdfFile, 'wb')
            f.write(self.__pdfReport)
            f.close()
        except:
            msg = """Errore nel salvataggio!
Verificare i permessi della cartella"""
            messageError(msg=msg)
            return

    def on_directprint_button_clicked(self, button):
        if gtkunixprint:
            pdfFile = os.path.join(self._folder + self._pdfName +'.pdf')
            self.tryToSavePdf(pdfFile)
            dialog = GtkPrintDialog(pdfFile)
            dialog.run()
            #os.unlink(report.filename)
        elif os.name == "nt":
            try:
                import win32api
                pdfFile = os.path.join(self._folder + self._pdfName +'.pdf')
                self.tryToSavePdf(pdfFile)
                win32api.ShellExecute (0, "print", pdfFile, None, ".", 0)
            except:
                messageInfo(msg="Per fare funzionare questa opzione su windows installa questo pacchetto: ftp://promotux.it/pywin32-216.win32-py2.6.exe ")


    def on_send_email_button_clicked(self, widget):
        '''
        '''
        self.email = self.printDialog.email_destinatario_entry.get_text()
        pdfFile = os.path.join(self._folder + self._pdfName +'.pdf')
        self.tryToSavePdf(pdfFile)

        fileName = self._pdfName +'.pdf'
        subject= "Invio: %s" % fileName
        body = conf.body %fileName

        messageInfo(msg="""Il client di posta consigliato è <b>Thunderbird</b>.

Chi avesse bisogno di un template di spedizione email più complesso anche in formato
html contatti <b>assistenza@promotux.it</b> per informazioni.""")

        if os.name == "nt":
            arghi = "start thunderbird -compose subject='%s',body='%s',attachment='file:///%s',to='%s'" %(subject, body, str(pdfFile), self.email)
        else:
            clients = ('thunderbird', 'icedove')
            flag = False
            for client in clients:
                if subprocess.call('which %s' % client, shell=True) == 0:
                    arghi = "%s -compose subject='%s',body='%s',attachment='file:///%s',to='%s'" % (client, subject, body, str(pdfFile), self.email)
                    flag = True
                    break
            #TODO: dividere self.email al carattere ';' e accodare ciascun indirizzo come 'a@email.com' 'b@email.com' 
            if not flag:
                arghi = "xdg-email --utf8 --subject '%s' --body '%s' --attach '%s' '%s'" %(subject, body, str(pdfFile), self.email)
        subprocess.Popen(arghi, shell=True)

    def on_close_button_clicked(self,widget):
        self.on_records_print_dialog_close(self.printDialog)

    def on_save_button_clicked(self, widget):
        self.__handleSaveResponse(self.printDialog.getTopLevel())
        #self.on_records_print_dialog_close(self.printDialog)

    def on_open_button_clicked(self, widget):
        self.__handleOpenResponse(self.printDialog.getTopLevel())
        #self.on_records_print_dialog_close(self.printDialog)

    def on_records_print_dialog_close(self, dialog, event=None):
        dialog.hide()
#        del self.__pdfReport
#        del self.__pdfGenerator

    def __handleOpenResponse(self, dialog):
        """ Qui gestiamo l'apertura
        """
        pdfFile = os.path.join(self._folder + self._pdfName +'.pdf')
        self.pdfFile = pdfFile
        self.tryToSavePdf(pdfFile)
        try:
            subprocess.Popen(['xdg-open', pdfFile])
        except:
            os.startfile(pdfFile)

    def __handleSaveResponse(self, dialog):
        fileDialog = gtk.FileChooserDialog(title='Salva il file',
                                           parent=dialog,
                                           action=gtk.FILE_CHOOSER_ACTION_SAVE,
                                           buttons=(gtk.STOCK_CANCEL,
                                                    GTK_RESPONSE_CANCEL,
                                                    gtk.STOCK_SAVE,
                                                    GTK_RESPONSE_OK),
                                           backend=None)
        fileDialog.set_current_name(self._pdfName+".pdf")
        fileDialog.set_current_folder(self._folder)

        fltr = gtk.FileFilter()
        fltr.add_mime_type('application/pdf')
        fltr.set_name('File Promogest:(*.pdf & *.ods)')
        fltr.add_pattern("*.pdf")
        fileDialog.add_filter(fltr)

        fltr = gtk.FileFilter()
        fltr.set_name("All files")
        fltr.add_pattern("*")
        fltr.set_name('Tutti i file')
        fileDialog.add_filter(fltr)

        response = fileDialog.run()
        # FIXME: handle errors here
        if ( (response == GTK_RESPONSE_CANCEL) or ( response == GTK_RESPONSE_DELETE_EVENT)) :
            pass
        elif response == GTK_RESPONSE_OK:
            filename = fileDialog.get_filename()

            #modifiche
            can_save = 0
            esci = False
            # Let's check whether the file is going to be overwritten

            while esci == False:

                if os.path.exists(filename):
                    msg = 'Il file "%s" esiste.  Sovrascrivere?' % filename
                    if YesNoDialog(msg=msg, transient=self.getTopLevel()):
                        can_save = 1
                        #overwrite the file if user click  yes
                        break
                    else:
                        response =  fileDialog.run()
                        if response == GTK_RESPONSE_CANCEL or response == GTK_RESPONSE_DELETE_EVENT:
                            #exit but don't save the file
                            esci = True
                            can_save = 0
                            break
                        elif response == GTK_RESPONSE_OK:
                            filename = fileDialog.get_filename()
                else:
                    can_save = 1

                if can_save == 1:
                    while True:
                        try:
                            #trying to save the file
                            f = file(filename, 'wb')
                            f.write(self.__pdfReport)
                            f.close()
                            esci = True
                            break
                        except:
                            msg = """Errore nel salvataggio!
    Verificare i permessi della cartella"""
                            response = messageError(msg=msg)
                            if response == GTK_RESPONSE_CANCEL or \
                                            response == GTK_RESPONSE_DELETE_EVENT:
                                response = fileDialog.run()
                                if response == GTK_RESPONSE_CANCEL or \
                                            response == GTK_RESPONSE_DELETE_EVENT:
                                    #exit but don't save the file
                                    esci  = True
                                    break
                                elif response == GTK_RESPONSE_OK:
                                    filename = fileDialog.get_filename()
                                    break


        fileDialog.destroy()

    def setFocus(self, widget=None):
        self.filter.setFocus()

    def on_anagrafica_window_close(self, widget, event=None):
        if self.anagrafica_complessa_window in Environment.windowGroup:
            Environment.windowGroup.remove(self.anagrafica_complessa_window)
        self.destroy()

    def getHtmlWidget(self):
        return self.html

    def hideNavigator(self):
        self.bodyWidget.filter_navigation_hbox.set_no_show_all(True)
        self.bodyWidget.filter_navigation_hbox.hide()
