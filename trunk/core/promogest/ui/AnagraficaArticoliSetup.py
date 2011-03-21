# -*- coding: utf-8 -*-

# Promogest
#
# Copyright (C) 2005-2009 by Promotux Informatica - http://www.promotux.it/
# Author: Francesco Meloni <francesco@promotux.it>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.

from promogest.ui.utils import *
from promogest.dao.Setconf import SetConf
from promogest import Environment
from GladeWidget import GladeWidget


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
        return

    def _saveSetup(self):
        """ Salviamo i dati modificati in interfaccia """
        return
