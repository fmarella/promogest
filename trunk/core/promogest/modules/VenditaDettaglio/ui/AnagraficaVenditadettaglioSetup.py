# -*- coding: utf-8 -*-

#    Copyright (C) 2005-2012 by Promotux
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

from promogest.lib.utils import *
from promogest.dao.Setconf import SetConf
from promogest import Environment
from promogest.ui.GladeWidget import GladeWidget


class VenditadettaglioSetup(GladeWidget):
    """ Widget di configurazione del codice installazione e dei parametri
        di configurazione

    [VenditaDettaglio]
    operazione = Scarico venduto da cassa
    puntocassa =
    jolly = gen
    migrazione_sincro_effettuata = yes
    mod_enable = yes
    magazzino = CENTRALE
    direct_confirm = yes
    listino = VenditaDettaglio
    disabilita_stampa_chiusura = yes
    disabilita_stampa = yes
    export_path = /home/vete/promogest2/elisir/temp/
    """
    def __init__(self, maino):
        GladeWidget.__init__(self, root='_vendita_dettaglio_setup_frame',
                                    path='VenditaDettaglio/gui/_vendita_dettaglio_setup.glade',
                                    isModule=True)
        self.maino = maino
        self._draw()

    def _draw(self):
        """ Riempiamo le combo """
        fillComboboxMagazzini(self.id_magazzino_filter_combobox, True)
        fillComboboxListini(self.id_listino_filter_combobox, True)
        return

    def _refresh(self):
        """
        Carichiamo i dati in interfaccia
        """
        try:
            self.disabilita_stampa_chiusura_check.set_active(int(setconf("VenditaDettaglio", "disabilita_stampa_chiusura")))
        except:
            self.disabilita_stampa_chiusura_check.set_active(1)
        try:
            self.disabilita_stampa_check.set_active(int(setconf("VenditaDettaglio", "disabilita_stampa")))
        except:
            self.disabilita_stampa_check.set_active(1)
        if setconf("VenditaDettaglio", "listino_vendita"):
            findComboboxRowFromId(self.id_listino_filter_combobox, int(setconf("VenditaDettaglio", "listino_vendita")))
        if setconf("VenditaDettaglio", "magazzino_vendita"):
            findComboboxRowFromId(self.id_magazzino_filter_combobox, int(setconf("VenditaDettaglio", "magazzino_vendita")))
        if setconf("VenditaDettaglio", "jolly"):
            idART = int(setconf("VenditaDettaglio", "jolly"))
        else:
            idART = None
        self.id_articolo_filter_customcombobox.setId(idART)


    def _saveSetup(self):
        """ Salviamo i dati modificati in interfaccia """
        c = SetConf().select(key="disabilita_stampa_chiusura", section="VenditaDettaglio")
        if c:
            c[0].value = str(self.disabilita_stampa_chiusura_check.get_active())
            c[0].tipo = "bool"
            Environment.session.add(c[0])
        else:
            a = SetConf()
            a.section = "VenditaDettaglio"
            a.tipo_section ="Modulo"
            a.description = "disabilita_stampa_chiusura"
            a.tipo = "bool"
            a.key = "disabilita_stampa_chiusura"
            a.value = str(self.disabilita_stampa_chiusura_check.get_active())
            a.active = True
            Environment.session.add(a)

        c = SetConf().select(key="disabilita_stampa", section="VenditaDettaglio")
        if c:
            c[0].value = str(self.disabilita_stampa_check.get_active())
            c[0].tipo = "bool"
            Environment.session.add(c[0])
        else:
            a = SetConf()
            a.section = "VenditaDettaglio"
            a.tipo_section ="Modulo"
            a.description = "disabilita_stampa"
            a.tipo = "bool"
            a.key = "disabilita_stampa"
            a.value = str(self.disabilita_stampa_check.get_active())
            a.active = True
            Environment.session.add(a)

        c = SetConf().select(key="jolly", section="VenditaDettaglio")
        if c:
            c[0].value = str(self.id_articolo_filter_customcombobox.getId())
            c[0].tipo = "int"
            Environment.session.add(c[0])
        else:
            a = SetConf()
            a.section = "VenditaDettaglio"
            a.tipo_section ="Modulo"
            a.description = "jolly"
            a.tipo = "int"
            a.key = "jolly"
            a.value = str(self.id_articolo_filter_customcombobox.getId())
            a.active = True
            Environment.session.add(a)

        c = SetConf().select(key="listino_vendita", section="VenditaDettaglio")
        if c:
            c[0].value = str(findIdFromCombobox(self.id_listino_filter_combobox))
            c[0].tipo = "int"
            Environment.session.add(c[0])
        else:
            a = SetConf()
            a.section = "VenditaDettaglio"
            a.tipo_section ="Modulo"
            a.description = "listino_vendita"
            a.tipo = "int"
            a.key = "listino_vendita"
            a.value = str(findIdFromCombobox(self.id_listino_filter_combobox))
            a.active = True
            Environment.session.add(a)
        c = SetConf().select(key="magazzino_vendita", section="VenditaDettaglio")
        if c:
            c[0].value = str(findIdFromCombobox(self.id_magazzino_filter_combobox))
            c[0].tipo = "int"
            Environment.session.add(c[0])
        else:
            a = SetConf()
            a.section = "VenditaDettaglio"
            a.tipo_section ="Modulo"
            a.description = "magazzino_vendita"
            a.tipo = "int"
            a.key = "magazzino_vendita"
            a.value = str(findIdFromCombobox(self.id_magazzino_filter_combobox))
            a.active = True
            Environment.session.add(a)
