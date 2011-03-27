# -*- coding: utf-8 -*-

#    Copyright (C) 2005, 2006, 2007 2008, 2009, 2010, 2011 by Promotux
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
from promogest.ui.GladeWidget import GladeWidget


class AnagraficaPrimaNotaSetup(GladeWidget):
    """ Widget di configurazione del codice installazione e dei parametri
    di configurazione
    """
    def __init__(self, maino):
        GladeWidget.__init__(self, 'PrimaNota/gui/_anagrafica_primanota_setup_frame',
                                    'PrimaNota/gui/_anagrafica_primanota_setup.glade',
                                    isModule=True)
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
