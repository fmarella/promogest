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

from promogest.ui.RicercaComplessa import parseModel, onColumnEdited, columnSelectAll
from promogest.modules.PromoWear.dao.Colore import Colore
from promogest.modules.PromoWear.dao.Taglia import Taglia
from promogest.modules.PromoWear.dao.ArticoloTagliaColore import ArticoloTagliaColore
from promogest.modules.PromoWear.dao.AnnoAbbigliamento import AnnoAbbigliamento
from promogest.modules.PromoWear.dao.StagioneAbbigliamento import StagioneAbbigliamento
from promogest.modules.PromoWear.dao.GenereAbbigliamento import GenereAbbigliamento
from promogest.modules.PromoWear.dao.GruppoTaglia import GruppoTaglia
from promogest.modules.PromoWear.ui.PromowearUtils import *

def drawPromoWearPart(anaarti, renderer):

    treeview = anaarti.filter.resultsElement
    renderer = gtk.CellRendererText()


    column = gtk.TreeViewColumn('Gruppo taglia', renderer, text=9, background=1)
    column.set_sizing(GTK_COLUMN_GROWN_ONLY)
    column.set_clickable(False)
    column.connect("clicked", anaarti.filter._changeOrderBy, (GruppoTaglia, GruppoTaglia.denominazione))
    column.set_resizable(True)
    column.set_expand(False)
    column.set_min_width(100)
    treeview.append_column(column)

    column = gtk.TreeViewColumn('Taglia', renderer, text=10, background=1)
    column.set_sizing(GTK_COLUMN_GROWN_ONLY)
    column.set_clickable(False)
    column.connect("clicked", anaarti.filter._changeOrderBy, (Taglia, Taglia.denominazione))
    column.set_resizable(True)
    column.set_expand(False)
    column.set_min_width(100)
    treeview.append_column(column)

    column = gtk.TreeViewColumn('Colore', renderer, text=11, background=1)
    column.set_sizing(GTK_COLUMN_GROWN_ONLY)
    column.set_clickable(False)
    column.connect("clicked", anaarti.filter._changeOrderBy, (Colore, Colore.denominazione))
    column.set_resizable(True)
    column.set_expand(False)
    column.set_min_width(100)
    treeview.append_column(column)

    column = gtk.TreeViewColumn('Anno', renderer, text=12, background=1)
    column.set_sizing(GTK_COLUMN_GROWN_ONLY)
    column.set_clickable(False)
    column.connect("clicked", anaarti.filter._changeOrderBy, (AnnoAbbigliamento,AnnoAbbigliamento.denominazione))
    column.set_resizable(True)
    column.set_expand(False)
    column.set_min_width(100)
    treeview.append_column(column)

    column = gtk.TreeViewColumn('Stagione', renderer, text=13, background=1)
    column.set_sizing(GTK_COLUMN_GROWN_ONLY)
    column.set_clickable(False)
    column.connect("clicked", anaarti.filter._changeOrderBy, (StagioneAbbigliamento,StagioneAbbigliamento.denominazione))
    column.set_resizable(True)
    column.set_expand(False)
    column.set_min_width(100)
    treeview.append_column(column)

    column = gtk.TreeViewColumn('Genere', renderer, text=14, background=1)
    column.set_sizing(GTK_COLUMN_GROWN_ONLY)
    column.set_clickable(False)
    column.connect("clicked", anaarti.filter._changeOrderBy, (None, "genere"))
    column.set_resizable(True)
    column.set_expand(False)
    column.set_min_width(100)
    treeview.append_column(column)
    model = gtk.ListStore(object, str, str, str, str, str, str, str, str, str, str, str, str, str, str)
    return model

def drawRicercaSemplicePromoWearPart(anaarti):
    anaarti.filter_promowear.set_property('visible', True)
    fillComboboxGruppiTaglia(anaarti.id_gruppo_taglia_articolo_filter_combobox, True)
    fillComboboxTaglie(anaarti.id_taglia_articolo_filter_combobox, True)
    fillComboboxColori(anaarti.id_colore_articolo_filter_combobox, True)
    fillComboboxAnniAbbigliamento(anaarti.id_anno_articolo_filter_combobox, True)
    fillComboboxStagioniAbbigliamento(anaarti.id_stagione_articolo_filter_combobox, True)
    fillComboboxModelli(anaarti.id_modello_filter_combobox, True)
    fillComboboxGeneriAbbigliamento(anaarti.id_genere_articolo_filter_combobox, True)
    if anaarti._idGruppoTaglia is not None:
        findComboboxRowFromId(anaarti.id_gruppo_taglia_articolo_filter_combobox, anaarti._idGruppoTaglia)
    anaarti.id_taglia_articolo_filter_combobox.set_active(0)
    if anaarti._idTaglia is not None:
        findComboboxRowFromId(anaarti.id_taglia_articolo_filter_combobox, anaarti._idTaglia)
    anaarti.id_colore_articolo_filter_combobox.set_active(0)
    if anaarti._idColore is not None:
        findComboboxRowFromId(anaarti.id_colore_articolo_filter_combobox, anaarti._idColore)
    anaarti.id_anno_articolo_filter_combobox.set_active(0)
    anaarti.id_anno_articolo_filter_combobox.set_active(0)
    try:
        anno = getattr(Environment.conf.PromoWear,'anno_default', None)
    except:
        anno = None

    if anno is not None:
        try:
            idAnno = AnnoAbbigliamento().select(denominazione = anno)[0].id
            findComboboxRowFromId(anaarti.id_anno_articolo_filter_combobox, idAnno)
        except:
            pass
    #gestione stagione abbigliamento con prelievo del dato di default dal configure ( nb da usare l'id)
    anaarti.id_stagione_articolo_filter_combobox.set_active(0)
    try:
        stagione = getattr(Environment.conf.PromoWear,'stagione_default', None)
    except:
        stagione =None
    if stagione is not "" and stagione is not None:
        findComboboxRowFromId(anaarti.id_stagione_articolo_filter_combobox, int(stagione))
    anaarti.id_genere_articolo_filter_combobox.set_active(0)
    if anaarti._idGenere is not None:
        findComboboxRowFromId(anaarti.id_colore_articolo_filter_combobox, anaarti._idGenere)
    anaarti.taglie_colori_filter_combobox.set_active(0)
    anaarti.id_stato_articolo_filter_combobox.set_active(0)
    anaarti.id_modello_filter_combobox.set_active(0)


def drawRicercaComplessaPromoWearPart(anaarti):
    drawGruppoTagliaTreeView(anaarti)
    drawTagliaTreeView(anaarti)
    drawColoreTreeView(anaarti)
    drawAnnoTreeView(anaarti)
    drawStagioneTreeView(anaarti)
    drawGenereTreeView(anaarti)
    drawCutSizeTreeView(anaarti)


def drawGruppoTagliaTreeView(anaarti):
    treeview = anaarti.gruppo_taglia_articolo_filter_treeview
    treeview.selectAllIncluded = False
    treeview.selectAllExcluded = False
    model = gtk.ListStore(bool, bool, int, str, str)
    anaarti._gruppoTagliaTreeViewModel = model

    for c in treeview.get_columns():
        treeview.remove_column(c)

    renderer = gtk.CellRendererToggle()
    renderer.set_property('activatable', True)
    renderer.connect('toggled', anaarti.onColumnEdited, None, treeview)
    #GTK3
    renderer.model_index = 0
    renderer.column = 1
    column = gtk.TreeViewColumn('Includi', renderer, active=0)
    column.connect("clicked", anaarti.columnSelectAll, treeview)
    column.set_sizing(GTK_COLUMN_GROWN_ONLY)
    column.set_clickable(True)
    column.set_resizable(True)
    column.set_expand(False)
    treeview.append_column(column)

    renderer = gtk.CellRendererText()
    column = gtk.TreeViewColumn('Descrizione breve', renderer, text=3)
    column.set_sizing(GTK_COLUMN_GROWN_ONLY)
    column.set_clickable(False)
    column.set_resizable(True)
    column.set_expand(False)
    treeview.append_column(column)

    renderer = gtk.CellRendererText()
    column = gtk.TreeViewColumn('Descrizione', renderer, text=4)
    column.set_sizing(GTK_COLUMN_GROWN_ONLY)
    column.set_clickable(False)
    column.set_resizable(True)
    column.set_expand(True)
    treeview.append_column(column)

    treeview.set_search_column(4)

    grts = GruppoTaglia().select(offset=None, batchSize=None)


    for g in grts:
        included = excluded = False
        if anaarti._idGruppoTaglia is not None:
            included = anaarti._idGruppoTaglia == g.id

        model.append((included,
                        excluded,
                        g.id,
                        g.denominazione_breve,
                        g.denominazione))

    treeview.set_model(model)


def drawTagliaTreeView(anaarti):
    treeview = anaarti.taglia_articolo_filter_treeview
    treeview.selectAllIncluded = False
    treeview.selectAllExcluded = False
    model = gtk.ListStore(bool, bool, int, str, str)
    anaarti._tagliaTreeViewModel = model

    for c in treeview.get_columns():
        treeview.remove_column(c)

    renderer = gtk.CellRendererToggle()
    renderer.set_property('activatable', True)
    renderer.connect('toggled', anaarti.onColumnEdited, None, treeview)
    renderer.model_index = 0
    renderer.column = 1
    column = gtk.TreeViewColumn('Includi', renderer, active=0)
    column.connect("clicked", anaarti.columnSelectAll, treeview)
    column.set_sizing(GTK_COLUMN_GROWN_ONLY)
    column.set_clickable(True)
    column.set_resizable(True)
    column.set_expand(False)
    treeview.append_column(column)

    renderer = gtk.CellRendererText()
    column = gtk.TreeViewColumn('Descrizione breve', renderer, text=3)
    column.set_sizing(GTK_COLUMN_GROWN_ONLY)
    column.set_clickable(False)
    column.set_resizable(True)
    column.set_expand(False)
    treeview.append_column(column)

    renderer = gtk.CellRendererText()
    column = gtk.TreeViewColumn('Descrizione', renderer, text=4)
    column.set_sizing(GTK_COLUMN_GROWN_ONLY)
    column.set_clickable(False)
    column.set_resizable(True)
    column.set_expand(True)
    treeview.append_column(column)

    treeview.set_search_column(4)

    tags = Taglia().select(offset=None, batchSize=None)

    for t in tags:
        included = excluded = False
        if anaarti._idTaglia is not None:
            included = anaarti._idTaglia == t.id

        model.append((included,
                        excluded,
                        t.id,
                        t.denominazione_breve,
                        t.denominazione))

    treeview.set_model(model)


def drawColoreTreeView(anaarti):
    treeview = anaarti.colore_articolo_filter_treeview
    treeview.selectAllIncluded = False
    treeview.selectAllExcluded = False
    model = gtk.ListStore(bool, bool, int, str, str)
    anaarti._coloreTreeViewModel = model

    for c in treeview.get_columns():
        treeview.remove_column(c)

    renderer = gtk.CellRendererToggle()
    renderer.set_property('activatable', True)
    renderer.connect('toggled', anaarti.onColumnEdited, None, treeview)
    renderer.model_index = 0
    renderer.column = 1
    column = gtk.TreeViewColumn('Includi', renderer, active=0)
    column.connect("clicked", anaarti.columnSelectAll, treeview)
    column.set_sizing(GTK_COLUMN_GROWN_ONLY)
    column.set_clickable(True)
    column.set_resizable(True)
    column.set_expand(False)
    treeview.append_column(column)

    renderer = gtk.CellRendererText()
    column = gtk.TreeViewColumn('Descrizione breve', renderer, text=3)
    column.set_sizing(GTK_COLUMN_GROWN_ONLY)
    column.set_clickable(False)
    column.set_resizable(True)
    column.set_expand(False)
    treeview.append_column(column)

    renderer = gtk.CellRendererText()
    column = gtk.TreeViewColumn('Descrizione', renderer, text=4)
    column.set_sizing(GTK_COLUMN_GROWN_ONLY)
    column.set_clickable(False)
    column.set_resizable(True)
    column.set_expand(True)
    treeview.append_column(column)

    treeview.set_search_column(4)

    cols = Colore().select(offset=None, batchSize=None)


    for c in cols:
        included = excluded = False
        if anaarti._idColore is not None:
            included = anaarti._idColore == c.id

        model.append((included,
                        excluded,
                        c.id,
                        c.denominazione_breve,
                        c.denominazione))

    treeview.set_model(model)


def drawAnnoTreeView(anaarti):
    treeview = anaarti.anno_articolo_filter_treeview
    treeview.selectAllIncluded = False
    treeview.selectAllExcluded = False
    model = gtk.ListStore(bool, bool, int, str)
    anaarti._annoTreeViewModel = model

    for c in treeview.get_columns():
        treeview.remove_column(c)

    renderer = gtk.CellRendererToggle()
    renderer.set_property('activatable', True)
    renderer.connect('toggled', anaarti.onColumnEdited, None, treeview)
    renderer.model_index = 0
    renderer.column = 1
    column = gtk.TreeViewColumn('Includi', renderer, active=0)
    column.connect("clicked", anaarti.columnSelectAll, treeview)
    column.set_sizing(GTK_COLUMN_GROWN_ONLY)
    column.set_clickable(True)
    column.set_resizable(True)
    column.set_expand(False)
    treeview.append_column(column)

    renderer = gtk.CellRendererText()
    column = gtk.TreeViewColumn('Descrizione', renderer, text=3)
    column.set_sizing(GTK_COLUMN_GROWN_ONLY)
    column.set_clickable(False)
    column.set_resizable(True)
    column.set_expand(True)
    treeview.append_column(column)

    treeview.set_search_column(3)

    anno = anaarti._idAnno
    if hasattr(Environment.conf.PromoWear,'TaglieColori'):
        default = getattr(Environment.conf.PromoWear.TaglieColori,'anno_default', None)
        if default is not None:
            anno = int(default)


    anns = AnnoAbbigliamento().select(offset=None, batchSize=None)
    for a in anns:
        included = excluded = False
        if anno is not None:
            included = anno == a['id']

        model.append((included,
                        excluded,
                        a.id,
                        a.denominazione))

    treeview.set_model(model)

def drawCutSizeTreeView(anaarti):
    treeview = anaarti.cutsize_articolo_filter_treeview
    treeview.selectAllIncluded = False
    treeview.selectAllExcluded = False
    model = gtk.ListStore(bool, bool, str)
    anaarti._cutisizeTreeViewModel = model

    for c in treeview.get_columns():
        treeview.remove_column(c)

    renderer = gtk.CellRendererToggle()
    renderer.set_property('activatable', True)
    renderer.connect('toggled', anaarti.onColumnEdited, None, treeview)
    renderer.model_index = 0
    renderer.column = 1
    column = gtk.TreeViewColumn('Includi', renderer, active=0)
    column.connect("clicked", anaarti.columnSelectAll, treeview)
    column.set_sizing(GTK_COLUMN_GROWN_ONLY)
    column.set_clickable(True)
    column.set_resizable(True)
    column.set_expand(False)
    treeview.append_column(column)

    renderer = gtk.CellRendererText()
    column = gtk.TreeViewColumn('Descrizione', renderer, text=2)
    column.set_sizing(GTK_COLUMN_GROWN_ONLY)
    column.set_clickable(False)
    column.set_resizable(True)
    column.set_expand(True)
    treeview.append_column(column)

    treeview.set_search_column(2)

    stas = [(True,False,"Tutti"),(False,True,"Solo principali"), (False,True,"Solo Varianti")]

    for s in stas:
        model.append((s[0],
                        s[1],
                        s[2]))

    treeview.set_model(model)


def drawStagioneTreeView(anaarti):
    treeview = anaarti.stagione_articolo_filter_treeview
    treeview.selectAllIncluded = False
    treeview.selectAllExcluded = False
    model = gtk.ListStore(bool, bool, int, str)
    anaarti._stagioneTreeViewModel = model

    for c in treeview.get_columns():
        treeview.remove_column(c)

    renderer = gtk.CellRendererToggle()
    renderer.set_property('activatable', True)
    renderer.connect('toggled', anaarti.onColumnEdited, None, treeview)
    renderer.model_index = 0
    renderer.column = 1
    column = gtk.TreeViewColumn('Includi', renderer, active=0)
    column.connect("clicked", anaarti.columnSelectAll, treeview)
    column.set_sizing(GTK_COLUMN_GROWN_ONLY)
    column.set_clickable(True)
    column.set_resizable(True)
    column.set_expand(False)
    treeview.append_column(column)

    renderer = gtk.CellRendererText()
    column = gtk.TreeViewColumn('Descrizione', renderer, text=3)
    column.set_sizing(GTK_COLUMN_GROWN_ONLY)
    column.set_clickable(False)
    column.set_resizable(True)
    column.set_expand(True)
    treeview.append_column(column)

    treeview.set_search_column(3)

    stagione = anaarti._idStagione
    if hasattr(Environment.conf,'TaglieColori'):
        default = getattr(Environment.conf.TaglieColori,'stagione_default', None)
        if default is not None:
            stagione = int(default)

    stas = StagioneAbbigliamento().select(offset=None, batchSize=None)

    for s in stas:
        included = excluded = False
        if stagione is not None:
            included = stagione == s['id']

        model.append((included,
                        excluded,
                        s.id,
                        s.denominazione))

    treeview.set_model(model)


def drawGenereTreeView(anaarti):
    treeview = anaarti.genere_articolo_filter_treeview
    treeview.selectAllIncluded = False
    treeview.selectAllExcluded = False
    model = gtk.ListStore(bool, bool, int, str)
    anaarti._genereTreeViewModel = model

    for c in treeview.get_columns():
        treeview.remove_column(c)

    renderer = gtk.CellRendererToggle()
    renderer.set_property('activatable', True)
    renderer.connect('toggled', anaarti.onColumnEdited, None, treeview)
    renderer.model_index = 0
    renderer.column = 1
    column = gtk.TreeViewColumn('Includi', renderer, active=0)
    column.connect("clicked", anaarti.columnSelectAll, treeview)
    column.set_sizing(GTK_COLUMN_GROWN_ONLY)
    column.set_clickable(True)
    column.set_resizable(True)
    column.set_expand(False)
    treeview.append_column(column)

    renderer = gtk.CellRendererText()
    column = gtk.TreeViewColumn('Descrizione', renderer, text=3)
    column.set_sizing(GTK_COLUMN_GROWN_ONLY)
    column.set_clickable(False)
    column.set_resizable(True)
    column.set_expand(True)
    treeview.append_column(column)

    treeview.set_search_column(3)

    gens = GenereAbbigliamento().select(offset=None, batchSize=None)

    for g in gens:
        included = excluded = False
        if anaarti._idGenere is not None:
            included = anaarti._idGenere == g['id']

        model.append((included,
                        excluded,
                        g.id,
                        g.denominazione))

    treeview.set_model(model)

def collapseAllExpandersPromoWearPart(anaarti):
    anaarti.gruppo_taglia_articolo_filter_expander.set_expanded(False)
    anaarti.taglia_articolo_filter_expander.set_expanded(False)
    anaarti.colore_articolo_filter_expander.set_expanded(False)
    anaarti.anno_articolo_filter_expander.set_expanded(False)
    anaarti.stagione_articolo_filter_expander.set_expanded(False)
    anaarti.genere_articolo_filter_expander.set_expanded(False)

def setRiepilogoArticoloPromoWearPart(anaarti):

    def buildIncludedString(row, index):
        if row[0]:
            anaarti._includedString += '     + ' + row[index] + '\n'

    def buildExcludedString(row, index):
        if row[1]:
            anaarti._excludedString += '     - ' + row[index] + '\n'

    model = anaarti._gruppoTagliaTreeViewModel
    anaarti._includedString = ''
    parseModel(model, buildIncludedString, 4)
    if anaarti._includedString != '':
        testo += '  Gruppo taglia:\n'
        testo += anaarti._includedString

    model = anaarti._tagliaTreeViewModel
    anaarti._includedString = ''
    parseModel(model, buildIncludedString, 4)
    if anaarti._includedString != '':
        testo += '  Taglia:\n'
        testo += anaarti._includedString

    model = anaarti._coloreTreeViewModel
    anaarti._includedString = ''
    parseModel(model, buildIncludedString, 4)
    if anaarti._includedString != '':
        testo += '  Colore:\n'
        testo += anaarti._includedString

    model = anaarti._annoTreeViewModel
    anaarti._includedString = ''
    parseModel(model, buildIncludedString, 3)
    if anaarti._includedString != '':
        testo += '  Anno:\n'
        testo += anaarti._includedString

    model = anaarti._stagioneTreeViewModel
    anaarti._includedString = ''
    parseModel(model, buildIncludedString, 3)
    if anaarti._includedString != '':
        testo += '  Stagione:\n'
        testo += anaarti._includedString

    model = anaarti._genereTreeViewModel
    anaarti._includedString = ''
    parseModel(model, buildIncludedString, 3)
    if anaarti._includedString != '':
        testo += '  Genere:\n'
        testo += anaarti._includedString

def refreshPromoWearPart(anaarti):
    if anaarti._tipoRicerca == 'semplice':
        idGruppoTaglia = findIdFromCombobox(anaarti.id_gruppo_taglia_articolo_filter_combobox)
        idTaglia = findIdFromCombobox(anaarti.id_taglia_articolo_filter_combobox)
        idColore = findIdFromCombobox(anaarti.id_colore_articolo_filter_combobox)
        idAnno = findIdFromCombobox(anaarti.id_anno_articolo_filter_combobox)
        idStagione = findIdFromCombobox(anaarti.id_stagione_articolo_filter_combobox)
        idModello = findIdFromCombobox(anaarti.id_modello_filter_combobox)
        idGenere = findIdFromCombobox(anaarti.id_genere_articolo_filter_combobox)
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
    elif anaarti._tipoRicerca == 'avanzata':
        idGruppoTaglia = None
        idTaglia = None
        idColore = None
        idAnno = None
        idStagione = None
        idModello = None
        idGenere = None
        padriTagliaColore = None
        figliTagliaColore = None

    if idGruppoTaglia:
        anaarti.filterDict.update(idGruppoTaglia=idGruppoTaglia)
    if idTaglia:
        anaarti.filterDict.update(idTaglia=idTaglia)
    if idColore:
        anaarti.filterDict.update(idColore=idColore)
    if idAnno:
        anaarti.filterDict.update(idAnno=idAnno)
    if idModello:
        anaarti.filterDict.update(idModello=idModello)
    if idStagione:
        anaarti.filterDict.update(idStagione=idStagione)
    if idGenere:
        anaarti.filterDict.update(idGenere=idGenere)
    if padriTagliaColore:
        anaarti.filterDict.update(padriTagliaColore=padriTagliaColore)
    if figliTagliaColore:
        anaarti.filterDict.update(figliTagliaColore=figliTagliaColore)


def preparePromoWearPart(anaarti):
    anaarti._idGruppiTagliaIn = []
    anaarti._idTaglieIn = []
    anaarti._idColoriIn = []
    anaarti._idAnniIn = []
    anaarti._idStagioniIn = []
    anaarti._idGeneriIn = []
    anaarti._idCutSizeIn = []
    anaarti._principaliIn = None
    anaarti._variantiIn = None
    anaarti._normaliIn = None

    def getGruppiTagliaIn(row, index):
        if row[0]:
            anaarti._idGruppiTagliaIn.append(row[index])

    def getTaglieIn(row, index):
        if row[0]:
            anaarti._idTaglieIn.append(row[index])

    def getColoriIn(row, index):
        if row[0]:
            anaarti._idColoriIn.append(row[index])

    def getAnniIn(row, index):
        if row[0]:
            anaarti._idAnniIn.append(row[index])

    def getStagioniIn(row, index):
        if row[0]:
            anaarti._idStagioniIn.append(row[index])

    def getGeneriIn(row, index):
        if row[0]:
            anaarti._idGeneriIn.append(row[index])

    def getCutSizeIn(row, index):
        if row[0]:
            anaarti._idCutSizeIn.append(row[index])

    parseModel(anaarti._gruppoTagliaTreeViewModel, getGruppiTagliaIn, 2)
    parseModel(anaarti._tagliaTreeViewModel, getTaglieIn, 2)
    parseModel(anaarti._coloreTreeViewModel, getColoriIn, 2)
    parseModel(anaarti._annoTreeViewModel, getAnniIn, 2)
    parseModel(anaarti._stagioneTreeViewModel, getStagioniIn, 2)
    parseModel(anaarti._genereTreeViewModel, getGeneriIn, 2)
    parseModel(anaarti._cutisizeTreeViewModel, getCutSizeIn, 2)
