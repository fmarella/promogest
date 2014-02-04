# -*- coding: utf-8 -*-

#    Copyright (C) 2005-2013 by Promotux
#                        di Francesco Meloni snc - http://www.promotux.it/

#    Author: Francesco Meloni <francesco@promotux.it>

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

from promogest.ui.gtk_compat import *
from promogest.lib.utils import *
from promogest import Environment
from promogest.ui.GladeWidget import GladeWidget

from promogest.dao.Fornitore import Fornitore
from promogest.modules.Provvigione.dao.Provvigione import Provvigione
from promogest.modules.Provvigione.dao.ProvvPgAzArt import ProvvPgAzArt


class ProvvNotebookPage(GladeWidget):
    """ Widget di configurazione del codice installazione e dei parametri
    di configurazione """
    def __init__(self, mainnn):
        GladeWidget.__init__(self, root='csa_frame',
                                    path='Provvigione/gui/provv_notebook.glade',
                                    isModule=True)
        self.rowBackGround = None
        self.ana = mainnn
        self.dao_articolo_provv = None
        self.draw()

    def draw(self):

        self._clear()

    def _clear(self):
        return

    def provvSetDao(self, dao):
        """ Estensione del SetDao principale"""
        return

    def provvRefresh(self):
        self.provv_listore.clear()
        forni = Fornitore().select(batchSize=None)
        for c in forni:
            pp = ProvvPgAzArt().select(id_persona_giuridica_to=c.id)
            if pp and pp[0].id_persona_giuridica_from == self.ana.dao.id:
                p = mN(pp[0].provv.valore_provv,2)
                t = pp[0].provv.tipo_provv
            else:
                p = ""
                t = "%"
            self.provv_listore.append((
                c,
                c.ragione_sociale or ((c.cognome or '') + ' ' + (c.nome or '')),
                p,
                t))

    def provvSaveDao(self):
        self.dao_provv_pg_az_art = ProvvPgAzArt().select(id_persona_giuridica_from=self.ana.dao.id, batchSize=None)
        for a in self.dao_provv_pg_az_art:
            a.delete()
        for a in self.provv_listore:
            if a[2] != "":
                dao_provv = Provvigione()
                dao_provv.valore_provv = a[2]
                dao_provv.tipo_provv = a[3]
                dao_provv.persist()
                dao_provv_pg_az_art = ProvvPgAzArt()
                dao_provv_pg_az_art.id_persona_giuridica_to = a[0].id
                dao_provv_pg_az_art.id_persona_giuridica_from = self.ana.dao.id
                dao_provv_pg_az_art.id_provvigione = dao_provv.id
                dao_provv_pg_az_art.persist()

    def on_column_valore_edited(self, cell, path, value):
        """ Set the value "quantita" edit in the cell """
        self.provv_listore[path][2] = value

    def on_column_tipo_edited(self, cell, path, value):
        """ Set the value "quantita" edit in the cell """
        if value in ["%","€"]:
            self.provv_listore[path][3] = value
