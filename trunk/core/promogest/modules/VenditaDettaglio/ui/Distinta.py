# -*- coding: utf-8 -*-

#    Copyright (C) 2005, 2006, 2007 2008, 2009, 2010 by Promotux
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
from promogest.ui.utils import *
from promogest import Environment
from promogest.dao.CategoriaArticolo import CategoriaArticolo
from promogest.dao.Magazzino import Magazzino
from promogest.modules.VenditaDettaglio.dao.ChiusuraFiscale import ChiusuraFiscale
from promogest.lib.HtmlHandler import createHtmlObj, renderTemplate, renderHTML
from promogest.ui.PrintDialog import PrintDialogHandler



class Distinta(GladeWidget):
    """ Classe per la gestione della distinta di fine giornata
    """

    def __init__(self, righe = []):
        self._scontrini = righe
        self._htmlTemplate = None

        GladeWidget.__init__(self, 'visualizzatore_html',
                fileName="htmlviewer.glade")
        self._window = self.visualizzatore_html
        self.windowTitle = "Distinta giornaliera"
#        self.set_title("Distinta giornaliera")
        self.categorie = CategoriaArticolo().select(batchSize=None)
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
            tot += m.totale_scontrino
            totccr += m.totale_carta_credito
            totass += m.totale_assegni
            if m.totale_contanti:
                totcont_resto += (m.totale_contanti-m.totale_scontrino)
                totcont_netto += m.totale_scontrino
            totcont += m.totale_contanti
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
        #return (mN(tot),mN(totcont), mN(totccr), mN(totass),mN(tot_sconti), totnum, mN(totcont_resto), mN(totcont_netto) )
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
        for partz in parziali:
            if partz[1]:
                for p in partz[1]:
                    if p.sconti:
                        tot_sconti += self.calcolascontoXRiga(p)
                    tot += p.prezzo*p.quantita
                    totnum += p.quantita
                partz_def.append((partz[0].denominazione, mN(tot), mN(tot_sconti), totnum))
                tot = 0
                tot_sconti = 0
                totnum = 0
        return partz_def

    def refreshHtml(self, dao=None):
        pageData = {}
        parziali = []
        totali = self.calcolaTotale(self._scontrini)
        catelist =[]
        self.html = '<html></html>'
        dataeora = datetime.datetime.now()
        ragione_sociale = Environment.azienda
        chiusure = ChiusuraFiscale().select( dataChiusura = dataeora,
                                                offset = None,
                                                batchSize = None)
        if chiusure:
            aperto = "NO"
        else:
            aperto ="SI"
        if self._scontrini:
            for cate in self.categorie:
                for s in self._scontrini:
                    for una in s.righe:
                        if cate.denominazione == leggiArticolo(una.id_articolo)["daoArticolo"].denominazione_categoria:
                            catelist.append(una)
                parziali.append((cate,catelist))
                catelist= []
            partz = self.aggiungiTotaliXRiga(parziali)
            if hasattr(Environment.conf, "VenditaDettaglio"):
                magazzino = Environment.conf.VenditaDettaglio.magazzino
            else:
                magdao = setconf("VenditaDettaglio", "magazzino_vendita")
                if magdao:
                    magazzino = Magazzino().getRecord(id=magdao).denominazione
            castellettoIva = {}
            for s in self._scontrini:
                for r in s.righe:
                    a = leggiArticolo(r.id_articolo)
                    ali = a["percentualeAliquotaIva"]
                    prezzo_scontato = r.prezzo_scontato * r.quantita
                    imponibile = float(prezzo_scontato)/(1+float(ali)/100)
                    iva = float(prezzo_scontato) - imponibile
                    if ali not in castellettoIva.keys():
                        castellettoIva[ali] = {'percentuale': ali,
                                               'imponibile': imponibile,
                                                'imposta': iva,
                                                'totale': prezzo_scontato
                                                }
                    else:
                        castellettoIva[ali]['percentuale'] = ali
                        castellettoIva[ali]['imponibile'] += imponibile
                        castellettoIva[ali]['imposta'] += iva
                        castellettoIva[ali]['totale'] += prezzo_scontato
            #print "CASTELLETOOOOOOOOOOOOOOOOOOOOOOOOOOO", castellettoIva
            pageData = {
                    "file": "distinta_giornaliera.html",
                    "parziali": partz,
                    "totali": totali,
                    "dataeora": dataeora,
                    "ragione_sociale": ragione_sociale,
                    "aperto": aperto,
                    "magazzino":magazzino,
                    "castellettoIva": castellettoIva
                    }
            self.html = renderTemplate(pageData)
        renderHTML(self.detail,self.html)

    def on_pdf_button_clicked(self, button):
        try:
            import ho.pisa as pisa
        except:
            return
        f = str(self.html)
#        f = "Hello <strong>World</strong>"
        filename =Environment.tempDir + "distintaTemp.pdf"
        g = file(filename, "wb")
        pdf = pisa.CreatePDF(f,g)
        g .close()
        anag = PrintDialogHandler(self,self.windowTitle, tempFile=Environment.tempDir + "distintaTemp.pdf")
        anagWindow = anag.getTopLevel()
        returnWindow = self.getTopLevel().get_toplevel()
        anagWindow.set_transient_for(returnWindow)
        anagWindow.show_all()

    def on_quit_button_clicked(self, button):
        self.destroy()
        return None
