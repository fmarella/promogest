# -*- coding: utf-8 -*-

#    Copyright (C) 2005-2015 by Promotux
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

from promogest import Environment
from promogest.lib.utils import *
from promogest.ui.gtk_compat import *
from promogest.modules.PromoWear.ui.PromowearUtils import *
from promogest.modules.PromoWear.dao.ArticoloTagliaColore import ArticoloTagliaColore
from promogest.dao.Articolo import Articolo

def treeViewExpand(gtkgui, treeview):
    """ Expand the normal article treeview """
    renderer = gtk.CellRendererText()
    if posso("PW"):
        column = gtk.TreeViewColumn('Gruppo taglia', renderer, text=9, background=1)
        column.set_sizing(GTK_COLUMN_GROWN_ONLY)
        column.set_clickable(False)
        column.connect("clicked", gtkgui._changeOrderBy, (ArticoloTagliaColore, ArticoloTagliaColore.id_gruppo_taglia))
        column.set_resizable(True)
        column.set_expand(False)
        column.set_min_width(100)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Modello', renderer, text=10, background=1)
        column.set_sizing(GTK_COLUMN_GROWN_ONLY)
        column.set_clickable(False)
        column.connect("clicked", gtkgui._changeOrderBy, (None, Articolo.denominazione_modello))
        column.set_resizable(True)
        column.set_expand(False)
        column.set_min_width(100)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Taglia', renderer, text=11, background=1)
        column.set_sizing(GTK_COLUMN_GROWN_ONLY)
        column.set_clickable(False)
        column.connect("clicked", gtkgui._changeOrderBy, (None,Articolo.denominazione_taglia))
        column.set_resizable(True)
        column.set_expand(False)
        column.set_min_width(100)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Colore', renderer, text=12, background=1)
        column.set_sizing(GTK_COLUMN_GROWN_ONLY)
        column.set_clickable(False)
        column.connect("clicked", gtkgui._changeOrderBy, 'denominazione_colore')
        column.set_resizable(True)
        column.set_expand(False)
        column.set_min_width(100)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Anno', renderer, text=13, background=1)
        column.set_sizing(GTK_COLUMN_GROWN_ONLY)
        column.set_clickable(True)
        column.connect("clicked", gtkgui._changeOrderBy, 'anno')
        column.set_resizable(True)
        column.set_expand(False)
        column.set_min_width(100)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Stagione', renderer, text=14, background=1)
        column.set_sizing(GTK_COLUMN_GROWN_ONLY)
        column.set_clickable(False)
        column.connect("clicked", gtkgui._changeOrderBy, 'stagione')
        column.set_resizable(True)
        column.set_expand(False)
        column.set_min_width(100)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Genere', renderer, text=15, background=1)
        column.set_sizing(GTK_COLUMN_GROWN_ONLY)
        column.set_clickable(False)
        column.connect("clicked", gtkgui._changeOrderBy, 'genere')
        column.set_resizable(True)
        column.set_expand(False)
        column.set_min_width(100)
        treeview.append_column(column)
        gtkgui._treeViewModel = gtkgui.promowear_liststore
    else:
        pass

def articleTypeGuiManage(anagrafica, dao, new):
    """ complex manage the new aticles type: plus, father son """
    gtkgui = anagrafica
    if articleType(dao) == "son":
        gtkgui.memo_wear.set_text("""ARTICOLO VARIANTE TAGLIA E COLORE""")
        # niente possibilita' di variare gruppo taglie, genere, anno e stagione
        gtkgui.con_taglie_colori_radiobutton.set_active(True)
        gtkgui.con_taglie_colori_radiobutton.set_sensitive(True)
        #gtkgui.on_con_taglie_colori_radiobutton_toggled(gtk.RadioButton())
        gtkgui.codici_a_barre_togglebutton.set_sensitive(True)
        gtkgui.taglie_colori_togglebutton.set_sensitive(False)
        #gtkgui.varianti_taglia_colore_label.set_sensitive(False)
        findComboboxRowFromId(gtkgui.id_gruppo_taglia_customcombobox.combobox, gtkgui.dao.id_gruppo_taglia)
        gtkgui.id_gruppo_taglia_customcombobox.set_property('visible', False)
        gtkgui.denominazione_gruppo_taglia_label.set_markup(
                '<span weight="bold">%s</span>' % (dao.denominazione_gruppo_taglia,))
        gtkgui.denominazione_gruppo_taglia_label.set_property('visible', True)

        findComboboxRowFromId(gtkgui.id_genere_combobox, dao.id_genere)
        gtkgui.id_genere_combobox.set_property('visible', False)
        gtkgui.denominazione_genere_label.set_markup(
                '<span weight="bold">%s</span>' % (dao.genere,))
        gtkgui.denominazione_genere_label.set_property('visible', True)

        findComboboxRowFromId(gtkgui.id_modello_customcombobox.combobox, gtkgui.dao.id_modello)
        gtkgui.id_modello_customcombobox.set_property('visible', False)
        gtkgui.denominazione_modello_label.set_markup(
                '<span weight="bold">%s</span>' % (dao.denominazione_modello,))
        gtkgui.denominazione_modello_label.set_property('visible', True)
        findComboboxRowFromId(gtkgui.id_stagione_combobox, dao.id_stagione)
        gtkgui.id_stagione_combobox.set_property('visible', False)
        gtkgui.denominazione_stagione_anno_label.set_markup(
                '<span weight="bold">%s - %s</span>' % (dao.stagione,dao.anno))
        gtkgui.denominazione_stagione_anno_label.set_property('visible', True)

        findComboboxRowFromId(gtkgui.id_anno_combobox, dao.id_anno)
        gtkgui.id_anno_combobox.set_property('visible', False)
        gtkgui.denominazione_stagione_anno_label.set_markup(
                '<span weight="bold">%s - %s</span>' % (dao.stagione,dao.anno))
        gtkgui.denominazione_stagione_anno_label.set_property('visible', True)

        # possibilita' di variare taglia e colore solo nella misura in cui non ci sia già una variante
        articoliTagliaColore = dao.articoliTagliaColore
        idTaglie = set(a.id_taglia for a in articoliTagliaColore)
        idTaglie.remove(dao.id_taglia)
        fillComboboxTaglie(gtkgui.id_taglia_customcombobox.combobox,
            idGruppoTaglia=dao.id_gruppo_taglia,
            ignore=list(idTaglie))
        findComboboxRowFromId(gtkgui.id_taglia_customcombobox.combobox,
                            dao.id_taglia)
        gtkgui.id_taglia_customcombobox.combobox.set_property('visible', True)
        gtkgui.id_taglia_customcombobox.set_sensitive(True)
        gtkgui.denominazione_taglia_label.set_markup('-')
        gtkgui.denominazione_taglia_label.set_property('visible', False)
        idColori = set(a.id_colore for a in articoliTagliaColore)
        idColori.remove(dao.id_colore)
        fillComboboxColori(gtkgui.id_colore_customcombobox.combobox, ignore=list(idColori))
        findComboboxRowFromId(gtkgui.id_colore_customcombobox.combobox, dao.id_colore)
        gtkgui.id_colore_customcombobox.combobox.set_property('visible', True)
        gtkgui.id_colore_customcombobox.set_sensitive(True)
        gtkgui.denominazione_colore_label.set_markup('-')
        gtkgui.denominazione_colore_label.set_property('visible', False)
        findComboboxRowFromId(gtkgui.id_colore_customcombobox.combobox, dao.id_colore)
        findComboboxRowFromId(gtkgui.id_taglia_customcombobox.combobox, dao.id_taglia)
        gtkgui.id_aliquota_iva_customcombobox.set_sensitive(False)
        gtkgui.denominazione_entry.set_sensitive(True)
        #gtkgui.id_famiglia_articolo_customcombobox.set_sensitive(False)
        #gtkgui.id_categoria_articolo_customcombobox.set_sensitive(False)
        gtkgui.id_unita_base_combobox.set_sensitive(False)
        gtkgui.produttore_comboboxentry.set_sensitive(False)
    elif articleType(dao) == "father":
        """ Articolo principale in quando id_articolo_padre è vuoto
            possibilita' di inserire gruppo taglia, genere, anno, stagione """

        gtkgui.con_taglie_colori_radiobutton.set_sensitive(True)
        gtkgui.on_con_taglie_colori_radiobutton_toggled(gtk.RadioButton())
        varianti = str(len(dao.articoliTagliaColore))
        testo= """ARTICOLO PRINCIPALE CON %s VARIANTI""" %varianti
        gtkgui.memo_wear.set_text(testo)

        findComboboxRowFromId(gtkgui.id_gruppo_taglia_customcombobox.combobox, dao.id_gruppo_taglia)

        findComboboxRowFromId(gtkgui.id_genere_combobox, dao.id_genere)
        gtkgui.id_genere_combobox.set_property('visible', True)

        findComboboxRowFromId(gtkgui.id_modello_customcombobox.combobox, dao.id_modello)
        gtkgui.id_modello_customcombobox.set_property('visible', True)

        findComboboxRowFromId(gtkgui.id_stagione_combobox, dao.id_stagione)
        gtkgui.id_stagione_combobox.set_property('visible', True)

        findComboboxRowFromId(gtkgui.id_anno_combobox, dao.id_anno)
        gtkgui.id_anno_combobox.set_property('visible', True)

        gtkgui.id_taglia_customcombobox.combobox.set_active(-1)
        gtkgui.id_colore_customcombobox.combobox.set_active(-1)

        gtkgui.denominazione_genere_label.set_property('visible', False)
        gtkgui.denominazione_taglia_label.set_property('visible', False)
        gtkgui.denominazione_colore_label.set_property('visible', False)
        gtkgui.denominazione_modello_label.set_property('visible', False)
        gtkgui.denominazione_gruppo_taglia_label.set_property('visible', False)
        gtkgui.denominazione_stagione_anno_label.set_property('visible', False)
        gtkgui.produttore_comboboxentry.set_sensitive(True)


    elif articleType(dao) == "normal":
        gtkgui.normale_radiobutton.set_sensitive(True)
        gtkgui.on_normale_radiobutton_toggled(gtk.RadioButton())
        gtkgui.id_anno_combobox.set_active(-1)
        gtkgui.id_genere_combobox.set_active(-1)
        gtkgui.id_modello_customcombobox.combobox.set_active(-1)
        gtkgui.id_stagione_combobox.set_active(-1)
        gtkgui.id_gruppo_taglia_customcombobox.combobox.set_active(-1)
        gtkgui.id_taglia_customcombobox.combobox.set_active(-1)
        gtkgui.id_colore_customcombobox.combobox.set_active(-1)
        gtkgui.denominazione_genere_label.set_property('visible', False)
        gtkgui.denominazione_taglia_label.set_property('visible', False)
        gtkgui.denominazione_colore_label.set_property('visible', False)
        gtkgui.denominazione_modello_label.set_property('visible', False)
        gtkgui.denominazione_gruppo_taglia_label.set_property('visible', False)
        gtkgui.denominazione_stagione_anno_label.set_property('visible', False)
        gtkgui.memo_wear.set_text("""ARTICOLO NORMALE""")
        print "ARTICOLO SEMPLICE"

    elif articleType(dao) == "plus":
        gtkgui.frame_promowear.set_sensitive(True)
        gtkgui.plus_radiobutton.set_sensitive(True)
        gtkgui.on_plus_radiobutton_toggled(gtk.RadioButton())
        findComboboxRowFromId(gtkgui.id_colore_customcombobox.combobox, dao.id_colore)
        findComboboxRowFromId(gtkgui.id_taglia_customcombobox.combobox, dao.id_taglia)
        findComboboxRowFromId(gtkgui.id_modello_customcombobox.combobox, dao.id_modello)
        findComboboxRowFromId(gtkgui.id_anno_combobox,dao.id_anno)
        findComboboxRowFromId(gtkgui.id_stagione_combobox,dao.id_stagione)
        findComboboxRowFromId(gtkgui.id_genere_combobox,dao.id_genere)
        findComboboxRowFromId(gtkgui.id_gruppo_taglia_customcombobox.combobox,dao.id_gruppo_taglia)
        #gtkgui.denominazione_genere_label.set_markup('-')
        gtkgui.denominazione_genere_label.set_property('visible', False)
        gtkgui.denominazione_taglia_label.set_property('visible', False)
        gtkgui.denominazione_modello_label.set_property('visible', False)
        gtkgui.denominazione_colore_label.set_property('visible', False)
        gtkgui.denominazione_gruppo_taglia_label.set_property('visible', False)
        gtkgui.denominazione_stagione_anno_label.set_property('visible', False)
        gtkgui.memo_wear.set_text("""ARTICOLO PLUS""")
        print "ARTICOLO PLUS"

    elif articleType(dao) == "new":
        gtkgui.normale_radiobutton.set_sensitive(True)
        gtkgui.on_normale_radiobutton_toggled(gtk.RadioButton())
        gtkgui.id_anno_combobox.set_active(-1)
        gtkgui.id_genere_combobox.set_active(-1)
        gtkgui.id_stagione_combobox.set_active(-1)
        gtkgui.id_gruppo_taglia_customcombobox.combobox.set_active(-1)
        gtkgui.id_taglia_customcombobox.combobox.set_active(-1)
        gtkgui.id_modello_customcombobox.combobox.set_active(-1)
        gtkgui.id_colore_customcombobox.combobox.set_active(-1)
        gtkgui.denominazione_genere_label.set_property('visible', False)
        gtkgui.denominazione_taglia_label.set_property('visible', False)
        gtkgui.denominazione_modello_label.set_property('visible', False)
        gtkgui.denominazione_colore_label.set_property('visible', False)
        gtkgui.denominazione_gruppo_taglia_label.set_property('visible', False)
        gtkgui.denominazione_stagione_anno_label.set_property('visible', False)
        gtkgui.memo_wear.set_text("""ARTICOLO NUOVO""")
        print "ARTICOLO NEW"
    else:
        messageError(msg="ATTENZIONE LA TIPOLOGIA DI ARTICOLO NON E' CONTEMPLATA",
                     transient=None)

def clear(anaarti):
    fillComboboxGruppiTaglia(anaarti.id_gruppo_taglia_articolo_filter_combobox, True)
    fillComboboxTaglie(anaarti.id_taglia_articolo_filter_combobox, True)
    fillComboboxColori(anaarti.id_colore_articolo_filter_combobox, True)
    fillComboboxModelli(anaarti.id_modello_filter_combobox, True)
    fillComboboxAnniAbbigliamento(anaarti.id_anno_articolo_filter_combobox, True)
    fillComboboxStagioniAbbigliamento(anaarti.id_stagione_articolo_filter_combobox, True)
    fillComboboxGeneriAbbigliamento(anaarti.id_genere_articolo_filter_combobox, True)
    anaarti.id_modello_filter_combobox.set_active(0)
    anaarti.id_categoria_articolo_filter_combobox.set_active(0)
    anaarti.id_gruppo_taglia_articolo_filter_combobox.set_active(0)
    anaarti.id_taglia_articolo_filter_combobox.set_active(0)
    anaarti.id_colore_articolo_filter_combobox.set_active(0)
    #gestione anno abbigliamento con prelievo del dato di default dal configure
    anaarti.id_anno_articolo_filter_combobox.set_active(0)
    anno = getattr(Environment.conf.PromoWear,'anno_default', None)
    if anno is not None:
        try:
            idAnno = AnnoAbbigliamento().select(denominazione = anno)[0].id
            findComboboxRowFromId(anaarti.id_anno_articolo_filter_combobox, idAnno)
        except:
            pass
    #gestione stagione abbigliamento con prelievo del dato di default dal configure ( nb da usare l'id)
    anaarti.id_stagione_articolo_filter_combobox.set_active(0)
    stagione = getattr(Environment.conf.PromoWear,'stagione_default', 0)
    if stagione:
        findComboboxRowFromId(anaarti.id_stagione_articolo_filter_combobox, int(stagione))
    anaarti.id_genere_articolo_filter_combobox.set_active(0)
    anaarti.taglie_colori_filter_combobox.set_active(0)

def refresh(anaarti):
    padriTagliaColore = ((anaarti.taglie_colori_filter_combobox.get_active() == 0) or
                        (anaarti.taglie_colori_filter_combobox.get_active() == 1))
    if padriTagliaColore:
        padriTagliaColore = None
    else:
        padriTagliaColore = True
    figliTagliaColore = ((anaarti.taglie_colori_filter_combobox.get_active() == 0) or
                            (anaarti.taglie_colori_filter_combobox.get_active() == 2))
    if figliTagliaColore:
        figliTagliaColore = None
    else:
        figliTagliaColore = True
    idGruppoTaglia = findIdFromCombobox(anaarti.id_gruppo_taglia_articolo_filter_combobox)
    idModello = findIdFromCombobox(anaarti.id_modello_filter_combobox)
    idTaglia = findIdFromCombobox(anaarti.id_taglia_articolo_filter_combobox)
    idColore = findIdFromCombobox(anaarti.id_colore_articolo_filter_combobox)
    idAnno = findIdFromCombobox(anaarti.id_anno_articolo_filter_combobox)
    idStagione = findIdFromCombobox(anaarti.id_stagione_articolo_filter_combobox)
    idGenere = findIdFromCombobox(anaarti.id_genere_articolo_filter_combobox)
    anaarti.filterDict.update(idGruppoTaglia=idGruppoTaglia,
                            idTaglia=idTaglia,
                            idColore=idColore,
                            idAnno=idAnno,
                            idStagione=idStagione,
                            idGenere=idGenere,
                            idModello=idModello,
                            padriTagliaColore=padriTagliaColore,
                            figliTagliaColore=figliTagliaColore)

def on_taglie_colori_filter_combobox_changed(anaarti, combobox):
    selected = anaarti.taglie_colori_filter_combobox.get_active()
    if selected == 1:
        # solo principali
        anaarti.id_taglia_articolo_filter_combo.set_active(0)
        anaarti.id_taglia_articolo_filter_combo.set_sensitive(False)
        anaarti.id_colore_articolo_filter_combobox.set_active(0)
        anaarti.id_colore_articolo_filter_combobox.set_sensitive(False)
    else:
        anaarti.id_taglia_articolo_filter_combo.set_sensitive(True)
        anaarti.id_colore_articolo_filter_combobox.set_sensitive(True)
