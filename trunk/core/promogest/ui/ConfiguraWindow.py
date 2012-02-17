# -*- coding: utf-8 -*-

#    Copyright (C) 2005-2012 by Promotux
#                        di Francesco Meloni snc - http://www.promotux.it/

#    Author: Francesco Meloni  <francesco@promotux.it>
#    Author: Francesco Marella <francesco.marella@gmail.com>

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
import datetime
from promogest import Environment
from GladeWidget import GladeWidget
from promogest.ui.anagDocumenti.AnagraficaDocumentiSetup import AnagraficaDocumentiSetup
from promogest.ui.AnagraficaArticoliSetup import AnagraficaArticoliSetup
from promogest.ui.AnagraficaClientiSetup import AnagraficaClientiSetup
from promogest.ui.AnagraficaFornitoriSetup import AnagraficaFornitoriSetup
from promogest.modules.PrimaNota.ui.AnagraficaPrimaNotaSetup import AnagraficaPrimaNotaSetup
from promogest.modules.Label.ui.AnagraficaLabelSetup import AnagraficaLabelSetup
from ParametriFrame import ParametriFrame
from promogest.dao.Setconf import SetConf
from promogest.ui.utils import setconf, messageInfo, posso, findIdFromCombobox
from promogest.ui.utilsCombobox import findComboboxRowFromId

class ConfiguraWindow(GladeWidget):

    def __init__(self, mainWindow):
        self.mainWindow = mainWindow
        GladeWidget.__init__(self, 'configura_window',
                                    fileName='configura_window.glade')
        self.placeWindow(self.getTopLevel())

        self.draw()
        self.addTabs()

    def draw(self):
        folder = setconf("General", "cartella_predefinita") or ""
        self.cartella_predefinita_filechooserbutton.set_current_folder(folder)
        self.path_label.set_text(folder)

    def on_cartella_predefinita_filechooserbutton_file_set(self,filechooser):
        self.path_label.set_text(str(filechooser.get_current_folder()))

    def addTabs(self):
        self.documenti_setup_page = AnagraficaDocumentiSetup(self)
        self.setup_notebook.append_page(self.documenti_setup_page._anagrafica_documenti_setup_frame, self.documenti_setup_page.documenti_setup_page_label)

        self.articoli_setup_page = AnagraficaArticoliSetup(self)
        self.setup_notebook.append_page(self.articoli_setup_page._anagrafica_articoli_setup_frame, self.articoli_setup_page.articoli_setup_page_label)

        self.clienti_setup_page = AnagraficaClientiSetup(self)
        self.setup_notebook.append_page(self.clienti_setup_page._anagrafica_clienti_setup_frame, self.clienti_setup_page.clienti_setup_page_label)

        self.fornitori_setup_page = AnagraficaFornitoriSetup(self)
        self.setup_notebook.append_page(self.fornitori_setup_page._anagrafica_fornitori_setup_frame, self.fornitori_setup_page.fornitori_setup_page_label)

        self.primanota_setup_page = AnagraficaPrimaNotaSetup(self)
        self.setup_notebook.append_page(self.primanota_setup_page._anagrafica_primanota_setup_frame, self.primanota_setup_page.primanota_setup_page_label)

        self.label_setup_page = AnagraficaLabelSetup(self)
        self.setup_notebook.append_page(self.label_setup_page._anagrafica_label_setup_frame, self.label_setup_page.label_setup_page_label)
        if posso("VD"):
            from promogest.modules.VenditaDettaglio.ui.AnagraficaVenditadettaglioSetup import VenditadettaglioSetup
            self.vendita_dettaglio_setup_page = VenditadettaglioSetup(self)
            self.setup_notebook.append_page(self.vendita_dettaglio_setup_page._vendita_dettaglio_setup_frame, self.vendita_dettaglio_setup_page.venditadettaglio_setup_page_label)

        self._refresh()

#        frame = ParametriFrame(self,"NONE", modules=self.parametri_modules)
#        self.setup_notebook.append_page(frame, documenti_setup_page_label)

    def _refresh(self):
        try:
            self.zeri_in_riga_check.set_active(int(setconf("Stampa", "zeri_in_riga")))
        except:
            self.zeri_in_riga_check.set_active(0)
        try:
            self.zeri_in_totali_check.set_active(int(setconf("Stampa", "zeri_in_totali")))
        except:
            self.zeri_in_totali_check.set_active(0)
        try:
            self.feed_check.set_active(int(setconf("Feed", "feed")))
        except:
            self.feed_check.set_active(1)
        try:
            findComboboxRowFromId(self.timer_combobox, str(setconf("General", "updates_timeout")))
        except:
            findComboboxRowFromId(self.timer_combobox, '300')

        try:
            curr = setconf("Valuta", "valuta_curr")
            if curr =="€":
                self.euro_radio.set_active(1)
            elif curr =="$":
                self.dollaro_radio.set_active(1)
            elif curr =="£":
                self.sterlina_radio.set_active(1)
        except:
            self.euro_radio.set_active(1)
        try:
            self.mercatino_check.set_active(int(setconf("General", "gestione_totali_mercatino")))
        except:
            self.mercatino_check.set_active(0)

        try:
            self.vettore_codice_upper_check.set_active(int(setconf("Vettori", "vettore_codice_upper")))
        except:
            self.vettore_codice_upper_check.set_active(1)

        self.vettore_struttura_codice_entry.set_text(str(setconf("Vettori", "vettore_struttura_codice")))
        self.altezza_logo_entry.set_text(str(setconf("Documenti", "altezza_logo")))
        self.larghezza_logo_entry.set_text(str(setconf("Documenti", "larghezza_logo")))
        self.combo_column_entry.set_text(str(setconf("Numbers", "combo_column")))
        self.decimals_entry.set_text(str(setconf("Numbers","decimals")))
        self.batch_size_entry.set_text(str(setconf("Numbers","batch_size")))
        self.documenti_setup_page._refresh()
        self.articoli_setup_page._refresh()
        self.clienti_setup_page._refresh()
        self.fornitori_setup_page._refresh()
        self.primanota_setup_page._refresh()
        self.label_setup_page._refresh()
        if posso("VD"):
            self.vendita_dettaglio_setup_page._refresh()

    def on_salva_button_clicked(self, button_salva):

        a = SetConf().select(key="feed", section="Feed")
        a[0].value= str(self.feed_check.get_active())
        a[0].tipo = "bool"
        Environment.session.add(a[0])

        a = SetConf().select(key="updates_timeout", section="General")
        a[0].value = str(findIdFromCombobox(self.timer_combobox))
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
        if Environment.tipo_eng =="postgresql":
            if not hasattr(Environment.conf, "Documenti"):
                Environment.conf.add_section("Documenti")
                Environment.conf.save()
            if  hasattr(Environment.conf, "Documenti") and not hasattr(Environment.conf.Documenti, "cartella_predefinita"):
                setattr(Environment.conf.Documenti,"cartella_predefinita",Environment.documentsDir)
                Environment.conf.save()
            Environment.conf.Documenti.cartella_predefinita = str(self.path_label.get_text()+os.sep)
            Environment.conf.save()
        else:
            d = SetConf().select(key="cartella_predefinita", section="General")
            d[0].value = str(self.path_label.get_text()+os.sep)
            d[0].tipo = "str"
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
        g[0].value = str(self.decimals_entry.get_text()) or "2"
        g[0].tipo = "int"
        Environment.session.add(g[0])

        f = SetConf().select(key="batch_size", section="Numbers")
        f[0].value = str(self.batch_size_entry.get_text()) or "3"
        f[0].tipo = "int"
        Environment.session.add(f[0])

        c = SetConf().select(key="vettore_codice_upper", section="Vettori")
        c[0].value = str(self.vettore_codice_upper_check.get_active())
        c[0].tipo = "bool"
        Environment.session.add(c[0])

        c = SetConf().select(key="gestione_totali_mercatino", section="General")
        c[0].value = str(self.mercatino_check.get_active())
        c[0].tipo = "bool"
        Environment.session.add(c[0])


        g = SetConf().select(key="vettore_struttura_codice", section="Vettori")
        g[0].value = str(self.vettore_struttura_codice_entry.get_text())
        g[0].tipo = "str"
        Environment.session.add(g[0])

        g = SetConf().select(key="valuta_curr", section="Valuta")
        if self.euro_radio.get_active():
            g[0].value = "€"
        elif self.dollaro_radio.get_active():
            g[0].value = "$"
        elif self.sterlina_radio.get_active():
            g[0].value = "£"
        g[0].tipo = "str"
        Environment.session.add(g[0])


        self.documenti_setup_page._saveSetup()
        self.articoli_setup_page._saveSetup()
        self.clienti_setup_page._saveSetup()
        self.fornitori_setup_page._saveSetup()
        self.primanota_setup_page._saveSetup()
        self.label_setup_page._saveSetup()
        if posso("VD"):
            self.vendita_dettaglio_setup_page._saveSetup()

        Environment.session.commit()
        confList = SetConf().select(batchSize=None)
        Environment.confList = confList
        self.destroy()


    def on_quit(self, widget=None, event=None):
        self.destroy()
