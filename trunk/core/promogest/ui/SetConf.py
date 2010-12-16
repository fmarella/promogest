# -*- coding: utf-8 -*-

# Promogest
#
# Copyright (C) 2005-2009 by Promotux Informatica - http://www.promotux.it/
# Author: Alceste Scalas <alceste@promotux.it>
# Author: Francesco Meloni <francesco@promotux.it>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.

import gtk
import hashlib
from promogest.ui.utils import orda
from promogest.dao.Setconf import SetConf
from promogest.dao.SectionUser import SectionUser
from GladeWidget import GladeWidget
import datetime

class SetConfUI(GladeWidget):
    """ Widget di configurazione del codice installazione e dei parametri
    di configurazione """
    def __init__(self, main):
        GladeWidget.__init__(self, 'setconf_window',
                                    'setconf_ui.glade')
        self.placeWindow(self.getTopLevel())
        self.rowBackGround = None
        self.rowBoldFont = 'arial bold 11'
        self.draw()

    def draw(self):
        self.mastercode = SetConf().select(key="install_code", section="Master")[0]
        self.cod_installazione_entry.set_text(self.mastercode.value)
        self.cod_installazione_entry.set_sensitive(False)
        self.treeview = self.setconf_treeview
        rendererSx = gtk.CellRendererText()
        column = gtk.TreeViewColumn("Sezione/Chiave", rendererSx, text=1, background=6, font=7)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(False)
        column.set_resizable(True)
        column.set_min_width(70)
        self.treeview.append_column(column)

        celltext = gtk.CellRendererText()
        celltext.set_property("editable", True)
        celltext.set_property("visible", True)
        celltext.connect('edited', self.on_column_codice_edited, self.treeview, True)
        column = gtk.TreeViewColumn('Valore', celltext, text=2)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
#        column.set_resizable(True)
#        column.set_expand(True)
#        column.set_min_width(50)
        self.treeview.append_column(column)

        rendererSx = gtk.CellRendererText()
        rendererSx.set_property("wrap-width",290)
        rendererSx.set_property("wrap-mode", gtk.WRAP_WORD)
        column = gtk.TreeViewColumn("Descrizione", rendererSx, text=3)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(False)
        column.set_resizable(True)
        column.set_min_width(300)
        self.treeview.append_column(column)

        rendererSx = gtk.CellRendererText()
        column = gtk.TreeViewColumn("Tipo Sezione", rendererSx, text=4)
#        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(False)
#        column.set_resizable(True)
        column.set_min_width(70)
        self.treeview.append_column(column)

        rendererSx = gtk.CellRendererText()
        column = gtk.TreeViewColumn("Tipo Chiave", rendererSx, text=5)
#        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(False)
#        column.set_resizable(True)
        column.set_min_width(70)
        self.treeview.append_column(column)

        cellspin = gtk.CellRendererToggle()
        cellspin.set_property('activatable', True)
        cellspin.connect('toggled', self.on_column_selected_edited, self.treeview, True)
        column = gtk.TreeViewColumn('Attiva', cellspin)
        column.add_attribute( cellspin, "active", 8)
#        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_resizable(False)
        column.set_expand(False)
        column.set_min_width(70)
        self.treeview.append_column(column)

        self._treeViewModel = gtk.TreeStore(object,str,str,str, str,str,str,str,bool)
        self.treeview.set_model(self._treeViewModel)
        self._refresh()

    def on_edit_togglebutton_toggled(self, button):
        if button.get_active():
            self.cod_installazione_entry.set_sensitive(True)
        else:
            self.cod_installazione_entry.set_sensitive(False)

    def _refresh(self):
        self._treeViewModel.clear()
        sc = SetConf().select(batchSize=None, orderBy=SetConf.section)
        sect = list(set([ x.section for x in sc]))
        for s in sect:
            if s != "Master":
                iter = self._treeViewModel.append(None,(s,
                                            s,
                                            "",
                                            "",
                                            "",
                                           "",
                                            self.rowBackGround,
                                            self.rowBoldFont,
                                            False))
            ss = SetConf().select(section=s,batchSize=None, orderBy=SetConf.section)
            for s in ss:
                if (s.key != "install_code") and\
                        (s.key !="pan") and \
                            (s.key != "password") and\
                                (s.key != "username") :
                    if s.tipo == "BOOLEAN":
                        valore = "USARE 'ATTIVA' PER ATTIVARE / DISATTIVARE"
                    else:
                        valore = s.value
                    self._treeViewModel.append(iter,(s,
                                            s.key,
                                            valore,
                                            s.description,
                                            s.tipo_section,
                                            s.tipo,
                                            None,
                                            None,
                                            s.active))

    def on_column_selected_edited(self, cell, path, treeview,value, editNext=True):
        """ Function to set the value quantita edit in the cell"""
        model = treeview.get_model()
        model[path][8] = not model[path][8]
        for a in  model[path].iterchildren():
             a[8] = model[path][8]

    def on_column_codice_edited(self, cell, path, value, treeview, editNext=True):
        """ Function ti set the value codice edit in the cell"""
        model = treeview.get_model()
        model[path][2] = value

    def saveDao(self, model, path, iter):
        check = model.get_value(iter, 1)
        fatherPath = model.get_path(iter)
        if check:
            if len(fatherPath) == 1:
                return
            oggettoFiglio = model.get_value(iter, 0)
            if oggettoFiglio.value != model.get_value(iter, 2):
                oggettoFiglio.value = model.get_value(iter, 2)
            if oggettoFiglio.active !=  model.get_value(iter, 8):
                oggettoFiglio.active = model.get_value(iter, 8)
            oggettoFiglio.persist()
        mcode = self.cod_installazione_entry.get_text()
        mcode = mcode.lower().strip()
        if mcode != "":
            self.mastercode.value =  mcode
            self.mastercode.tipo = "PRO"
            self.mastercode.persist()

    def on_save_button_clicked(self,button):
        self._treeViewModel.foreach(self.saveDao)
        self.destroy()

    def on_close_button_clicked(self, button):
        self.destroy()



if not SetConf().select(key="install_code",section="Master"):
    k = SetConf()
    k.key = "install_code"
    k.value =str(hashlib.sha224("aziendapromo"+orda("aziendapromo")).hexdigest())
    k.section = "Master"
    k.description = "codice identificativo della propria installazione"
    k.tipo_section = "General"
    k.tipo = "ONE"
    k.active = True
    k.date = datetime.datetime.now()
    k.persist()

codice=  SetConf().select(key="install_code",section="Master")
if codice:
    if codice[0].value =="ad2a57ed2bd4d4df494e174b576cf8e822a18be2e1b074871c69b31f":
        codice[0].value = "8f0eff136d1fb1d2b76fde5de7c83eb60d558c4f155ee687dcac5504"
        codice[0].persist()


if not SetConf().select(key="fornitore_predefinito",section="Documenti"):
    k = SetConf()
    k.key = "fornitore_predefinito"
    k.value =""
    k.section = "Documenti"
    k.description = "eventuale fornitore preferenziale da preimpostare"
    k.tipo_section = "Generico"
    k.active = True
    k.date = datetime.datetime.now()
    k.persist()
if not SetConf().select(key="cliente_predefinito",section="Documenti"):
    k = SetConf()
    k.key = "cliente_predefinito"
    k.value =""
    k.section = "Documenti"
    k.description = "eventuale cliente preferenziale da preimpostare"
    k.tipo_section = "Generico"
    k.active = True
    k.date = datetime.datetime.now()
    k.persist()
if not SetConf().select(key="tipo_documento_predefinito",section="Documenti"):
    k = SetConf()
    k.key = "tipo_documento_predefinito"
    k.value =""
    k.section = "Documenti"
    k.description = "eventuale tipo documento preferenziale da preimpostare"
    k.tipo_section = "Generico"
    k.active = True
    k.date = datetime.datetime.now()
    k.persist()
if not SetConf().select(key="altezza_logo",section="Documenti"):
    k = SetConf()
    k.key = "altezza_logo"
    k.value ="110"
    k.section = "Documenti"
    k.description = "altezza logo documento"
    k.tipo_section = "Generico"
    k.active = True
    k.date = datetime.datetime.now()
    k.persist()
if not SetConf().select(key="larghezza_logo",section="Documenti"):
    k = SetConf()
    k.key = "larghezza_logo"
    k.value ="300"
    k.section = "Documenti"
    k.description = "larghezza logo documento"
    k.tipo_section = "Generico"
    k.active = True
    k.date = datetime.datetime.now()
    k.persist()
if not SetConf().select(key="tipo_movimento_predefinito",section="Documenti"):
    k = SetConf()
    k.key = "tipo_movimento_predefinito"
    k.value =""
    k.section = "Documenti"
    k.description = "eventuale tipo movimento preferenziale da preimpostare"
    k.tipo_section = "Generico"
    k.active = True
    k.date = datetime.datetime.now()
    k.persist()
if not SetConf().select(key="ricerca_per",section="Documenti"):
    k = SetConf()
    k.key = "ricerca_per"
    k.value ="codice"
    k.section = "Documenti"
    k.description = "Preimposta un tipo di ricerca Valori possibili:(codice,descrizione,codice_a_barre,codice_articolo_fornitore "
    k.tipo_section = "Generico"
    k.active = True
    k.date = datetime.datetime.now()
    k.persist()
if not SetConf().select(key="color_base",section="Documenti"):
    k = SetConf()
    k.key = "color_base"
    k.value ="#F9FBA7"
    k.section = "Documenti"
    k.description = "Preimposta il colore di base "
    k.tipo_section = "Generico"
    k.tipo = "Colore"
    k.active = True
    k.date = datetime.datetime.now()
    k.persist()
if not SetConf().select(key="color_text",section="Documenti"):
    k = SetConf()
    k.key = "color_text"
    k.value ="black"
    k.section = "Documenti"
    k.description = "Preimposta il colore del testo "
    k.tipo_section = "Generico"
    k.tipo = "Colore"
    k.active = True
    k.date = datetime.datetime.now()
    k.persist()
if not SetConf().select(key="feed",section="Feed"):
    k = SetConf()
    k.key = "feed"
    k.value =""
    k.section = "Feed"
    k.description = "Notizie nella home"
    k.tipo_section = "Generico"
    k.active = True
    k.tipo = "BOOLEAN"
    k.date = datetime.datetime.now()
    k.persist()
ff = SetConf().select(key="feed", section="Feed")
if ff:
    ff[0].tipo = "BOOLEAN"
    ff[0].persist()
if not SetConf().select(key="smtpserver", section="Smtp"):
    k = SetConf()
    k.key = "smtpserver"
    k.value =""
    k.section = "Smtp"
    k.tipo_section = "Generico"
    k.description = "server per l'invio della posta"
    k.active = True
    k.date = datetime.datetime.now()
    k.persist()
if not SetConf().select(key="emailmittente", section="Smtp"):
    k = SetConf()
    k.key = "emailmittente"
    k.value =""
    k.section = "Smtp"
    k.tipo_section = "Generico"
    k.description = "Email del mittente"
    k.active = True
    k.date = datetime.datetime.now()
    k.persist()
if not SetConf().select(key="multilinealimite", section="Multilinea"):
    k = SetConf()
    k.key = "multilinealimite"
    k.value ="60"
    k.section = "Multilinea"
    k.tipo_section = "Generico"
    k.description = "Gestione dei multilinea nei documenti"
    k.active = True
    k.date = datetime.datetime.now()
    k.persist()

bb = SetConf().select(key="decimals", section="Numbers")
if not bb:
    k = SetConf()
    k.key = "decimals"
    k.value ="2"
    k.section = "Numbers"
    k.tipo_section = "Generico"
    k.description = "Gestione dei decimali"
    k.active = True
    k.date = datetime.datetime.now()
    k.persist()
else:
    try:
        int(bb[0].value)
    except:
        bb[0].value ="2"
        bb[0].persist()

aa = SetConf().select(key="batch_size", section="Numbers")
if not aa:
    k = SetConf()
    k.key = "batch_size"
    k.value ="15"
    k.section = "Numbers"
    k.tipo_section = "Generico"
    k.description = "Gestione dei batchSize"
    k.active = True
    k.date = datetime.datetime.now()
    k.persist()
else:
    try:
        int(aa[0].value)
    except:
        aa[0].value ="15"
        aa[0].persist()

cc = SetConf().select(key="combo_column", section="Numbers")
if not cc:
    k = SetConf()
    k.key = "combo_column"
    k.value ="3"
    k.section = "Numbers"
    k.tipo_section = "Generico"
    k.description = "Gestione dei combo_column cioè le colonne nelle combobox"
    k.active = True
    k.date = datetime.datetime.now()
    k.persist()
else:
    try:
        int(cc[0].value)
    except:
        cc[0].value ="3"
        cc[0].persist()

if not SetConf().select(key="rotazione_primanota", section="Primanota"):
    k = SetConf()
    k.key = "rotazione_primanota"
    k.value ="mensile"
    k.section = "Primanota"
    k.tipo_section = "Generico"
    k.description = "Gestione della creazione della prima nota, valori ammessi, MESE, SETTIMANA, TRIMESTRE"
    k.active = True
    k.date = datetime.datetime.now()
    k.persist()
