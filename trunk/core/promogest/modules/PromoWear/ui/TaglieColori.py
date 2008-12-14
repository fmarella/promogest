# -*- coding: utf-8 -*-

# Promogest
#
# Copyright (C) 2005 by Promotux Informatica - http://www.promotux.it/
# Author: Andrea Argiolas <andrea@promotux.it>
# Author: Francesco Meloni <francesco@promotux.it>

import gtk
import gobject, gtkhtml2

from promogest.ui.GladeWidget import GladeWidget

from promogest import Environment
from promogest.dao.Dao import Dao
from promogest.modules.PromoWear.dao.ArticoloPromowear import Articolo
from promogest.modules.PromoWear.dao.ArticoloTagliaColore import ArticoloTagliaColore
from promogest.modules.PromoWear.dao.GruppoTaglia import GruppoTaglia
from promogest.modules.PromoWear.dao.GruppoTagliaTaglia import GruppoTagliaTaglia
from promogest.modules.PromoWear.dao.Taglia import Taglia
from promogest.modules.PromoWear.dao.Colore import Colore
from promogest.dao.CodiceABarreArticolo import CodiceABarreArticolo
import genshi
from genshi.template import TemplateLoader
from promogest.ui.utils import *


templates_dir = './promogest/modules/PromoWear/templates/'
loader = TemplateLoader([templates_dir])

class GestioneTaglieColori(GladeWidget):

    def __init__(self, articolo):
        GladeWidget.__init__(self, 'creazione_taglie_colore',
                            './promogest/modules/PromoWear/gui/creazione_varianti_taglia_colore.glade', isModule=True)

        #dialog = self.creazione_taglie_colore
        #self.placeWindow(self.getTopLevel())
        self._treeViewModel = None
        self._articoloBase = articolo
        self._articoloPadre = articolo.articoloTagliaColore
        self.idGruppoTaglia = self._articoloBase.id_gruppo_taglia
        if self._articoloPadre is None:
            self._articoloPadre = ArticoloTagliaColore()
        self._articoliTagliaColore = self._articoloBase.articoliTagliaColore
        self._noValue = 'n/a'
        self._varianti = {}
        self._gruppoTaglia = None
        self._gtkHtml = None
        self.order="color"
        self.filtered = True
        # Taglie attualmente presenti nella treeview
        self._taglie = [] # Verra` aggiornato al refresh della combobox gruppi taglia

        # Colori attualmente presenti nella treeview
        #colori = set(a.id_colore for a in self._articoliTagliaColore)
        #self._colori = [Colore().getRecord(id= c) for c in colori]
        self.colori = Colore().select(batchSize=None)
        self.sizes = self.sizesAvailable()
        self.selected = False
        ## Dizionario che associa alla chiave (taglia,colore) l'id della variante
        #for a in self._articoliTagliaColore:
            #self._varianti[(a.id_taglia, a.id_colore)] = a.id_articolo

        #self._ripetizione_taglie = 3 # Ogni quante colonne ripetere le taglie?
        self.group_size_label.set_markup('<span weight="bold">%s</span>'
                                       % (self._articoloBase.denominazione_gruppo_taglia,))

        self.father_label.set_markup('Articolo: '
                                       + '<span weight="bold">%s</span>'
                                       % (self._articoloBase.denominazione,))

        #self._drawColoriTreeView()
        #self.refreshColoriTreeView()
        #self.refreshTaglie()
        self._refreshHtml()
        self.draw()

    def sizesAvailable(self):
        idtaglie = GruppoTagliaTaglia().select(idGruppoTaglia=self.idGruppoTaglia, batchSize=None)
        return idtaglie

    def _refreshHtml(self, data= None):
        """ show the html page in the custom widget"""
        if self._gtkHtml is None:
            self._gtkHtml = self.getHtmlWidget()
            # A bit of double buffering here
            #self._gtkHtmlDocuments = (gtkhtml2.Document(),
                                      #gtkhtml2.Document())
            #for doc in self._gtkHtmlDocuments:
                #doc.connect('request_url', self.on_html_request_url)
                #doc.connect('link_clicked', self.on_html_link_clicked)

            self._currGtkHtmlDocument = 0
        document =gtkhtml2.Document()
        document.open_stream('text/html')
        if data is None:
            html = '<html></html>'
        else:
            tmpl = loader.load("creazione_taglie_colori.html")
            stream = tmpl.generate(datas=data)
            html = stream.render('xhtml')
        document.write_stream(html)
        document.close_stream()
        self._gtkHtml.set_document(document)
            ##self._refresh(html)


    def getHtmlWidget(self):
        return self.creazione_varianti_html

    def draw(self):
        """Creo una treeview che abbia come colonne i colori e come righe
           le taglie direi che sia il caso di gestire anche le descrizioni variante visto che le ho
        """
        self.treeview = self.color_and_size_treeview
        cellspin = gtk.CellRendererToggle()
        cellspin.set_property('activatable', True)
        cellspin.connect('toggled', self.on_column_selected_edited, self.treeview, True)
        column = gtk.TreeViewColumn('Seleziona', cellspin)
        column.add_attribute( cellspin, "active", 1)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_resizable(True)
        #column.set_expand(True)
        #column.set_min_width(40)
        self.treeview.append_column(column)

        rendererSx = gtk.CellRendererText()
        column = gtk.TreeViewColumn("Taglia / Colore", rendererSx, text=2)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(False)
        column.set_resizable(True)
        #column.set_expand(False)
        column.set_min_width(40)
        self.treeview.append_column(column)

        celltext = gtk.CellRendererText()
        celltext.set_property("editable", True)
        celltext.set_property("visible", True)
        celltext.connect('edited', self.on_column_codice_edited, self.treeview, True)
        column = gtk.TreeViewColumn('Codice', celltext, text=3)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        #column.set_clickable(True)
        #column.connect("clicked", self._changeOrderBy, 'denominazione_breve')
        column.set_resizable(True)
        column.set_expand(True)
        column.set_min_width(50)
        self.treeview.append_column(column)

        self._treeViewModel = gtk.TreeStore(object,bool,str,str)
        self.treeview.set_model(self._treeViewModel)
        self.head_color.set_active(True)
        self.only_variation.set_active(True)
        self.refresh()

    def refresh(self,order="color",filtered =True):
        # Aggiornamento TreeView
        self._treeViewModel.clear()
        #varianti = self.data["varianti"]
        #print varianti

        if self.order == "color":
            if self.filtered:
                for c in self._articoloBase.colori:
                    parent = self._treeViewModel.append(None,(c,
                                                self.selected,
                                                c.denominazione,
                                                ""))
                    sizesFilterd= ArticoloTagliaColore().select(idArticoloPadre =self._articoloBase.id,
                                                                idColore=c.id, batchSize=None)
                    for s in sizesFilterd:
                        self._treeViewModel.append(parent,(s,
                                            self.selected,
                                            s.denominazione_taglia,
                                            ""))
            else:
                for c in self.colori:
                    parent = self._treeViewModel.append(None,(c,
                                                self.selected,
                                                c.denominazione,
                                                ""))
                    for s in self.sizes:
                        self._treeViewModel.append(parent,(s,
                                                self.selected,
                                                s.denominazione_taglia,
                                                ""))
        else:
            if self.filtered:
                for s in self._articoloBase.taglie:
                    parent = self._treeViewModel.append(None,(s,
                                                            self.selected,
                                                            s.denominazione,
                                                            ""))
                    colorFilterd= ArticoloTagliaColore().select(idArticoloPadre =self._articoloBase.id,
                                                                idTaglia=s.id, batchSize=None)
                    for c in colorFilterd:
                        self._treeViewModel.append(parent,(c,
                                                    self.selected,
                                                    c.denominazione_colore,
                                                    ""))

            else:
                for s in self.sizes:
                    parent = self._treeViewModel.append(None,(s,
                                                            self.selected,
                                                            s.denominazione_taglia,
                                                            ""))
                    for c in self.colori:
                        self._treeViewModel.append(parent,(c,
                                                    self.selected,
                                                    c.denominazione,
                                                    ""))
        self.printModel()

    def printModel(self):
        #model = self.treeview.get_model()
        self.datas= []
        self._treeViewModel.foreach(self.selectFilter )
        #print "FGFGGGGGGGGGGGG", model.get_path((0,0))

    def selectFilter(self, model, path, iter):

        #Seleziona elementi che concordano con il filtro
        check = model.get_value(iter, 1)
        if check:
            c = model.get_value(iter, 0)
            d = model.get_value(iter, 3)
            self.datas.append((c,d))
            #print "CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC",c, d
        #print "DATAAAAAAAAAAAAAAAAAAA", self.datas
        #self._refreshHtml(data=self.datas)

    def on_column_selected_edited(self, cell, path, treeview,value, editNext=True):
        """ Function ti set the value quantita edit in the cell"""
        model = treeview.get_model()
        #treeiter = model.get_iter(path)
        #fffff = model.get_path(treeiter)
        model[path][1] = not model[path][1]
        for a in  model[path].iterchildren():
             a[1] = not a[1]
        self.printModel()

    def on_column_codice_edited(self, cell, path, value, treeview, editNext=True):
        """ Function ti set the value quantita edit in the cell"""
        model = treeview.get_model()
        model[path][3] = value
        self.printModel()

    def on_head_color_toggled(self, radioButton):
        if self.head_color.get_active():
            self.order="color"
        elif self.head_size.get_active():
            self.order="size"
        self.refresh(order=self.order)

    def on_only_variation_toggled(self, radioButton):
        if self.only_variation.get_active():
            self.filtered= True
        elif self.all_variation.get_active():
            self.filtered= False
        self.refresh(filtered=self.filtered)







































    def refreshTaglie(self):
        # identificazione taglie associate al gruppo taglia selezionato
        id = self._articoloPadre.id_gruppo_taglia

        gruppo = None
        if id is None:
            id = 1 # Nessuna taglia
        gruppo = GruppoTaglia().getRecord(id=id)

        self.gruppo_taglia_label.set_markup('<span weight="bold">%s</span>'
                                            % (gruppo.denominazione,))

        self._gruppoTaglia = gruppo
        self._taglie = gruppo.taglie
        self.refreshTaglieColoriTreeView()

    def _drawColoriTreeView(self):
        # disegno della treeview per la selezione dei colori
        treeview = self.colori_treeview

        renderer = gtk.CellRendererToggle()
        renderer.set_property('activatable', True)
        renderer.connect('toggled', self.on_colori_cell_edited)
        renderer.set_data('column', 0)
        column = gtk.TreeViewColumn('Seleziona', renderer, active=1)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(False)
        column.set_resizable(False)
        column.set_expand(False)
        column.set_min_width(50)
        treeview.append_column(column)

        renderer = gtk.CellRendererText()
        renderer.set_property('editable', False)
        column = gtk.TreeViewColumn('Colore', renderer, text=2, background = 3)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(False)
        column.set_resizable(True)
        column.set_expand(True)
        column.set_min_width(100)
        treeview.append_column(column)

        model = gtk.ListStore(object, bool, str, str)
        treeview.set_model(model)
        treeview.set_search_column(2)

    def on_colori_cell_edited(self, cell, path):
        # selezione / deselezione dei colori
        model = self.colori_treeview.get_model()
        iterator = model.get_iter(path)
        column = 1
        model.set_value(iterator, column, not cell.get_active())

    def refreshColoriTreeView(self):
        # Crea l'elenco dei colori, evidenziando quelli gia' presenti

        selectedIds = [c.id for c in self._colori]

        model = self.colori_treeview.get_model()
        model.clear()
        cols = Colore().select( denominazione=None,
                                           orderBy = 'denominazione',
                                           offset = None,
                                           batchSize = None)

        for c in cols:
            if selectedIds and c.id in selectedIds:
                colorRow = '#E6E6FF'
            else:
                colorRow = None
            model.append((c, False, (c.denominazione or '')[0:25], colorRow))


    def on_colore_add_button_clicked(self, button):
        # aggiunge ogni colore selezionato come colonna della
        # treeview taglie - colori, se non gia' presente
        colorIds = [c.id for c in self._colori]

        model = self.colori_treeview.get_model()
        for r in model:
            selected = r[1]
            if selected:
                color = r[0]
                if color.id not in colorIds:
                    self._colori.append(color)

        # riordino colori in ordine alfabetico
        coloriDict = dict([c.denominazione, c] for c in self._colori)
        nomi = coloriDict.keys()
        nomi.sort()
        self._colori = list(coloriDict[k] for k in nomi)

        self.refreshColoriTreeView()
        self.refreshTaglieColoriTreeView()


    def on_colore_remove_button_clicked(self, button):
        # rimuove ogni colore selezionato come colonna della
        # treeview taglie - colori, se gia' presente
        model = self.colori_treeview.get_model()
        colors = dict([c.id, c] for c in self._colori)
        selectedIds = [c[0].id for c in model if c[1]]

        for id in colors.keys():
            if id in selectedIds:
                self._colori.remove(colors[id])

        self.refreshColoriTreeView()
        self.refreshTaglieColoriTreeView()


    def on_taglie_colori_cell_edited(self, cellrenderer, path, value, taglia, idx):
        # conserva il valore inserito nella treeview taglie - colori
        model = self.taglie_colori_treeview.get_model()
        itr = model.get_iter_from_string(path)
        colore = model.get_value(itr, 0)
        model[path][idx] = value


    def refreshTaglieColoriTreeView(self):
        # ricostruisce la treeview taglie - colori,
        # con i colori nelle colonne in ordine alfabetico,
        # e le taglie nelle righe nell'ordine ripotato all'interno del gruppo taglia

        def getDictValue(dictionary, key):
            if dictionary.has_key(key):
                return dictionary[key]
            else:
                return None

        treeview = self.taglie_colori_treeview
        columns = treeview.get_columns()
        taglie = self._taglie
        colori = self._colori
        ripetizione_taglie = self._ripetizione_taglie

        # salvataggio valori immessi
        valuesDict = {}
        model = treeview.get_model()
        if model is not None:
            for r in model:
                if r[0] is not None:
                    idTaglia = r[0].id
                    for i, column in enumerate(columns):
                        idColore = column.get_cell_renderers()[0].get_data('idCol')
                        index = column.get_cell_renderers()[0].get_data('idxRow')
                        if idColore is not None and index is not None:
                            value = r[index]
                            if value != self._noValue:
                                valuesDict[(idTaglia, idColore)] = value

        # Ripulitura treeview
        for c in treeview.get_columns():
            treeview.remove_column(c)

        style = treeview.get_style()

        modelList = [object, str] # Oggetto Taglia + stringa taglia

        curr_idx = 2
        for i, c in enumerate(colori):
            curr_idx = i + 2
            if (i % ripetizione_taglie) == 0:
                renderer = gtk.CellRendererText()
                renderer.set_data('idxRow', None)
                renderer.set_data('idCol', None)
                renderer.set_property('editable', False)
                renderer.set_property('cell-background-set', True)
                renderer.set_property('cell-background-gdk', style.bg[0])
                column = gtk.TreeViewColumn('', renderer, text=1)
                column.set_resizable(False)
                column.set_expand(False)
                column.set_clickable(False)
                column.set_visible(True)
                treeview.append_column(column)

            renderer = gtk.CellRendererText()
            renderer.set_data('idxRow', curr_idx)
            renderer.set_data('idCol', c.id)
            renderer.set_property('editable', True)
            renderer.connect('edited', self.on_taglie_colori_cell_edited, c, curr_idx)
            column = gtk.TreeViewColumn(c.denominazione, renderer, text=curr_idx)
            column.set_resizable(True)
            column.set_expand(True)
            column.set_clickable(False)
            column.set_visible(True)
            treeview.append_column(column)
            modelList.append(str)

        modelList = modelList or [str]
        model = gtk.ListStore(*modelList)
        treeview.set_model(model)

        for t in taglie:
            row = [t, t.denominazione]
            for i, c in enumerate(colori):
                try:
                    idVariante = self._varianti[(t.id, c.id)]
                except:
                    idVariante = None

                if idVariante is None:
                    value = getDictValue(valuesDict, (t.id,c.id)) or self._noValue
                    row.append(value)
                else:
                    codici = CodiceABarreArticolo().select( idArticolo=idVariante,
                                                                       orderBy='primario',
                                                                       offset=None,
                                                                       batchSize=None)
                    codici.reverse() # Prima i codici a barre primari

                    if len(codici) == 0:
                        value = ''
                    else:
                        value = codici[0].codice
                    value = getDictValue(valuesDict, (t.id,c.id)) or value
                    row.append(value)

            model.append(row)

    def on_ok_button_clicked(self, button):
        model = self.taglie_colori_treeview.get_model()

        articoloBase = self._articoloBase
        articoloPadre = self._articoloPadre
        gruppoTaglia = self._gruppoTaglia
        taglie = self._taglie
        colori = self._colori
        articoliTagliaColore = self._articoliTagliaColore

        # verifica esistenza codici a barre e codici interni
        for row in model:
            taglia = row[0]
            for i, colore in enumerate(colori):
                try:
                    idVariante = self._varianti[(taglia.id, colore.id)]
                except:
                    idVariante = None

                codice = row[i + 2]
                if codice != self._noValue:
                    codici = CodiceABarreArticolo().select(codice=codice,
                                                                       orderBy=None,
                                                                       offset=None,
                                                                       batchSize=None)

                    for dao in codici:
                        # FIXME: la select non esegue una ricerca esatta !!
                        if dao.codice != codice:
                            continue

                        if dao.id_articolo != idVariante:
                            msg = "Attenzione !\n\nIl codice a barre " + codice + " e\' gia' presente !"
                            dialog = gtk.MessageDialog(self.getTopLevel(), gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
                                                       gtk.MESSAGE_QUESTION, gtk.BUTTONS_OK, msg)
                            response = dialog.run()
                            dialog.destroy()
                            return

                    codice = articoloBase.codice + gruppoTaglia.denominazione_breve + taglia.denominazione_breve + colore.denominazione_breve
                    codici = CodiceABarreArticolo().select(codice=codice,
                                                           offset = None,
                                                           batchSize = None)

                    for dao in codici:
                        # FIXME: la select non esegue una ricerca esatta !!
                        if dao.codice != codice:
                            continue

                        if dao.id != idVariante:
                            msg = "Attenzione !\n\nIl codice interno " + codice + " e\' gia' presente !"
                            dialog = gtk.MessageDialog(self.getTopLevel(), gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
                                                       gtk.MESSAGE_QUESTION, gtk.BUTTONS_OK, msg)
                            response = dialog.run()
                            dialog.destroy()
                            return

        #conn.startTransaction()

        #try:
            # Rimozione articoli
        idTaglie = set(t.id for t in taglie)
        idColori = set(c.id for c in colori)

        for a in articoliTagliaColore:
            if (a.id_gruppo_taglia != gruppoTaglia.id
                or a.id_taglia not in idTaglie
                or a.id_colore not in idColori):

                articolo = a.articolo()
                articolo.delete()

        for row in model:
            taglia = row[0]
            for i, colore in enumerate(colori):
                try:
                    idVariante = self._varianti[(taglia.id, colore.id)]
                except:
                    idVariante = None

                newCodice = row[i + 2]
                if idVariante is None:
                    if newCodice == self._noValue:
                        continue
                    # La combinazione taglia/colore non esiste sul DB

                    articolo = Articolo()
                    articolo.codice = articoloBase.codice + gruppoTaglia.denominazione_breve + taglia.denominazione_breve + colore.denominazione_breve
                    articolo.denominazione = articoloBase.denominazione + ' ' + taglia.denominazione + ' ' + colore.denominazione
                    articolo.id_aliquota_iva = articoloBase.id_aliquota_iva
                    articolo.id_famiglia_articolo = articoloBase.id_famiglia_articolo
                    articolo.id_categoria_articolo = articoloBase.id_categoria_articolo
                    articolo.id_unita_base = articoloBase.id_unita_base
                    articolo.id_stato_articolo = articoloBase.id_stato_articolo
                    articolo.id_imballaggio = articoloBase.id_imballaggio
                    articolo.produttore = articoloBase.produttore
                    articolo.unita_dimensioni = articoloBase.unita_dimensioni
                    articolo.unita_volume = articoloBase.unita_volume
                    articolo.unita_peso = articoloBase.unita_peso
                    articolo.lunghezza = articoloBase.lunghezza
                    articolo.larghezza = articoloBase.larghezza
                    articolo.altezza = articoloBase.altezza
                    articolo.volume = articoloBase.volume
                    articolo.peso_lordo = articoloBase.peso_lordo
                    articolo.peso_imballaggio = articoloBase.peso_imballaggio
                    articolo.stampa_etichetta = articoloBase.stampa_etichetta
                    articolo.codice_etichetta = articoloBase.codice_etichetta
                    articolo.descrizione_etichetta = articoloBase.descrizione_etichetta
                    articolo.stampa_listino = articoloBase.stampa_listino
                    articolo.descrizione_listino = articoloBase.descrizione_listino
                    articolo.note = articoloBase.note
                    articolo.sospeso = articoloBase.sospeso
                    articolo.cancellato = articoloBase.cancellato
                    articolo.aggiornamento_listino_auto = articoloBase.aggiornamento_listino_auto
                    articolo.persist()

                    articoloTagliaColore = ArticoloTagliaColore()
                    articoloTagliaColore.id_articolo = articolo.id
                    idVariante = articolo.id
                else:
                    # La combinazione taglia/colore esiste gia'
                    articoloTagliaColore = ArticoloTagliaColore().getRecord(id=idVariante)

                articoloTagliaColore.id_articolo_padre = articoloPadre.id_articolo
                articoloTagliaColore.id_gruppo_taglia = articoloPadre.id_gruppo_taglia
                articoloTagliaColore.id_taglia = taglia.id
                articoloTagliaColore.id_colore = colore.id
                articoloTagliaColore.id_anno = articoloPadre.id_anno
                articoloTagliaColore.id_stagione = articoloPadre.id_stagione
                articoloTagliaColore.id_genere = articoloPadre.id_genere
                articoloTagliaColore.persist()

                codici = CodiceABarreArticolo().select( idArticolo=idVariante,
                                                                    orderBy='primario',
                                                                    offset=None,
                                                                    batchSize=None)

                codici.reverse() # Prima i codici a barre primari

                codice = None
                if len(codici) == 0:
                    if newCodice == self._noValue or newCodice.strip() == '':
                        # Codice a barre non impostato, niente salvataggio
                        continue

                    codice = CodiceABarreArticolo()
                    codice.codice = newCodice
                    codice.id_articolo = articoloTagliaColore.id_articolo
                    codice.primario = True
                else:
                    codice = CodiceABarreArticolo().getRecord(id=codici[0].id)
                    if newCodice == self._noValue or newCodice.strip() == '':
                        # Codice a barre non impostato, rimozione
                        codice.delete()
                        continue
                    codice.codice = newCodice
                codice.persist()

        self.destroy()


    def on_cancel_button_clicked(self, button):
        self.destroy()


    def on_color_button_toggled(self, toggleButton):
        if toggleButton.get_property('active') is False:
            return

        from AnagraficaColori import AnagraficaColori
        anag = AnagraficaColori()

        showAnagraficaRichiamata(self.getTopLevel(), anag.getTopLevel(), toggleButton, self.refreshColoriTreeView)


    def on_size_button_toggled(self, toggleButton):
        if toggleButton.get_property('active') is False:
            return

        from AnagraficaTaglie import AnagraficaTaglie
        anag = AnagraficaTaglie()

        showAnagraficaRichiamata(self.getTopLevel(), anag.getTopLevel(), toggleButton, self.refreshTaglie)


    def on_gestione_taglie_colori_close(self, widget, event=None):
        self.destroy()
        return None



class SelezioneTaglieColori(GladeWidget):

    def __init__(self, articolo, varianti = []):
        GladeWidget.__init__(self, 'selezione_taglie_colori')

        dialog = self.selezione_taglie_colori
        self.placeWindow(self.getTopLevel())

        self._articoloBase = articolo
        self._articoloPadre = articolo.articoloTagliaColore
        self._articoliTagliaColore = self._articoloBase.articoliTagliaColore
        self._varianti = {}
        self._selected = varianti

        self._gruppoTaglia = self._articoloPadre.id_gruppo_taglia

        # Taglie (ordinate) che saranno presenti nella treeview (righe)
        self._taglie = self._articoloPadre.gruppoTaglia.taglie

        # Colori (ordinati) che saranno presenti nella treeview(colonne)
        idColori = set(a.id_colore for a in self._articoliTagliaColore)
        colori = [Colore(Environment.connection, c) for c in idColori]
        coloriDict = dict([c.denominazione, c] for c in colori)
        nomi = coloriDict.keys()
        nomi.sort()
        self._colori = list(coloriDict[k] for k in nomi)

        # Dizionario che associa alla chiave (taglia,colore) l'id della variante
        for a in self._articoliTagliaColore:
            if not a.articolo().cancellato:
                self._varianti[(a.id_taglia, a.id_colore)] = a.id_articolo

        self._ripetizione_taglie = 3 # Ogni quante colonne ripetere le taglie?

        self.articolo_label.set_markup('<span weight="bold">%s</span>'
                                       % (self._articoloBase.denominazione,))
        self.gruppo_taglia_label.set_markup('<span weight="bold">%s</span>'
                                            % (self._articoloPadre.gruppoTaglia.denominazione,))
        self.refreshTaglieColoriTreeView()


    def refreshTaglieColoriTreeView(self):
        treeview = self.taglie_colori_treeview
        colori = self._colori
        ripetizione_taglie = self._ripetizione_taglie

        # Ripulitura treeview
        for c in treeview.get_columns():
            treeview.remove_column(c)

        style = treeview.get_style()

        modelList = [object, str] # Oggetto Taglia + stringa taglia
        # Per ogni colonna si specificheranno 2 valori booleani:
        # il 1. mantiene il valore della selezione (vero o falso),
        # il 2. indica se la check box deve essere editabile (la variante esiste)

        curr_idx = 2
        for i, c in enumerate(colori):
            if i == 0:
                curr_idx = curr_idx + 1
            else:
                curr_idx = curr_idx + 2
            if (i % ripetizione_taglie) == 0:
                renderer = gtk.CellRendererText()
                renderer.set_property('editable', False)
                column = gtk.TreeViewColumn('', renderer, text=1)
                column.set_resizable(False)
                column.set_expand(False)
                column.set_clickable(False)
                column.set_visible(True)
                treeview.append_column(column)

            renderer = gtk.CellRendererToggle()
            renderer.connect('toggled', self.on_taglie_colori_cell_edited, treeview, c)
            num_col = curr_idx - 1
            renderer.set_data('column', num_col)
            renderer.set_property('cell-background-set', True)
            renderer.set_property('cell-background-gdk', style.bg[1])
            column = gtk.TreeViewColumn(c.denominazione, renderer, active=num_col, activatable=num_col + 1)
            column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
            column.set_clickable(False)
            column.set_resizable(True)
            column.set_expand(True)
            column.set_visible(True)
            treeview.append_column(column)
            modelList.append(bool)
            modelList.append(bool)
        if len(colori) == 0:
            renderer = gtk.CellRendererText()
            renderer.set_property('editable', False)
            column = gtk.TreeViewColumn('', renderer, text=1)
            column.set_resizable(False)
            column.set_expand(False)
            column.set_clickable(False)
            column.set_visible(True)
            treeview.append_column(column)

        model = gtk.ListStore(*modelList)
        treeview.set_model(model)

        for t in self._taglie:
            row = [t, t.denominazione]
            for c in self._colori:
                try:
                    variante = self._varianti[(t.id, c.id)]
                    found = True
                except:
                    found = False
                # La check e' deselezionata per default, ed e' editabile se la
                # relativa variante esiste
                row.append(False)
                row.append(found)

            model.append(row)


    def on_taglie_colori_cell_edited(self, cell, path, value, colore):
        model = self.taglie_colori_treeview.get_model()
        iterator = model.get_iter(path)
        column = cell.get_data('column')
        model.set_value(iterator, column, not cell.get_active())

        taglia = model.get_value(iterator, 0)
        variante = self._varianti[(taglia.id, colore.id)]
        selezionata = model.get_value(iterator, column)
        try:
            # Verifica se la variante e' gia' stata selezionata
            indice = self._selected(variante)
            # Se e' stata trovata ma e' stata deselezionata: la rimuove dalla lista
            if not selezionata:
                self._selected.pop(indice)
        except:
            # Non e' stata trovata: se e' stata selezionata l'aggiunge alla lista
            if selezionata:
                self._selected.append(variante)


    def on_ok_button_clicked(self, button):
        """
        Restituisce la lista delle varianti selezionate
        nell'ordine di selezione
        """
        print "uhm.. non ho fatto proprio nulla!"
        self.destroy()


    def on_cancel_button_clicked(self, button):
        self._selected = []
        self.destroy()


    def on_selezione_taglie_colori_close(self, widget, event=None):
        self.destroy()
        return None
