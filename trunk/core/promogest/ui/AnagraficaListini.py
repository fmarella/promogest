# -*- coding: iso-8859-15 -*-

"""
 Promogest
 Copyright (C) 2005-2008 by Promotux Informatica - http://www.promotux.it/
 Author: Andrea Argiolas <andrea@promotux.it>
 Author: Francesco Meloni <francesco@promotux.it>
 License: GNU GPLv2
 """

import gtk
import gobject
from promogest.lib.sqlalchemy import *
from promogest.lib.sqlalchemy.orm import *
from AnagraficaComplessa import Anagrafica, AnagraficaFilter, AnagraficaHtml, AnagraficaReport, AnagraficaEdit

from promogest import Environment
from promogest.dao.Dao import Dao
import promogest.dao.Listino
from promogest.dao.Listino import Listino
import promogest.dao.ListinoCategoriaCliente
from promogest.dao.ListinoCategoriaCliente import ListinoCategoriaCliente
import promogest.dao.ListinoMagazzino
from promogest.dao.ListinoMagazzino import ListinoMagazzino

from utils import *
from utilsCombobox import *



class AnagraficaListini(Anagrafica):
    """ Anagrafica listini """

    def __init__(self, denominazione=None, aziendaStr=None):
        self._denominazione = denominazione
        Anagrafica.__init__(self,
                            windowTitle='Promogest - Anagrafica listini',
                            recordMenuLabel='_Listini',
                            filterElement=AnagraficaListiniFilter(self),
                            htmlHandler=AnagraficaListiniHtml(self),
                            reportHandler=AnagraficaListiniReport(self),
                            editElement=AnagraficaListiniEdit(self),
                            aziendaStr=aziendaStr)



class AnagraficaListiniFilter(AnagraficaFilter):
    """ Filtro per la ricerca nell'anagrafica dei listini """

    def __init__(self, anagrafica):
        AnagraficaFilter.__init__(self,
                                  anagrafica,
                                  'anagrafica_listini_filter_table',
                                  gladeFile='_anagrafica_listini_elements.glade')
        self._widgetFirstFocus = self.denominazione_filter_entry


    def draw(self):
        # Colonne della Treeview per il filtro
        treeview = self._anagrafica.anagrafica_filter_treeview
        renderer = gtk.CellRendererText()

        column = gtk.TreeViewColumn('Denominazione', renderer, text=1)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        column.connect("clicked", self._changeOrderBy, 'denominazione')
        column.set_resizable(True)
        column.set_expand(False)
        column.set_min_width(150)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Descrizione', renderer, text=2)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        column.connect("clicked", self._changeOrderBy, 'descrizione')
        column.set_resizable(True)
        column.set_expand(True)
        column.set_min_width(200)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Data listino', renderer, text=3)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        column.connect("clicked", self._changeOrderBy, 'data_listino')
        column.set_resizable(True)
        column.set_expand(False)
        column.set_min_width(100)
        treeview.append_column(column)

        self._treeViewModel = gtk.ListStore(gobject.TYPE_PYOBJECT, str, str, str)
        self._anagrafica.anagrafica_filter_treeview.set_model(self._treeViewModel)

        if self._anagrafica._denominazione is not None:
            self.denominazione_filter_entry.set_text(self._anagrafica._denominazione)

        self.refresh()

        if self._anagrafica._denominazione is not None:
            self._anagrafica.anagrafica_filter_treeview.grab_focus()


    def clear(self):
        # Annullamento filtro
        self.denominazione_filter_entry.set_text('')
        self.refresh()


    def refresh(self):
        # Aggiornamento TreeView
        denominazione = prepareFilterString(self.denominazione_filter_entry.get_text())

        def filterCountClosure():
            return Listino(isList=True).count(denominazione=denominazione)

        self._filterCountClosure = filterCountClosure

        self.numRecords = self.countFilterResults()

        self._refreshPageCount()

        # Let's save the current search as a closure
        def filterClosure(offset, batchSize):
            return Listino(isList=True).select( denominazione=denominazione,
                                                orderBy=self.orderBy,
                                                offset=offset,
                                                batchSize=batchSize)

        self._filterClosure = filterClosure

        liss = self.runFilter()

        self._treeViewModel.clear()

        for l in liss:
            self._treeViewModel.append((l,
                                        (l.denominazione or ''),
                                        (l.descrizione or ''),
                                        dateToString(l.data_listino)))



class AnagraficaListiniHtml(AnagraficaHtml):
    def __init__(self, anagrafica):
        AnagraficaHtml.__init__(self, anagrafica, 'listino',
                                'Listino')



class AnagraficaListiniReport(AnagraficaReport):
    def __init__(self, anagrafica):
        AnagraficaReport.__init__(self, anagrafica=anagrafica,
                                  description='Elenco dei listini',
                                  defaultFileName='listini',
                                  htmlTemplate='listini',
                                  sxwTemplate='listini')



class AnagraficaListiniEdit(AnagraficaEdit):
    """ Modifica un record dell'anagrafica dei listini """

    def __init__(self, anagrafica):
        AnagraficaEdit.__init__(self,
                                  anagrafica,
                                  'anagrafica_listini_detail_table',
                                  'Dati listino',
                                  gladeFile='_anagrafica_listini_elements.glade')
        self._widgetFirstFocus = self.denominazione_entry


    def draw(self):
        #Elenco categorie
        rendererText = gtk.CellRendererText()
        column = gtk.TreeViewColumn('Categoria', rendererText, text=1)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(False)
        column.set_resizable(True)
        column.set_expand(True)
        self.categorie_treeview.append_column(column)

        rendererPixbuf = gtk.CellRendererPixbuf()
        column = gtk.TreeViewColumn('', rendererPixbuf, pixbuf=2)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(False)
        column.set_resizable(False)
        column.set_expand(False)
        column.set_min_width(20)
        self.categorie_treeview.append_column(column)

        model = gtk.ListStore(int, str, gtk.gdk.Pixbuf, str)
        self.categorie_treeview.set_model(model)

        #Elenco magazzini
        rendererText = gtk.CellRendererText()
        column = gtk.TreeViewColumn('Magazzino', rendererText, text=1)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(False)
        column.set_resizable(True)
        column.set_expand(True)
        self.magazzini_treeview.append_column(column)

        rendererPixbuf = gtk.CellRendererPixbuf()
        column = gtk.TreeViewColumn('', rendererPixbuf, pixbuf=2)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(False)
        column.set_resizable(False)
        column.set_expand(False)
        column.set_min_width(20)
        self.magazzini_treeview.append_column(column)

        model = gtk.ListStore(int, str, gtk.gdk.Pixbuf, str)
        self.magazzini_treeview.set_model(model)

        fillComboboxCategorieClienti(self.id_categoria_cliente_customcombobox.combobox)
        self.id_categoria_cliente_customcombobox.connect('clicked',
                                                         on_id_categoria_cliente_customcombobox_clicked)
        fillComboboxMagazzini(self.id_magazzino_customcombobox.combobox)
        self.id_magazzino_customcombobox.connect('clicked',
                                                 on_id_magazzino_customcombobox_clicked)


    def setDao(self, dao):
        if dao is None:
            # Crea un nuovo Dao vuoto
            self.dao = Listino().getRecord()

        else:
            # Ricrea il Dao con una connessione al DBMS SQL
            self.dao = Listino(isList=True).select(id=dao.id)[0]
        self._refresh()


    def _refresh(self):
        self.denominazione_entry.set_text(self.dao.denominazione or '')
        self.descrizione_entry.set_text(self.dao.descrizione or '')
        self.data_listino_entry.set_text(dateToString(self.dao.data_listino))
        self._refreshCategorieClienti()
        self._refreshMagazzini()


    def _refreshCategorieClienti(self):
        self.id_categoria_cliente_customcombobox.combobox.set_active(-1)
        model = self.categorie_treeview.get_model()
        model.clear()
        if not self.dao.id:
            return
        categorie = self.dao.categorieCliente
        for c in categorie:
            model.append((c.id_categoria_cliente, c.categoria_cliente, None, None))


    def _refreshMagazzini(self):
        self.id_magazzino_customcombobox.combobox.set_active(-1)
        model = self.magazzini_treeview.get_model()
        model.clear()
        if not self.dao.id:
            return
        magazzini = self.dao.magazzini
        for m in magazzini:
            model.append((m.id_magazzino, m.magazzino, None, None))


    def saveDao(self):
        if (self.denominazione_entry.get_text() == ''):
            obligatoryField(self.dialogTopLevel, self.denominazione_entry)

        if (self.descrizione_entry.get_text() == ''):
            obligatoryField(self.dialogTopLevel, self.descrizione_entry)

        if (self.data_listino_entry.get_text() == ''):
            obligatoryField(self.dialogTopLevel, self.data_listino_entry)
        # ATTENZIONE: incremento ottenuto richiamando esplicitamente la sequence, in quanto id non e' PK
        #             della tabella listino
        if not self.dao.id:
            listino_sequence = Sequence("listino_id_seq", schema=Environment.params['schema'])
            self.dao.id = Environment.params['session'].connection().execute(listino_sequence)
            #provaaaaaaaaa = (Listino(isList=True).select(batchSize=None)[-1].id)+1
            #self.dao.id = provaaaaaaaaa
        self.dao.denominazione = self.denominazione_entry.get_text()
        listinoAtt = Listino(isList=True).select(denominazione=self.dao.denominazione)
        if listinoAtt ==[]:
            self.dao.listino_attuale = False

        self.dao.descrizione = self.descrizione_entry.get_text()
        self.dao.data_listino = stringToDate(self.data_listino_entry.get_text())

        self.dao.persist()
        model = self.categorie_treeview.get_model()
        cleanListinoCategoriaCliente = ListinoCategoriaCliente(isList=True)\
                                            .select(idListino=self.dao.id,
                                            batchSize=None)
        for lcc in cleanListinoCategoriaCliente:
            lcc.delete()
        for c in model:
            if c[3] == 'deleted':
                pass
            else:
                daoListinoCategoriaCliente = ListinoCategoriaCliente().getRecord()
                daoListinoCategoriaCliente.id_listino = self.dao.id
                daoListinoCategoriaCliente.id_categoria_cliente = c[0]
                daoListinoCategoriaCliente.persist()

        model = self.magazzini_treeview.get_model()
        cleanMagazzini = ListinoMagazzino(isList=True)\
                                            .select(idListino=self.dao.id,
                                            batchSize=None)
        for mag in cleanMagazzini:
            mag.delete()
        for m in model:
            if m[3] == 'deleted':
                pass
            else:
                daoListinoMagazzino = ListinoMagazzino().getRecord()
                daoListinoMagazzino.id_listino = self.dao.id
                daoListinoMagazzino.id_magazzino = m[0]
                daoListinoMagazzino.persist()

        #self.dao.persist()

        self._refreshCategorieClienti()
        self._refreshMagazzini()


    def on_add_row_categoria_button_clicked(self, widget):
        id = findIdFromCombobox(self.id_categoria_cliente_customcombobox.combobox)
        if id is not None:
            categoria = findStrFromCombobox(self.id_categoria_cliente_customcombobox.combobox, 2)
            model = self.categorie_treeview.get_model()
            for c in model:
                if c[0] == id:
                    return
            image = gtk.Image()
            anagPixbuf = image.render_icon(gtk.STOCK_ADD,
                                           gtk.ICON_SIZE_BUTTON)
            model.append((id, categoria, anagPixbuf, 'added'))
        self.categorie_treeview.get_selection().unselect_all()


    def on_add_row_magazzino_button_clicked(self, widget):
        id = findIdFromCombobox(self.id_magazzino_customcombobox.combobox)
        if id is not None:
            magazzino = findStrFromCombobox(self.id_magazzino_customcombobox.combobox, 2)
            model = self.magazzini_treeview.get_model()
            for m in model:
                if m[0] == id:
                    return
            image = gtk.Image()
            anagPixbuf = image.render_icon(gtk.STOCK_ADD,
                                           gtk.ICON_SIZE_BUTTON)
            model.append((id, magazzino, anagPixbuf, 'added'))
        self.magazzini_treeview.get_selection().unselect_all()


    def on_delete_row_categoria_button_clicked(self, widget):
        id = findIdFromCombobox(self.id_categoria_cliente_customcombobox.combobox)
        if id is not None:
            image = gtk.Image()
            anagPixbuf = image.render_icon(gtk.STOCK_REMOVE,
                                           gtk.ICON_SIZE_BUTTON)
            model = self.categorie_treeview.get_model()
            for c in model:
                if c[0] == id:
                    if c[2] is None:
                        c[2] = anagPixbuf
                        c[3] = 'deleted'
                    else:
                        model.remove(c.iter)
        self.categorie_treeview.get_selection().unselect_all()


    def on_delete_row_magazzino_button_clicked(self, widget):
        id = findIdFromCombobox(self.id_magazzino_customcombobox.combobox)
        if id is not None:
            image = gtk.Image()
            anagPixbuf = image.render_icon(gtk.STOCK_REMOVE,
                                           gtk.ICON_SIZE_BUTTON)
            model = self.magazzini_treeview.get_model()
            for m in model:
                if m[0] == id:
                    if m[2] is None:
                        m[2] = anagPixbuf
                        m[3] = 'deleted'
                    else:
                        model.remove(m.iter)
        self.magazzini_treeview.get_selection().unselect_all()


    def on_undelete_row_categoria_button_clicked(self, widget):
        id = findIdFromCombobox(self.id_categoria_cliente_customcombobox.combobox)
        if id is not None:
            model = self.categorie_treeview.get_model()
            for c in model:
                if c[0] == id:
                    if c[3] == 'deleted':
                        c[2] = None
                        c[3] = None
        self.categorie_treeview.get_selection().unselect_all()


    def on_undelete_row_magazzino_button_clicked(self, widget):
        id = findIdFromCombobox(self.id_magazzino_customcombobox.combobox)
        if id is not None:
            model = self.magazzini_treeview.get_model()
            for m in model:
                if m[0] == id:
                    if m[3] == 'deleted':
                        m[2] = None
                        m[3] = None
        self.magazzini_treeview.get_selection().unselect_all()


    def on_categorie_treeview_cursor_changed(self, treeview):
        sel = treeview.get_selection()
        (model, iterator) = sel.get_selected()
        if iterator is not None:
            idCategoriaCliente = model.get_value(iterator, 0)
            findComboboxRowFromId(self.id_categoria_cliente_customcombobox.combobox, idCategoriaCliente)
            status = model.get_value(iterator, 3)
            self.delete_row_categoria_button.set_sensitive(status != 'deleted')
            self.undelete_row_categoria_button.set_sensitive(status == 'deleted')


    def on_magazzini_treeview_cursor_changed(self, treeview):
        sel = treeview.get_selection()
        (model, iterator) = sel.get_selected()
        if iterator is not None:
            idMagazzino = model.get_value(iterator, 0)
            findComboboxRowFromId(self.id_magazzino_customcombobox.combobox, idMagazzino)
            status = model.get_value(iterator, 3)
            self.delete_row_magazzino_button.set_sensitive(status != 'deleted')
            self.undelete_row_magazzino_button.set_sensitive(status == 'deleted')


    def on_listini_articoli_togglebutton_clicked(self, toggleButton):
        if not(toggleButton.get_active()):
            toggleButton.set_active(False)
            return

        if self.dao.id is None:
            msg = 'Prima di poter inserire gli articoli occorre salvare il listino.\n Salvare ?'
            dialog = gtk.MessageDialog(self.dialogTopLevel, gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
                                       gtk.MESSAGE_QUESTION, gtk.BUTTONS_YES_NO, msg)
            response = dialog.run()
            dialog.destroy()
            if response == gtk.RESPONSE_YES:
                self.on_anagrafica_complessa_detail_dialog_response(self.dialogTopLevel, gtk.RESPONSE_APPLY)
            else:
                toggleButton.set_active(False)
                return

        from AnagraficaListiniArticoli import AnagraficaListiniArticoli
        anag = AnagraficaListiniArticoli(idListino=self.dao.id)
        anagWindow = anag.getTopLevel()

        showAnagraficaRichiamata(self.dialogTopLevel, anagWindow, toggleButton)
