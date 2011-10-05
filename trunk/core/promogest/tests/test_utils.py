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

from promogest import Environment as env
from promogest.ui.utils import *


class TestUtils(unittest.TestCase):
    """Test per il modulo Utils
    """
    def test_stringToDateBumped(self):
        """Test stringToDateBumped
        """
        if env.tipodb == 'sqlite':
            self.assertEqual(stringToDateBumped('31/12/2011'),
                             stringToDate('1/1/2012'))
        else:
            self.assertEqual(stringToDateBumped('31/12/2011'),
                             stringToDate('31/12/2011'))

    def test_addPointToString(self):
        """ Test, prendo una stringa di sei caratteri/numeri e aggiungo
            un punto al terzultimo posto e poi lo converto in Decimal
        """
        quan = "001318"
        quantita = list(quan)
        quantita.insert(-3,".")
        stringa_quantita =  ",".join(quantita).replace(",","").strip('[]')
        print Decimal(stringa_quantita)

if __name__ == '__main__':
    tests = ['test_stringToDateBumped', "test_addPointToString"]
    suite = unittest.TestSuite(map(TestUtils, tests))
    unittest.TextTestRunner(verbosity=2).run(suite)
