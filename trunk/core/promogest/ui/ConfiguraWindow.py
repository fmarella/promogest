# -*- coding: utf-8 -*-

#    Copyright (C) 2005, 2006, 2007 2008, 2009, 2010 by Promotux
#                        di Francesco Meloni snc - http://www.promotux.it/

#    Author: Francesco Meloni  <francesco@promotux.it>

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

import gtk
from promogest import Environment
from GladeWidget import GladeWidget
from promogest.ui.AnagraficaDocumentiSetup import AnagraficaDocumentiSetup
from ParametriFrame import ParametriFrame
from promogest.dao.Setconf import SetConf
from promogest.ui.utils import setconf, messageInfo

class ConfiguraWindow(GladeWidget):

    def __init__(self, mainWindow):
        self.mainWindow = mainWindow
        GladeWidget.__init__(self, 'configura_window',
                                    fileName='configura_window.glade')
        self.placeWindow(self.getTopLevel())
        self.addTabs()

    def addTabs(self):
        self.documenti_setup_page = AnagraficaDocumentiSetup(self)
        documenti_setup_page_label = gtk.Label()
        documenti_setup_page_label.set_markup("DOCUMENTI")
        self.setup_notebook.append_page(self.documenti_setup_page._anagrafica_documenti_setup_frame, documenti_setup_page_label)
        self._refresh()

#        frame = ParametriFrame(self,"NONE", modules=self.parametri_modules)
#        self.setup_notebook.append_page(frame, documenti_setup_page_label)

    def _refresh(self):
        self.zeri_in_riga_check.set_active(int(setconf("Stampa", "zeri_in_riga") or 0))
        self.zeri_in_totali_check.set_active(int(setconf("Stampa", "zeri_in_totali") or 0 ))
        self.feed_check.set_active(int(setconf("Feed", "feed") or 1))

        self.altezza_logo_entry.set_text(str(setconf("Documenti", "altezza_logo")))
        self.larghezza_logo_entry.set_text(str(setconf("Documenti", "larghezza_logo")))
        self.combo_column_entry.set_text(str(setconf("Numbers", "combo_column")))
        self.decimals_entry.set_text(str(setconf("Numbers","decimals")))
        self.batch_size_entry.set_text(str(setconf("Numbers","batch_size")))
        self.documenti_setup_page._refresh()

    def on_salva_button_clicked(self, button_salva):

        a = SetConf().select(key="feed", section="Feed")
        a[0].value= str(self.feed_check.get_active())
        a[0].tipo = "bool"
        Environment.session.add(a[0])

        b = SetConf().select(key="zeri_in_totali", section="Stampa")
        b[0].value = str(self.zeri_in_totali_check.get_active())
        b[0].tipo = "bool"
        Environment.session.add(b[0])

        c = SetConf().select(key="zeri_in_riga", section="Stampa")
        c[0].value = str(self.zeri_in_riga_check.get_active())
        c[0].tipo = "bool"
        Environment.session.add(c[0])

        d = SetConf().select(key="altezza_logo", section="Documenti")
        d[0].value = str(self.altezza_logo_entry.get_text())
        d[0].tipo = "float"
        Environment.session.add(d[0])

        e = SetConf().select(key="larghezza_logo", section="Documenti")
        e[0].value = str(self.larghezza_logo_entry.get_text())
        e[0].tipo = "float"
        Environment.session.add(e[0])

        f = SetConf().select(key="combo_column", section="Numbers")
        f[0].value = str(self.combo_column_entry.get_text())
        f[0].tipo = "int"
        Environment.session.add(f[0])

        g = SetConf().select(key="decimals", section="Numbers")
        g[0].value = str(self.decimals_entry.get_text())
        g[0].tipo = "int"
        Environment.session.add(g[0])

        f = SetConf().select(key="batch_size", section="Numbers")
        f[0].value = str(self.batch_size_entry.get_text())
        f[0].tipo = "int"
        Environment.session.add(f[0])

        self.documenti_setup_page._saveSetup()

        Environment.session.commit()
        confList = SetConf().select(batchSize=None)
        Environment.confList = confList
        messageInfo(msg="SALVATO CORRETTAMENTE")


    def on_quit(self, widget=None, event=None):
        self.destroy()
