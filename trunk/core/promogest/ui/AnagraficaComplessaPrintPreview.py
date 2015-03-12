# -*- coding: utf-8 -*-

#    Copyright (C) 2005-2013 by Promotux
#                        di Francesco Meloni snc - http://www.promotux.it/

#    Author: Alceste Scalas <alceste@promotux.it>
#    Author: Andrea Argiolas <andrea@promotux.it>
#    Author: Francesco Meloni <francesco@promotux.it
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

import sys
from promogest.ui.gtk_compat import *
from promogest.ui.GladeWidget import GladeWidget
from promogest.ui.widgets.FilterWidget import FilterWidget
from promogest.lib.utils import *
from promogest import Environment
from promogest.lib.HtmlHandler import createHtmlObj, renderTemplate, renderHTML
from promogest.dao.Azienda import  Azienda


class AnagraficaPrintPreview(GladeWidget):
    """ Print preview """
    # FIXME: a lot of duplicated code from AnagraficaFilter here!

    def __init__(self, anagrafica, windowTitle, previewTemplate, tipo=None):
        GladeWidget.__init__(self, root='htmlviewer', path="htmlviewer.glade")
        self.windowTitle = windowTitle
        self.visualizzatore_html.set_title(windowTitle)
        self._anagrafica = anagrafica
        self._tipo = tipo

        self.bodyWidget = FilterWidget(owner=self, resultsElement='html')
        self.bodyWidget.filter_navigation_hbox.destroy()
        self.bodyWidget.info_label.set_markup("INSERT INFO")
        self.html_scrolledwindow.add_with_viewport(
                                            self.bodyWidget.getTopLevel())

        self.print_on_screen_html = self.bodyWidget.resultsElement
        self._gtkHtmlDocuments = None
        self._previewTemplate = previewTemplate
        self.html = createHtmlObj(self)
        #Prendo tutti i dati dalla finestra di filtraggio, compresi i dati
        # di ordinamento e di batchSize
        self._changeOrderBy = self.bodyWidget._changeOrderBy
        self.orderBy = self.bodyWidget.orderBy
        self.batchSize = self.bodyWidget.batchSize
        self.offset = self.bodyWidget.offset
        self.numRecords = self.bodyWidget.numRecords
        self._filterClosure = self._anagrafica.filter._filterClosure
        self._filterCountClosure = self._anagrafica.filter._filterCountClosure
        self.placeWindow(self.visualizzatore_html)
        self.bodyWidget.generic_button.set_property('visible', False)
        def test():
            self.html_code = "<html><body></body></html>"
        glib.idle_add(self.refresh)

    def on_csv_button_clicked(self, button):
        messageInfo(msg="NON ANCORA IMPLEMENTATO")

    def on_generic_combobox_changed(self, combobox):
        if self.codBar_combo.get_active() == 0:
            from PrintDialog import PrintDialogHandler
            from  xhtml2pdf import pisa
            f = self.html_code
            g = file(Environment.tempDir + ".temp.pdf", "wb")
            pisa.CreatePDF(str(f), g)
            g .close()
            anag = PrintDialogHandler(self, self.windowTitle)
            anagWindow = anag.getTopLevel()
            returnWindow = self.bodyWidget.getTopLevel().get_toplevel()
            anagWindow.set_transient_for(returnWindow)
            anagWindow.show_all()
            #self.codBar_combo.set_active(0)
        elif self.codBar_combo.get_active() == 1:
            print "ANTEPRIMA CSV"
        else:
            self.codBar_combo.set_active(-1)

    def _refreshPageCount(self):
        """ Aggiorna la paginazione """
        self.bodyWidget.numRecords = self.numRecords
        self.bodyWidget._refreshPageCount()

    @timeit
    def refresh(self):
        """ show the html page in the custom widget"""
        self.bodyWidget.orderBy = self.orderBy
        self.bodyWidget.tipo = self._tipo
        # self.pbar_dialog.run()
        #self.pbar_dialog.destroy()
        daos = self.bodyWidget.runFilter(offset=None,
                                        batchSize=None,
                                        filterClosure=self._filterClosure,
                                        )
        azienda = Azienda().getRecord(id=Environment.azienda)
        # pbar(self.pbar_report,parziale=daos.index(ragsoc), totale=len(nomi), text=ragsoc, noeta=False)
        #pbar(self.pbar_report,parziale=1, totale=4)
        if hasattr(self._anagrafica,"funzione_ordinamento") and self._anagrafica.funzione_ordinamento == "cliforn":
            if self._anagrafica.aa < 0:
                daos.sort(key=lambda x: x.intestatario.strip().upper())
            else:
                daos.sort(key=lambda x: x.intestatario.strip().upper(),reverse=True)
        elif hasattr(self._anagrafica,"funzione_ordinamento") and self._anagrafica.funzione_ordinamento == "impo":
            for t in daos:
                try:
                    t._totaleImponibileScontato
                except:
                    t.totali
            if self._anagrafica.aa < 0:
                daos.sort(key=lambda x: x._totaleImponibileScontato)
            else:
                daos.sort(key=lambda x: x._totaleImponibileScontato,reverse=True)
        self.numRecords = self.bodyWidget.countFilterResults(
                                        self._filterCountClosure,
                                        )
#        self._refreshPageCount()
        #pbar(self.pbar_report,parziale=2, totale=4)
        pageData = {}
        self.html_code = "<html><body></body></html>"
        if self._tipo == "veter":
            daos = daos[:]
            da = []
            for d in daos:
                c = []
                for a in d.righe:
                    if "TRIPLICE" in a.rig.arti.denominazione_famiglia:
                        c.append(a)
                if len(c)>0:
                    da.append(d)
            daos = da
        elif self._tipo == "massa":
            daos=daos[:]
            articoli_dict = {}
            if daos:
                cliente = daos[0].CLI
            else:
                cliente = None
            for d in daos:
                for x in d.righe:
                    if x.id_articolo:
                        if x.rig.arti.APADR and (x.rig.arti.APADR.percentuale_carbonio or
                            x.rig.arti.APADR.percentuale_cov or
                            x.rig.arti.APADR.percentuale_secco):
                            a_adr = x.rig.arti
                            # print(a_adr)
                            if a_adr in articoli_dict:
                                articoli_dict[a_adr] += ( x.quantita*x.moltiplicatore )
                            else:
                                articoli_dict[a_adr] = (
                                    x.quantita * x.moltiplicatore )
            print(self._anagrafica.filter)
            daData = self._anagrafica.filter.daData
            aData =  self._anagrafica.filter.aData
            pageData = {
                "file" : "report_massa.html",
                "rows": articoli_dict,
                "azienda":azienda,
                "cliente":cliente,
                "daData":daData,
                "aData":aData,
                "daos":daos,

            }
            self.html_code = renderTemplate(pageData)
            try:
                renderHTML(self.print_on_screen_html, str(self.html_code))
            except:
                renderHTML(self.print_on_screen_html, self.html_code)
            return

        #pbar(self.pbar_report,parziale=2.5, totale=4)
        if daos:
            pageData = {
                    "file": self._previewTemplate[1],
                    #"dao":daos,
                    "objects": daos,
                    "azienda" : azienda,
                    }
            self.html_code = renderTemplate(pageData)
        #pbar(self.pbar_report,parziale=3.75, totale=4)
        #pbar(self.pbar_report,stop=True)
        #self.pbar_dialog.hide()
        try:
            renderHTML(self.print_on_screen_html, str(self.html_code))
        except:
            renderHTML(self.print_on_screen_html, self.html_code)

    def on_print_on_screen_dialog_response(self, dialog, responseId):
        if responseId == GTK_RESPONSE_CLOSE:
            self.on_print_on_screen_dialog_delete_event()

    def on_print_on_screen_dialog_delete_event(self, dialog=None, event=None):
        self.destroy()


    def on_pdf_button_clicked(self, button):
        from PrintDialog import PrintDialogHandler

        operation = Gtk.PrintOperation()
        setting = Gtk.PageSetup()
        ps = Gtk.PaperSize.new_custom("cc", "cc", 210, 297, gtk.Unit.MM)
        st = Gtk.PrintSettings()
        s = Gtk.PageSetup()
        s.set_paper_size(ps)
        margine_fondo = float(setconf("Stampa", "report_margine_basso") or 4.3)
        s.set_bottom_margin(margine_fondo, gtk.Unit.MM)
        margine_sinistro = float(
            setconf("Stampa", "report_margine_sinistro") or 4.3)
        s.set_left_margin(margine_sinistro, gtk.Unit.MM)
        margine_destro = float(
            setconf("Stampa", "report_margine_destro") or 4.3)
        s.set_right_margin(margine_destro, gtk.Unit.MM)
        margine_alto = float(setconf("Stampa", "report_margine_alto") or 4.3)
        s.set_top_margin(margine_alto, gtk.Unit.MM)
        orientamento = str(setconf("Stampa", "report_ori"))
        if not orientamento or orientamento == "orizzontale":
            s.set_orientation(Gtk.PageOrientation.LANDSCAPE)
        operation.set_default_page_setup(s)
        operation.set_export_filename(Environment.tempDir + ".temp.pdf")
        p = self.print_on_screen_html.get_main_frame().print_full(operation,
                                                      gtk.PrintOperationAction.EXPORT)
        pbar(self.pbar, pulse=True, text="GENERAZIONE STAMPA ATTENDERE")
        pbar(self.pbar, stop=True)
        anag = PrintDialogHandler(self, self.windowTitle, tipo="report")
        anagWindow = anag.getTopLevel()
        returnWindow = self.bodyWidget.getTopLevel().get_toplevel()
        anagWindow.set_transient_for(returnWindow)
        anagWindow.show_all()