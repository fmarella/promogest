# -*- coding: utf-8 -*-

# Promogest
#
# Copyright (C) 2007 by Promotux Informatica - http://www.promotux.it/
# Author: Andrea Argiolas <andrea@promotux.it>
# Author: Francesco Meloni <francesco@promotux.it>

import gtk
from utils import *
import subprocess
import os, sys, threading, os.path
from utilsCombobox import *
from promogest import Environment
from GladeWidget import GladeWidget

class PrintDialogHandler(GladeWidget):

    def __init__(self,anacomplex,nome, pdfGenerator=None, report=None, daos=None, label=None, tempFile=None ):
        GladeWidget.__init__(self, 'records_print_dialog',fileName='records_print_dialog.glade')
        try:
            self._pdfName = nome.replace(" ","_") + '_report_' + time.strftime('%d-%m-%Y')
        except:
            self._pdfName = "generic labels"+ time.strftime('%d-%m-%Y')
#        self._folder = getattr(Environment.conf.Documenti,'cartella_predefinita','')
        if hasattr(Environment.conf,'Documenti'):
            self._folder = getattr(Environment.conf.Documenti,'cartella_predefinita','')
        if self._folder == '':
            if os.name == 'posix':
                self._folder = os.environ['HOME']
            elif os.name == 'nt':
                self._folder = os.environ['USERPROFILE']
        self.__pdfGenerator = pdfGenerator
        if tempFile:
            filetemp= file(tempFile,"r")
        else:
            filetemp=file(".temp.pdf", "r")
        self.__pdfReport= filetemp.read()
        filetemp.close()
        self.records_print_dialog_size_label.set_markup('<span weight="bold">' + str(len(self.__pdfReport) / 1024) + ' Kb</span>')
        self.records_print_dialog_description_label.set_markup('<span weight="bold">' + self._pdfName + '</span>')
        self._reportType = report

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
        self.email = self.riferimento2_combobox_entry.get_active_text()
        pdfFile = os.path.join(self._folder + self._pdfName +'.pdf')

        self.tryToSavePdf(pdfFile)

        fileName = self._pdfName +'.pdf'
        subject= "Invio: %s" %fileName
        body = Environment.conf.body %fileName
        if self.email:
            arghi = "xdg-email --attach '%s' --subject '%s' --body '%s' '%s'" %(str(pdfFile),subject,body,self.email)
        else:
            arghi = "xdg-email --attach '%s' --subject '%s' --body '%s'" %(str(pdfFile),subject,body)
        subprocess.Popen(arghi, shell=True)


    def on_close_button_clicked(self,widget):
        self.on_records_print_dialog_close(self)

    def on_save_button_clicked(self, widget):
        self.__handleSaveResponse(self.getTopLevel())
        #self.on_records_print_dialog_close(self.printDialog)

    def on_open_button_clicked(self, widget):
        self.__handleOpenResponse(self.getTopLevel())
        #self.on_records_print_dialog_close(self.printDialog)


    def on_records_print_dialog_close(self, dialog, event=None):
        del self.__pdfReport
        del self.__pdfGenerator
        self.getTopLevel().destroy()


    def __handleOpenResponse(self, dialog):

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
                            msg = 'Errore nel salvataggio!\n Verificare i permessi della cartella'
                            overDialog = gtk.MessageDialog(None, gtk.DIALOG_MODAL
                                                                | gtk.DIALOG_DESTROY_WITH_PARENT,
                                                                gtk.MESSAGE_ERROR,
                                                                gtk.BUTTONS_CANCEL, msg)
                            response = overDialog.run()
                            #overDialog.destroy()
                            if response == gtk.RESPONSE_CANCEL or response == gtk.RESPONSE_DELETE_EVENT:
                                overDialog.destroy()
                                response = fileDialog.run()
                                if response == gtk.RESPONSE_CANCEL or response == gtk.RESPONSE_DELETE_EVENT:
                                    #exit but don't save the file
                                    esci  = True
                                    break
                                elif response == gtk.RESPONSE_OK:
                                    filename = fileDialog.get_filename()
                                    break


        fileDialog.destroy()
