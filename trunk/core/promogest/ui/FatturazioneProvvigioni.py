# -*- coding: utf-8 -*-

#    Copyright (C) 2005-2012 by Promotux
#                        di Francesco Meloni snc - http://www.promotux.it/

#    Author: Francesco Meloni  <francesco@promotux.it>
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

import os
from shutil import copy2

from promogest.ui.gtk_compat import *
from promogest.lib.utils import *
from promogest.ui.GladeWidget import GladeWidget
from promogest import Environment
from promogest.dao.TestataDocumentoUtils import do_genera_fatture_provvigioni, TIPO_DATA_DOC, TIPO_DATA_SPED


class FatturazioneProvvigioni(GladeWidget):

    def __init__(self, selection=None):
        """ finestra di gestione della fattura differita"""
        GladeWidget.__init__(self, root='fatturazione_provv_window',
                             path='fatturazione_provv.glade')
        if selection is None:
            return
        self.draw()

    def draw(self):
        self.data_documento_entry.set_text(dateToString(datetime.datetime.today()))
        self.data_documento_entry.grab_focus()

    def on_esporta_button_clicked(self, widget):
        fileDialog = gtk.FileChooserDialog(title='Salva il file',
                                           parent=self.getTopLevel(),
                                           action=gtk.FILE_CHOOSER_ACTION_SAVE,
                                           buttons=(gtk.STOCK_CANCEL,
                                                    gtk.RESPONSE_CANCEL,
                                                    gtk.STOCK_SAVE,
                                                    gtk.RESPONSE_OK),
                                           backend=None)
        fileDialog.set_current_name("fatturazione_provvigioni.csv")
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
                copy2(os.path.join(Environment.tempDir, "riepilogo_provv.csv"), filename)

    def on_confirm_button_clicked(self, button=None):
        tipo_data = None
        if self.data_spedizione_radiobutton.get_active():
            tipo_data = TIPO_DATA_SPED
        if self.data_documento_radiobutton.get_active():
            tipo_data = TIPO_DATA_DOC
        if self.da_data_entry.get_text() == '':
            obligatoryField(self.getTopLevel(), self.da_data_entry)
        if self.a_data_entry.get_text() == '':
            obligatoryField(self.getTopLevel(), self.a_data_entry)
        if self.data_documento_entry.get_text() == '':
            obligatoryField(self.getTopLevel(), self.data_documento_entry)

        da_data = self.da_data_entry.get_text()
        a_data = self.a_data_entry.get_text()
        data_documento = self.data_documento_entry.get_text()

        do_genera_fatture_provvigioni(tipo_data, stringToDate(da_data), stringToDate(a_data), stringToDate(data_documento), self.progress)
