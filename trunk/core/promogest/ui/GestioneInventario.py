# -*- coding: utf-8 -*-

# Promogest
#
# Copyright (C) 2005 by Promotux Informatica - http://www.promotux.it/
# Author: Andrea Argiolas <andrea@promotux.it>
# Author: Francesco Meloni <francesco@promotux.it>

import gtk, gobject, os
from datetime import datetime, timedelta
from RicercaComplessaArticoli import RicercaComplessaArticoli
from promogest import Environment
from promogest.dao.Inventario import Inventario
from promogest.dao.TestataMovimento import TestataMovimento
from promogest.dao.RigaMovimento import RigaMovimento
from promogest.dao.Riga import Riga
from promogest.dao.Magazzino import Magazzino
from promogest.dao.Articolo import Articolo
from promogest.ui.GladeWidget import GladeWidget
from utils import *


class GestioneInventario(RicercaComplessaArticoli):
    """ Gestione inventario di magazzino """

    def __init__(self, idMagazzino = None):

        # aggiornamento inventario con gli articoli eventualmente non presenti
        #self.update()

        # filtri propri della parte inventario
        self.additional_filter = GladeWidget(rootWidget='inventario_filter_table')
        fillComboboxMagazzini(self.additional_filter.id_magazzino_filter_combobox2, noempty=True)
        if idMagazzino is not None:
            findComboboxRowFromId(self.additional_filter.id_magazzino_filter_combobox2,
                                  idMagazzino)
        # aggiunta della parte di dettaglio
        self._modifica = GladeWidget(rootWidget='inventario_detail_vbox')

        RicercaComplessaArticoli.__init__(self)

        # modifiche all'interfaccia originaria
        self.getTopLevel().set_title('Promogest - Gestione inventario ' + Environment.workingYear)
        self.search_image.set_no_show_all(True)
        self.search_image.set_property('visible', False)
        self.filter.filter_search_button.set_label('_Seleziona')
        self.buttons_hbox.destroy()
        self._ricerca.varie_articolo_filter_expander.set_no_show_all(True)
        self._ricerca.varie_articolo_filter_expander.set_property('visible', False)
        self.anno = int(Environment.workingYear)
        self.annoScorso= int(Environment.workingYear) -1
        # aggiunta dei filtri propri e della parte di dettaglio
        self.filters.ricerca_avanzata_articoli_filter_filters_vbox.pack_start(self.additional_filter.getTopLevel(), expand=False)
        self.filters.ricerca_avanzata_articoli_filter_filters_vbox.reorder_child(self.additional_filter.getTopLevel(), 0)
        self.results_vbox.pack_start(self._modifica.getTopLevel(),expand=False)

        self.additional_filter.id_magazzino_filter_combobox2.connect('changed',
                                                                    self.on_filter_field_changed)
        self.additional_filter.da_data_aggiornamento_filter_entry.connect('focus_out_event',
                                                                          self.on_filter_field_changed)
        self.additional_filter.a_data_aggiornamento_filter_entry.connect('focus_out_event',
                                                                         self.on_filter_field_changed)

        #self._modifica.quantita_entry.connect('key_press_event', self.detail_key_press_event)
        #self._modifica.valore_unitario_entry.connect('key_press_event', self.detail_key_press_event)

        self._modifica.azzera_button.connect('clicked', self.on_azzera_button_clicked)
        self._modifica.ricrea_button.connect('clicked', self.on_ricrea_button_clicked)
        self._modifica.aggiorna_button.connect('clicked', self.on_aggiorna_button_clicked)
        self._modifica.esporta_button.connect('clicked', self.on_esporta_button_clicked)
        self._modifica.valorizza_button.connect('clicked', self.on_valorizza_button_clicked)
        self._modifica.movimento_button.connect('clicked', self.on_movimento_button_clicked)
        self._modifica.chiudi_button.connect('clicked', self.on_chiudi_button_clicked)
        self.setRiepilogo()

        #print sel2, sel

    def draw(self):
        """ Disegna la treeview relativa al risultato del filtraggio """
        treeview = self.filter.resultsElement
        model = gtk.ListStore(object, str, str, str, str, str, str, str, str, str, str, str)
        rendererSx = gtk.CellRendererText()
        rendererDx = gtk.CellRendererText()
        rendererDx.set_property('xalign', 1)

        cellspin = gtk.CellRendererSpin()
        cellspin.set_property("editable", True)
        cellspin.set_property("visible", True)
        adjustment = gtk.Adjustment(1, 1, 1000,0.500,2)
        cellspin.set_property("adjustment", adjustment)
        cellspin.set_property("digits",2)
        cellspin.set_property("climb-rate",3)
        cellspin.set_property('xalign', 1)
        cellspin.connect('edited', self.on_column_quantita_edited, treeview, True)
        column = gtk.TreeViewColumn('Quantità', cellspin, text=1)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        #column.set_clickable(False)
        column.set_resizable(True)
        column.set_expand(False)
        column.set_min_width(50)
        treeview.append_column(column)


        cellspin1 = gtk.CellRendererSpin()
        cellspin1.set_property("editable", True)
        cellspin1.set_property("visible", True)
        adjustment = gtk.Adjustment(1, 1, 1000,0.500,2)
        cellspin1.set_property("adjustment", adjustment)
        cellspin1.set_property("digits",2)
        cellspin1.set_property("climb-rate",3)
        cellspin1.set_property('xalign', 1)
        cellspin1.connect('edited', self.on_column_valore_unitario_edited, treeview, True)
        column = gtk.TreeViewColumn('Valore unitario', cellspin1, text=2)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(False)
        column.set_resizable(True)
        column.set_expand(False)
        column.set_min_width(70)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Unita\' base', rendererSx, text=3)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        column.connect("clicked", self.filter._changeOrderBy, 'denominazione_breve_unita_base')
        column.set_resizable(True)
        column.set_expand(False)
        column.set_min_width(30)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Data aggiornamento', rendererSx, text=4)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        column.connect("clicked", self.filter._changeOrderBy, 'data_aggiornamento')
        column.set_resizable(True)
        column.set_expand(False)
        column.set_min_width(100)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Codice articolo', rendererSx, text=5)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        column.connect("clicked", self.filter._changeOrderBy, 'codice_articolo')
        column.set_resizable(True)
        column.set_expand(False)
        column.set_min_width(100)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Descrizione', rendererSx, text=6)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        column.connect("clicked", self.filter._changeOrderBy, 'articolo')
        column.set_resizable(True)
        column.set_expand(True)
        column.set_min_width(250)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Produttore', rendererSx, text=7)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        column.connect("clicked", self.filter._changeOrderBy, 'produttore')
        column.set_resizable(True)
        column.set_expand(False)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Famiglia', rendererSx, text=8)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        column.connect("clicked", self.filter._changeOrderBy, 'denominazione_famiglia')
        column.set_resizable(True)
        column.set_expand(False)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Categoria', rendererSx, text=9)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        column.connect("clicked", self.filter._changeOrderBy, 'denominazione_categoria')
        column.set_resizable(True)
        column.set_expand(False)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Codice articolo fornitore', rendererSx, text=11)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        column.connect("clicked", self.filter._changeOrderBy, 'codice_articolo_fornitore')
        column.set_resizable(True)
        column.set_expand(False)
        treeview.append_column(column)

        treeview.set_search_column(4)
        treeview.set_model(model)

    def setInitialSearch(self):
        """ Imposta il tipo di ricerca iniziale """
        self._ricerca.setRicercaAvanzata()
        self._ricerca.ricerca_semplice_articoli_button.set_no_show_all(True)
        self._ricerca.ricerca_semplice_articoli_button.set_property('visible', False)


    def refresh(self):
        """ Esegue il filtraggio in base ai filtri impostati e aggiorna la treeview """
        self.anno = int(Environment.workingYear)
        self.annoScorso= int(Environment.workingYear) -1
        if (findIdFromCombobox(self.additional_filter.id_magazzino_filter_combobox2) is None):
            obligatoryField(self.getTopLevel(),
                            self.additional_filter.id_magazzino_filter_combobox2,
                            'Inserire il magazzino !')

        idMagazzino = findIdFromCombobox(self.additional_filter.id_magazzino_filter_combobox2)
        daData = stringToDate(self.additional_filter.da_data_aggiornamento_filter_entry.get_text())
        aData = stringToDate(self.additional_filter.a_data_aggiornamento_filter_entry.get_text())

        model = self.filter.resultsElement.get_model()

        self._ricerca._prepare()

        self.filter.numRecords = Inventario().count(anno=self.anno,
                                                    idMagazzino=idMagazzino,
                                                    daDataAggiornamento=daData,
                                                    aDataAggiornamento=aData)

        self.filter._refreshPageCount()

        invs = Inventario().select(orderBy=self.filter.orderBy,
                                               anno=self.anno,
                                               idMagazzino=idMagazzino,
                                               daDataAggiornamento=daData,
                                               aDataAggiornamento=aData,
                                               offset=self.filter.offset,
                                               batchSize=self.filter.batchSize)

        model.clear()

        for i in invs:
            model.append((i,
                          ('%8.3f') % float(i.quantita or 0),
                          ('%14.' + Environment.conf.decimals + 'f') % float(i.valore_unitario or 0),
                          (i.denominazione_breve_unita_base or ''),
                          dateToString(i.data_aggiornamento),
                          (i.codice_articolo or ''),
                          (i.articolo or ''),
                          (i.produttore or ''),
                          (i.denominazione_famiglia or ''),
                          (i.denominazione_categoria or ''),
                          (i.codice_a_barre or ''),
                          (i.codice_articolo_fornitore or '')))


    def on_filter_treeview_row_activated(self, treeview, path, column):
        """ Rileva la riga attualmente selezionata e aggiorna il dettaglio """
        self.refreshDetail()


    def _changeTreeViewSelectionType(self):
        """ Imposta la modalita' di selezione nella treeview ad una sola riga """
        selection = self.filter.resultsElement.get_selection()
        selection.set_mode(gtk.SELECTION_SINGLE)


    def on_filter_field_changed(self, widget=None, event=None):
        """ Aggiorna il testo del riepilogo perche' almeno uno dei filtri propri e' cambiato """
        self.setRiepilogo()


    def setRiepilogo(self):
        """ Aggiorna il testo del riepilogo """
        testo = ''
        if self.additional_filter.id_magazzino_filter_combobox2.get_active() != -1:
            value = findStrFromCombobox(self.additional_filter.id_magazzino_filter_combobox2, 2)
            testo += '  Magazzino:\n'
            testo += '       ' + value + '\n'
        value = self.additional_filter.da_data_aggiornamento_filter_entry.get_text()
        if value != '':
            testo += '  Da data aggiornamento:\n'
            testo += '       ' + value + '\n'
        value = self.additional_filter.a_data_aggiornamento_filter_entry.get_text()
        if value != '':
            testo += '  A data aggiornamento:\n'
            testo += '       ' + value + '\n'

        self.setSummaryTextBefore(testo)


    #def refreshDetail(self):
        #""" Aggiorna il dettaglio relativo alla riga attualmente selezionata """
        #self._modifica.articolo_label.set_markup('<b>' + self.dao.codice_articolo + '  ' + self.dao.articolo + '</b>')
        #self._modifica.unita_base_label1.set_text('(' + self.dao.denominazione_breve_unita_base + ')')
        #self._modifica.quantita_entry.set_text('%8.3f' % float(self.dao.quantita or 0))
        #self._modifica.valore_unitario_entry.set_text(('%14.' + Environment.conf.decimals + 'f') % float(self.dao.valore_unitario or 0))
        #self._modifica.quantita_entry.grab_focus()


    #def detail_key_press_event(self, widget=None, event=None):
        #""" Aggiorna i dati relativi alla riga selezionata e passa alla successiva """
        #keyname = gtk.gdk.keyval_name(event.keyval)
        #if keyname == 'Return' or keyname == 'KP_Enter':
            #self.confirm()
            #self.next()
        #return False

    def on_column_quantita_edited(self, cell, path, value, treeview, editNext=True):
        """ Function ti set the value quantita edit in the cell """
        model = treeview.get_model()
        value=value.replace(",",".")
        value = mN(value)
        model[path][1] = value
        #model[path][4] = dateToString(datetime.datetime.today().date())
        quantita = float(value)
        valore_unitario = float(model[path][2])
        data = model[path][4] or datetime.datetime.today().date()
        dao = Inventario().getRecord(id=self.dao.id)
        dao.anno = self.dao.anno
        dao.id_magazzino = self.dao.id_magazzino
        dao.id_articolo = self.dao.id_articolo
        dao.quantita = quantita
        dao.valore_unitario = valore_unitario
        dao.data_aggiornamento = data
        Environment.params['session'].add(dao)
        Environment.params['session'].commit()
        #dao.persist()

        #self.refreshTotal()
        #self.on_cancel_button_clicked(self.getTopLevel)

    def on_column_valore_unitario_edited(self, cell, path, value, treeview, editNext=True):
        """ Function ti set the value quantita edit in the cell """
        model = treeview.get_model()
        value=value.replace(",",".")
        value = mN(value)
        model[path][2] = value
        model[path][4] = dateToString(datetime.datetime.today().date())
        valore_unitario = float(value)
        quantita= float(model[path][2])
        data = model[path][4] or datetime.datetime.today().date()
        dao = Inventario().getRecord(id=self.dao.id)
        dao.anno = self.dao.anno
        dao.id_magazzino = self.dao.id_magazzino
        dao.id_articolo = self.dao.id_articolo
        dao.quantita = quantita
        dao.valore_unitario = valore_unitario
        dao.data_aggiornamento = data
        Environment.params['session'].add(dao)
        Environment.params['session'].commit()
        #dao.persist()
        #self.next()
        #self.refreshTotal()
        #self.on_cancel_button_clicked(self.getTopLevel)


    #def confirm(self):
        #""" Aggiorna i dai relativi al dao corrente """
        #self.dao.quantita = float(self._modifica.quantita_entry.get_text())
        #self.dao.valore_unitario = float(self._modifica.valore_unitario_entry.get_text())
        #self.dao.data_aggiornamento = datetime.datetime.today().date()

        #dao = Inventario().getRecord(id=self.dao.id)
        #dao.anno = self.dao.anno
        #dao.id_magazzino = self.dao.id_magazzino
        #dao.id_articolo = self.dao.id_articolo
        #dao.quantita = self.dao.quantita
        #dao.valore_unitario = self.dao.valore_unitario
        #dao.data_aggiornamento = self.dao.data_aggiornamento
        #dao.persist()

        #treeview = self.filter.resultsElement
        #selection = treeview.get_selection()
        #(model, iterator) = selection.get_selected()

        #model.set_value(iterator, 0, self.dao)
        #model.set_value(iterator, 1, '%8.3f' % float(self.dao.quantita or 0))
        #model.set_value(iterator, 2, ('%14.' + Environment.conf.decimals + 'f') % float(self.dao.valore_unitario or 0))
        #model.set_value(iterator, 4, dateToString(self.dao.data_aggiornamento))


    def next(self):
        """ Passa alla riga successiva della treeview """
        treeview = self.filter.resultsElement
        selection = treeview.get_selection()
        (model, iterator) = selection.get_selected()
        nextIter = model.iter_next(iterator)
        if nextIter is not None:
            path = model.get_path(nextIter)
            selection.select_path(path)
            treeview.scroll_to_cell(path)
            self.on_filter_treeview_cursor_changed(treeview)
        else:
            if not(self.filter.isLastPage()):
                self.filter.filter_next_button.clicked()
                path=model.get_path(model.get_iter_root())
                selection.select_path(path)
                treeview.scroll_to_cell(path)
                self.on_filter_treeview_cursor_changed(treeview)


    def on_azzera_button_clicked(self, button):
        msg = """ATTENZIONE!!!
    Stai per cancellare il precedente inventario,
    il movimento di magazzino e successivo
    valorizzazione e quantificazione
    delle giacenze. Conferma SOLO
    se sei sicuro di quel che stai per fare.
        Confermi la cancellazione ?"""
        dialog = gtk.MessageDialog(self.getTopLevel(),
                                gtk.DIALOG_MODAL
                                | gtk.DIALOG_DESTROY_WITH_PARENT,
                                gtk.MESSAGE_QUESTION, gtk.BUTTONS_YES_NO,
                                msg)

        response = dialog.run()
        dialog.destroy()
        if response ==  gtk.RESPONSE_YES:
            print "cancello TUTTO IL MOVIMENTO INVENTARIO"
            idMagazzino = findIdFromCombobox(self.additional_filter.id_magazzino_filter_combobox2)
            sel2 = Environment.params['session']\
                            .query(Inventario)\
                            .filter(and_(Inventario.anno ==self.anno,
                                    Inventario.id_magazzino==idMagazzino))\
                            .all()


            for s in sel2:
                Environment.params['session'].delete(s)
            Environment.params['session'].commit()
                #s.delete()
            dat = '01/01/' + str(self.anno)
            data = stringToDate(dat)
            OneDay = datetime.timedelta(days=1)
            aData= data+OneDay
            movimento = TestataMovimento().select(daData = data,
                                                    aData= aData,
                                                    idOperazione= "Carico per inventario")
            if movimento:
                movimento.delete()
            model = self.filter.resultsElement.get_model()
            model.clear()
            return True

    def on_ricrea_button_clicked(self, button):

        def calcolaGiacenza(quantita=None, moltiplicatore=None, segno=None, valunine=None):
                giacenza=0
                if segno =="-":
                    giacenza -= quantita*moltiplicatore
                else:
                    giacenza += quantita*moltiplicatore
                valore= giacenza*valunine
                return (giacenza, valore)

        """ Verifica se esistono gia' delle righe di inventario nell'anno di esercizio """
        idMagazzino = findIdFromCombobox(self.additional_filter.id_magazzino_filter_combobox2)
        res = Inventario().select(anno=self.anno,
                                    idMagazzino=idMagazzino)

        print "REEEEEEEEEEEEEEEEEEEESSS PER INVENTARIO", res
        if res:
            dialog = gtk.MessageDialog(self.getTopLevel(), gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
                                   gtk.MESSAGE_INFO, gtk.BUTTONS_OK, '\nElaborazione Impossibile !')
            response = dialog.run()
            dialog.destroy()
            return
        else:
            giacenza = 0
            #sel2 = Environment.params['session'].query(Inventario.id_magazzino, Inventario.id_articolo).filter(Inventario.anno ==Environment.workingYear).all()
            sel = Environment.params['session'].query(Magazzino.id, Articolo.id)\
                                                .filter(Articolo.cancellato != True).all()
            for s in sel:
                righeArticoloMovimentate=  Environment.params["session"]\
                    .query(RigaMovimento,TestataMovimento)\
                    .filter(and_(func.date_part("year", TestataMovimento.data_movimento)==(int(Environment.workingYear)-1)))\
                    .filter(RigaMovimento.id_testata_movimento == TestataMovimento.id)\
                    .filter(Riga.id_articolo==s[1])\
                    .filter(Riga.id_magazzino==s[0])\
                    .filter(Articolo.cancellato!=True)\
                    .all()

                for ram in righeArticoloMovimentate:
                    giacenza = calcolaGiacenza(quantita=ram[0].quantita,
                                                moltiplicatore=ram[0].moltiplicatore,
                                                segno=ram[1].segnoOperazione,
                                                valunine=ram[0].valore_unitario_netto)[0]
                    giacenza +=giacenza
                #if s not in sel2:
                inv = Inventario()
                inv.anno = Environment.workingYear
                inv.id_magazzino = s[0]
                inv.quantita = giacenza
                inv.id_articolo = s[1]
                Environment.params['session'].add(inv)

                #inv.persist()
            print "RICREA"
            Environment.params['session'].commit()
            self.refresh()

    def on_aggiorna_button_clicked(self, button):
        """ Aggiornamento inventario con gli articoli eventualmente non presenti """
        #Environment.connection.execStoredProcedure('InventarioUpd', (int(Environment.conf.workingYear),))
        #sql_statement:= \'INSERT INTO inventario (anno, id_magazzino, id_articolo, quantita, valore_unitario, data_aggiornamento)
                            #(SELECT \' || _anno || \', M.id, A.id, NULL, NULL, NULL
                            #FROM magazzino M CROSS JOIN articolo A
                            #WHERE (M.id, A.id) NOT IN (SELECT I.id_magazzino, I.id_articolo FROM INVENTARIO I WHERE I.anno = \' || _anno || \')
                            #AND A.cancellato <> True)\';
        sel2 = Environment.params['session'].query(Inventario.id_magazzino, Inventario.id_articolo).filter(Inventario.anno ==Environment.workingYear).all()
        sel = Environment.params['session'].query(Magazzino.id, Articolo.id).filter(Articolo.cancellato != True).all()
        print "AGGIORNA"
        for s in sel:
            if s not in sel2:
                inv = Inventario()
                inv.anno = Environment.workingYear
                inv.id_magazzino = s[0]
                inv.id_articolo = s[1]
                Environment.params['session'].add(inv)
        Environment.params['session'].commit()
        self.refresh()

    def on_esporta_button_clicked(self, button):
        """ Esportazione inventario in formato csv """
        if (findIdFromCombobox(self.additional_filter.id_magazzino_filter_combobox2) is None):
            obligatoryField(self.getTopLevel(),
                            self.additional_filter.id_magazzino_filter_combobox2,
                            'Inserire il magazzino !')

        idMagazzino = findIdFromCombobox(self.additional_filter.id_magazzino_filter_combobox2)

        fileDialog = gtk.FileChooserDialog(title='Esportazione inventario ',
                                           parent=self.getTopLevel(),
                                           action=gtk.FILE_CHOOSER_ACTION_SAVE,
                                           buttons=(gtk.STOCK_CANCEL,
                                                    gtk.RESPONSE_CANCEL,
                                                    gtk.STOCK_SAVE,
                                                    gtk.RESPONSE_OK),
                                           backend=None)


        folder = ''
        if hasattr(Environment.conf,'Documenti'):
            folder = getattr(Environment.conf.Documenti,'cartella_predefinita','')
        if folder == '':
            if os.name == 'posix':
                folder = os.environ['HOME']
            elif os.name == 'nt':
                folder = os.environ['USERPROFILE']
        fileDialog.set_current_folder(folder)

        fltr = gtk.FileFilter()
        fltr.add_pattern("*.csv")
        fltr.set_name('File CSV (*.csv)')
        fileDialog.add_filter(fltr)

        fileDialog.set_current_name('inv_' + Environment.workingYear + '.csv')

        response = fileDialog.run()
        if response == gtk.RESPONSE_OK:
            filename = fileDialog.get_filename()
            fileDialog.destroy()

            f = open(filename,'w')
            riga = ('Codice, Descrizione, Quantita\', Valore unitario, U.M., ' +
                    'Codice a barre, Famiglia, Categoria\n')
            f.write(riga)
            invs = Inventario().select(anno=Environment.conf.workingYear,
                                                    idMagazzino=idMagazzino,
                                                    offset=None,
                                                    batchSize=None)


            for i in invs:
                quantita = '%14.4f' % float(i.quantita or 0)
                quantita = quantita.replace('.',',')
                valore = '%14.4f' % float(i.valore_unitario or 0)
                valore = valore.replace('.',',')
                riga = ('"' + str(i.codice_articolo or '') + '",' +
                        '"' + str(i.articolo or '') + '",' +
                        '"' + quantita + '",' +
                        '"' + valore + '",' +
                        '"' + str(i.denominazione_breve_unita_base or '') + '",' +
                        '"' + str(i.codice_a_barre or '') + '",' +
                        '"' + str(i.denominazione_famiglia or '') + '",' +
                        '"' + str(i.denominazione_categoria or '') + '"\n')
                f.write(riga)
            f.close()
        else:
            fileDialog.destroy()
            return


    def on_valorizza_button_clicked(self, button):
        """ Valorizzazione inventario (modifica automatica del valore unitario) """
        dialog = gtk.Dialog('Attenzione',
                            self.getTopLevel(),
                            gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
                            None)
        hbox = gtk.HBox()
        image = gtk.image_new_from_stock(gtk.STOCK_DIALOG_QUESTION, gtk.ICON_SIZE_DIALOG)
        image.set_padding(10,10)
        label = gtk.Label('Verranno aggiornati i valori unitari non ancora\nspecificati secondo la modalita\' scelta.')
        label.set_justify(gtk.JUSTIFY_LEFT)
        label.set_alignment(0,0)
        label.set_padding(15,10)
        hbox.pack_start(image, False, False, 0)
        hbox.pack_start(label, True, True, 0)
        dialog.vbox.pack_start(hbox, True, True, 0)

        buttonAcquistoUltimo = gtk.Button(label = 'Ultimo prezzo\n di acquisto')
        buttonAcquistoUltimo.connect('clicked', self.on_buttonAcquistoUltimo_clicked)
        buttonVenditaUltimo = gtk.Button(label = 'Ultimo prezzo\n di vendita')
        buttonVenditaUltimo.connect('clicked', self.on_buttonVenditaUltimo_clicked)
        buttonAcquistoMedio = gtk.Button(label = 'Prezzo medio\n di acquisto')
        buttonAcquistoMedio.connect('clicked', self.on_buttonAcquistoMedio_clicked)
        buttonVenditaMedio = gtk.Button(label = 'Prezzo medio\n di vendita')
        buttonVenditaMedio.connect('clicked', self.on_buttonVenditaMedio_clicked)
        dialog.action_area.pack_start(buttonAcquistoUltimo)
        dialog.action_area.pack_start(buttonVenditaUltimo)
        dialog.action_area.pack_start(buttonAcquistoMedio)
        dialog.action_area.pack_start(buttonVenditaMedio)

        dialog.show_all()
        result = dialog.run()
        dialog.destroy()


    def confermaValorizzazione(self):
        """ Chiede conferma per la modifica dei dati """
        dialog = gtk.MessageDialog(self.getTopLevel(),
                                   gtk.DIALOG_MODAL
                                   | gtk.DIALOG_DESTROY_WITH_PARENT,
                                   gtk.MESSAGE_QUESTION, gtk.BUTTONS_YES_NO,
                                   'Confermi l\'elaborazione ?')

        response = dialog.run()
        dialog.destroy()
        return (response ==  gtk.RESPONSE_YES)


    def fineElaborazione(self):
        """ Messaggio di fine elaborazione """
        dialog = gtk.MessageDialog(self.getTopLevel(), gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
                                   gtk.MESSAGE_INFO, gtk.BUTTONS_OK, '\nElaborazione terminata !')
        response = dialog.run()
        dialog.destroy()


    def on_buttonAcquistoUltimo_clicked(self, button):
        """ Valorizzazione a ultimo prezzo di acquisto
        sql_stateme nt:= \'CREATE TEMPORARY TABLE valorizzazione_tmp AS
                                (SELECT R.id_magazzino, R.id_articolo,
                                 MAX(R.valore_unitario_netto) AS prezzo,
                                 MAX(TM.data_movimento) AS data
                                 FROM riga_movimento RM INNER JOIN riga R ON RM.id = R.id
                                 INNER JOIN testata_movimento TM ON RM.id_testata_movimento = TM.id
                                 INNER JOIN promogest.operazione O ON TM.operazione = O.denominazione
                                 WHERE (R.valore_unitario_netto <> 0 AND O.segno = \'\'+\'\' AND
                                        DATE_PART(\'\'year\'\', TM.data_movimento) = \' || _anno_prec || \' AND
                                        R.id_magazzino = \' || _id_magazzino || \')
                                 GROUP BY R.id_magazzino, R.id_articolo) \';
        EXECUTE sql_statement;
        sql_statement:= \'UPDATE inventario SET valore_unitario = (SELECT prezzo FROM valorizzazione_tmp T WHERE inventario.id_magazzino = T.id_magazzino AND inventario.id_articolo = T.id_articolo) WHERE anno = \' || _anno || \' AND (valore_unitario IS NULL OR valore_unitario = 0)\';
        EXECUTE sql_statement;"""
        if self.confermaValorizzazione():
            idMagazzino = findIdFromCombobox(self.additional_filter.id_magazzino_filter_combobox2)
            sel = Inventario().select(batchSize= None)
            for s in sel:
                righeArticoloMovimentate=  Environment.params["session"]\
                    .query(RigaMovimento,TestataMovimento)\
                    .filter(and_(func.date_part("year", TestataMovimento.data_movimento)==(int(Environment.workingYear)-1)))\
                    .filter(RigaMovimento.id_testata_movimento == TestataMovimento.id)\
                    .filter(Riga.id_articolo==s.id_articolo)\
                    .filter(Riga.id_magazzino==idMagazzino)\
                    .filter(Riga.valore_unitario_netto!=0)\
                    .filter(Operazione.segno=="+")\
                    .filter(Articolo.cancellato!=True)\
                    .all()

                print righeArticoloMovimentate,
                date = []
                for r in righeArticoloMovimentate:
                    date.append(r[1].data_movimento)
                if date:
                    print "DATEEEEEEEEEEEEEEEEEEEEE", date
                    k = max(date)
                    print "KAAAAAAAAAAAAAAAAAAPPA", k
                inv = Inventario().getRecord(id=s.id)
                #inv.valore_unitario = 
                #inv.anno = self.anno
                #inv.id_magazzino = idMagazzino
                #inv.quantita = giacenza
                #inv.id_articolo = s.id_articolo
                #Environment.params['session'].add(inv)

                #inv.persist()
            print "RICREA"
            Environment.params['session'].commit()
            self.refresh()

            #idMagazzino = findIdFromCombobox(self.additional_filter.id_magazzino_filter_combobox)
            #Environment.connection.execStoredProcedure('InventarioPrezzoAcquistoUltimoUpd', (int(Environment.conf.workingYear), idMagazzino))
            #self.refresh()
            self.fineElaborazione()


    def on_buttonVenditaUltimo_clicked(self, button):
        """ Valorizzazione a ultimo prezzo di vendita
        sql_statement:= \'CREATE TEMPORARY TABLE valorizzazione_tmp AS
                                (SELECT R.id_magazzino, R.id_articolo,
                                 MAX(R.valore_unitario_netto) AS prezzo,
                                 MAX(TM.data_movimento) AS data
                                 FROM riga_movimento RM INNER JOIN riga R ON RM.id = R.id
                                 INNER JOIN testata_movimento TM ON RM.id_testata_movimento = TM.id
                                 INNER JOIN promogest.operazione O ON TM.operazione = O.denominazione
                                 WHERE (R.valore_unitario_netto <> 0 AND O.segno = \'\'-\'\' AND
                                        DATE_PART(\'\'year\'\', TM.data_movimento) = \' || _anno_prec || \' AND
                                        R.id_magazzino = \' || _id_magazzino || \')
                                 GROUP BY R.id_magazzino, R.id_articolo) \';
        EXECUTE sql_statement;
        sql_statement:= \'UPDATE inventario SET valore_unitario = (SELECT prezzo FROM valorizzazione_tmp T WHERE inventario.id_magazzino = T.id_magazzino AND inventario.id_articolo = T.id_articolo) WHERE anno = \' || _anno || \' AND (valore_unitario IS NULL OR valore_unitario = 0)\';
        EXECUTE sql_statement;"""
        if self.confermaValorizzazione():
            idMagazzino = findIdFromCombobox(self.additional_filter.id_magazzino_filter_combobox)
            Environment.connection.execStoredProcedure('InventarioPrezzoVenditaUltimoUpd', (int(Environment.conf.workingYear), idMagazzino))
            self.refresh()
            self.fineElaborazione()


    def on_buttonAcquistoMedio_clicked(self, button):
        """ Valorizzazione a prezzo medio di acquisto
        sql_statement:= \'CREATE TEMPORARY TABLE valorizzazione_tmp AS
                                (SELECT R.id_magazzino, R.id_articolo,
                                 AVG(R.valore_unitario_netto) AS prezzo
                                 FROM riga_movimento RM INNER JOIN riga R ON RM.id = R.id
                                 INNER JOIN testata_movimento TM ON RM.id_testata_movimento = TM.id
                                 INNER JOIN promogest.operazione O ON TM.operazione = O.denominazione
                                 WHERE (R.valore_unitario_netto <> 0 AND O.segno = \'\'+\'\' AND
                                        DATE_PART(\'\'year\'\', TM.data_movimento) = \' || _anno_prec || \' AND
                                        R.id_magazzino = \' || _id_magazzino || \')
                                 GROUP BY R.id_magazzino, R.id_articolo) \';
        EXECUTE sql_statement;

        sql_statement:= \'UPDATE inventario SET valore_unitario = (SELECT prezzo FROM valorizzazione_tmp T WHERE inventario.id_magazzino = T.id_magazzino AND inventario.id_articolo = T.id_articolo) WHERE anno = \' || _anno || \' AND (valore_unitario IS NULL OR valore_unitario = 0)\';
        EXECUTE sql_statement;"""
        if self.confermaValorizzazione():
            idMagazzino = findIdFromCombobox(self.additional_filter.id_magazzino_filter_combobox)
            Environment.connection.execStoredProcedure('InventarioPrezzoAcquistoMedioUpd', (int(Environment.conf.workingYear), idMagazzino))
            self.refresh()
            self.fineElaborazione()


    def on_buttonVenditaMedio_clicked(self, button):
        """ Valorizzazione a prezzo medio di vendita
        sql_statement:= \'CREATE TEMPORARY TABLE valorizzazione_tmp AS
                        (SELECT R.id_magazzino, R.id_articolo,
                            AVG(R.valore_unitario_netto) AS prezzo
                            FROM riga_movimento RM INNER JOIN riga R ON RM.id = R.id
                            INNER JOIN testata_movimento TM ON RM.id_testata_movimento = TM.id
                            INNER JOIN promogest.operazione O ON TM.operazione = O.denominazione
                            WHERE (R.valore_unitario_netto <> 0 AND O.segno = \'\'-\'\' AND
                                DATE_PART(\'\'year\'\', TM.data_movimento) = \' || _anno_prec || \' AND
                                R.id_magazzino = \' || _id_magazzino || \')
                            GROUP BY R.id_magazzino, R.id_articolo) \';
        EXECUTE sql_statement;
        sql_statement:= \'UPDATE inventario SET valore_unitario = (SELECT prezzo FROM valorizzazione_tmp T WHERE inventario.id_magazzino = T.id_magazzino AND inventario.id_articolo = T.id_articolo) WHERE anno = \' || _anno || \' AND (valore_unitario IS NULL OR valore_unitario = 0)\';
        EXECUTE sql_statement;"""
        if self.confermaValorizzazione():
            idMagazzino = findIdFromCombobox(self.additional_filter.id_magazzino_filter_combobox)
            Environment.connection.execStoredProcedure('InventarioPrezzoVenditaMedioUpd', (int(Environment.conf.workingYear), idMagazzino))
            self.refresh()
            self.fineElaborazione()


    def on_movimento_button_clicked(self, button):
        """ Generazione movimento di carico magazzino """
        if (findIdFromCombobox(self.additional_filter.id_magazzino_filter_combobox) is None):
            obligatoryField(self.getTopLevel(),
                            self.additional_filter.id_magazzino_filter_combobox,
                            'Inserire il magazzino !')

        idMagazzino = findIdFromCombobox(self.additional_filter.id_magazzino_filter_combobox)

        msg = ("Attenzione !\n\nEventuali altri movimenti che sono stati creati devono essere eliminati manualmente.\n" +
               "Creare il movimento di carico per inventario ? ")
        dialog = gtk.MessageDialog(self.getTopLevel(), gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
                                   gtk.MESSAGE_QUESTION, gtk.BUTTONS_YES_NO, msg)
        response = dialog.run()
        dialog.destroy()
        if response == gtk.RESPONSE_YES:
            testata = TestataMovimento()
            data = '01/01/' + Environment.conf.workingYear
            testata.data_movimento = stringToDate(data)
            testata.operazione = 'Carico per inventario'
            righe = []

            invs = Inventario().select( anno=Environment.conf.workingYear,
                                                   idMagazzino=idMagazzino,
                                                   offset=None,
                                                   batchSize=None)


            for i in invs:
                if i.quantita is not None and i.quantita > 0:
                    riga = RigaMovimento()
                    riga.id_testata_movimento = testata.id
                    riga.id_articolo = i.id_articolo
                    riga.id_magazzino = i.id_magazzino
                    riga.descrizione = i.articolo
                    riga.percentuale_iva = i.percentuale_aliquota_iva
                    riga.quantita = i.quantita
                    riga.moltiplicatore = 1
                    riga.valore_unitario_lordo = riga.valore_unitario_netto = i.valore_unitario or 0
                    righe.append(riga)

            testata.righe = righe
            testata.persist()

            dialog = gtk.MessageDialog(self.getTopLevel(), gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
                                       gtk.MESSAGE_INFO, gtk.BUTTONS_OK, '\nElaborazione terminata !')
            response = dialog.run()
            dialog.destroy()


    def on_chiudi_button_clicked(self, button):
        """ Uscita dalla maschera """
        self.destroy()


    def on_ricerca_window_close(self, widget, event=None):
        """ Uscita dalla maschera """
        self.destroy()
        return True
