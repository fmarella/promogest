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

from promogest.ui.GladeWidget import GladeWidget
from promogest.lib.utils import pbar
from promogest.ui.widgets.HTMLViewerWidget import HTMLViewerWidget
from promogest.dao.StoricoDocumento import get_padre


def ricerca_movimenti_spedizione(daos, progress=None):
    tipi_ddt_figlio = ['DDT vendita', 'DDT vendita diretta']

    res = []

    for doc in daos:
        if progress:
            pbar(progress, parziale=daos.index(doc), totale=len(daos), text="Attendere...", noeta=True)
        if doc.operazione in tipi_ddt_figlio:
            doc._padre = get_padre(doc.id)
            res.append(doc)

    if progress:
        pbar(progress, stop=True)

    return res

class ReportMovimentiSpedizioniWindow(GladeWidget):

    def __init__(self, parent, daos=None):
        GladeWidget.__init__(self,
                             root='report_mov_sped_window',
                             path='report_mov_sped.glade')
        self.__parent = parent
        self.__daos = daos
        self.placeWindow(self.getTopLevel())

        self.html_viewer = HTMLViewerWidget(self)
        self.viewer_placeholder.add(self.html_viewer.get_viewer())

        self.draw()

    def draw(self):
        ddt = ricerca_movimenti_spedizione(self.__daos, progress=self.html_viewer.progressbar)

        pageData = {
            'file': 'spedizione_documenti.html',
            'objects': ddt
        }

        self.html_viewer.renderHTML(pageData)