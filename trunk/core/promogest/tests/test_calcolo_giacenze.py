# -*- coding: utf-8 -*-

#    Copyright (C) 2005, 2006, 2007 2008, 2009, 2010, 2011 by Promotux
#                        di Francesco Meloni snc - http://www.promotux.it/

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

import sys
sys.path.append('../..')
from promogest import bindtextdomain
bindtextdomain('promogest', locale_dir='./po/locale')
import unittest

from promogest.Environment import *
from promogest.dao.Articolo import Articolo
from promogest.ui.utils import *

from promogest.dao.TestataMovimento import TestataMovimento
from promogest.dao.TestataDocumento import TestataDocumento
from promogest.dao.RigaMovimento import RigaMovimento
from promogest.dao.Riga import Riga
from promogest.dao.Fornitura import Fornitura
from promogest.dao.Magazzino import Magazzino
from promogest.dao.Stoccaggio import Stoccaggio
from promogest.dao.Operazione import Operazione



#mi serve un movimento di tipo trasferimento merce magazzino

class TestCalcoloGiacenza(unittest.TestCase):
    """Test per il modulo Calcolo giacenza
    """
    numero = -1
    print azienda


    def _getTotaliOperazioniMovimento(self):
        self.__dbTotaliOperazioniMovimento = self.giacenzaSel(year=workingYear, idMagazzino= self.id_magazzino, idArticolo=self.id_articolo)
        self.__totaliOperazioniMovimento = self.__dbTotaliOperazioniMovimento[:]

        return self.__totaliOperazioniMovimento

    def _setTotaliOperazioniMovimento(self, value):
        self.__totaliOperazioniMovimento = value

    totaliOperazioniMovimento = property(_getTotaliOperazioniMovimento,
                                         _setTotaliOperazioniMovimento)

    def _getGiacenza(self):
        totaliOperazioniMovimento = self.totaliOperazioniMovimento
        totGiacenza = 0

        for t in totaliOperazioniMovimento:
            totGiacenza += (mN(t['giacenza']) or 0)

        return totGiacenza

    giacenzaaa = property(_getGiacenza, )

    def setUp(self):
        stocs = Stoccaggio().select(
                                       idMagazzino=None,
                                       idArticolo = None,
                                       batchSize=None,
                                       )
        print len(stocs)
        for s in stocs:
            self.id_magazzino = s.id_magazzino
            self.id_articolo = s.id_articolo
            self.giacenzaaa




    def giacenzaArticolo(self,year=None, idMagazzino=None, idArticolo=None,allMag= None):
        """
        Calcola la quantità di oggetti presenti in magazzino
        """
        if not idArticolo or not year or (not idMagazzino and not allMag):
            return "0"
        if allMag:
            magazzini = Environment.params["session"].query(Magazzino.id).all()
            if not magazzini:
                return []
            else:
                mag=[]
                for m in magazzini:
                    mag.append(m[0])
                magazzini = mag
            righeArticoloMovimentate= Environment.params["session"]\
                    .query(RigaMovimento.quantita, RigaMovimento.moltiplicatore,Operazione.segno).join(TestataMovimento,Operazione)\
                    .filter(TestataMovimento.data_movimento.between(datetime.date(int(year), 1, 1), datetime.date(int(year) + 1, 1, 1)))\
                    .filter(RigaMovimento.id_testata_movimento == TestataMovimento.id)\
                    .filter(Riga.id_magazzino.in_(magazzini))\
                    .filter(RigaMovimento.id_articolo==idArticolo)\
                    .all()
        else:
            magazzini = idMagazzino
            righeArticoloMovimentate= Environment.params["session"]\
                    .query(RigaMovimento.quantita, RigaMovimento.moltiplicatore,Operazione.segno).join(TestataMovimento,Operazione)\
                    .filter(TestataMovimento.data_movimento.between(datetime.date(int(year), 1, 1), datetime.date(int(year) + 1, 1, 1)))\
                    .filter(RigaMovimento.id_testata_movimento == TestataMovimento.id)\
                    .filter(RigaMovimento.id_magazzino ==magazzini)\
                    .filter(RigaMovimento.id_articolo==idArticolo)\
                    .all()
        lista = []

        giacenza=0
        for ram in righeArticoloMovimentate:
            segno = ram[2]
            qua = ram[0]*(ram[1] or 1)
            #if hasattr(ram[0], "reversed"):
                #if ram[1].reversed:
                    #qua = -1*qua
            if segno =="-":
                giacenza -= qua
            elif segno =="+":
                giacenza += qua
            else:
                giacenza += qua
        return round(giacenza,2)

    def test_calcolo_giacenza(self):
        """ Do something interesting here...
        """
        print "Ciao"



if __name__ == '__main__':
    tests = ['test_calcolo_giacenza']
    suite = unittest.TestSuite(map(TestCalcoloGiacenza, tests))
    unittest.TextTestRunner(verbosity=2).run(suite)
