# -*- coding: iso-8859-15 -*-

# Promogest
#
# Copyright (C) 2005 by Promotux Informatica - http://www.promotux.it/
# Author: Alessandro Scano <alessandro@promotux.it>

import gtk, gobject, os, threading
from promogest import Environment
from promogest.ui.GladeWidget import GladeWidget
from promogest.ui.utilsCombobox import fillComboboxMagazzini


class CasseFrame(GladeWidget):
    """ Frame per la gestione della comunicazione  """

    def __init__(self, mainWindow):
        self.mainWindow = mainWindow
        self.magazzino = None
        GladeWidget.__init__(self, 'casse_frame')
        # Imposto comando di esportazione
        export_program = getattr(Environment.conf.Delfis,'export_program','')
        self.casse_export_text_entry.set_text(export_program)
        # Imposto comando di importazione
        export_program = getattr(Environment.conf.Delfis,'import_program','')
        self.casse_import_text_entry.set_text(export_program)
        # Riempio combobox magazzini
        fillComboboxMagazzini(self.magazzino_casse_combobox)


    def on_export_button_clicked(self, toggleButton):
        if toggleButton.get_property('active') is False:
            return

        if self.casse_export_text_entry.get_text()=='':
            return

        def exitFunc(dialog):
            gobject.source_remove(self.__pulseSourceTag)
            dialog.getTopLevel().destroy()
            if self.__cancelOperation:
                self.export_message_label.set_markup("Esecuzione interrotta")
                self.__cancelOperation = False
            elif self.__exitStatus!=0:
                self.export_message_label.set_markup("<b>Attenzione</b>: L' esecuzione del comando e` fallita miseramente, controllare il log per informazioni")
            else:
                self.export_message_label.set_markup("<b>Esportazione completata con successo</b>")
            return False

        # Instanziare finestra di progresso e schedulare funzione di pulse
        progressDialog = GladeWidget('delfis_export_progress_dialog',
                                     callbacks_proxy=self)
        progressDialog.getTopLevel().set_transient_for(self.mainWindow)
        progressDialog.getTopLevel().show_all()

        pbar = progressDialog.export_progressbar
        self.__pulseSourceTag = None
        self.__cancelOperation = False

        pbar.set_pulse_step(0.07)

        def pulsePBar():
            pbar.pulse()
            return True

        self.__pulseSourceTag = gobject.timeout_add(33, pulsePBar)

        def exportingThread():
            program_params = self.casse_export_text_entry.get_text().split()
            program_path = program_params[0]
            program_params[0] = 'delfis_export'

            self.__exportingProcessPid = os.spawnv(os.P_NOWAIT, program_path, program_params)
            id, self.__exitStatus = os.waitpid(self.__exportingProcessPid, 0)
            self.__exitStatus = self.__exitStatus >> 8
            gobject.idle_add(exitFunc, progressDialog)

        t = threading.Thread(group=None, target=exportingThread,
                                     name='Delfis exporting thread', args=(),
                                     kwargs={})
        t.setDaemon(True) # FIXME: are we sure? ( he does'nt remember )
        t.start()

        toggleButton.set_property('active',False)


    def on_import_button_clicked(self, toggleButton):

        if toggleButton.get_property('active') is False:
            return

        def exitFunc(dialog):
            gobject.source_remove(self.__pulseSourceTag)
            dialog.getTopLevel().destroy()
            if self.__cancelOperation:
                self.exit_message_label.set_markup("Esecuzione interrotta")
                self.__cancelOperation = False
            elif self.__exitStatus!=0:
                self.exit_message_label.set_markup("<b>Attenzione</b>: L' esecuzione del comando e` fallita miseramente, controllare il log per informazioni")
            else:
                self.exit_message_label.set_markup("<b>Importazione completata con successo</b>")
            return False

        if self.magazzino is None:
            dialog = gtk.MessageDialog(self.mainWindow,
                                        gtk.DIALOG_MODAL
                                        | gtk.DIALOG_DESTROY_WITH_PARENT,
                                        gtk.MESSAGE_WARNING, gtk.BUTTONS_OK,
                                        "Occorre selezionare un magazzino")
            response = dialog.run()
            dialog.destroy()
            toggleButton.set_property('active', False)
            return

        if self.casse_import_text_entry.get_text()=='':
            return

        # Instanziare finestra di progresso e schedulare funzione di pulse
        progressDialog = GladeWidget('delfis_import_progress_dialog',
                                     callbacks_proxy=self)
        progressDialog.getTopLevel().set_transient_for(self.mainWindow)
        progressDialog.getTopLevel().show_all()

        pbar = progressDialog.import_progressbar
        self.__pulseSourceTag = None
        self.__cancelOperation = False

        pbar.set_pulse_step(0.07)

        def pulsePBar():
            pbar.pulse()
            return True

        self.__pulseSourceTag = gobject.timeout_add(33, pulsePBar)

        def importingThread():
            program_params = self.casse_import_text_entry.get_text().split()
            program_path = program_params[0]
            program_params[0] = 'delfis_import'
            program_params.append('-m')
            program_params.append(self.magazzino)

            self.__importingProcessPid = os.spawnv(os.P_NOWAIT, program_path, program_params)
            id, self.__exitStatus = os.waitpid(self.__importingProcessPid, 0)
            self.__exitStatus = self.__exitStatus >> 8
            gobject.idle_add(exitFunc, progressDialog)

        t = threading.Thread(group=None, target=importingThread,
                                     name='Delfis importing thread', args=(),
                                     kwargs={})
        #t.setDaemon(True) # FIXME: are we sure? ( he does'nt remember )
        t.start()
        toggleButton.set_property('active',False)


    def on_exporting_file_progress_dialog_response(self, dialog, responseId):
        if responseId == gtk.RESPONSE_CANCEL:
            if self.__pulseSourceTag is not None:
                gobject.source_remove(self.__pulseSourceTag)
                os.kill(self.__exportingProcessPid,signal.SIGKILL)
            self.__cancelOperation = True


    def on_importing_file_progress_dialog_response(self, dialog, responseId):
        if responseId == gtk.RESPONSE_CANCEL:
            if self.__pulseSourceTag is not None:
                gobject.source_remove(self.__pulseSourceTag)
                os.kill(self.__importingProcessPid,signal.SIGKILL)
            self.__cancelOperation = True


    def on_magazzino_casse_combobox_changed( self, combo ):
        index = combo.get_active()
        if index >= 0:
            self.magazzino = combo.get_model()[index][2].strip()
            combo.child.set_text(self.magazzino)
