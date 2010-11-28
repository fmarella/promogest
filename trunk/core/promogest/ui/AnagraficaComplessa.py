# -*- coding: utf-8 -*-

#    Copyright (C) 2005, 2006, 2007 2008, 2009, 2010 by Promotux
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
import gtk
import gobject
import os
import sys
import threading
import os.path
from promogest.Environment import conf
from GladeWidget import GladeWidget
from promogest.ui.widgets.FilterWidget import FilterWidget
from promogest.lib.XmlGenerator import XlsXmlGenerator
from promogest.lib.CsvGenerator import CsvFileGenerator
from utils import *
import Login
import subprocess ,shlex
from promogest import Environment
from calendar import Calendar
#if Environment.new_print_enjine:
from promogest.lib.sla2pdf.Sla2Pdf_ng import Sla2Pdf_ng
from promogest.lib.sla2pdf.SlaTpl2Sla import SlaTpl2Sla as SlaTpl2Sla_ng
from promogest.lib.SlaTpl2Sla import SlaTpl2Sla
#else:


from promogest.ui.SendEmail import SendEmail
from promogest.lib.HtmlHandler import createHtmlObj, renderTemplate, renderHTML
from promogest.dao.Azienda import Azienda


class Anagrafica(GladeWidget):
    """ Classe base per le anagrafiche di Promogest """

    def __init__(self, windowTitle, recordMenuLabel,
                 filterElement, htmlHandler, reportHandler, editElement, labelHandler = None, gladeFile=None, aziendaStr=None):
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
        # Initial (in)sensitive widgets
        textStatusBar = "     *****   PromoGest - 800 034561 - www.promotux.it - info@promotux.it  *****     "
        context_id =  self.pg2_statusbar.get_context_id("anagrafica_complessa_windows")
        self.pg2_statusbar.push(context_id,textStatusBar)
        self.record_delete_button.set_sensitive(False)
        self.record_delete_menu.set_sensitive(False)
        self.record_edit_button.set_sensitive(False)
        self.record_edit_menu.set_sensitive(False)
        self.record_duplicate_menu.set_property('visible', False)
        self.record_duplicate_menu.set_no_show_all(True)
        self.record_duplicate_menu.set_sensitive(False)
        self.selected_record_print_button.set_sensitive(False)
        self.selected_record_print_menu.set_sensitive(False)
        self.placeWindow(self.anagrafica_complessa_window)
        self.filter.draw()
        self.editElement.draw(cplx=True)
        self.email = ""
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
                            accelGroup, gtk.keysyms.Escape, 0, gtk.ACCEL_VISIBLE)
        self.bodyWidget.filter_search_button.add_accelerator('clicked',
                            accelGroup, gtk.keysyms.F3, 0, gtk.ACCEL_VISIBLE)
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

    def on_records_file_export_clicked(self, widget):
        dao = self.editElement.setDao(None)
        print "DAOO", dao
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
                                                gtk.RESPONSE_CANCEL,
                                                gtk.STOCK_SAVE,
                                            gtk.RESPONSE_OK))
        saveDialog.set_default_response(gtk.RESPONSE_OK)

        self.__homeFolder = ''
        if hasattr(Environment.conf,'Documenti'):
            self.__homeFolder = getattr(Environment.conf.Documenti,
                                                    'cartella_predefinita','')
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
        if response == gtk.RESPONSE_OK:
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
        elif response == gtk.RESPONSE_CANCEL:
            saveDialog.destroy()

    def on_credits_menu_activate(self, widget):
        creditsDialog = GladeWidget('credits_dialog', callbacks_proxy=self)
        creditsDialog.getTopLevel().set_transient_for(self.getTopLevel())
        creditsDialog.getTopLevel().show_all()
        response = creditsDialog.credits_dialog.run()
        if response == gtk.RESPONSE_OK:
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
        if response == gtk.RESPONSE_OK:
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
        dialog = gtk.MessageDialog(self.getTopLevel(),
                                   gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
                                   gtk.MESSAGE_INFO,
                                   gtk.BUTTONS_OK,
                                   msg)
        dialog.run()
        dialog.destroy()

    def on_anagrafica_filter_treeview_cursor_changed(self, treeview=None):
        sel = self.anagrafica_filter_treeview.get_selection()
        if sel.get_mode() == gtk.SELECTION_MULTIPLE:
            return
        elif sel.get_mode() == gtk.SELECTION_SINGLE:
            (model, iterator) = sel.get_selected()
            if iterator is not None:
                self.dao = model.get_value(iterator, 0)
            else:
                self.dao = None
        if self.dao is not None:
            self.htmlHandler.setDao(self.dao)

        self.record_edit_button.set_sensitive(self.dao is not None)
        self.record_edit_menu.set_sensitive(self.dao is not None)

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
        if sel.get_mode() == gtk.SELECTION_MULTIPLE:
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

        self.record_duplicate_menu.set_sensitive(self.dao is not None)

        self.record_delete_button.set_sensitive(self.dao is not None)
        self.record_delete_menu.set_sensitive(self.dao is not None)

        self.selected_record_print_button.set_sensitive(self.dao is not None)
        self.selected_record_print_menu.set_sensitive(self.dao is not None)
        return self.daoSelection or self.dao or False

    def on_record_new_activate(self, widget=None):
        self.editElement.setVisible(True)
        self.editElement.setDao(None)
        self.setFocus()

    def on_record_delete_activate(self, widget):
        dialog = gtk.MessageDialog(self.getTopLevel(),
                                   gtk.DIALOG_MODAL
                                   | gtk.DIALOG_DESTROY_WITH_PARENT,
                                   gtk.MESSAGE_QUESTION, gtk.BUTTONS_YES_NO,
                                   'Confermi l\'eliminazione ?')

        response = dialog.run()
        dialog.destroy()
        if response !=  gtk.RESPONSE_YES:
            return

        dao = self.filter.getSelectedDao()
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
        self._folder = ''
        self._pdfName = str(pdfGenerator.defaultFileName)
        if hasattr(Environment.conf,'Documenti'):
            self._folder = getattr(Environment.conf.Documenti,'cartella_predefinita','')
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

            printDialog.records_print_dialog_description_label.\
                                        set_markup('<span weight="bold">' +\
                                        self._pdfName + '</span>')
            printDialog.records_print_dialog_size_label.\
                                        set_markup('<span weight="bold">' +\
                                        str(len(self.__pdfReport) / 1024) +\
                                        ' Kb</span>')
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
                    print "TEMPLATE FILE", self._template_file
                    self._pdfName = str(pdfGenerator.defaultFileName)

                    if pdfGenerator.defaultFileName == 'documento':
                        dao = self.filter.getSelectedDao()
                        data = dao.data_documento
                        operationName = dao.operazione
                        self._pdfName = operationName + \
                                        '_' +\
                                        str(dao.numero) +\
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
        previewDialog = self.reportHandler.buildPreviewWidget()
#        previewDialog.getTopLevel().show_all()

    def on_records_print_progress_dialog_response(self, dialog, responseId):
        if responseId == gtk.RESPONSE_CANCEL:
            self.__cancelOperation = True

            #self.__pdfGenerator.cancelOperation()

            if self.__pulseSourceTag is not None:
                gobject.source_remove(self.__pulseSourceTag)

            self.on_records_print_dialog_close(dialog)
#            del self.__pdfReport
#            del self.__pdfGenerator


    def on_records_print_progress_dialog_close(self, dialog, event=None):
        # FIXME: we're leaving the threads running!
        print 'diediedie'
        dialog.destroy()

    def on_riferimento2_combobox_entry_changed(self, combobox):
        stringContatti = 'Contatti...'
        def refresh_combobox(anagWindow, tipo):
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
            if res.has_key("ragioneSociale") and res["ragioneSociale"] != '':
                self.printDialog.riferimento2_combobox_entry.\
                                            child.set_text(res["ragioneSociale"])
            else:
                self.printDialog.riferimento2_combobox_entry.\
                                            child.set_text(res["email"])
            self.email = res["email"]
            anagWindow.destroy()
        if self.printDialog.riferimento2_combobox_entry.get_active_text() == stringContatti:
            from promogest.modules.Contatti.ui.RicercaContatti import RicercaContatti
            anag = RicercaContatti()
            anagWindow = anag.getTopLevel()
            anagWindow.connect("hide", refresh_combobox, 'contatto')
            returnWindow = combobox.get_toplevel()
            anagWindow.set_transient_for(returnWindow)
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
            overDialog = gtk.MessageDialog(None, gtk.DIALOG_MODAL
                                            | gtk.DIALOG_DESTROY_WITH_PARENT,
                                                gtk.MESSAGE_ERROR,
                                                gtk.BUTTONS_CANCEL, msg)
            response = overDialog.run()
            overDialog.destroy()
            return

    def on_send_email_button_clicked(self, widget):
        """ ATTENZIONE: l'errore parrebbe corretto nel launchpad ma ancora non funziona
        con thunderbird controllando in simplescan dà lo stesso errore che riscontro io
        aspettiamo...."""
        self.email = self.printDialog.riferimento2_combobox_entry.\
                                                                get_active_text()
        pdfFile = os.path.join(self._folder + self._pdfName +'.pdf')
        self.tryToSavePdf(pdfFile)

        fileName = self._pdfName +'.pdf'
        subject= "Invio: %s" %fileName
        body = conf.body %fileName
        if self.email:
            arghi = "xdg-email --attach '%s' --subject '%s' --body '%s' '%s'" %(str(pdfFile),subject,body,self.email)
        else:
            arghi = "xdg-email --attach '%s' --subject '%s' --body '%s'" %(str(pdfFile),subject,body)
        args = shlex.split(arghi)
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
                                                    gtk.RESPONSE_CANCEL,
                                                    gtk.STOCK_SAVE,
                                                    gtk.RESPONSE_OK),
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
        if ( (response == gtk.RESPONSE_CANCEL) or ( response == gtk.RESPONSE_DELETE_EVENT)) :
            pass
        elif response == gtk.RESPONSE_OK:
            filename = fileDialog.get_filename()

            #modifiche
            can_save = 0
            esci = False
            # Let's check whether the file is going to be overwritten

            while esci == False:

                if os.path.exists(filename):
                    msg = 'Il file "%s" esiste.  Sovrascrivere?' % filename
                    overDialog = gtk.MessageDialog(None, gtk.DIALOG_MODAL
                                                | gtk.DIALOG_DESTROY_WITH_PARENT,
                                                gtk.MESSAGE_QUESTION,
                                                gtk.BUTTONS_YES_NO, msg)
                    response = overDialog.run()
                    overDialog.destroy()
                    if response == gtk.RESPONSE_YES:
                        can_save = 1
                        #overwrite the file if user click  yes
                        break
                    else:
                        response =  fileDialog.run()
                        if response == gtk.RESPONSE_CANCEL or response == gtk.RESPONSE_DELETE_EVENT:
                            #exit but don't save the file
                            esci = True
                            can_save = 0
                            break
                        elif response == gtk.RESPONSE_OK:
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
                            overDialog = gtk.MessageDialog(None, gtk.DIALOG_MODAL
                                                | gtk.DIALOG_DESTROY_WITH_PARENT,
                                                gtk.MESSAGE_ERROR,
                                                gtk.BUTTONS_CANCEL, msg)
                            response = overDialog.run()
                            #overDialog.destroy()
                            if response == gtk.RESPONSE_CANCEL or \
                                            response == gtk.RESPONSE_DELETE_EVENT:
                                overDialog.destroy()
                                response = fileDialog.run()
                                if response == gtk.RESPONSE_CANCEL or \
                                            response == gtk.RESPONSE_DELETE_EVENT:
                                    #exit but don't save the file
                                    esci  = True
                                    break
                                elif response == gtk.RESPONSE_OK:
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

class AnagraficaFilter(GladeWidget):
    """ Filtro per la ricerca nell'anagrafica articoli """

    def __init__(self, anagrafica, rootWidget, gladeFile=None, module=False):
        GladeWidget.__init__(self, rootWidget, fileName=gladeFile, isModule=module)

        self._anagrafica = anagrafica
        self._widgetFirstFocus = None
        self._isSensitive = True
        self._treeViewModel = None

        # A closure that returns a list of Dao's that match the
        # current filter parameters.  It is invoked through
        # self.runFilter() (unless the derived classes redefine it)
        #
        # This closure takes two parameters: offset and batchSize
        def __defaultFilterClosure(offset, batchSize):
            raise NotImplementedError
        self._filterClosure = __defaultFilterClosure

        # Same concept as above, but this closure counts filter results
        def __defaultFilterCountClosure():
            raise NotImplementedError
        self._filterCountClosure = __defaultFilterCountClosure

    def build(self):
        """ reindirizza alcuni campi e metodi dal filterWidget """
        self.bodyWidget = self._anagrafica.bodyWidget
        # mapping fields and methods from bodyWidget to this class
        self._changeOrderBy = self.bodyWidget._changeOrderBy
        self.orderBy = self.bodyWidget.orderBy = None
        self.join =self.bodyWidget.join =None
        self.batchSize =  setconf("Numbers", "batch_size")
        model = self._anagrafica.batchsize_combo.get_model()
        for r in model:
            if r[0] == int(self.batchSize):
                self._anagrafica.batchsize_combo.set_active_iter(r.iter)

        self.offset = self.bodyWidget.offset = 0
        self.numRecords = self.bodyWidget.numRecords = 0

    def draw(self):
        """
        Disegna i contenuti del filtro anagrafica.  Metodo invocato
        una sola volta, dopo la costruzione dell'oggetto
        """
        raise NotImplementedError

    def clear(self):
        """ Ripulisci il filtro di ricerca e aggiorna la ricerca stessa """
        raise NotImplementedError

    def refresh(self):
        """ Aggiorna il filtro di ricerca in base ai parametri impostati """
        raise NotImplementedError

    def on_filter_treeview_row_activated(self, treeview, path, column):
        """ Gestisce la conferma della riga """
        self._anagrafica.on_anagrafica_filter_treeview_row_activated(treeview, path, column)


    def on_filter_treeview_cursor_changed(self, treeview):
        """ Gestisce lo spostamento tra le righe """
        self._anagrafica.on_anagrafica_filter_treeview_cursor_changed(treeview)

    def on_filter_treeview_selection_changed(self, treeSelection):
        """
        Gestisce le selezioni multiple (se attive)
        """
        self._anagrafica.on_anagrafica_filter_treeview_selection_changed(treeSelection)

    def runFilter(self, offset='__default__', batchSize='__default__',
                                      progressCB=None, progressBatchSize=0):
        """ Recupera i dati """
        self.bodyWidget.orderBy = self.orderBy
        if batchSize == '__default__' and  self._anagrafica.batchsize_combo.get_active_iter():
            iterator = self._anagrafica.batchsize_combo.get_active_iter()
            model = self._anagrafica.batchsize_combo.get_model()
            if iterator is not None:
                batchSize = model.get_value(iterator, 0)
        return self.bodyWidget.runFilter(offset=offset, batchSize=batchSize,
                                         progressCB=progressCB, progressBatchSize=progressBatchSize,
                                         filterClosure=self._filterClosure)

    def countFilterResults(self):
        """ Conta i dati """
        totale_daos = self.bodyWidget.countFilterResults(self._filterCountClosure)
        self._anagrafica.tot_daos_label.set_markup(" <b>"+str(totale_daos or "Nessuno")+"</b>")
        return totale_daos

    def _refreshPageCount(self):
        """ Aggiorna la paginazione """
        self.bodyWidget.numRecords = self.numRecords
        self.bodyWidget._refreshPageCount()

    def selectCurrentDao(self):
        """ Select the dao currently shown in the HTML detail (if possible) """
        def foreach_handler(model, path, iter, selection):
            # Get value from current row, column 1
            dao = model.get_value(iter, 0)
            if dao.sameRecord(self._anagrafica._selectedDao):
                selection.select_path(path)
                self._anagrafica.on_anagrafica_filter_treeview_cursor_changed(self._anagrafica.anagrafica_filter_treeview)
                return True
            else:
                return False

        treeView = self._anagrafica.anagrafica_filter_treeview
        selection = treeView.get_selection()
        selection.unselect_all()
        model = treeView.get_model()

        model.foreach(foreach_handler, selection)

    def getSelectedDao(self):
        treeViewSelection = self._anagrafica.anagrafica_filter_treeview.get_selection()
        if treeViewSelection.get_mode() != gtk.SELECTION_MULTIPLE:
            (model, iterator) = treeViewSelection.get_selected()
            if iterator is not None:
                dao = model.get_value(iterator, 0)
            else:
                dao = None
        else:
            model, iterator = treeViewSelection.get_selected_rows()
            count = treeViewSelection.count_selected_rows()
            if count == 1:
                dao = model[iterator[0]][0]
                daoSelection = None
            else:
                dao = None
        return dao

    def getTreeViewModel(self):
        return self._treeViewModel

    def on_campo_filter_entry_key_press_event(self, widget, event):
        return self._anagrafica.bodyWidget.on_filter_element_key_press_event(widget, event)

    def setFocus(self, widget=None):
        self._anagrafica.bodyWidget.setFocus(widget)


class AnagraficaHtml(object):
    """ Interfaccia HTML read-only per la lettura dell'anagrafica """

    def __init__(self, anagrafica, template, description):
        self._anagrafica = anagrafica
        self._gtkHtml = None # Will be filled later
        self.description = description
        self.defaultFileName = template
        self.dao = None
        self._slaTemplateObj = None

    def setDao(self, dao):
        """ Visualizza il Dao specificato """
        self.dao = dao

        self._refresh()
        if dao and Environment.debugDao:
            #FIXME: add some logging level check here
            import pprint
            pp = pprint.PrettyPrinter(indent=4)
            print ("\n\n=== DAO object dump ===\n\n"
                    + pp.pformat(dao.dictionary(complete=True))
                    + "\n\n")

    def refresh(self):
        """ Aggiorna la vista HTML """
        self._refresh()

    def _refresh(self):
        """ show the html page in the custom widget"""
        pageData = {}
        eventipreves = []
        eventiprevesAT = []
        calendarioDatetime = []
        html = "<html><body></body></html>"
        if not self._gtkHtml:
            self._gtkHtml = self._anagrafica.getHtmlWidget()
        if self.dao:
            if posso("GN"):
                from promogest.dao.TestataDocumento import TestataDocumento
                from promogest.modules.GestioneNoleggio.dao.TestataGestioneNoleggio import TestataGestioneNoleggio
                preves = TestataDocumento().select(daData= stringToDate("1/1/"+Environment.workingYear),
                                aData=stringToDate("31/12/"+Environment.workingYear), batchSize=None,
                                idArticolo=self.dao.id)
                for p in preves:
                    eventipreves.append((p.data_documento.toordinal(),{"id":p.id,
                                                        "operazione":p.operazione,
                                                        "short":p.ragione_sociale_cliente,
                                                        "tipo":"data_documento",
                                                        "colore":"#6495ED"},p.data_documento.day))
                    arcTemp = TestataGestioneNoleggio().select(idTestataDocumento=p.id, batchSize=None)
                    for a in arcTemp:
                        startDate =a.data_inizio_noleggio
                        stopDate =a.data_fine_noleggio
                        dateList= date_range(startDate,stopDate)
                        for d in dateList:
                            eventiprevesAT.append((d.toordinal(),{"id":p.id,
                                            "operazione":p.operazione,
                                            "short":p.ragione_sociale_cliente,
                                            "tipo":"data_documento",
                                            "colore":"#AFEEEE"},d.day))
                calendarioDatetime = Calendar().yeardatescalendar(int(Environment.workingYear))
            pageData = {
                    "file" :self.defaultFileName+".html",
                    "dao":self.dao,
                    "objects":self.dao,
                    "eventipreves": eventipreves,
                    "eventiprevesAT": eventiprevesAT,
                    "calendarioDatetime": calendarioDatetime,
                    }
            html = renderTemplate(pageData)
        self.hh = html
        renderHTML(self._gtkHtml,html)

    def setObjects(self, objects):
        # FIXME: dummy function for API compatibility, refactoring(TM) needed!
        pass

    def pdf(self, operationName, classic=None, template_file=None):
        """ Qui si stampa selezione """
        self._slaTemplate = None
        self._slaTemplateObj=None
        # aggiungo i dati azienda al dao in modo che si gestiscano a monte
        azienda = Azienda().getRecord(id=Environment.azienda)
        operationNameUnderscored = operationName.replace(' ' , '_').lower()
        print "PER LA STAMPA", operationNameUnderscored, Environment.templatesDir + operationNameUnderscored + '.sla'
        if os.path.exists(Environment.templatesDir + operationNameUnderscored + '.sla'):
            self._slaTemplate = Environment.templatesDir + operationNameUnderscored + '.sla'
        elif "DDT" in operationName and os.path.exists(Environment.templatesDir + 'ddt.sla'):
            self._slaTemplate = Environment.templatesDir + 'ddt.sla'
        else:
            Environment.pg2log.info("UTILIZZO il documento.sla normale per la stampa")
            self._slaTemplate = Environment.templatesDir + self.defaultFileName + '.sla'
        """ Restituisce una stringa contenente il report in formato PDF """

        print "DAO", self.dao.__class__.__name__

        if self.dao.__class__.__name__ in Environment.fromHtmlLits:
#            try:
            import ho.pisa as pisa
#            except:
#                print "ERRORE NELL'IMPORT DI PISA"
#            return
            f = self.hh
            g = file(Environment.tempDir+".temp.pdf", "wb")
            pdf = pisa.CreatePDF(str(f),g)
            g .close()
            g=file(Environment.tempDir+".temp.pdf", "r")
            f= g.read()
            g.close()
            return f
        param = [self.dao.dictionary(complete=True)]
        multilinedirtywork(param)
        if hasattr(Environment.conf.Documenti,"jnet"):
            from promogest.modules.NumerazioneComplessa.jnet import numerazioneJnet
            param[0]["numero"]= numerazioneJnet(self.dao)
        if azienda:
            azidict = azienda.dictionary(complete=True)
            for a,b in azidict.items():
                k = "azi_"+a
                azidict[k] = b
                del azidict[a]
            param[0].update(azidict)
        if "operazione" in param[0]:
            if (param[0]["operazione"] =="DDT vendita" or\
                     param[0]["operazione"] =="DDT acquisto") and \
                                     param[0]["causale_trasporto"] != "":
                param[0]["operazione"] = "DDT"
        # controllo la versione dello sla che devo elaborare
        versione = scribusVersion(self._slaTemplate)

        if Environment.new_print_enjine:
            stpl2sla = SlaTpl2Sla_ng(slafile=None,label=None, report=None,
                                    objects=param,
                                    daos=self.dao,
                                    slaFileName=self._slaTemplate,
                                    pdfFolder=self._anagrafica._folder,
                                    classic=True,
                                    template_file=None).fileElaborated()
            return Sla2Pdf_ng(slafile=stpl2sla).translate()
        else:
            if self._slaTemplateObj is None:
                self._slaTemplateObj = SlaTpl2Sla(slaFileName=self._slaTemplate,
                                            pdfFolder=self._anagrafica._folder,
                                            report=self._anagrafica._reportType,
                                            classic = True,
                                            template_file=template_file)
            return self._slaTemplateObj.serialize(param, classic = True,dao=self.dao)

    def cancelOperation(self):
        """ Cancel current operation """
        self._slaTemplateObj.cancelOperation()


class AnagraficaReport(object):
    """ Interfaccia HTML read-only per la lettura dell'anagrafica
    """
    def __init__(self, anagrafica, description, defaultFileName,
                 htmlTemplate, sxwTemplate,
                templatesDir =None):
        self._anagrafica = anagrafica
        self.description = description
        self.defaultFileName = defaultFileName
        self._htmlTemplate = [os.path.join('report-templates'),htmlTemplate + '.html']
        if templatesDir:
            self._slaTemplate = templatesDir + sxwTemplate + '.sla'
        else:
            self._slaTemplate = Environment.reportTemplatesDir + sxwTemplate + '.sla'
        #self.htmlName = htmlTemplate + '.html'
        self.objects = None
        self._slaTemplateObj = None


    def setObjects(self, objects):
        """ Imposta gli oggetti che verranno inclusi nel report """
        self.objects = objects

    def pdf(self,operationName, classic=None, template_file=None):
        """ Restituisce una stringa contenente il report in formato PDF
        """
        azienda = Azienda().getRecord(id=Environment.azienda)
        versione = scribusVersion(self._slaTemplate)
        print "OHOHOHHHO", Environment.new_print_enjine
        if not Environment.new_print_enjine:
            if self._slaTemplateObj is None:
                self._slaTemplateObj = SlaTpl2Sla(slaFileName=self._slaTemplate,
                                            pdfFolder=self._anagrafica._folder,
                                            report=self._anagrafica._reportType,
                                            classic = classic,
                                            template_file=template_file)

        param = []
        for d in self.objects:
            d.resolveProperties()
            param.append(d.dictionary(complete=True))
        multilinedirtywork(param)
        if azienda and param:
            azidict = azienda.dictionary(complete=True)
            for a,b in azidict.items():
                k = "azi_"+a
                azidict[k] = b
                del azidict[a]
            param[0].update(azidict)
        if not Environment.new_print_enjine:
            return self._slaTemplateObj.serialize(param, self.objects)
        else:
            return Sla2Pdf(slaFileName=self._slaTemplate,
                        pdfFolder=self._anagrafica._folder,
                        report=self._anagrafica._reportType).createPDF(objects=param, daos=self.objects)


    def cancelOperation(self):
        """ Cancel current operation
        """
        if self._slaTemplateObj is not None:
            self._slaTemplateObj.cancelOperation()


    def buildPreviewWidget(self):
        """Build and return GladeWidget-derived component for print
        preview
        """
        return AnagraficaPrintPreview(anagrafica=self._anagrafica,
                                      windowTitle=self.description,
                                      previewTemplate=self._htmlTemplate)

class AnagraficaLabel(object):

    def __init__(self, anagrafica, description, defaultFileName,
                                                    htmlTemplate,sxwTemplate):
        """ Create labels """
        self._anagrafica = anagrafica
        self.description = description
        self.defaultFileName = defaultFileName
        self._htmlTemplate = os.path.join('label-templates', htmlTemplate + '.html')
        self._slaTemplate = Environment.labelTemplatesDir + sxwTemplate + '.sla'
        self.objects = None
        self._slaTemplateObj = None

    def setObjects(self, objects):
        """ Imposta gli oggetti che verranno inclusi nel report """
        self.objects = objects

    def pdf(self,operationName, classic=None, template_file=None):
        """ Restituisce una stringa contenente il report in formato PDF
        """
        azienda = Azienda().getRecord(id=Environment.azienda)
        param = []
        for d in self.objects:
            d.resolveProperties()
            param.append(d.dictionary(complete=True))
#        multilinedirtywork(param)
        if azienda:
            azidict = azienda.dictionary(complete=True)
            for a,b in azidict.items():
                k = "azi_"+a
                azidict[k] = b
                del azidict[a]
            if param:
                param[0].update(azidict)
        if template_file:
            versione = scribusVersion(Environment.labelTemplatesDir +template_file)
        else:
            versione = scribusVersion(self._slaTemplate)
        if not Environment.new_print_enjine:
            print "OLD PRINT ENGINE"
            self._slaTemplateObj = SlaTpl2Sla(slaFileName=self._slaTemplate,
                                        pdfFolder=self._anagrafica._folder,
                                        report=self._anagrafica._reportType,
                                        label=True).serialize(
                                                    param,
                                                    self.objects,
                                                    classic = classic,
                                                    template_file=template_file)
            return self._slaTemplateObj
        else:
            print "NEW PRINT ENGINE"
            if template_file:
                slafile = Environment.labelTemplatesDir +template_file
            else:
                slafile = self._slaTemplate
            stpl2sla = SlaTpl2Sla_ng(slafile=None,label=True,
                                    report=self._anagrafica._reportType,
                                    objects=param, daos=self.objects,
                                    slaFileName=slafile,
                                    pdfFolder=self._anagrafica._folder,
                                    classic=classic,
                                    template_file=template_file)
            return Sla2Pdf_ng(slafile=self._anagrafica._folder+"_temppp.sla").translate()




#            return Sla2Pdf(slaFileName=self._slaTemplate,
#                            pdfFolder=self._anagrafica._folder,
#                            report=self._anagrafica._reportType,
#                            label=True).createPDF(objects=param, daos=self.objects,
#                                                classic = classic,
#                                                template_file=template_file)
class AnagraficaEdit(GladeWidget):
    """ Interfaccia di editing dell'anagrafica """

    def __init__(self, anagrafica, rootWidget, windowTitle,gladeFile=None,module=False):
        GladeWidget.__init__(self, rootWidget, fileName=gladeFile, isModule=module)

        self._anagrafica = anagrafica
        self._widgetFirstFocus = None
        self._isSensitive = True
        self._windowTitle = windowTitle
        self.dao = None


    def setVisible(self, isVisible):
        """ Make the window visible/invisible """
        self._isSensitive = isVisible

        if isVisible:
            self.dialog = GladeWidget('anagrafica_complessa_detail_dialog',
                                      callbacks_proxy=self)
            self.dialogTopLevel = self.dialog.getTopLevel()
            self.dialogTopLevel.set_title(self._windowTitle)
            self.dialogTopLevel.vbox.pack_start(self.getTopLevel())
            accelGroup = gtk.AccelGroup()
            self.dialogTopLevel.add_accel_group(accelGroup)
            self.dialog.ok_button.add_accelerator('grab_focus', accelGroup, gtk.keysyms.F5, 0, gtk.ACCEL_VISIBLE)
            self.dialog.ok_button.connect('grab_focus',self.on_ok_button_grab_focus)
            Environment.windowGroup.append(self.dialogTopLevel)
            self.dialogTopLevel.set_transient_for(self._anagrafica.getTopLevel())
            self.placeWindow(self.dialogTopLevel)
            self.dialogTopLevel.show_all()
            self.setFocus()
        else:
            Environment.windowGroup.remove(self.dialogTopLevel)
            self.dialogTopLevel.vbox.remove(self.getTopLevel())
            self.on_top_level_closed()
            self.dialogTopLevel.destroy()


    def draw(self):
        """
        Disegna i contenuti del dettaglio anagrafica.  Metodo invocato
        una sola volta, dopo la costruzione dell'oggetto
        """
        raise NotImplementedError


    def clear(self):
        """ Svuota tutti i campi di input del dettaglio anagrafica """
        raise NotImplementedError

    def setDao(self, dao):
        """ Visualizza il Dao specificato """
        raise NotImplementedError

    def saveDao(self):
        """ Salva il Dao attualmente selezionato """
        raise NotImplementedError

    def setFocus(self, widget=None):
        if widget is None:
            self._widgetFirstFocus.grab_focus()
        else:
            widget.grab_focus()

    def on_ok_button_grab_focus(self, button):
        if self.dialog.ok_button.is_focus():
            self.on_anagrafica_complessa_detail_dialog_response(self.dialog, gtk.RESPONSE_OK)

    def on_anagrafica_complessa_detail_dialog_response(self, dialog, responseId):
        """ Main function connected with ok applica and cancel in Anagrafica Edit"""
        if responseId == gtk.RESPONSE_CANCEL:
            #self.clearDao()
            self.setVisible(False)
        elif responseId == gtk.RESPONSE_OK:
            self.saveDao()
            self._anagrafica.filter.refresh()
            self._anagrafica.filter.selectCurrentDao()
            self._anagrafica.filter.getSelectedDao()
            self.setVisible(False)
        elif responseId == gtk.RESPONSE_APPLY:
            self.saveDao()
            self._anagrafica.filter.refresh()
            self._anagrafica.filter.selectCurrentDao()


    def on_anagrafica_complessa_detail_dialog_close(self, dialog, event=None):
        dialog = gtk.MessageDialog(self.dialogTopLevel,
                                   gtk.DIALOG_MODAL
                                   | gtk.DIALOG_DESTROY_WITH_PARENT,
                                   gtk.MESSAGE_QUESTION, gtk.BUTTONS_YES_NO,
                                   'Confermi la chiusura ?')
        response = dialog.run()
        dialog.destroy()
        if response ==  gtk.RESPONSE_YES:
            self.setVisible(False)
        else:
            return True



class AnagraficaPrintPreview(GladeWidget):
    """ Print preview """
    # FIXME: a lot of duplicated code from AnagraficaFilter here!

    def __init__(self, anagrafica, windowTitle, previewTemplate):
        GladeWidget.__init__(self, 'htmlviewer')
        self.windowTitle = windowTitle
        self.visualizzatore_html.set_title(windowTitle)
        self._anagrafica = anagrafica

        self.bodyWidget = FilterWidget(owner=self, resultsElement='html')
        self.html_scrolledwindow.add(self.bodyWidget.getTopLevel())
#        self.bodyWidget.filter_body_label.set_no_show_all(True)
#        self.bodyWidget.filter_body_label.set_property('visible', False)

        self.print_on_screen_html = self.bodyWidget.resultsElement
        self._gtkHtmlDocuments = None # Will be filled later
        self._previewTemplate = previewTemplate
        self.html = createHtmlObj(self)
        self._changeOrderBy = self.bodyWidget._changeOrderBy
        self.orderBy = self.bodyWidget.orderBy
        self.batchSize = self.bodyWidget.batchSize
        self.offset = self.bodyWidget.offset
        self.numRecords = self.bodyWidget.numRecords
        self._filterClosure = self._anagrafica.filter._filterClosure
        self._filterCountClosure = self._anagrafica.filter._filterCountClosure
        #self._allResultForHtml = self._anagrafica.filter._allResultForHtml
#        self.visualizzatore_html.set_transient_for(self._anagrafica.getTopLevel())
        self.placeWindow(self.visualizzatore_html)


        self.codBar_combo = gtk.combo_box_new_text()
        self.codBar_combo.append_text("Genera Pdf Anteprima Html")
        self.codBar_combo.append_text("Genera CSV da Anteprima Html")
        self.bodyWidget.hbox1.pack_start(self.codBar_combo)
        self.codBar_combo.connect('changed', self.on_generic_combobox_changed )

        self.bodyWidget.generic_button.set_no_show_all(True)
        self.bodyWidget.generic_button.set_property('visible', False)
        #generaButton = self.bodyWidget.generic_button
        #generaButton.connect('clicked', self.on_generic_button_clicked )
        #generaButton.set_label("Genera Pdf Anteprima Html")
        self.refresh()

    def on_pdf_button_clicked(self, button):
        from PrintDialog import PrintDialogHandler
        try:
            import ho.pisa as pisa
        except:
            print "ERRORE NELL'IMPORT DI PISA"
#                import pisaLib.ho.pisa as pisa
            return
        f = self.html_code
        g = file(Environment.tempDir+".temp.pdf", "wb")
        pdf = pisa.CreatePDF(str(f),g)
        g .close()
        anag = PrintDialogHandler(self,self.windowTitle)
        anagWindow = anag.getTopLevel()
        returnWindow = self.bodyWidget.getTopLevel().get_toplevel()
        anagWindow.set_transient_for(returnWindow)
        anagWindow.show_all()

    def on_csv_button_clicked(self, button):
        messageInfo(msg="NON ANCORA IMPLEMENTATO")


    def on_generic_combobox_changed(self,combobox):
        if self.codBar_combo.get_active()==0:
            from PrintDialog import PrintDialogHandler
            try:
                import ho.pisa as pisa
            except:
                print "ERRORE NELL'IMPORT DI PISA"
#                import pisaLib.ho.pisa as pisa
                return
            f = self.html_code
            g = file(Environment.tempDir+".temp.pdf", "wb")
            pdf = pisa.CreatePDF(str(f),g)
            g .close()
            anag = PrintDialogHandler(self,self.windowTitle)
            anagWindow = anag.getTopLevel()
            returnWindow = self.bodyWidget.getTopLevel().get_toplevel()
            anagWindow.set_transient_for(returnWindow)
            anagWindow.show_all()
            #self.codBar_combo.set_active(0)
        elif self.codBar_combo.get_active()==1:
            print "ANTEPRIMA CSV"
        else:
            self.codBar_combo.set_active(-1)

    def _refreshPageCount(self):
        """ Aggiorna la paginazione """
        self.bodyWidget.numRecords = self.numRecords
        self.bodyWidget._refreshPageCount()

    def refresh(self):
        """ show the html page in the custom widget"""
        self.bodyWidget.orderBy = self.orderBy
        daos = self.bodyWidget.runFilter(offset=None, batchSize=None,
                                         filterClosure=self._filterClosure)
        self.numRecords = self.bodyWidget.countFilterResults(self._filterCountClosure)
        self._refreshPageCount()
        pageData = {}
        self.html_code = "<html><body></body></html>"
        if daos:
            pageData = {
                    "file" :self._previewTemplate[1],
                    "dao":daos,
                    "objects":daos
                    }
            self.html_code = renderTemplate(pageData)
        renderHTML(self.print_on_screen_html,self.html_code)

    def on_print_on_screen_dialog_response(self, dialog, responseId):
        if responseId == gtk.RESPONSE_CLOSE:
            self.on_print_on_screen_dialog_delete_event()

    def on_print_on_screen_dialog_delete_event(self, dialog=None, event=None):
        self.destroy()
