# -*- coding: utf-8 -*-

#    Copyright (C) 2005-2013 by Promotux
#                        di Francesco Meloni snc - http://www.promotux.it/

#    Author: Francesco Meloni  <francesco@promotux.it>

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

from datetime import datetime
from promogest.ui.GladeWidget import GladeWidget
from promogest.lib.utils import *
from promogest import Environment
from promogest.dao.Cliente import Cliente
from promogest.modules.VenditaDettaglio.dao.TestataScontrinoCliente import TestataScontrinoCliente
from promogest.modules.VenditaDettaglio.dao.TestataScontrino import TestataScontrino
from promogest.lib.HtmlHandler import createHtmlObj, renderTemplate, renderHTML
from promogest.ui.PrintDialog import PrintDialogHandler



class AcquistoMedioCliente(GladeWidget):
    """ Classe per la gestione della distinta di fine giornata
    """

    def __init__(self, righe = []):
        self._scontrini = righe
        self._htmlTemplate = None

        GladeWidget.__init__(self, root='visualizzatore_html',
                path="htmlviewer.glade")
        self._window = self.visualizzatore_html
        self.windowTitle = "Acquisto medio Cliente"
        self.placeWindow(self._window)
        self.draw()

    def draw(self):
        self.detail = createHtmlObj(self)
        self.html_scrolledwindow.add(self.detail)
        self.refreshHtml()

    def calcolaTotale(self, scontrini):
        tot = 0
        totccr = 0
        totass = 0
        totnum = 0
        totcont = 0
        tot_sconti = 0
        totcont_resto = 0
        totcont_netto = 0
        for m in scontrini:
            if m.sconti:
                tot_sconti += self.calcolasconto(m)
            tot += m.totale_scontrino # totale incassato
            totccr += m.totale_carta_credito #totale carta di credito
            totass += m.totale_assegni # totale assegni
            totcont += m.totale_contanti # totale dato in contanti
            if m.totale_carta_credito == 0 and m.totale_assegni == 0 and m.totale_contanti ==0 :
                totcont += m.totale_scontrino
            if m.totale_carta_credito == 0 and m.totale_assegni == 0:
                totcont_netto += m.totale_scontrino
            totcont_resto = totcont-totcont_netto
            totnum += 1
        totali = {
            "tot" : mN(tot,2),
            "tot_cont": mN(totcont,2),
            "tot_ccr": mN(totccr,2),
            "tot_ass": mN(totass,2),
            "tot_sconti": mN(tot_sconti,2),
            "tot_num": mN(totnum,0),
            "tot_cont_resto": mN(totcont_resto,2),
            "tot_cont_netto": mN(totcont_netto,2)
        }

        return totali

    def calcolasconto(self, dao):
        if dao.sconti[0].tipo_sconto=="valore":
            return dao.sconti[0].valore
        else:
            return (100 * dao.totale_scontrino) / (100 - dao.sconti[0].valore) -(dao.totale_scontrino)

    def calcolascontoXRiga(self, dao):
        if dao.sconti[0].tipo_sconto=="valore":
            return dao.sconti[0].valore*dao.quantita
        else:
            return (dao.prezzo - dao.prezzo_scontato)*dao.quantita

    def aggiungiTotaliXRiga(self, parziali):
        tot = 0
        totnum = 0
        tot_sconti = 0
        partz_def = []
        for k,v in parziali.iteritems():
            if v:
                for p in v:
                    if p.sconti:
                        tot_sconti += self.calcolascontoXRiga(p)
                    tot += p.prezzo*p.quantita
                    totnum += p.quantita
                categoria = CategoriaArticolo().getRecord(id=k)
                partz_def.append((categoria.denominazione_breve, mN(tot), mN(tot_sconti), totnum))
                tot = 0
                tot_sconti = 0
                totnum = 0
        return partz_def

    def refreshHtml(self, dao=None):
        pageData = {}
        #totali = self.calcolaTotale(self._scontrini)
        self.html = '<html></html>'
        dataeora = datetime.datetime.now()
        dizio = {}
        for s in self._scontrini:
            tsc = TestataScontrinoCliente().select(id_testata_scontrino = s.id, batchSize=None)
            if tsc:
                cli_id = tsc[0].id_cliente
                cli = Cliente().getRecord(id=cli_id)
                if cli in dizio:
                    trini = dizio[cli]
                    trini.append(s)
                    dizio[cli] = trini
                else:
                    dizio[cli] = [s]

        pageData = {
                "file": "acquisto_medio_cliente.html",
                "dizio":dizio
                }
        self.html = renderTemplate(pageData)
        renderHTML(self.detail,self.html)

    def on_pdf_button_clicked(self, button):
        from  xhtml2pdf import pisa
        f = str(self.html)
        filename =Environment.tempDir + "acqmedcliTemp.pdf"
        g = file(filename, "wb")
        pdf = pisa.CreatePDF(f,g)
        g .close()
        anag = PrintDialogHandler(self,self.windowTitle, tempFile=Environment.tempDir + "acqmedcliTemp.pdf")
        anagWindow = anag.getTopLevel()
        returnWindow = self.getTopLevel().get_toplevel()
        anagWindow.set_transient_for(returnWindow)
        anagWindow.show_all()

    def on_quit_button_clicked(self, button):
        self.destroy()
        return None
