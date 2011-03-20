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
