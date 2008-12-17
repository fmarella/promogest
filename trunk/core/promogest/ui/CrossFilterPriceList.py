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
from promogest.dao.CodiceABarreArticolo import CodiceABarreArticolo
import genshi
from genshi.template import TemplateLoader
from promogest.ui.utils import *


#templates_dir = './promogest/modules/PromoWear/templates/'
#loader = TemplateLoader([templates_dir])

class CrossFilterPriceList(GladeWidget):

    def __init__(self, idListino):
        GladeWidget.__init__(self, 'cross_filter_pricelist',
                            'cross_filter_pricelist.glade')

        dialog = self.cross_filter_pricelist
        self.placeWindow(self.getTopLevel())
        self._treeViewModel = None
        #self._articoloBase = articolo
        #self._articoloPadre = articolo.articoloTagliaColore
        #self.idGruppoTaglia = self._articoloBase.id_gruppo_taglia
        #if self._articoloPadre is None:
            #self._articoloPadre = ArticoloTagliaColore()
        #self._articoliTagliaColore = self._articoloBase.articoliTagliaColore
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
        #self.refreshColori()
        #self.sizesAvailable()
        #self.selected = False
        ## Dizionario che associa alla chiave (taglia,colore) l'id della variante
        #for a in self._articoliTagliaColore:
            #self._varianti[(a.id_taglia, a.id_colore)] = a.id_articolo

        #self._ripetizione_taglie = 3 # Ogni quante colonne ripetere le taglie?
        #self.group_size_label.set_markup('<span weight="bold">%s</span>'
                                       #% (self._articoloBase.denominazione_gruppo_taglia,))

        #self.father_label.set_markup('Articolo: ' + '<span weight="bold">%s %s</span>'
                                       #% (self._articoloBase.codice,self._articoloBase.denominazione))

        #self._drawColoriTreeView()
        #self.refreshColoriTreeView()
        #self.refreshTaglie()
        #self._refreshHtml()
        self.rowBackGround = '#E6E6FF'
        self.rowBoldFont = 'arial bold 12'
        self.draw()


    def refreshColori(self):
        self.colori = Colore().select(batchSize=None)
        return self.colori

    def sizesAvailable(self):
        self.sizes = GruppoTagliaTaglia().select(idGruppoTaglia=self.idGruppoTaglia, batchSize=None)
        return self.sizes

    def _refreshHtml(self, data= None):
        """ show the html page in the custom widget"""
        if self._gtkHtml is None:
            self._gtkHtml = self.getHtmlWidget()
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

    def getHtmlWidget(self):
        return self.creazione_varianti_html

    def draw(self):
        """Creo una treeview che abbia come colonne i colori e come righe
           le taglie direi che sia il caso di gestire anche le descrizioni variante visto che le ho
        """
        #parte dei duplicati
        treeview_duplicated = self.duplicated_treeview
        rendererSx = gtk.CellRendererText()
        rendererDx = gtk.CellRendererText()
        rendererDx.set_property('xalign', 1)

        column = gtk.TreeViewColumn('Listino', rendererSx, text=1)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        #column.connect("clicked", self._changeOrderBy, 'id_listino')
        column.set_resizable(False)
        column.set_expand(True)
        column.set_min_width(250)
        treeview_duplicated.append_column(column)

        column = gtk.TreeViewColumn('Codice articolo', rendererSx, text=2)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(False)
        #column.connect("clicked", self._changeOrderBy, 'codice_articolo')
        column.set_resizable(True)
        column.set_expand(False)
        column.set_min_width(100)
        treeview_duplicated.append_column(column)

        column = gtk.TreeViewColumn('Articolo', rendererSx, text=3)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(False)
        #column.connect("clicked", self._changeOrderBy, 'id_articolo')
        column.set_resizable(True)
        column.set_expand(True)
        column.set_min_width(200)
        treeview_duplicated.append_column(column)

        column = gtk.TreeViewColumn('Data variazione', rendererSx, text=4)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        #column.connect("clicked", self._changeOrderBy, 'data_listino_articolo')
        column.set_resizable(True)
        column.set_expand(False)
        column.set_min_width(100)
        treeview_duplicated.append_column(column)

        column = gtk.TreeViewColumn('Prezzo dettaglio', rendererDx, text=5)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        #column.connect("clicked", self._changeOrderBy, 'prezzo_dettaglio')
        column.set_resizable(True)
        column.set_expand(False)
        column.set_min_width(100)
        treeview_duplicated.append_column(column)

        column = gtk.TreeViewColumn('Prezzo ingrosso', rendererDx, text=6)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        #column.connect("clicked", self._changeOrderBy, 'prezzo_ingrosso')
        column.set_resizable(True)
        column.set_expand(False)
        column.set_min_width(100)
        treeview_duplicated.append_column(column)
        self._treeViewModel_duplicated = gtk.ListStore(object, str, str, str, str, str, str)
        treeview_duplicated.set_model(self._treeViewModel_duplicated)


        #parte delle opzioni possibili
        treeview_option = self.option_treeview
        rendererSx = gtk.CellRendererText()
        rendererDx = gtk.CellRendererText()
        rendererDx.set_property('xalign', 1)


        cellspin = gtk.CellRendererToggle()
        cellspin.set_property('activatable', True)
        cellspin.connect('toggled', self.on_column_selected_edited, self.treeview, True)
        column = gtk.TreeViewColumn('Seleziona', cellspin)
        column.add_attribute( cellspin, "active", 1)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_resizable(True)
        #column.set_expand(True)
        #column.set_min_width(40)
        treeview_option.append_column(column)

        column = gtk.TreeViewColumn('Listino', rendererSx, text=1)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        #column.connect("clicked", self._changeOrderBy, 'id_listino')
        column.set_resizable(False)
        column.set_expand(True)
        column.set_min_width(250)
        treeview_option.append_column(column)

        column = gtk.TreeViewColumn('Codice articolo', rendererSx, text=2)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(False)
        #column.connect("clicked", self._changeOrderBy, 'codice_articolo')
        column.set_resizable(True)
        column.set_expand(False)
        column.set_min_width(100)
        treeview_option.append_column(column)

        column = gtk.TreeViewColumn('Articolo', rendererSx, text=3)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(False)
        #column.connect("clicked", self._changeOrderBy, 'id_articolo')
        column.set_resizable(True)
        column.set_expand(True)
        column.set_min_width(200)
        treeview_option.append_column(column)

        column = gtk.TreeViewColumn('Data variazione', rendererSx, text=4)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        #column.connect("clicked", self._changeOrderBy, 'data_listino_articolo')
        column.set_resizable(True)
        column.set_expand(False)
        column.set_min_width(100)
        treeview_option.append_column(column)

        column = gtk.TreeViewColumn('Prezzo dettaglio', rendererDx, text=5)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        #column.connect("clicked", self._changeOrderBy, 'prezzo_dettaglio')
        column.set_resizable(True)
        column.set_expand(False)
        column.set_min_width(100)
        treeview_option.append_column(column)

        column = gtk.TreeViewColumn('Prezzo ingrosso', rendererDx, text=6)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        #column.connect("clicked", self._changeOrderBy, 'prezzo_ingrosso')
        column.set_resizable(True)
        column.set_expand(False)
        column.set_min_width(100)
        treeview_option.append_column(column)

        self._treeViewModel_option = gtk.ListStore(object,bool, str, str, str, str, str, str)
        treeview_option.set_model(self._treeViewModel_option)

        #parte degli articoli filtrati
        treeview_filtered = self.filtered_treeview
        rendererSx = gtk.CellRendererText()
        rendererDx = gtk.CellRendererText()
        rendererDx.set_property('xalign', 1)

        column = gtk.TreeViewColumn('Listino', rendererSx, text=1)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        #column.connect("clicked", self._changeOrderBy, 'id_listino')
        column.set_resizable(False)
        column.set_expand(True)
        column.set_min_width(250)
        treeview_filtered.append_column(column)

        column = gtk.TreeViewColumn('Codice articolo', rendererSx, text=2)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(False)
        #column.connect("clicked", self._changeOrderBy, 'codice_articolo')
        column.set_resizable(True)
        column.set_expand(False)
        column.set_min_width(100)
        treeview_filtered.append_column(column)

        column = gtk.TreeViewColumn('Articolo', rendererSx, text=3)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(False)
        #column.connect("clicked", self._changeOrderBy, 'id_articolo')
        column.set_resizable(True)
        column.set_expand(True)
        column.set_min_width(200)
        treeview_filtered.append_column(column)

        column = gtk.TreeViewColumn('Data variazione', rendererSx, text=4)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        #column.connect("clicked", self._changeOrderBy, 'data_listino_articolo')
        column.set_resizable(True)
        column.set_expand(False)
        column.set_min_width(100)
        treeview_filtered.append_column(column)

        column = gtk.TreeViewColumn('Prezzo dettaglio', rendererDx, text=5)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        #column.connect("clicked", self._changeOrderBy, 'prezzo_dettaglio')
        column.set_resizable(True)
        column.set_expand(False)
        column.set_min_width(100)
        treeview_filtered.append_column(column)

        column = gtk.TreeViewColumn('Prezzo ingrosso', rendererDx, text=6)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        #column.connect("clicked", self._changeOrderBy, 'prezzo_ingrosso')
        column.set_resizable(True)
        column.set_expand(False)
        column.set_min_width(100)
        treeview_filtered.append_column(column)

        self._treeViewModel_filtered = gtk.ListStore(object, str, str, str, str, str, str)
        treeview_filtered.set_model(self._treeViewModel_filtered)




        #self.treeview = self.color_and_size_treeview
        #cellspin = gtk.CellRendererToggle()
        #cellspin.set_property('activatable', True)
        #cellspin.connect('toggled', self.on_column_selected_edited, self.treeview, True)
        #column = gtk.TreeViewColumn('Seleziona', cellspin)
        #column.add_attribute( cellspin, "active", 1)
        #column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        #column.set_resizable(True)
        ##column.set_expand(True)
        ##column.set_min_width(40)
        #self.treeview.append_column(column)

        #rendererSx = gtk.CellRendererText()
        #column = gtk.TreeViewColumn("Taglia / Colore", rendererSx, text=2, background=4, font=5)
        #column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        #column.set_clickable(False)
        #column.set_resizable(True)
        ##column.set_expand(False)
        #column.set_min_width(70)
        #self.treeview.append_column(column)

        #celltext = gtk.CellRendererText()
        #celltext.set_property("editable", True)
        #celltext.set_property("visible", True)
        #celltext.connect('edited', self.on_column_codice_edited, self.treeview, True)
        #column = gtk.TreeViewColumn('Codice', celltext, text=3)
        #column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        ##column.set_clickable(True)
        ##column.connect("clicked", self._changeOrderBy, 'denominazione_breve')
        #column.set_resizable(True)
        #column.set_expand(True)
        #column.set_min_width(50)
        #self.treeview.append_column(column)

        #self._treeViewModel = gtk.TreeStore(object,bool,str,str, str, str, object)
        #self.treeview.set_model(self._treeViewModel)
        #self.head_color.set_active(True)
        #self.only_variation.set_active(True)
        #self.refresh()

    def refresh(self,order="color",filtered =True):
        # Aggiornamento TreeView
        self._treeViewModel.clear()
        #varianti = self.data["varianti"]
        #print varianti

        if self.order == "color":
            if self.filtered:
                for c in self._articoloBase.colori:
                    #oggetto Colore
                    parent = self._treeViewModel.append(None,(c,
                                                True,
                                                c.denominazione,
                                                "",
                                                self.rowBackGround,
                                                self.rowBoldFont,
                                                None))
                    sizesFilterd= ArticoloTagliaColore().select(idArticoloPadre =self._articoloBase.id,
                                                                idColore=c.id,
                                                                batchSize=None)
                    for r in sizesFilterd:
                        s = Taglia().getRecord(id=r.id_taglia)
                        articoloTagliaColore = ArticoloTagliaColore().select(idArticoloPadre =self._articoloBase.id,
                                                                                idTaglia=s.id,
                                                                                idColore=c.id)
                        if articoloTagliaColore:
                            codiceArticolo = Articolo().getRecord(id=articoloTagliaColore[0].id_articolo)
                            codice = codiceArticolo.codice_a_barre or ""
                        else:
                            codice = ""
                            codiceArticolo = None
                        #oggetto Taglia
                        self._treeViewModel.append(parent,(s,
                                            True,
                                            s.denominazione,
                                            codice,
                                            None,
                                            None,
                                            codiceArticolo))
            else:
                for c in self.colori:
                    #oggetto Colore
                    parent = self._treeViewModel.append(None,(c,
                                                self.selected,
                                                c.denominazione,
                                                "",
                                                self.rowBackGround,
                                                self.rowBoldFont,
                                                None))
                    for g in self.sizes:
                        alreadyexist= ArticoloTagliaColore().select(idArticoloPadre =self._articoloBase.id,
                                                                idColore=c.id,
                                                                idTaglia=g.id_taglia,
                                                                batchSize=None)
                        if alreadyexist:
                            selected = True
                            codiceArticolo = Articolo().getRecord(id=alreadyexist[0].id_articolo)
                            codice= codiceArticolo.codice_a_barre or ""
                        else:
                            selected = False
                            codice = ""
                            codiceArticolo = None
                        # oggetto Gruppo Taglia Taglia
                        s = Taglia().getRecord(id=g.id_taglia)

                        self._treeViewModel.append(parent,(s,
                                                selected,
                                                s.denominazione,
                                                codice,
                                                None,
                                                None,
                                                codiceArticolo))
        else:
            if self.filtered:
                for s in self._articoloBase.taglie:
                    parent = self._treeViewModel.append(None,(s,
                                                            True,
                                                            s.denominazione,
                                                            "",
                                                            self.rowBackGround,
                                                            self.rowBoldFont,
                                                            None))
                    colorFilterd= ArticoloTagliaColore().select(idArticoloPadre =self._articoloBase.id,
                                                                idTaglia=s.id, batchSize=None)
                    for d in colorFilterd:
                        c = Colore().getRecord(id=d.id_colore)
                        articoloTagliaColore = ArticoloTagliaColore().select(idArticoloPadre =self._articoloBase.id,
                                                                            idTaglia=s.id,
                                                                            idColore=c.id)
                        if articoloTagliaColore:
                            codiceArticolo = Articolo().getRecord(id=articoloTagliaColore[0].id_articolo)
                            codice = codiceArticolo.codice_a_barre or ""
                        else:
                            codice = ""
                            codiceArticolo = None
                        self._treeViewModel.append(parent,(c,
                                                    True,
                                                    c.denominazione,
                                                    codice,
                                                    None,
                                                    None,
                                                    codiceArticolo))

            else:
                for s in self.sizes:
                    h = Taglia().getRecord(id=s.id_taglia)
                    #oggetto GruppoTagliaTaglia
                    parent = self._treeViewModel.append(None,(h,
                                                            self.selected,
                                                            h.denominazione,
                                                            "",
                                                            self.rowBackGround,
                                                            self.rowBoldFont,
                                                            None))
                    for c in self.colori:
                        #oggetto Colore
                        alreadyexist= ArticoloTagliaColore().select(idArticoloPadre =self._articoloBase.id,
                                                                idColore=c.id,
                                                                idTaglia=h.id,
                                                                batchSize=None)
                        if alreadyexist:
                            selected = True
                            codiceArticolo = Articolo().getRecord(id=alreadyexist[0].id_articolo)
                            codice = codiceArticolo.codice_a_barre or ""
                        else:
                            selected = False
                            codice = ""
                            codiceArticolo = None
                        self._treeViewModel.append(parent,(c,
                                                    selected,
                                                    c.denominazione,
                                                    codice,
                                                    None,
                                                    None,
                                                    codiceArticolo))
        self.printModel()

    def printModel(self):
        self.datas= []
        self._treeViewModel.foreach(self.selectFilter )

    def selectFilter(self, model, path, iter):
        check = model.get_value(iter, 1)
        fatherPath = model.get_path(iter)
        if check:
            if len(fatherPath) ==1:
                return
            oggettoFiglio = model.get_value(iter, 0)
            padre = model.iter_parent(iter)
            oggettoPadre =model.get_value(padre, 0)
            codice = model.get_value(iter, 3)
            articolo = model.get_value(iter, 6)
            self.datas.append((self._articoloBase,oggettoFiglio,oggettoPadre,codice, articolo))
        #print self.datas
        self._refreshHtml(data=self.datas)


    def on_column_selected_edited(self, cell, path, treeview,value, editNext=True):
        """ Function ti set the value quantita edit in the cell"""
        model = treeview.get_model()
        model[path][1] = not model[path][1]
        for a in  model[path].iterchildren():
             a[1] = model[path][1]
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

    def on_cancel_button_clicked(self, button):
        self.destroy()


    def on_color_button_toggled(self, toggleButton):
        if toggleButton.get_property('active') is False:
            return

        from AnagraficaColori import AnagraficaColori
        anag = AnagraficaColori()

        showAnagraficaRichiamata(self.getTopLevel(), anag.getTopLevel(), toggleButton, self.refresh)


    def on_size_button_toggled(self, toggleButton):
        if toggleButton.get_property('active') is False:
            return

        from AnagraficaTaglie import AnagraficaTaglie
        anag = AnagraficaTaglie()

        showAnagraficaRichiamata(self.getTopLevel(), anag.getTopLevel(), toggleButton, self.refresh)

    def on_ok_button_clicked(self, button):
        for dat in self.datas:
            codici = None
            print dat
            articoloPadre = dat[0]
            if dat[1].__module__ =="promogest.modules.PromoWear.dao.Taglia":
                daoTaglia = dat[1]
                daoColore = dat[2]
            else:
                daoColore = dat[1]
                daoTaglia = dat[2]
            codiceabarre = dat[3]
            articoloFiglio = dat[4]

            if codiceabarre:
                if articoloFiglio:
                #verifico la correttezza del codice a barre della variante già esistente
                # in precedenza
                    if codiceabarre != articoloFiglio.codice_a_barre:
                        codici = CodiceABarreArticolo().select(codiceEM=codiceabarre,
                                                                offset=None,
                                                                batchSize=None)
                else:
                    codici = CodiceABarreArticolo().select(codiceEM=codiceabarre,
                                                                offset=None,
                                                                batchSize=None)
                if codici:
                        msg = """Attenzione !
Il codice a barre  %s è gia' presente nel Database, ricontrolla!""" % codiceabarre
                        dialog = gtk.MessageDialog(self.getTopLevel(), gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
                                                       gtk.MESSAGE_QUESTION, gtk.BUTTONS_OK, msg)
                        response = dialog.run()
                        dialog.destroy()
                        return
            if articoloFiglio:
                #aggiorno articoloesistenze può essere cambiato solo il codice a barre
                if codiceabarre and codiceabarre != articoloFiglio.codice_a_barre:
                    codici = CodiceABarreArticolo().select(codiceEM=codiceabarre,
                                                                    offset=None,
                                                                    batchSize=None)
                    if not codici:
                        cba = CodiceABarreArticolo()
                        cba.codice = codiceabarre
                        cba.primario = True
                        cba.persist()
            else:
                #inserisco la nuova variazione articolo ed il relativo codice a barre
                articolo = Articolo()
                articolo.codice = articoloPadre.codice + articoloPadre.denominazione_gruppo_taglia[0:3] + daoTaglia.denominazione_breve + daoColore.denominazione_breve
                articolo.denominazione = articoloPadre.denominazione + ' ' + daoTaglia.denominazione_breve + ' ' + daoColore.denominazione
                articolo.id_aliquota_iva = articoloPadre.id_aliquota_iva
                articolo.id_famiglia_articolo = articoloPadre.id_famiglia_articolo
                articolo.id_categoria_articolo = articoloPadre.id_categoria_articolo
                articolo.id_unita_base = articoloPadre.id_unita_base
                articolo.id_stato_articolo = articoloPadre.id_stato_articolo
                articolo.id_imballaggio = articoloPadre.id_imballaggio
                articolo.produttore = articoloPadre.produttore
                articolo.unita_dimensioni = articoloPadre.unita_dimensioni
                articolo.unita_volume = articoloPadre.unita_volume
                articolo.unita_peso = articoloPadre.unita_peso
                articolo.lunghezza = articoloPadre.lunghezza
                articolo.larghezza = articoloPadre.larghezza
                articolo.altezza = articoloPadre.altezza
                articolo.volume = articoloPadre.volume
                articolo.peso_lordo = articoloPadre.peso_lordo
                articolo.peso_imballaggio = articoloPadre.peso_imballaggio
                articolo.stampa_etichetta = articoloPadre.stampa_etichetta
                articolo.codice_etichetta = articoloPadre.codice_etichetta
                articolo.descrizione_etichetta = articoloPadre.descrizione_etichetta
                articolo.stampa_listino = articoloPadre.stampa_listino
                articolo.descrizione_listino = articoloPadre.descrizione_listino
                articolo.note = articoloPadre.note
                articolo.sospeso = articoloPadre.sospeso
                articolo.cancellato = articoloPadre.cancellato
                articolo.aggiornamento_listino_auto = articoloPadre.aggiornamento_listino_auto
                articolo.persist()

                articoloTagliaColore = ArticoloTagliaColore()
                articoloTagliaColore.id_articolo = articolo.id
                articoloTagliaColore.id_articolo_padre = articoloPadre.id
                articoloTagliaColore.id_gruppo_taglia = articoloPadre.id_gruppo_taglia
                articoloTagliaColore.id_taglia = daoTaglia.id
                articoloTagliaColore.id_colore = daoColore.id
                articoloTagliaColore.id_anno = articoloPadre.id_anno
                articoloTagliaColore.id_stagione = articoloPadre.id_stagione
                articoloTagliaColore.id_genere = articoloPadre.id_genere
                articoloTagliaColore.persist()
                if codiceabarre:
                    codici = CodiceABarreArticolo().select(codiceEM=codiceabarre,
                                                                    offset=None,
                                                                    batchSize=None)
                    if not codici:
                        cba = CodiceABarreArticolo()
                        cba.codice = codiceabarre
                        cba.id_articolo = articolo.id
                        cba.primario = True
                        cba.persist()
        self.destroy()

