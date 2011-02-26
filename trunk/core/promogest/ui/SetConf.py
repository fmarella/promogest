# -*- coding: utf-8 -*-

# Promogest
#
# Copyright (C) 2005-2009 by Promotux Informatica - http://www.promotux.it/
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
#        self.mastercode = SetConf().select(key="install_code", section="Master")[0]
#        self.cod_installazione_entry.set_text(self.mastercode.value)
#        self.cod_installazione_entry.set_sensitive(False)
        self.treeview = self.setconf_treeview
        rendererSx = gtk.CellRendererText()
        column = gtk.TreeViewColumn("Sezione/Chiave", rendererSx, text=1, background=4, font=5)
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
        column.set_expand(True)
        column.set_min_width(300)
        self.treeview.append_column(column)

#        rendererSx = gtk.CellRendererText()
#        column = gtk.TreeViewColumn("Tipo Sezione", rendererSx, text=4)
##        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
#        column.set_clickable(False)
##        column.set_resizable(True)
#        column.set_min_width(70)
#        self.treeview.append_column(column)

#        rendererSx = gtk.CellRendererText()
#        column = gtk.TreeViewColumn("Tipo Chiave", rendererSx, text=5)
##        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
#        column.set_clickable(False)
##        column.set_resizable(True)
#        column.set_min_width(70)
#        self.treeview.append_column(column)

        cellspin = gtk.CellRendererToggle()
        cellspin.set_property('activatable', True)
        cellspin.connect('toggled', self.on_column_selected_edited, self.treeview, True)
        column = gtk.TreeViewColumn('Attiva', cellspin)
        column.add_attribute( cellspin, "active", 6)
#        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_resizable(False)
        column.set_expand(False)
        column.set_min_width(70)
        self.treeview.append_column(column)

        self._treeViewModel = gtk.TreeStore(object,str,str,str, str,str,bool)
        self.treeview.set_model(self._treeViewModel)
        self._refresh()

    def _refresh(self):
        self._treeViewModel.clear()
        sc = SetConf().select(batchSize=None, orderBy=SetConf.section)
        sect = list(set([ x.section for x in sc]))
        for s in sect:
            if s in "Master":
                continue
            if s not in "Master":
                iter = self._treeViewModel.append(None,(s,
                                            s,
                                            "",
                                           "",
                                            self.rowBackGround,
                                            self.rowBoldFont,
                                            False))
            ss = SetConf().select(section=s,batchSize=None, orderBy=SetConf.section)
            for s in ss:
                if    (s.key != "password") and\
                                (s.key != "username") :
                    if s.tipo == "BOOLEAN":
                        valore = "USARE 'ATTIVA' / DISATTIVA"
                    else:
                        valore = s.value
                    self._treeViewModel.append(iter,(s,
                                            s.key,
                                            valore,
                                            s.description,
                                            None,
                                            None,
                                            s.active))

    def on_column_selected_edited(self, cell, path, treeview,value, editNext=True):
        """ Function to set the value quantita edit in the cell"""
        model = treeview.get_model()
        model[path][6] = not model[path][6]
        for a in  model[path].iterchildren():
             a[6] = model[path][6]

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
            if oggettoFiglio.active !=  model.get_value(iter, 6):
                oggettoFiglio.active = model.get_value(iter, 6)
            oggettoFiglio.persist()
#        mcode = self.cod_installazione_entry.get_text()
#        mcode = mcode.lower().strip()
#        if mcode != "":
#            self.mastercode.value =  mcode
#            self.mastercode.tipo = "PRO"
#            self.mastercode.persist()

    def on_save_button_clicked(self,button):
        self._treeViewModel.foreach(self.saveDao)
        self.destroy()

    def on_close_button_clicked(self, button):
        self.destroy()



if not SetConf().select(key="install_code",section="Master"):
    kmm = SetConf()
    kmm.key = "install_code"
    kmm.value =str(hashlib.sha224("aziendapromo"+orda("aziendapromo")).hexdigest())
    kmm.section = "Master"
    kmm.description = "codice identificativo della propria installazione"
    kmm.tipo_section = "General"
    kmm.tipo = "ONE BASIC"
    kmm.active = True
    kmm.date = datetime.datetime.now()
    kmm.persist()

codice=  SetConf().select(key="install_code",section="Master")
if codice:
    if codice[0].value =="ad2a57ed2bd4d4df494e174b576cf8e822a18be2e1b074871c69b31f":
        codice[0].value = "8f0eff136d1fb1d2b76fde5de7c83eb60d558c4f155ee687dcac5504"
        codice[0].persist()


if not SetConf().select(key="fornitore_predefinito",section="Documenti"):
    kkk = SetConf()
    kkk.key = "fornitore_predefinito"
    kkk.value =""
    kkk.section = "Documenti"
    kkk.description = "eventuale fornitore preferenziale da preimpostare"
    kkk.tipo_section = "Generico"
    kkk.active = True
    kkk.date = datetime.datetime.now()
    kkk.persist()

if not SetConf().select(key="cliente_predefinito",section="Documenti"):
    kll = SetConf()
    kll.key = "cliente_predefinito"
    kll.value =""
    kll.section = "Documenti"
    kll.description = "eventuale cliente preferenziale da preimpostare"
    kll.tipo_section = "Generico"
    kll.active = True
    kll.date = datetime.datetime.now()
    kll.persist()

if not SetConf().select(key="tipo_documento_predefinito",section="Documenti"):
    knn = SetConf()
    knn.key = "tipo_documento_predefinito"
    knn.value =""
    knn.section = "Documenti"
    knn.description = "eventuale tipo documento preferenziale da preimpostare"
    knn.tipo_section = "Generico"
    knn.active = True
    knn.date = datetime.datetime.now()
    knn.persist()

if not SetConf().select(key="altezza_logo",section="Documenti"):
    koo = SetConf()
    koo.key = "altezza_logo"
    koo.value ="110"
    koo.section = "Documenti"
    koo.description = "altezza logo documento"
    koo.tipo_section = "Generico"
    koo.active = True
    koo.date = datetime.datetime.now()
    koo.persist()

if not SetConf().select(key="larghezza_logo",section="Documenti"):
    kpp = SetConf()
    kpp.key = "larghezza_logo"
    kpp.value ="300"
    kpp.section = "Documenti"
    kpp.description = "larghezza logo documento"
    kpp.tipo_section = "Generico"
    kpp.active = True
    kpp.date = datetime.datetime.now()
    kpp.persist()

if not SetConf().select(key="tipo_movimento_predefinito",section="Documenti"):
    kqq = SetConf()
    kqq.key = "tipo_movimento_predefinito"
    kqq.value =""
    kqq.section = "Documenti"
    kqq.description = "eventuale tipo movimento preferenziale da preimpostare"
    kqq.tipo_section = "Generico"
    kqq.active = True
    kqq.date = datetime.datetime.now()
    kqq.persist()

if not SetConf().select(key="ricerca_per",section="Documenti"):
    krr = SetConf()
    krr.key = "ricerca_per"
    krr.value ="codice"
    krr.section = "Documenti"
    krr.description = "Preimposta un tipo di ricerca Valori possibili:(codice,descrizione,codice_a_barre,codice_articolo_fornitore "
    krr.tipo_section = "Generico"
    krr.active = True
    krr.date = datetime.datetime.now()
    krr.persist()

if not SetConf().select(key="color_base",section="Documenti"):
    kss = SetConf()
    kss.key = "color_base"
    kss.value ="#F9FBA7"
    kss.section = "Documenti"
    kss.description = "Preimposta il colore di base "
    kss.tipo_section = "Generico"
    kss.tipo = "Colore"
    kss.active = True
    kss.date = datetime.datetime.now()
    kss.persist()

if not SetConf().select(key="color_text",section="Documenti"):
    ktt = SetConf()
    ktt.key = "color_text"
    ktt.value ="black"
    ktt.section = "Documenti"
    ktt.description = "Preimposta il colore del testo "
    ktt.tipo_section = "Generico"
    ktt.tipo = "Colore"
    ktt.active = True
    ktt.date = datetime.datetime.now()
    ktt.persist()

if not SetConf().select(key="feed",section="Feed"):
    kuu = SetConf()
    kuu.key = "feed"
    kuu.value =""
    kuu.section = "Feed"
    kuu.description = "Notizie nella home"
    kuu.tipo_section = "Generico"
    kuu.active = True
    kuu.tipo = "BOOLEAN"
    kuu.date = datetime.datetime.now()
    kuu.persist()
ff = SetConf().select(key="feed", section="Feed")
if ff:
    ff[0].tipo = "BOOLEAN"
    ff[0].persist()

if not SetConf().select(key="smtpserver", section="Smtp"):
    kvv = SetConf()
    kvv.key = "smtpserver"
    kvv.value =""
    kvv.section = "Smtp"
    kvv.tipo_section = "Generico"
    kvv.description = "server per l'invio della posta"
    kvv.active = True
    kvv.date = datetime.datetime.now()
    kvv.persist()

if not SetConf().select(key="emailmittente", section="Smtp"):
    kzz = SetConf()
    kzz.key = "emailmittente"
    kzz.value =""
    kzz.section = "Smtp"
    kzz.tipo_section = "Generico"
    kzz.description = "Email del mittente"
    kzz.active = True
    kzz.date = datetime.datetime.now()
    kzz.persist()

if not SetConf().select(key="multilinealimite", section="Multilinea"):
    kaa = SetConf()
    kaa.key = "multilinealimite"
    kaa.value ="60"
    kaa.section = "Multilinea"
    kaa.tipo_section = "Generico"
    kaa.description = "Gestione dei multilinea nei documenti"
    kaa.active = True
    kaa.date = datetime.datetime.now()
    kaa.persist()

bb = SetConf().select(key="decimals", section="Numbers")
if not bb:
    kbb = SetConf()
    kbb.key = "decimals"
    kbb.value ="2"
    kbb.section = "Numbers"
    kbb.tipo_section = "Generico"
    kbb.description = "Gestione dei decimali"
    kbb.active = True
    kbb.date = datetime.datetime.now()
    kbb.persist()
else:
    try:
        int(bb[0].value)
    except:
        bb[0].value ="2"
        bb[0].persist()

aa = SetConf().select(key="batch_size", section="Numbers")
if not aa:
    kcc = SetConf()
    kcc.key = "batch_size"
    kcc.value ="15"
    kcc.section = "Numbers"
    kcc.tipo_section = "Generico"
    kcc.description = "Gestione dei batchSize"
    kcc.active = True
    kcc.date = datetime.datetime.now()
    kcc.persist()
else:
    try:
        int(aa[0].value)
    except:
        aa[0].value ="15"
        aa[0].persist()

cc = SetConf().select(key="combo_column", section="Numbers")
if not cc:
    kdd = SetConf()
    kdd.key = "combo_column"
    kdd.value ="3"
    kdd.section = "Numbers"
    kdd.tipo_section = "Generico"
    kdd.description = "Gestione dei combo_column cioè le colonne nelle combobox"
    kdd.active = True
    kdd.date = datetime.datetime.now()
    kdd.persist()
else:
    try:
        int(cc[0].value)
    except:
        cc[0].value ="3"
        cc[0].persist()

if not SetConf().select(key="rotazione_primanota", section="Primanota"):
    kee = SetConf()
    kee.key = "rotazione_primanota"
    kee.value ="mensile"
    kee.section = "Primanota"
    kee.tipo_section = "Generico"
    kee.description = "Gestione della creazione della prima nota, valori ammessi, MESE, SETTIMANA, TRIMESTRE"
    kee.active = True
    kee.date = datetime.datetime.now()
    kee.persist()

if not SetConf().select(key="zeri_in_riga",section="Stampa"):
    kuu = SetConf()
    kuu.key = "zeri_in_riga"
    kuu.value =""
    kuu.section = "Stampa"
    kuu.description = "Visualizza gli zeri nelle righe documento"
    kuu.tipo_section = "Generico"
    kuu.active = False
    kuu.tipo = "BOOLEAN"
    kuu.date = datetime.datetime.now()
    kuu.persist()
ff = SetConf().select(key="zeri_in_riga", section="Stampa")
if ff:
    ff[0].tipo = "BOOLEAN"
    ff[0].persist()

if not SetConf().select(key="zeri_in_totali",section="Stampa"):
    kuu1 = SetConf()
    kuu1.key = "zeri_in_totali"
    kuu1.value =""
    kuu1.section = "Stampa"
    kuu1.description = "Visualizza gli zeri nei totali"
    kuu1.tipo_section = "Generico"
    kuu1.active = False
    kuu1.tipo = "BOOLEAN"
    kuu1.date = datetime.datetime.now()
    kuu1.persist()
ff1 = SetConf().select(key="zeri_in_totali", section="Stampa")
if ff1:
    ff1[0].tipo = "BOOLEAN"
    ff1[0].persist()
