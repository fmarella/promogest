# -*- coding: utf-8 -*-

#    Copyright (C) 2005-2012 by Promotux
#                        di Francesco Meloni snc - http://www.promotux.it/

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

import datetime

from promogest.Environment import session, workingYear
from promogest.ui.GladeWidget import GladeWidget
from promogest.lib.utils import pbar
from promogest.ui.widgets.HTMLViewerWidget import HTMLViewerWidget
from promogest.dao.TestataDocumento import TestataDocumento
from promogest.dao.StoricoDocumento import get_figli, get_padre

def ricerca_movimenti_spedizione(da_data, al_data, progress=None):
    tipi_ddt_figlio = ['DDT vendita', 'DDT vendita diretta']
    # Tutti i documenti (ordini) non saldati dall'inizio dell'anno
    ordini = session.query(TestataDocumento).filter(TestataDocumento.data_documento >= da_data,
                                                    TestataDocumento.operazione == 'Ordine da cliente',
                                                    TestataDocumento.documento_saldato == False).all()
    res = []

    for ordine in ordini:
        if progress:
            pbar(progress, parziale=ordini.index(ordine), totale=len(ordini),
                text="Attendere...", noeta=True)
        # ottengo tutti i figli di questo ordine
        figli = get_figli(ordine.id)
        for figlio in figli:
            if figlio.operazione in tipi_ddt_figlio:
                figlio._padre = get_padre(figlio.id)
                res.append(figlio)

    if progress:
        pbar(progress, stop=True)

    return res


class ReportMovimentiSpedizioniWindow(GladeWidget):

    def __init__(self, parent):
        GladeWidget.__init__(self,
                             root='report_mov_sped_window',
                             path='report_mov_sped.glade')
        self.__parent = parent
        self.placeWindow(self.getTopLevel())

        self.html_viewer = HTMLViewerWidget(self)
        self.viewer_placeholder.add(self.html_viewer.get_viewer())

        self.draw()

    def draw(self):
        da_data = datetime.datetime(int(workingYear), 1, 1)
        al_data = datetime.date.today()
        ddt = ricerca_movimenti_spedizione(da_data, al_data, progress=self.html_viewer.progressbar)

        pageData = {
            'data_inizio_report': da_data,
            'data_fine_report': al_data,
            'file': 'spedizione_documenti.html',
            'objects': ddt
        }

        self.html_viewer.renderHTML(pageData)



