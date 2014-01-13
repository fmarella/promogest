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

from promogest.ui.gtk_compat import *
from promogest.lib.utils import *
from promogest.ui.GladeWidget import GladeWidget
from promogest import Environment
from promogest.dao.TestataDocumentoUtils import do_genera_fatture_provvigioni


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

    def on_confirm_button_clicked(self, button=None):
        if self.da_data_entry.get_text() == '':
            obligatoryField(self.getTopLevel(), self.da_data_entry)
        if self.a_data_entry.get_text() == '':
            obligatoryField(self.getTopLevel(), self.a_data_entry)
        if self.data_documento_entry.get_text() == '':
            obligatoryField(self.getTopLevel(), self.data_documento_entry)

        da_data = self.da_data_entry.get_text()
        a_data = self.a_data_entry.get_text()
        data_documento = self.data_documento_entry.get_text()

        do_genera_fatture_provvigioni(stringToDate(da_data), stringToDate(a_data), stringToDate(data_documento), self.progress)

        self.getTopLevel().destroy()
