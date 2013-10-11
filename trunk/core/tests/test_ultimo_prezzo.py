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
from promogest.dao.Inventario import Inventario
from promogest.dao.TestataMovimento import TestataMovimento
from promogest.dao.TestataDocumento import TestataDocumento
from promogest.dao.RigaMovimento import RigaMovimento
from promogest.dao.RigaDocumento import RigaDocumento
from promogest.dao.Riga import Riga
from promogest.dao.Magazzino import Magazzino
from promogest.dao.Articolo import Articolo
from promogest.dao.UnitaBase import *

s= select([t_unita_base.c.denominazione_breve]).execute().fetchall()
print s

class TestUltimiPrezzi(unittest.TestCase):

    def setUp(self):
        self.codiceArticolo = "22 A"
        self.annoScorso = 2012
        self.idMagazzino = 1
        self.idArticolo = 13


    def test_ultimo_prezzo_acquisto(self):
        sel = Inventario().select(anno=self.annoScorso,
                                    idMagazzino=self.idMagazzino, batchSize=None)
        print "SEEEEL", sel
        for s in sel:
            print " ELABORO ARTICOLO", s.id_articolo
            righeArticoloMovimentateMov = Environment.params["session"]\
                .query(Riga.valore_unitario_netto, TestataMovimento.data_movimento,TestataMovimento.operazione)\
                .filter(Riga.id_articolo==s.id_articolo)\
                .filter(Riga.id==RigaMovimento.id)\
                .filter(Riga.id_magazzino==self.idMagazzino)\
                .filter(RigaMovimento.id_testata_movimento == TestataMovimento.id)\
                .filter(TestataMovimento.data_movimento.between(datetime.date(self.annoScorso,1, 1), datetime.date(self.annoScorso, 12, 31)))\
                .filter(TestataMovimento.operazione.ilike("%acquisto%"))\
                .filter(Riga.valore_unitario_netto!=0)\
                .all()

            righeArticoloMovimentateDoc = Environment.params["session"]\
                .query(Riga.valore_unitario_netto, TestataDocumento.data_documento, TestataDocumento.operazione)\
                .filter(Riga.id_articolo==s.id_articolo)\
                .filter(Riga.id==RigaDocumento.id)\
                .filter(Riga.id_magazzino==self.idMagazzino)\
                .filter(RigaDocumento.id_testata_documento == TestataDocumento.id)\
                .filter(TestataDocumento.data_documento.between(datetime.date(self.annoScorso,1, 1), datetime.date(self.annoScorso, 12, 31)))\
                .filter(TestataDocumento.operazione.ilike("%acquisto%"))\
                .filter(Riga.valore_unitario_netto!=0)\
                .all()



            righeArticoloMovimentate = righeArticoloMovimentateDoc+righeArticoloMovimentateMov
            righeArticoloMovimentate.sort(key=lambda x: x[1], reverse=True)


            print righeArticoloMovimentate
            if righeArticoloMovimentate and righeArticoloMovimentate[0][0]:
                s.valore_unitario = righeArticoloMovimentate[0][0]
                #Environment.params['session'].add(s)
                print "VALORIZZA", righeArticoloMovimentate[0][0]
        #Environment.params['session'].commit()




suite = unittest.TestLoader().loadTestsFromTestCase(TestUltimiPrezzi)
unittest.TextTestRunner(verbosity=2).run(suite)


#                .filter(TestataMovimento.operazione.in_(Environment.solo_acquisto_con_DDT))\
#.filter(Riga.valore_unitario_netto!=0)\