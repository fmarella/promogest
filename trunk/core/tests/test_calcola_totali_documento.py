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
path = ".."
if path not in sys.path:
    sys.path.append(path)
from promogest import preEnv

preEnv.tipodbforce = "postgresql"
preEnv.aziendaforce = "urbani"
from promogest.buildEnv import set_configuration
from promogest import Environment
conf = set_configuration("urbani", "2013")
Environment.conf = conf
from promogest.Environment import session

from promogest.dao.TestataDocumento import TestataDocumento
from decimal import Decimal


class TestTestataDocumentoTotali(unittest.TestCase):

    def test_doc1(self):
        """controllo totali per il documento 23701"""
        doc = session.query(TestataDocumento).filter_by(operazione="Fattura differita vendita", id=23701).one()
        doc.totali
        assert doc._totaleImponibile == Decimal('88.52')
        assert doc._totaleImposta == Decimal('8.85')
        assert doc._totaleScontato == Decimal('97.37')
        for info_iva in doc._castellettoIva:
            if info_iva['aliquota'] == Decimal(10):
                assert info_iva['imponibile'] == Decimal("88.52")
                assert info_iva['imposta'] == Decimal("8.85")
                assert info_iva['totale'] == Decimal("97.37")

    def test_doc2(self):
        """controllo totali per il documento 23700"""
        doc = session.query(TestataDocumento).filter_by(operazione="Fattura differita vendita", id=23700).one()
        doc.totali
        assert doc._totaleImponibile == Decimal('224.04')
        assert doc._totaleImposta == Decimal('22.40')
        assert doc._totaleScontato == Decimal('246.44')
        for info_iva in doc._castellettoIva:
            if info_iva['aliquota'] == Decimal(10):
                assert info_iva['imponibile'] == Decimal("224.04")
                assert info_iva['imposta'] == Decimal("22.40")
                assert info_iva['totale'] == Decimal("246.44")

    def test_doc3(self):
        """controllo totali per il documento 23699"""
        doc = session.query(TestataDocumento).filter_by(operazione="Fattura differita vendita", id=23699).one()
        doc.totali
        assert doc._totaleImponibile == Decimal('90.21')
        assert doc._totaleImposta == Decimal('8.34')
        assert doc._totaleScontato == Decimal('98.55')
        for info_iva in doc._castellettoIva:
            if info_iva['aliquota'] == Decimal(4):
                assert info_iva['imponibile'] == Decimal("11.4")
                assert info_iva['imposta'] == Decimal("0.46")
                assert info_iva['totale'] == Decimal("11.86")
            if info_iva['aliquota'] == Decimal(10):
                assert info_iva['imponibile'] == Decimal("78.81")
                assert info_iva['imposta'] == Decimal("7.88")
                assert info_iva['totale'] == Decimal("86.69")

    def test_doc4(self):
        """controllo totali per il documento 23697"""
        doc = session.query(TestataDocumento).filter_by(operazione="Fattura differita vendita", id=23697).one()
        doc.totali
        assert doc._totaleImponibile == Decimal('63.44')
        assert doc._totaleImposta == Decimal('2.54')
        assert doc._totaleScontato == Decimal('65.98')
        for info_iva in doc._castellettoIva:
            if info_iva['aliquota'] == Decimal(4):
                assert info_iva['imponibile'] == Decimal("63.44")
                assert info_iva['imposta'] == Decimal("2.54")
                assert info_iva['totale'] == Decimal("65.98")

    def test_doc5(self):
        """controllo totali per il documento 23694"""
        doc = session.query(TestataDocumento).filter_by(operazione="Fattura differita vendita", id=23694).one()
        doc.totali
        assert doc._totaleImponibile == Decimal('79.86')
        assert doc._totaleImposta == Decimal('7.99')
        assert doc._totaleScontato == Decimal('87.85')
        for info_iva in doc._castellettoIva:
            if info_iva['aliquota'] == Decimal(10):
                assert info_iva['imponibile'] == Decimal("79.86")
                assert info_iva['imposta'] == Decimal("7.99")
                assert info_iva['totale'] == Decimal("87.85")

suite = unittest.TestLoader().loadTestsFromTestCase(TestTestataDocumentoTotali)
unittest.TextTestRunner(verbosity=3).run(suite)
