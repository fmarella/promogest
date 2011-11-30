# -*- coding: utf-8 -*-

#    Copyright (C) 2005, 2006, 2007 2008, 2009, 2010, 2011 by Promotux
#                        di Francesco Meloni snc - http://www.promotux.it/

#    Author: Francesco Meloni  <francesco@promotux.it>
#    Author: Andrea Argiolas <andrea@promotux.it>
#    Author: Francesco Marella <francesco.marella@gmail.com>

#    This file is part of Promogest.

#    Promogest is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.

#    Promogest is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

#    You should have received a copy of the GNU General Public License
#    along with Promogest.  If not, see <http://www.gnu.org/licenses/>.

from promogest.ui.gtk_compat import *
import os
from datetime import datetime
from promogest.ui.RicercaComplessaArticoli import RicercaComplessaArticoli
from promogest import Environment
from promogest.dao.Operazione import Operazione
from promogest.dao.Inventario import Inventario
from promogest.dao.TestataMovimento import TestataMovimento
from promogest.dao.RigaMovimento import RigaMovimento
from promogest.dao.Riga import Riga
from promogest.dao.Magazzino import Magazzino
from promogest.dao.Articolo import Articolo
from promogest.dao.Stoccaggio import Stoccaggio
from promogest.dao.Listino import Listino
from promogest.ui.GladeWidget import GladeWidget
from promogest.ui.utils import *
from promogest.dao.DaoUtils import giacenzaArticolo
from sqlalchemy import func

if posso("PW"):
    from promogest.modules.PromoWear.ui.PromowearUtils import *
    from promogest.modules.PromoWear.ui import AnagraficaArticoliPromoWearExpand


class GestioneInventario(RicercaComplessaArticoli):
    """ Gestione inventario di magazzino """

    def __init__(self, idMagazzino = None):

        # aggiornamento inventario con gli articoli eventualmente non presenti
#        self.checkTable()
        # filtri propri della parte inventario
        self.additional_filter = GladeWidget(rootWidget='inventario_filter_table',
        fileName="Inventario/gui/inventario_filter_table.glade", isModule=True)
        fillComboboxMagazzini(self.additional_filter.id_magazzino_filter_combobox2, noempty=True)
        if idMagazzino:
            findComboboxRowFromId(self.additional_filter.id_magazzino_filter_combobox2,
                                                              idMagazzino)
        # aggiunta della parte di dettaglio
        self._modifica = GladeWidget(rootWidget='inventario_detail_vbox',
            fileName="Inventario/gui/_inventario_select.glade", isModule=True)

        RicercaComplessaArticoli.__init__(self)
        self.anno = int(Environment.workingYear)
        self.annoScorso= int(Environment.workingYear) -1
        # modifiche all'interfaccia originaria
        self.getTopLevel().set_title('Promogest - Gestione inventario ' + str(self.annoScorso))
        #self.search_image.set_no_show_all(True)
        #self.search_image.set_property('visible', False)
        self.filter.filter_search_button.set_label('_Seleziona')
#        self.buttons_hbox.destroy()
        self._ricerca.varie_articolo_filter_expander.set_no_show_all(True)
        self._ricerca.varie_articolo_filter_expander.set_property('visible', False)

        # aggiunta dei filtri propri e della parte di dettaglio
#        ricerca_semplice_articoli_filter_vbox
        self.filters.ricerca_semplice_articoli_filter_vbox.pack_start(self.additional_filter.getTopLevel(), False, True, 0)
        self.filters.ricerca_semplice_articoli_filter_vbox.reorder_child(self.additional_filter.getTopLevel(), 0)
        self.results_vbox.pack_start(self._modifica.getTopLevel(), False, True, 0)

        self.additional_filter.id_magazzino_filter_combobox2.connect('changed',
                                                                    self.on_filter_field_changed)
        self.additional_filter.da_data_aggiornamento_filter_entry.connect('focus_out_event',
                                                                          self.on_filter_field_changed)
        self.additional_filter.a_data_aggiornamento_filter_entry.connect('focus_out_event',
                                                                         self.on_filter_field_changed)

        #self._modifica.quantita_entry.connect('key_press_event', self.detail_key_press_event)
        #self._modifica.valore_unitario_entry.connect('key_press_event', self.detail_key_press_event)

        self._modifica.azzera_button.connect('clicked', self.on_azzera_button_clicked)
        self._modifica.azzera_selected_button.connect('clicked', self.on_azzera_selected_button_clicked)
        self._modifica.ricrea_button.connect('clicked', self.on_ricrea_button_clicked)
        self._modifica.aggiorna_button.connect('clicked', self.on_aggiorna_button_clicked)
        self._modifica.aggiorna_da_ana_articoli.connect('clicked', self.on_aggiorna_da_ana_articoli_clicked)
        self._modifica.esporta_button.connect('clicked', self.on_esporta_button_clicked)

        self._modifica.esporta_conquantita_button.connect('clicked', self.on_esporta_conquantita_button_clicked)
        self._modifica.valorizza_button.connect('clicked', self.on_valorizza_button_clicked)
        self._modifica.movimento_button.connect('clicked', self.on_movimento_button_clicked)
        self._modifica.chiudi_button.connect('clicked', self.on_chiudi_button_clicked)
        self._modifica.giacenze_button.connect('clicked', self.on_giacenze_button_clicked)
        self._modifica.tutti_radio.connect('toggled', self.on_macro_filter_toggled)
        self._modifica.qa_zero_radio.connect('toggled', self.on_macro_filter_toggled)
        self._modifica.qa_negativa_radio.connect('toggled', self.on_macro_filter_toggled)
        self._modifica.val_negativo_radio.connect('toggled', self.on_macro_filter_toggled)
        self._modifica.calcola_pezzi_button.connect("clicked", self.on_calcola_pezzi_button_clicked)
        self._modifica.calcola_valori_button.connect("clicked", self.on_calcola_valori_button_clicked)

#        self.setRiepilogo()

    def checkTable(self):
        tutti = Environment.session.query(Inventario.id_articolo,Inventario.id_magazzino).all()
        cancellati = []
#        print "tutti", tutti
        for a in tutti:
            if tutti.count(a) >1 and a not in cancellati:
                dacancellare = Inventario().select(idArticolo=a[0],idMagazzino=a[1])
                cancellati.append(a)
                for g in dacancellare[1:]:
                    g.delete()

    def draw(self):
        """ Disegna la treeview relativa al risultato del filtraggio """
        treeview = self.filter.resultsElement
        model = gtk.ListStore(object, str, str, str, str, str, str, str, str, str, str, str, str)
        rendererSx = gtk.CellRendererText()
        rendererDx = gtk.CellRendererText()
        rendererDx.set_property('xalign', 1)

        cellspin = gtk.CellRendererSpin()
        cellspin.set_property("editable", True)
        cellspin.set_property("visible", True)
        adjustment = gtk.Adjustment(1, 1, 1000, 0.500, 2)
        cellspin.set_property("adjustment", adjustment)
        cellspin.set_property("digits", 2)
        cellspin.set_property("climb-rate", 3)
        cellspin.set_property('xalign', 1)
        cellspin.connect('edited', self.on_column_quantita_edited, treeview, True)
        column = gtk.TreeViewColumn('Quantità', cellspin, text=1)
        column.set_sizing(GTK_COLUMN_GROWN_ONLY)
        column.set_clickable(True)
        column.connect("clicked", self.filter._changeOrderBy, (None, Inventario.quantita))
        column.set_resizable(True)
        column.set_expand(False)
        column.set_min_width(50)
        treeview.append_column(column)


        cellspin1 = gtk.CellRendererSpin()
        cellspin1.set_property("editable", True)
        cellspin1.set_property("visible", True)
        adjustment = gtk.Adjustment(1, 1, 1000, 0.500, 2)
        cellspin1.set_property("adjustment", adjustment)
        cellspin1.set_property("digits", 2)
        cellspin1.set_property("climb-rate", 3)
        cellspin1.set_property('xalign', 1)
        cellspin1.connect('edited', self.on_column_valore_unitario_edited, treeview, True)

        column = gtk.TreeViewColumn('Val. unitario', cellspin1, text=2)
        column.set_sizing(GTK_COLUMN_GROWN_ONLY)
        column.set_clickable(True)
        column.connect("clicked", self.filter._changeOrderBy, (None, Inventario.valore_unitario))
        column.set_resizable(True)
        column.set_expand(False)
        column.set_min_width(70)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('U/B', rendererSx, text=3)
        column.set_sizing(GTK_COLUMN_GROWN_ONLY)
#        column.set_clickable(True)
#        column.connect("clicked", self.filter._changeOrderBy, (Articolo, Articolo.unita_base))
        column.set_resizable(False)
        column.set_expand(False)
        column.set_min_width(10)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Valorizza', rendererSx, text=4)
        column.set_sizing(GTK_COLUMN_GROWN_ONLY)
        column.set_clickable(False)
#        column.connect("clicked", self.filter._changeOrderBy, 'denominazione_breve_unita_base')
        column.set_resizable(False)
        column.set_expand(False)
        column.set_min_width(20)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Data agg', rendererSx, text=5)
        column.set_sizing(GTK_COLUMN_GROWN_ONLY)
        column.set_clickable(True)
        column.connect("clicked", self.filter._changeOrderBy, (None, Inventario.data_aggiornamento))
        column.set_resizable(True)
        column.set_expand(False)
        column.set_min_width(100)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Cod. ART', rendererSx, text=6)
        column.set_sizing(GTK_COLUMN_GROWN_ONLY)
        column.set_clickable(True)
        column.connect("clicked", self.filter._changeOrderBy,(Articolo, Articolo.codice))
        column.set_resizable(True)
        column.set_expand(False)
        column.set_min_width(100)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Descriz', rendererSx, text=7)
        column.set_sizing(GTK_COLUMN_GROWN_ONLY)
        column.set_clickable(True)
        column.connect("clicked", self.filter._changeOrderBy, (Articolo, Articolo.denominazione))
        column.set_resizable(True)
        column.set_expand(True)
        column.set_min_width(250)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('C Barre', rendererSx, text=8)
        column.set_sizing(GTK_COLUMN_GROWN_ONLY)
        column.set_clickable(False)
        column.connect("clicked", self.filter._changeOrderBy, (None, 'produttore'))
        column.set_resizable(True)
        column.set_expand(False)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Produttore', rendererSx, text=9)
        column.set_sizing(GTK_COLUMN_GROWN_ONLY)
        column.set_clickable(True)
        column.connect("clicked", self.filter._changeOrderBy, 'produttore')
        column.set_resizable(True)
        column.set_expand(False)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Famiglia', rendererSx, text=10)
        column.set_sizing(GTK_COLUMN_GROWN_ONLY)
        column.set_clickable(True)
        column.connect("clicked", self.filter._changeOrderBy, 'denominazione_famiglia')
        column.set_resizable(True)
        column.set_expand(False)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Categoria', rendererSx, text=11)
        column.set_sizing(GTK_COLUMN_GROWN_ONLY)
        column.set_clickable(True)
        column.connect("clicked", self.filter._changeOrderBy, 'denominazione_categoria')
        column.set_resizable(True)
        column.set_expand(False)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Cod arti forn', rendererSx, text=12)
        column.set_sizing(GTK_COLUMN_GROWN_ONLY)
        column.set_clickable(True)
        column.connect("clicked", self.filter._changeOrderBy, 'codice_articolo_fornitore')
        column.set_resizable(True)
        column.set_expand(False)
        treeview.append_column(column)

        treeview.set_search_column(4)
        treeview.set_model(model)

    def setInitialSearch(self):
        """ Imposta il tipo di ricerca iniziale """
        self._ricerca.setRicercaSemplice()
        self._ricerca.ricerca_avanzata_articoli_button.set_no_show_all(True)
        self._ricerca.ricerca_avanzata_articoli_button.set_property('visible', False)
        self._ricerca.ricerca_semplice_articoli_button.set_no_show_all(True)
        self._ricerca.ricerca_semplice_articoli_button.set_property('visible', False)
        self.buttons_hbox.destroy()

    def on_macro_filter_toggled(self, radio):
        if radio.get_active():
            self.refresh()

    def refresh(self, macro_filter="tutti"):
        """ Esegue il filtraggio in base ai filtri impostati e aggiorna la treeview """
        self.anno = int(Environment.workingYear)
        self.annoScorso= int(Environment.workingYear) -1
        if (findIdFromCombobox(self.additional_filter.id_magazzino_filter_combobox2) is None):
            obligatoryField(self.getTopLevel(),
                            self.additional_filter.id_magazzino_filter_combobox2,
                            'Inserire il magazzino !')

        self.idMagazzino = findIdFromCombobox(self.additional_filter.id_magazzino_filter_combobox2)
        self.qa_zero = self._modifica.qa_zero_radio.get_active() or None
        self.val_negativo =self._modifica.val_negativo_radio.get_active() or None
        self.qa_negativa =self._modifica.qa_negativa_radio.get_active() or None

        self.daData = stringToDate(self.additional_filter.da_data_aggiornamento_filter_entry.get_text())
        self.aData = stringToDate(self.additional_filter.a_data_aggiornamento_filter_entry.get_text())

        model = self.filter.resultsElement.get_model()
#        self.batchSize = 50
#        self._ricerca._prepare()
        denominazione = prepareFilterString(self._ricerca.denominazione_filter_entry.get_text())
        produttore = prepareFilterString(self._ricerca.produttore_filter_entry.get_text())
        codice = prepareFilterString(self._ricerca.codice_filter_entry.get_text())
        codiceABarre = prepareFilterString(self._ricerca.codice_a_barre_filter_entry.get_text())
        codiceArticoloFornitore = prepareFilterString(self._ricerca.codice_articolo_fornitore_filter_entry.get_text())
        idFamiglia = findIdFromCombobox(self._ricerca.id_famiglia_articolo_filter_combobox)
        idCategoria = findIdFromCombobox(self._ricerca.id_categoria_articolo_filter_combobox)
        idStato = findIdFromCombobox(self._ricerca.id_stato_articolo_filter_combobox)
        if self._ricerca.cancellato_filter_checkbutton.get_active():
            cancellato = False
        else:
            cancellato = True
        self.filterDict = { "articolo":denominazione,
                            "codice":codice,
                            "codiceABarre":codiceABarre,
                            "codiceArticoloFornitore":codiceArticoloFornitore,
                            "produttore":produttore,
                            "idFamiglia":idFamiglia,
                            "idCategoria":idCategoria,
                            "idStato":idStato,
                            "cancellato":cancellato
                            }
        self._ricerca.filterDict= self.filterDict
#        if posso("PW"):
#            AnagraficaArticoliPromoWearExpand.refresh(self._ricerca)

        self.filter.numRecords = Inventario().count(anno=self.annoScorso,
                                                    idMagazzino=self.idMagazzino,
                                                    daDataAggiornamento=self.daData,
                                                    aDataAggiornamento=self.aData,
                                                    qa_zero=self.qa_zero,
                                                    qa_negativa=self.qa_negativa,
                                                    val_negativo = self.val_negativo,
                                                    filterDict = self.filterDict
                                                    )

        self.filter._refreshPageCount()

        invs = Inventario().select(orderBy=self.filter.orderBy,
                                               anno=self.annoScorso,
                                               idMagazzino=self.idMagazzino,
                                               daDataAggiornamento=self.daData,
                                               aDataAggiornamento=self.aData,
                                               qa_zero=self.qa_zero,
                                               qa_negativa=self.qa_negativa,
                                               val_negativo =self.val_negativo,
                                               offset=self.filter.offset,
                                               filterDict=self.filterDict)
        self.inventariati_filtrati_tutti = Inventario().select(
                                               anno=self.annoScorso,
                                               idMagazzino=self.idMagazzino,
                                               daDataAggiornamento=self.daData,
                                               aDataAggiornamento=self.aData,
                                               qa_zero=self.qa_zero,
                                               qa_negativa=self.qa_negativa,
                                               val_negativo =self.val_negativo,
                                               batchSize =None,
                                               filterDict=self.filterDict
                                               )
        model.clear()

        for i in invs:
            if not i.quantita:
                quantita = mN("0.00")
            else:
                quantita = Decimal(str(i.quantita).strip()).quantize(Decimal('.01'))
            if not i.valore_unitario:
                valore_unitario = mN("0.00")
            else:
                valore_unitario = mN(i.valore_unitario )or 0
            model.append((i,
                          quantita,
                          valore_unitario,
                          (i.denominazione_breve_unita_base or ''),
                          mN(valore_unitario*quantita ) or 0 ,
                          dateTimeToString(i.data_aggiornamento),
                          (i.codice_articolo or ''),
                          (i.articolo or ''),
                          (i.codice_a_barre or ''),
                          (i.produttore or ''),
                          (i.denominazione_famiglia or ''),
                          (i.denominazione_categoria or ''),
                          (i.codice_articolo_fornitore or '')))
        self._modifica.numero_referenze.set_text(str(self.inventariati()))

    def on_calcola_pezzi_button_clicked(self, button):
        self._modifica.numero_referenze.set_text(str(self.inventariati()))
        self._modifica.numero_pezzi.set_text(str(self.totaleInventariati()))

    def on_calcola_valori_button_clicked(self, button):
        self._modifica.numero_referenze.set_text(str(self.inventariati()))
        self._modifica.numero_pezzi.set_text(str(self.totaleInventariati()))
        self._modifica.valore_complessivo.set_text(str(self.valoreComplessivo()))

    def inventariati(self):
        """ numero delle referenze inventariate"""
        return Inventario().count(inventariato = True)

    def totaleInventariati(self):
        """ Numero totale dei pezzi inventariati numero * quantita' """
        idMagazzino = findIdFromCombobox(self.additional_filter.id_magazzino_filter_combobox2)
        sel = Inventario().select(anno=self.annoScorso,
                                    idMagazzino=idMagazzino, batchSize=None)
        tot=0
        for s in sel:
            if s.quantita >=1:
                tot+=s.quantita
        return tot

    def valoreComplessivo(self):
        """ Valore complessivo inventariato"""
        idMagazzino = findIdFromCombobox(self.additional_filter.id_magazzino_filter_combobox2)
        sel = Inventario().select(anno=self.annoScorso,
                                    idMagazzino=idMagazzino, batchSize=None)
        tot=0
        for s in sel:
            if s.quantita >0:
                if s.valore_unitario:
                    valore = Decimal(s.quantita)*Decimal(s.valore_unitario)
                else:
                    valore = 0
                tot+=valore
                valore = 0
        return mN(tot)

    def on_filter_treeview_row_activated(self, treeview, path, column):
        """ Rileva la riga attualmente selezionata e aggiorna il dettaglio """
        self.refreshDetail()

    def _changeTreeViewSelectionType(self):
        """ Imposta la modalita' di selezione nella treeview ad una sola riga """
        selection = self.filter.resultsElement.get_selection()
        selection.set_mode(GTK_SELECTIONMODE_SINGLE)

    def on_filter_field_changed(self, widget=None, event=None):
        """ Aggiorna il testo del riepilogo perche' almeno uno dei filtri propri e' cambiato """
#        self.setRiepilogo()
        return

#    def setRiepilogo(self):
#        """ Aggiorna il testo del riepilogo """
#        testo = ''
#        if self.additional_filter.id_magazzino_filter_combobox2.get_active() != -1:
#            value = findStrFromCombobox(self.additional_filter.id_magazzino_filter_combobox2, 2)
#            testo += '  Magazzino:\n'
#            testo += '       ' + value + '\n'
#        value = self.additional_filter.da_data_aggiornamento_filter_entry.get_text()
#        if value != '':
#            testo += '  Da data aggiornamento:\n'
#            testo += '       ' + value + '\n'
#        value = self.additional_filter.a_data_aggiornamento_filter_entry.get_text()
#        if value != '':
#            testo += '  A data aggiornamento:\n'
#            testo += '       ' + value + '\n'

#        self.setSummaryTextBefore(testo)

    def on_column_quantita_edited(self, cell, path, value, treeview, editNext=True):
        """ Function to set the value quantita edit in the cell
        """
        model = treeview.get_model()
        value=value.replace(",", ".")
        value = mN(value)
        model[path][1] = value
        #model[path][4] = dateToString(datetime.datetime.today().date())
        quantita = Decimal(value)
        valore_unitario = Decimal(model[path][2])
        model[path][4] = mN(Decimal(quantita*valore_unitario).quantize(Decimal('.01')))
        data = model[path][5] or datetime.datetime.today().date()
        dao = Inventario().getRecord(id=self.dao.id)
        dao.anno = self.dao.anno
        dao.id_magazzino = self.dao.id_magazzino
        dao.id_articolo = self.dao.id_articolo
        dao.quantita = quantita
        dao.valore_unitario = valore_unitario
        dao.data_aggiornamento = data
        Environment.params['session'].add(dao)
        Environment.params['session'].commit()

    def on_column_valore_unitario_edited(self, cell, path, value, treeview, editNext=True):
        """ Function ti set the value valore unitario edit in the cell
        """
        model = treeview.get_model()
        value=value.replace(",", ".")
        value = mN(value)
        model[path][2] = value
        model[path][5] = dateToString(datetime.datetime.today().date())
        valore_unitario = Decimal(value)
        quantita= Decimal(model[path][1])
        model[path][4] = mN(Decimal(quantita*valore_unitario).quantize(Decimal('.01')))
        data = model[path][5] or datetime.datetime.today().date()
        dao = Inventario().getRecord(id=self.dao.id)
        dao.anno = self.dao.anno
        dao.id_magazzino = self.dao.id_magazzino
        dao.id_articolo = self.dao.id_articolo
        dao.quantita = quantita
        dao.valore_unitario = valore_unitario
        dao.data_aggiornamento = data
        Environment.params['session'].add(dao)
        Environment.params['session'].commit()

#    def next(self):
#        """ Passa alla riga successiva della treeview """
#        treeview = self.filter.resultsElement
#        selection = treeview.get_selection()
#        (model, iterator) = selection.get_selected()
#        nextIter = model.iter_next(iterator)
#        if nextIter is not None:
#            path = model.get_path(nextIter)
#            selection.select_path(path)
#            treeview.scroll_to_cell(path)
#            self.on_filter_treeview_cursor_changed(treeview)
#        else:
#            if not(self.filter.isLastPage()):
#                self.filter.filter_next_button.clicked()
#                path=model.get_path(model.get_iter_root())
#                selection.select_path(path)
#                treeview.scroll_to_cell(path)
#                self.on_filter_treeview_cursor_changed(treeview)

    def on_azzera_selected_button_clicked(self, button):
        msg = """ATTENZIONE!!!
    Stai per cancellare le informazioni
    relative alle voci di inventario filtrate e selezionate.
        Confermi la cancellazione ?
        """
        if YesNoDialog(msg=msg, transient=self.getTopLevel()):
            for i in  self.inventariati_filtrati_tutti:
                i.quantita = 0
                Environment.session.add(i)
            Environment.session.commit()
            self.refresh()
            self.fineElaborazione()





    def on_azzera_button_clicked(self, button):
        msg = """ATTENZIONE!!!
    Stai per cancellare il precedente inventario,
    TUTTI I MOVIMENTI DI MAGAZZINO FATTI COME
    CARICO DI INVENTARIO e successiva
    valorizzazione e quantificazione
    delle giacenze. Conferma SOLO
    se sei sicuro di quel che stai per fare.
        Confermi la cancellazione ?
        """
        if YesNoDialog(msg=msg, transient=self.getTopLevel()):
            print "cancello TUTTO IL MOVIMENTO INVENTARIO"
            idMagazzino = findIdFromCombobox(self.additional_filter.id_magazzino_filter_combobox2)
            sel2 = Environment.params['session']\
                            .query(Inventario)\
                            .filter(and_(Inventario.anno ==self.annoScorso,
                                    Inventario.id_magazzino==idMagazzino))\
                            .all()


            for s in sel2:
                Environment.params['session'].delete(s)
            Environment.params['session'].commit()
            dat = '01/01/' + str(self.anno)
            data = stringToDate(dat)
            OneDay = datetime.timedelta(days=1)
            aData= data+OneDay
            movimento = TestataMovimento().select(daData = data,
                                                    aData= aData,
                                                    idOperazione= "Carico per inventario")
            if movimento:
                for m in movimento:
                    for riga in movimento.righe:
                        if riga.id_magazzino == self.idMagazzino:
                            movimento.delete()
                            return True
            model = self.filter.resultsElement.get_model()
            model.clear()
            return False

    def on_giacenze_button_clicked(self, button):
        sovrascrivi = False
        msg = """Stiamo per aggiungere le giacenze,
        si dovranno sovrascrivere quelle già presenti?
            """
        if YesNoDialog(msg=msg, transient=self.getTopLevel()):
            sovrascrivi = True

        idMagazzino = findIdFromCombobox(self.additional_filter.id_magazzino_filter_combobox2)
        res = Inventario().select(anno=self.annoScorso,
                                  idMagazzino=idMagazzino, batchSize=None)
        if res:
            for r in res:
                if (sovrascrivi) or (not sovrascrivi and not r.quantita):
                    giacenza, valore = giacenzaArticolo(year=self.annoScorso,
                                                        idMagazzino=idMagazzino,
                                                        idArticolo=r.id_articolo)
                    r.quantita = giacenza
                    if giacenza > 0:
                        r.data_aggiornamento = datetime.datetime.today().date()
                    Environment.params['session'].add(r)
            Environment.params['session'].commit()
        self.refresh()
        self.fineElaborazione()

    def on_ricrea_button_clicked(self, button):
        """ Verifica se esistono gia' delle righe di inventario nell'anno di esercizio
        """
        idMagazzino = findIdFromCombobox(self.additional_filter.id_magazzino_filter_combobox2)
        res = Inventario().select(anno=self.anno,
                                    idMagazzino=idMagazzino)

        if res:
            messageInfo(msg='\nElaborazione Impossibile !', transient=self.getTopLevel())
            return
        else:
            giacenza = 0
            #sel2 = Environment.params['session'].query(Inventario.id_magazzino, Inventario.id_articolo).filter(Inventario.anno ==Environment.workingYear).all()
            sel = Environment.params['session'].query(Magazzino.id, Articolo.id)\
                                                .filter(Articolo.cancellato != True).all()
            for s in sel:
                righeArticoloMovimentate = Environment.params["session"]\
                    .query(RigaMovimento, TestataMovimento)\
                    .filter(and_(func.date_part("year", TestataMovimento.data_movimento)==(self.annoScorso)))\
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
        #sql_statement:= \'INSERT INTO inventario (anno, id_magazzino, id_articolo, quantita, valore_unitario, data_aggiornamento)
                            #(SELECT \' || _anno || \', M.id, A.id, NULL, NULL, NULL
                            #FROM magazzino M CROSS JOIN articolo A
                            #WHERE (M.id, A.id) NOT IN (SELECT I.id_magazzino, I.id_articolo FROM INVENTARIO I WHERE I.anno = \' || _anno || \')
                            #AND A.cancellato <> True)\';
        sel2 = Environment.params['session'].\
                query(Inventario.id_magazzino,
                    Inventario.id_articolo).\
                    filter(Inventario.id_magazzino==self.idMagazzino).\
                    filter(Inventario.anno == self.annoScorso).\
                    order_by(Inventario.id_articolo).all()
        sel = Environment.params['session'].\
                query(Stoccaggio.id_magazzino,
                    Stoccaggio.id_articolo).\
                    filter(Magazzino.id==self.idMagazzino).\
                    order_by(Stoccaggio.id_articolo).all()
        print "AGGIORNA" , self.idMagazzino
        print "SEL", sel,sel2
        if sel != sel2:
            for s in sel:
                if s not in sel2:
                    print "MA QUI CI PASSI"
                    inv = Inventario()
                    inv.anno = self.annoScorso
                    inv.id_magazzino = s[0]
                    inv.id_articolo = s[1]
                    Environment.params['session'].add(inv)
                Environment.params['session'].commit()
        self.refresh()

    def on_aggiorna_da_ana_articoli_clicked(self, button):
        """ Aggiornamento inventario con gli articoli eventualmente non presenti """

        sel2 = Environment.params['session'].\
                query(Inventario.id_articolo).\
                    filter(and_(Inventario.anno == self.annoScorso, Inventario.id_magazzino == self.idMagazzino)).\
                    order_by(Inventario.id_articolo).all()
        sel = Environment.params['session'].\
                query(Articolo.id).\
                    order_by(Articolo.id).all()
        if sel != sel2:
            for s in sel:
                if s not in sel2:
                    print "MA QUI CI PASSI"
                    inv = Inventario()
                    inv.anno = self.annoScorso
                    inv.id_magazzino =  self.idMagazzino
                    inv.id_articolo = s[0]
                    Environment.params['session'].add(inv)
            Environment.params['session'].commit()
        self.refresh()

    def on_esporta_conquantita_button_clicked(self, button):
        self.on_esporta_button_clicked(button=button, siquantita = True)

    def on_esporta_button_clicked(self, button= None, siquantita = False):
        """ Esportazione inventario in formato csv
        """
        if (findIdFromCombobox(self.additional_filter.id_magazzino_filter_combobox2) is None):
            obligatoryField(self.getTopLevel(),
                            self.additional_filter.id_magazzino_filter_combobox2,
                            'Inserire il magazzino !')

        idMagazzino = findIdFromCombobox(self.additional_filter.id_magazzino_filter_combobox2)

        fileDialog = gtk.FileChooserDialog(title='Esportazione inventario ',
                                           parent=self.getTopLevel(),
                                           action=GTK_FILE_CHOOSER_ACTION_SAVE,
                                           buttons=(gtk.STOCK_CANCEL,
                                                    GTK_RESPONSE_CANCEL,
                                                    gtk.STOCK_SAVE,
                                                    GTK_RESPONSE_OK),
                                           backend=None)


        folder = setconf("General", "cartella_predefinita") or ""
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
        if response == GTK_RESPONSE_OK:
            filename = fileDialog.get_filename()
            fileDialog.destroy()

            f = open(filename, 'w')
            riga = ('Codice; Descrizione; Quantita\'; Valore unitario; U.M.; ' +
                    'Codice a barre; Famiglia; Categoria;Anno ;idMagazzino ; idArticolo ;data_aggiornamento\n')
            f.write(riga)
            invs = Inventario().select(anno=self.annoScorso,
                                                    idMagazzino=idMagazzino,
                                                    offset=None,
                                                    batchSize=None)

            if invs:
                for i in invs:
                    quantita_ = '%14.4f' % float(i.quantita or 0)
                    quantita = quantita_.replace('.', ',')
                    valore = '%14.4f' % float(i.valore_unitario or 0)
                    valore = valore.replace('.', ',')
                    if siquantita:
                        if float(quantita_)>0:
                            riga = (str(i.codice_articolo or '') + ';' +
                                    str(i.articolo or '') + ';' +
                                    str(quantita).strip() + ';' +
                                    str(valore).strip() + ';' +
                                    str(i.denominazione_breve_unita_base or '') + ';' +
                                    str(i.codice_a_barre or '') + ';' +
                                    str(i.denominazione_famiglia or '') + ';' +
                                    str(i.denominazione_categoria or '') + ';'+
                                    str(i.anno or '') + ';'+
                                    str(i.id_magazzino or '') + ';'+
                                    str(i.id_articolo or '') + ';'+
                                    str(i.data_aggiornamento or '') + '\n')
                            f.write(riga)
                    else:
                        riga = (str(i.codice_articolo or '') + ';' +
                                    str(i.articolo or '') + ';' +
                                    '"' + quantita + '",' +
                                    '"' + valore + '",' +
                                    '"' + str(i.denominazione_breve_unita_base or '') + '",' +
                                    '"' + str(i.codice_a_barre or '') + '",' +
                                    '"' + str(i.denominazione_famiglia or '') + '",' +
                                    '"' + str(i.denominazione_categoria or '') + '",'+
                                    '"' + str(i.anno or '') + '",'+
                                    '"' + str(i.id_magazzino or '') + '",'+
                                    '"' + str(i.id_articolo or '') + '",'+
                                    '"' + str(i.data_aggiornamento or '') + '"\n')
                        f.write(riga)
                f.close()
                self.fineElaborazione()
        else:
            fileDialog.destroy()
            return

    def on_valorizza_button_clicked(self, button):
        """ Valorizzazione inventario (modifica automatica del valore unitario) """
        dialog = gtk.Dialog('Attenzione',
                            self.getTopLevel(),
                            GTK_DIALOG_MODAL | GTK_DIALOG_DESTROY_WITH_PARENT,
                            None)
        hbox = gtk.HBox()
        image = GTK_IMAGE_NEW_FROM_STOCK(gtk.STOCK_DIALOG_QUESTION, GTK_ICON_SIZE_BUTTON)
        image.set_padding(10, 10)
        label = gtk.Label('Verranno aggiornati i valori unitari non ancora\nspecificati secondo la modalita\' scelta.')
        label.set_justify(GTK_JUSTIFICATION_LEFT)
        label.set_alignment(0, 0)
        label.set_padding(15, 10)
        hbox.pack_start(image, False, False, 0)
        hbox.pack_start(label, True, True, 0)
        dialog.get_content_area().pack_start(hbox, True, True, 0)

        buttonAcquistoUltimo = gtk.Button(label = 'Ultimo prezzo\n di acquisto')
        buttonAcquistoUltimo.connect('clicked', self.on_buttonAcquistoUltimo_clicked)
        buttonVenditaUltimo = gtk.Button(label = 'Ultimo prezzo\n di vendita')
        buttonVenditaUltimo.connect('clicked', self.on_buttonVenditaUltimo_clicked)
        buttonAcquistoMedio = gtk.Button(label = 'Prezzo medio\n di acquisto')
        buttonAcquistoMedio.connect('clicked', self.on_buttonAcquistoMedio_clicked)
        buttonVenditaMedio = gtk.Button(label = 'Prezzo medio\n di vendita')
        buttonVenditaMedio.connect('clicked', self.on_buttonVenditaMedio_clicked)
        buttonVenditaDaListino = gtk.Button(label = 'Prezzo da listino\n di vendita')
        buttonVenditaDaListino.connect('clicked', self.on_buttonVenditaDaListino_clicked)
        dialog.get_action_area().pack_start(buttonAcquistoUltimo, True, True, 0)
        dialog.get_action_area().pack_start(buttonVenditaUltimo, True, True, 0)
        dialog.get_action_area().pack_start(buttonAcquistoMedio, True, True, 0)
        dialog.get_action_area().pack_start(buttonVenditaMedio, True, True, 0)
        dialog.get_action_area().pack_start(buttonVenditaDaListino, True, True, 0)

        dialog.show_all()
        result = dialog.run()
        dialog.destroy()

    def on_buttonVenditaDaListino_clicked(self, button):
        if self.confermaValorizzazione():
            idMagazzino = findIdFromCombobox(self.additional_filter.id_magazzino_filter_combobox2)
            sel = Inventario().select(anno=self.annoScorso,
                                    idMagazzino=idMagazzino, batchSize=None)
            noSconti = False
            if YesNoDialog(msg='Tengo conto degli sconti alla vendita?', transient=self.getTopLevel()):
                noSconti = True
            listino = Environment.conf.VenditaDettaglio.listino
            idListino = Listino().select(denominazioneEM = listino)
            for s in sel:
#                if s.quantita >=1:
                valori = leggiListino(idListino[0].id, s.id_articolo)
                if not noSconti:
                    s.valore_unitario = valori["prezzoDettaglio"]
                else:
                    prezzo = valori["prezzoDettaglio"]
                    prezzoScontato = prezzo
                    tipoSconto = None
                    if "scontiDettaglio" in valori:
                        if  len(valori["scontiDettaglio"]) > 0:
                            valoreSconto = valori['scontiDettaglio'][0].valore or 0
                            if valoreSconto == 0:
                                tipoSconto = None
                                prezzoScontato = prezzo
                            else:
                                tipoSconto = valori['scontiDettaglio'][0].tipo_sconto
                                if tipoSconto == "percentuale":
                                    prezzoScontato = mN(mN(prezzo) - (mN(prezzo) * mN(valoreSconto)) / 100)
                                else:
                                    prezzoScontato = mN(mN(prezzo) -mN(valoreSconto))
                        s.valore_unitario = prezzoScontato
                Environment.params['session'].add(s)
                print "VALORIZZA", valori
            Environment.params['session'].commit()
        self.refresh()
        self.fineElaborazione()

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
            sel = Inventario().select(anno=self.annoScorso,
                                    idMagazzino=idMagazzino, batchSize=None)
            for s in sel:
                print  s.id_articolo
                if s.quantita >0:
                    print s.quantita
                    righeArticoloMovimentate = Environment.params["session"]\
                        .query(func.max(RigaMovimento.valore_unitario_netto), func.max(TestataMovimento.data_movimento))\
                        .join(TestataMovimento, Articolo)\
                        .filter(TestataMovimento.data_movimento.between(datetime.date(int(self.annoScorso),1, 1), datetime.date(int(self.annoScorso), 12, 31)))\
                        .filter(RigaMovimento.id_testata_movimento == TestataMovimento.id)\
                        .filter(Operazione.segno=="+")\
                        .filter(Riga.id_magazzino==idMagazzino)\
                        .filter(Riga.id_articolo==s.id_articolo)\
                        .filter(Riga.valore_unitario_netto!=0)\
                        .all()

                    if righeArticoloMovimentate and righeArticoloMovimentate[0][0]:
                        s.valore_unitario = righeArticoloMovimentate[0][0]
                        Environment.params['session'].add(s)
            print "VALORIZZA"
            Environment.params['session'].commit()
            self.refresh()
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
            idMagazzino = findIdFromCombobox(self.additional_filter.id_magazzino_filter_combobox2)
            sel = Inventario().select(anno=self.annoScorso,
                        idMagazzino=idMagazzino, batchSize=None)
            for s in sel:
                righeArticoloMovimentate = Environment.params["session"]\
                    .query(func.max(RigaMovimento.valore_unitario_netto), func.max(TestataMovimento.data_movimento))\
                    .join(TestataMovimento, Articolo)\
                    .filter(TestataMovimento.data_movimento.between(datetime.date(int(self.annoScorso), 1, 1), datetime.date(int(self.annoScorso), 12, 31)))\
                    .filter(RigaMovimento.id_testata_movimento == TestataMovimento.id)\
                    .filter(Operazione.segno=="-")\
                    .filter(Riga.id_magazzino==idMagazzino)\
                    .filter(Riga.id_articolo==s.id_articolo)\
                    .filter(Riga.valore_unitario_netto!=0)\
                    .all()
                if righeArticoloMovimentate and righeArticoloMovimentate[0][0]:
                    s.valore_unitario = righeArticoloMovimentate[0][0]
                    Environment.params['session'].add(s)
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
            idMagazzino = findIdFromCombobox(self.additional_filter.id_magazzino_filter_combobox2)
            sel = Inventario().select(anno=self.annoScorso,
                        idMagazzino=idMagazzino, batchSize=None)
            for s in sel:
                righeArticoloMovimentate = Environment.params["session"]\
                    .query(func.avg(RigaMovimento.valore_unitario_netto))\
                    .join(TestataMovimento, Articolo)\
                    .filter(TestataMovimento.data_movimento.between(datetime.date(int(self.annoScorso), 1, 1), datetime.date(int(self.annoScorso), 12, 31)))\
                    .filter(RigaMovimento.id_testata_movimento == TestataMovimento.id)\
                    .filter(Operazione.segno=="+")\
                    .filter(Riga.id_magazzino==idMagazzino)\
                    .filter(Riga.id_articolo==s.id_articolo)\
                    .filter(Riga.valore_unitario_netto!=0)\
                    .all()
                if righeArticoloMovimentate and righeArticoloMovimentate[0][0]:
                    s.valore_unitario = righeArticoloMovimentate[0][0]
                    Environment.params['session'].add(s)
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
            idMagazzino = findIdFromCombobox(self.additional_filter.id_magazzino_filter_combobox2)
            sel = Inventario().select(anno=self.annoScorso,
                        idMagazzino=idMagazzino, batchSize=None)
            for s in sel:
                righeArticoloMovimentate = Environment.params["session"]\
                    .query(func.avg(RigaMovimento.valore_unitario_netto))\
                    .join(TestataMovimento, Articolo)\
                    .filter(TestataMovimento.data_movimento.between(datetime.date(int(self.annoScorso), 1, 1), datetime.date(int(self.annoScorso), 12, 31)))\
                    .filter(RigaMovimento.id_testata_movimento == TestataMovimento.id)\
                    .filter(Operazione.segno=="-")\
                    .filter(Riga.id_magazzino==idMagazzino)\
                    .filter(Riga.id_articolo==s.id_articolo)\
                    .filter(Riga.valore_unitario_netto!=0)\
                    .all()
                if righeArticoloMovimentate and righeArticoloMovimentate[0][0]:
                    s.valore_unitario = righeArticoloMovimentate[0][0]
                    Environment.params['session'].add(s)
            self.refresh()
            self.fineElaborazione()

    def on_movimento_button_clicked(self, button):
        """ Generazione movimento di carico magazzino """
        if (findIdFromCombobox(self.additional_filter.id_magazzino_filter_combobox2) is None):
            obligatoryField(self.getTopLevel(),
                            self.additional_filter.id_magazzino_filter_combobox2,
                            'Inserire il magazzino !')

        idMagazzino = findIdFromCombobox(self.additional_filter.id_magazzino_filter_combobox2)

        msg = ("Attenzione !\n\nEventuali altri movimenti che sono stati creati devono essere eliminati manualmente.\n" +
               "Creare il movimento di carico per inventario ? ")
        if YesNoDialog(msg=msg, transient=self.getTopLevel()):
            blocSize = 500
            conteggia = Inventario().count(anno=self.annoScorso,
                                        idMagazzino=idMagazzino,
                                        quantita = True,
                                        daDataAggiornamento=self.daData,
                                        aDataAggiornamento=self.aData,
                                        filterDict = self.filterDict
                                                    )

            print "NUMERO DEI RECORD PRESENTI:", conteggia
            if conteggia >= blocSize:
                blocchi = abs(conteggia/blocSize)
                for j in range(0,blocchi+1):
                    offset = j*blocSize
                    invs=Inventario().select(anno=self.annoScorso,
                                                   idMagazzino=idMagazzino,
                                                   quantita = True,
                                                   offset=offset,
                                                   batchSize=blocSize,
                                                   daDataAggiornamento=self.daData,
                                                    aDataAggiornamento=self.aData,
                                                    filterDict=self.filterDict)

                    testata = TestataMovimento()
                    data = '01/01/' + str(self.anno)
                    testata.data_movimento = stringToDate(data)
                    testata.operazione = 'Carico per inventario'
                    righe = []

                    for i in invs:
                        if i.quantita is not None and i.quantita > 0:
                            riga = RigaMovimento()
                            riga.id_testata_movimento = testata.id
                            riga.id_articolo = i.id_articolo
                            riga.id_magazzino = i.id_magazzino
                            riga.descrizione = i.arti.denominazione
                            riga.percentuale_iva = i.arti.percentuale_aliquota_iva
                            riga.quantita = i.quantita
                            riga.moltiplicatore = 1
                            riga.valore_unitario_lordo = riga.valore_unitario_netto = i.valore_unitario or 0
                            riga.scontiRigheMovimento = []
                            righe.append(riga)

                    testata.righeMovimento = righe
                    testata.persist()
            else:
                invs = Inventario().select(anno=self.annoScorso,
                                                   idMagazzino=idMagazzino,
                                                   quantita = True,
                                                   offset=None,
                                                   batchSize=None,
                                                    daDataAggiornamento=self.daData,
                                                    aDataAggiornamento=self.aData,
                                                    filterDict=self.filterDict)
                testata = TestataMovimento()
                data = '01/01/' + str(self.anno)
                testata.data_movimento = stringToDate(data)
                testata.operazione = 'Carico per inventario'
                righe = []

                for i in invs:
                    if i.quantita is not None and i.quantita > 0:
                        riga = RigaMovimento()
                        riga.id_testata_movimento = testata.id
                        riga.id_articolo = i.id_articolo
                        riga.id_magazzino = i.id_magazzino
                        riga.descrizione = i.arti.denominazione
                        riga.percentuale_iva = i.arti.percentuale_aliquota_iva
                        riga.quantita = i.quantita
                        riga.moltiplicatore = 1
                        riga.valore_unitario_lordo = riga.valore_unitario_netto = i.valore_unitario or 0
                        riga.scontiRigheMovimento = []
                        righe.append(riga)
                testata.righeMovimento = righe
                testata.persist()

            messageInfo(msg='\nElaborazione terminata !')

    def confermaValorizzazione(self):
        """ Chiede conferma per la modifica dei dati """
        return YesNoDialog(msg='Confermi l\'eliminazione ?', transient=self.getTopLevel())

    def fineElaborazione(self):
        """ Messaggio di fine elaborazione """
        messageInfo(msg='\nElaborazione terminata !')

    def on_chiudi_button_clicked(self, button):
        """ Uscita dalla maschera """
        self.destroy()

    def on_ricerca_window_close(self, widget, event=None):
        """ Uscita dalla maschera """
        self.destroy()
        return True
