# -*- coding: utf-8 -*-

#    Copyright (C) 2005-2012 by Promotux
#                        di Francesco Meloni snc - http://www.promotux.it/

#    Author: Francesco Meloni <francesco@promotux.it
#    Author: Francesco Marella <francesco.marella@gmail.com>

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
from promogest.ui.GladeWidget import GladeWidget


class AnagraficaArticoliSetup(GladeWidget):
    """ Widget di configurazione del codice installazione e dei parametri
    di configurazione

    [Articoli]
    lunghezza_progressivo = 7
    immagini = True
    struttura_codice = ART000000
    omogeneus_codice = upper
    numero_famiglie = 0
    prefisso_codice = ART
    lunghezza_codice_famiglia = 0
    """
    def __init__(self, maino):
        GladeWidget.__init__(self, '_anagrafica_articoli_setup_frame',
                                    '_anagrafica_articoli_setup.glade')
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
            self.articolo_codice_upper_check.set_active(int(setconf("Articoli", "articolo_codice_upper")))
        except:
            self.articolo_codice_upper_check.set_active(1)
        try:
            self.articolo_immagini_check.set_active(int(setconf("Articoli", "articolo_immagini")))
        except:
            self.articolo_immagini_check.set_active(1)
        self.articolo_struttura_codice_entry.set_text(str(setconf("Articoli", "articolo_struttura_codice")))

    def _saveSetup(self):
        """ Salviamo i dati modificati in interfaccia """
        g = SetConf().select(key="articolo_struttura_codice", section="Articoli")
        g[0].value = str(self.articolo_struttura_codice_entry.get_text())
        g[0].tipo = "str"
        Environment.session.add(g[0])

        c = SetConf().select(key="articolo_codice_upper", section="Articoli")
        c[0].value = str(self.articolo_codice_upper_check.get_active())
        c[0].tipo = "bool"
        Environment.session.add(c[0])
        c = SetConf().select(key="articolo_immagini", section="Articoli")
        c[0].value = str(self.articolo_immagini_check.get_active())
        c[0].tipo = "bool"
        Environment.session.add(c[0])
