# -*- coding: utf-8 -*-

#    Copyright (C) 2005-2013 by Promotux
#                        di Francesco Meloni snc - http://www.promotux.it/

#    Author: Francesco Meloni  <francesco@promotux.it>
#    Author:  Andrea Argiolas   <andrea@promotux.it>
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

from promogest.ui.Ricerca import Ricerca, RicercaFilter
from promogest.dao.Cliente import Cliente
from promogest.lib.utils import showAnagraficaRichiamata, fillComboboxCategorieClienti,\
                    prepareFilterString, findIdFromCombobox
from promogest.ui.gtk_compat import *
from promogest.ui.anagClienti.AnagraficaClientiFilter import AnagraficaClientiFilter

class RicercaClienti(Ricerca):
    """ Ricerca clienti """
    def __init__(self):
        Ricerca.__init__(self, 'Promogest - Ricerca clienti',
                         RicercaClientiFilter(self))

    def insert(self, toggleButton, returnWindow):

        def refresh():
            self.filter.refresh()
            self.filter.ragione_sociale_filter_entry.grab_focus()

        from promogest.ui.anagClienti.AnagraficaClienti import AnagraficaClienti
        anag = AnagraficaClienti()
        anagWindow = anag.getTopLevel()

        showAnagraficaRichiamata(returnWindow, anagWindow, toggleButton, refresh)

        anag.on_record_new_activate(anag.record_new_button)


class RicercaClientiFilter(AnagraficaClientiFilter):
    """ Filtro per la ricerca dei clienti """
    def __init__(self, ricerca):
        AnagraficaClientiFilter.__init__(self, ricerca)
        self.ricerca_avanzata_clienti_filter_vbox.destroy()
        self.ricerca_alignment.destroy()

    def on_filter_treeview_selection_changed(self, treeview):
        pass
