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
from promogest.dao.AliquotaIva import AliquotaIva
import unittest
from promogest import Environment
from promogest.ui.utils import *
import string


class TestUtils(unittest.TestCase):
    """Test per il modulo Utils
    """

    def test_stringToDate(self):
        """Test trasformazione di stringa in data
        """
        self.assertIsNotNone(stringToDate('1/1/2011'))

    def test_stringToDate_err(self):
        """Test trasformazione con stringa data errata
        """
        self.assertIsNone(stringToDate('1/1'))

    def test_stringToDateBumped(self):
        """Test bump di una data
        """
        self.assertEqual(stringToDateBumped('31/12/2011'),
                         stringToDate('1/1/2012'))

    def test_stringToDateBumped_giorni(self):
        """Test bump di una data con giorni
        """
        self.assertEqual(stringToDateBumped('31/12/2011', giorni=2),
                         stringToDate('2/1/2012'))

    def test_date_festivi(self):
        """Test controlla data se festiva"""
        self.assertTrue(controllaDateFestivi('31/12/2011'))

    def addPointToString(self):
        """ prendo una stringa di sei caratteri/numeri e aggiungo
            un punto al terzultimo posto e poi lo converto in Decimal
        """
        # TODO: da mettere in utils?
        quan = "001318"
        quantita = list(quan)
        quantita.insert(-3,".")
        stringa_quantita =  ",".join(quantita).replace(",","").strip('[]')
        return Decimal(stringa_quantita)

    def test_addPointToString(self):
        """ Test trasforma stringa in decimale
        """
        self.assertEqual(self.addPointToString(), Decimal('1.318'))

    def iva_dict(self):
        # TODO: da mettere in utils?
        tutte = Environment.session.query(AliquotaIva.id, AliquotaIva.percentuale).all()
        diz = {}
        for a in tutte:
            diz[a[0]] = a[1]
        return diz

    def test_iva_dict(self):
        """ Test conversione di una lista di tuple in dizionario
        """
        # brutto, ma funziona per ora...
        diz_atteso = {1: Decimal('10.0000'),
                      2: Decimal('20.0000'),
                      3: Decimal('21.0000')}
        diz = self.iva_dict()
        self.assertDictEqual(diz_atteso, diz)

    def string_to_number(self):
        """Stringa in numeri"""
        tutte = "elisir"
        val=0
        for a in tutte.lower():
            val += ord(a)
        return val

    def test_string_to_number(self):
        """Test stringa in numeri
        """
        pass


if __name__ == '__main__':
    tests = ['test_stringToDate',
             'test_stringToDate_err',
             'test_stringToDateBumped',
             'test_stringToDateBumped_giorni',
             'test_date_festivi',
             "test_addPointToString",
             "test_iva_dict",
             "test_string_to_number"]
    suite = unittest.TestSuite(map(TestUtils, tests))
    unittest.TextTestRunner(verbosity=2).run(suite)
