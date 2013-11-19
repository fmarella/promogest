# -*- coding: utf-8 -*-

#    Copyright (C) 2005-2013 by Promotux
#                       di Francesco Meloni snc - http://www.promotux.it/

#    Author: Francesco Meloni  <francesco@promotux.it>
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


import random
import unittest
import os
import sys
from datetime import datetime
path = ".."
if path not in sys.path:
    sys.path.append(path)
#from promogest import preEnv

#preEnv.tipodbforce = "sqlite"
#preEnv.aziendaforce = "urbani"
#from promogest.buildEnv import set_configuration
from promogest import Environment
#conf = set_configuration("aziendaPromo", "2012")
#Environment.conf = conf
from sqlalchemy import func
from promogest.dao.Operazione import Operazione
from promogest.dao.Riga import Riga
from promogest.dao.Magazzino import Magazzino
from promogest.dao.Articolo import Articolo
from promogest.modules.VenditaDettaglio.dao.TestataScontrino import TestataScontrino
from promogest.dao.UnitaBase import *

class TestAcquistoMedioCliente(unittest.TestCase):

    def setUp(self):
        self.codiceArticolo = "22 A"
        self.annoScorso = 2012
        self.idMagazzino = 1
        self.idArticolo = 13


    def test_acquisto_medio_cliente(self):

        idArticolo = self.filters.id_articolo_filter_customcombobox.getId()
        daData = stringToDate(self.filters.da_data_filter_entry.get_text())
        aData = stringToDateBumped(self.filters.a_data_filter_entry.get_text())
        idPuntoCassa = findIdFromCombobox(self.filters.id_pos_filter_combobox)
        idMagazzino = findIdFromCombobox(self.filters.id_magazzino_filter_combobox)
        idCliente =  self.filters.id_cliente_search_customcombobox.getId()

        scos = TestataScontrino().select( orderBy=self.filterss.orderBy,
                                                     idArticolo=idArticolo,
                                                     daData=daData,
                                                     aData=aData,
                                                     idMagazzino = idMagazzino,
                                                     idPuntoCassa = idPuntoCassa,
                                                     idCliente = idCliente,
                                                     offset=self.filterss.offset,
                                                     batchSize=self.filterss.batchSize)

        print "VALORIZZA"
        #Environment.params['session'].commit()




suite = unittest.TestLoader().loadTestsFromTestCase(TestAcquistoMedioCliente)
unittest.TextTestRunner(verbosity=2).run(suite)
