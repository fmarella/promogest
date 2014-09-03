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

from promogest import Environment as env
from promogest.ui.gtk_compat import *
from promogest.ui.GladeWidget import GladeWidget
from promogest.dao.RicercaLottiUtils import ricerca_lotto
from promogest.ui.widgets.HTMLViewerWidget import HTMLViewerWidget


class RicercaLottiWindow(GladeWidget):

    def __init__(self, parent):
        GladeWidget.__init__(self,
                             root='ricerca_lotti_window',
                             path='ricerca_lotti_window.glade')
        self.__parent = parent
        self.placeWindow(self.getTopLevel())

        self.html_viewer = HTMLViewerWidget(self)
        self.viewer_placeholder.add(self.html_viewer.get_viewer())

        self.draw()

    def draw(self):
        self.anno_entry.set_text(str(datetime.datetime.now().year))

    def on_trova_button_clicked(self, button):
        num_lotto = self.numero_lotto_entry.get_text()
        if not num_lotto:
            return
        anno = int(self.anno_entry.get_text())

        result = ricerca_lotto(num_lotto, anno, progress=self.html_viewer.progressbar)

        pageData = {
            'file': 'ricerca_lotti.html',
            'numero_lotto': num_lotto,
            'data': result
        }

        self.html_viewer.renderHTML(pageData)
