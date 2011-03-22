# -*- coding: utf-8 -*-

#    Copyright (C) 2005, 2006, 2007 2008, 2009, 2010 by Promotux
#                        di Francesco Meloni snc - http://www.promotux.it/

# Author: Francesco Meloni <francesco@promotux.it

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

from promogest.ui.utils import *
from promogest.dao.Setconf import SetConf
from promogest import Environment
from GladeWidget import GladeWidget


class AnagraficaFornitoriSetup(GladeWidget):
    """ Widget di configurazione del codice installazione e dei parametri
    di configurazione

    [Fornitori]
    lunghezza_codice = 5
    prefisso_codice = FO
    omogeneus_codice= upper
    struttura_codice = FOR000000
    """
    def __init__(self, maino):
        GladeWidget.__init__(self, '_anagrafica_fornitori_setup_frame',
                                    '_anagrafica_fornitori_setup.glade')
        self.maino = maino
        self._draw()

    def _draw(self):
        """ Riempiamo le combo """
        return

    def _refresh(self):
        """
        Carichiamo i dati in interfaccia
        """
        try:
            self.fornitore_codice_upper_check.set_active(int(setconf("Fornitori", "fornitore_codice_upper")))
        except:
            self.fornitore_codice_upper_check.set_active(1)
        try:
            self.fornitore_nome_cognome_check.set_active(int(setconf("Fornitori", "fornitore_nome_cognome")))
        except:
            self.fornitore_nome_cognome_check.set_active(0)
        self.fornitore_struttura_codice_entry.set_text(str(setconf("Fornitori", "fornitore_struttura_codice")))

    def _saveSetup(self):
        """ Salviamo i dati modificati in interfaccia """
        g = SetConf().select(key="fornitore_struttura_codice", section="Fornitori")
        g[0].value = str(self.fornitore_struttura_codice_entry.get_text())
        g[0].tipo = "str"
        Environment.session.add(g[0])

        c = SetConf().select(key="fornitore_codice_upper", section="Fornitori")
        c[0].value = str(self.fornitore_codice_upper_check.get_active())
        c[0].tipo = "bool"
        Environment.session.add(c[0])

        c = SetConf().select(key="fornitore_nome_cognome", section="Fornitori")
        c[0].value = str(self.fornitore_nome_cognome_check.get_active())
        c[0].tipo = "bool"
        Environment.session.add(c[0])
