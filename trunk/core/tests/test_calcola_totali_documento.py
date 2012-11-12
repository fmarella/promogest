# -*- coding: utf-8 -*-

#    Copyright (C) 2005-2012 by Promotux
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

import unittest
import sys
import os
path = ".."
if path not in sys.path:
    sys.path.append(path)
from promogest import preEnv

preEnv.tipodbforce = "postgresql"
preEnv.aziendaforce = "urbani"
from promogest.buildEnv import set_configuration
from promogest import Environment
conf = set_configuration("urbani", "2012")
Environment.conf = conf
print conf

from promogest.dao.TestataDocumento import TestataDocumento
daos = TestataDocumento().select(batchSize=100)

class TestTestataDocumentoTotali(unittest.TestCase):

    #def setUp(self):
        #self.daos = TestataDocumento().select(batchSize=1)

    def test_totali(self):
        #print 1
        # make sure the shuffled sequence does not lose any elements
        for d in daos:
            d.totali
            #print d.id ,  len(d.righe), d._totaleImponibileScontato
            #self.assertEqual(d.id, 10)

        # should raise an exception for an immutable sequence
        #self.assertRaises(TypeError, random.shuffle, (1,2,3))

    #def test_choice(self):
        #element = random.choice(self.seq)
        #self.assertTrue(element in self.seq)

    #def test_sample(self):
        #with self.assertRaises(ValueError):
            #random.sample(self.seq, 20)
        #for element in random.sample(self.seq, 5):
            #self.assertTrue(element in self.seq)

suite = unittest.TestLoader().loadTestsFromTestCase(TestTestataDocumentoTotali)
unittest.TextTestRunner(verbosity=3).run(suite)
