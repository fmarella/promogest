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

from promogest.modules.PrimaNota.dao.TestataPrimaNota import TestataPrimaNota
from promogest.ui.utils import *


class TestPrimaNota(unittest.TestCase):
    """Test per il modulo PrimaNota
    """
    numero = -1

    def setUp(self):
        tpn = TestataPrimaNota()
        import datetime
        tpn.data_inizio = datetime.datetime.now()
        tpn.persist()
        self.numero = tpn.numero

    def tearDown(self):
        tpn = TestataPrimaNota().select(numero=self.numero)
        tpn[0].delete()

    def test_primanota(self):
        """ Do something interesting here...
        """
        self.assertEqual(self.numero, 419)


if __name__ == '__main__':
    tests = ['test_primanota']
    suite = unittest.TestSuite(map(TestPrimaNota, tests))
    unittest.TextTestRunner(verbosity=2).run(suite)
