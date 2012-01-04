# -*- coding: utf-8 -*-

#    Copyright (C) 2005-2012 by Promotux
#                        di Francesco Meloni snc - http://www.promotux.it/

# Authors: Francesco Meloni <francesco@promotux.it>
#          Francesco Marella <francesco.marella@gmail.com>

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


class AnagraficaClientiSetup(GladeWidget):
    """ Widget di configurazione del codice installazione e dei parametri
    di configurazione

    [Clienti]
    lunghezza_codice = 5
    prefisso_codice = CL
    omogeneus_codice= upper
    struttura_codice = CLI000000
    """
    def __init__(self, maino):
        GladeWidget.__init__(self, '_anagrafica_clienti_setup_frame',
                                    '_anagrafica_clienti_setup.glade')
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
            self.clienti_codice_upper_check.set_active(int(setconf("Clienti", "cliente_codice_upper")))
        except:
            self.clienti_codice_upper_check.set_active(1)
        try:
            self.clienti_insegna_check.set_active(int(setconf("Clienti", "cliente_insegna")))
        except:
            self.clienti_insegna_check.set_active(0)

        try:
            self.clienti_nomi_check.set_active(int(setconf("Clienti", "cliente_nome")))
        except:
            self.clienti_nomi_check.set_active(0)

        try:
            self.clienti_cognomi_check.set_active(int(setconf("Clienti", "cliente_cognome")))
        except:
            self.clienti_cognomi_check.set_active(0)



        self.clienti_struttura_codice_entry.set_text(str(setconf("Clienti", "cliente_struttura_codice")))

    def _saveSetup(self):
        """ Salviamo i dati modificati in interfaccia """
        g = SetConf().select(key="cliente_struttura_codice", section="Clienti")
        g[0].value = str(self.clienti_struttura_codice_entry.get_text())
        g[0].tipo = "str"
        Environment.session.add(g[0])

        c = SetConf().select(key="cliente_codice_upper", section="Clienti")
        c[0].value = str(self.clienti_codice_upper_check.get_active())
        c[0].tipo = "bool"
        Environment.session.add(c[0])

        c = SetConf().select(key="cliente_insegna", section="Clienti")
        if c:
            c = c[0]
        else:
            c = SetConf()
        c.key = "cliente_insegna"
        c.section = "Clienti"
        c.value = str(self.clienti_insegna_check.get_active())
        c.tipo = "bool"
        c.description = "visualizzare il campo per insegna"
        c.tipo_section = "Generico"
        c.active = True
        c.visible = True
        c.date = datetime.datetime.now()
        Environment.session.add(c)

        c = SetConf().select(key="cliente_nome", section="Clienti")
        if c:
            c = c[0]
        else:
            c = SetConf()
        c.key = "cliente_nome"
        c.section = "Clienti"
        c.value = str(self.clienti_nomi_check.get_active())
        c.tipo = "bool"
        c.description = "visualizzare il campo per nome"
        c.tipo_section = "Generico"
        c.active = True
        c.visible = True
        c.date = datetime.datetime.now()
        Environment.session.add(c)

        c = SetConf().select(key="cliente_cognome", section="Clienti")
        if c:
            c = c[0]
        else:
            c = SetConf()
        c.key = "cliente_cognome"
        c.section = "Clienti"
        c.value = str(self.clienti_cognomi_check.get_active())
        c.tipo = "bool"
        c.description = "visualizzare il campo per cognome"
        c.tipo_section = "Generico"
        c.active = True
        c.visible = True
        c.date = datetime.datetime.now()
        Environment.session.add(c)
