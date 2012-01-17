# -*- coding: utf-8 -*-

#    Copyright (C) 2005-2012 by Promotux
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
from decimal import *
sys.path.append('../..')
from promogest import bindtextdomain
bindtextdomain('promogest', locale_dir='./po/locale')
import unittest

from promogest.Environment import *
from promogest.dao.TestataDocumento import TestataDocumento
from promogest.dao.InformazioniFatturazioneDocumento import InformazioniFatturazioneDocumento

from promogest.ui.utils import *

#mi serve un movimento di tipo trasferimento merce magazzino

class TestBuildFileConad(unittest.TestCase):
    """Test per il modulo Trasferimento merce magazzino
    """
    numero = -1
    print azienda

    def setUp(self):
        testata = TestataDocumento().select(numero="1367")
        if testata:
            self.t = testata[0]
        self.fc = open("file_conad", "w")

            #print self.t.__dict__

    def test_build_fileconad(self):
        """ Do something interesting here...
        """
        if self.t:
            #Scriviamo la testata della fattura
            dati_differita = InformazioniFatturazioneDocumento().select(id_fattura = self.t.id)
            if dati_differita:
                #print "RIGHE PER OGNI DDT", dati_differita
                for ddtt in dati_differita:
                    ddt = TestataDocumento().getRecord(id=ddtt.id_ddt)
                    self.fc.write("01")
                    self.fc.write(str(dati_differita.index(ddtt)+1).zfill(5))
                    self.fc.write(str(self.t.numero).rjust(6))
                    dt = self.t.data_documento
                    self.fc.write(str(dt.strftime('%y%m%d')))
                    self.fc.write(str(ddt.numero).rjust(6))
                    dt = ddt.data_documento
                    self.fc.write(str(dt.strftime('%y%m%d')))
                    self.fc.write("CodiceURBANI".rjust(15))
                    self.fc.write(" ")
                    self.fc.write(ddt.ragione_sociale_cliente.rjust(15))
                    self.fc.write("6800".rjust(15))
                    self.fc.write(" ".rjust(15))
                    self.fc.write(" ")
                    self.fc.write("F")
                    self.fc.write("EUR")
                    self.fc.write(" ".rjust(25))
                    self.fc.write(" ".rjust(6)+"\n")
                    for riga in ddt.righe:
                        if riga.id_articolo:
                            art = leggiArticolo(riga.id_articolo)
                            #print riga
                            self.fc.write("02")
                            self.fc.write(str(dati_differita.index(ddtt)+1).zfill(5))
                            self.fc.write(str(art["codice"]).rjust(15))
                            self.fc.write(str(art["denominazione"][0:26].replace("à","a")).rjust(30))
                            self.fc.write(str(art["unitaBase"]).upper().rjust(2))
                            self.fc.write(str(mN(Decimal(riga.quantita*(riga.moltiplicatore or 1)),2)).replace(".","").zfill(7))
                            self.fc.write(str(mN(Decimal(riga.valore_unitario_netto),3)).replace(".","").zfill(9))
                            self.fc.write(str(mN(Decimal(riga.quantita or 0) * Decimal(riga.moltiplicatore or 1) * Decimal(riga.valore_unitario_netto or 0),3)).replace(".","").zfill(9))
                            self.fc.write(" ".rjust(4))
                            self.fc.write(" ".rjust(1))
                            self.fc.write(str(mN(riga.percentuale_iva,0)).rjust(2))
                            self.fc.write(" ".rjust(1))
                            self.fc.write("1")
                            self.fc.write("".zfill(6))
                            self.fc.write(" ".rjust(2))
                            self.fc.write(" ")
                            self.fc.write(" ")
                            self.fc.write(" ")
                            self.fc.write("".zfill(5))
                            self.fc.write(" ")
                            self.fc.write(" ")
                            self.fc.write("".zfill(7))
                            self.fc.write(" ".rjust(3))
                            self.fc.write("".zfill(6))
                            self.fc.write(" ".rjust(6)+"\n")

            self.fc.close()

if __name__ == '__main__':
    tests = ['test_build_fileconad']
    suite = unittest.TestSuite(map(TestBuildFileConad, tests))
    unittest.TextTestRunner(verbosity=2).run(suite)
