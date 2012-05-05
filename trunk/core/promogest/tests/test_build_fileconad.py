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

from promogest.lib.utils import *

#mi serve un movimento di tipo trasferimento merce magazzino

def generaFileConad(testata, file_conad):
    """
    """
    if testata:
        #Scriviamo la testata della fattura
        dati_differita = InformazioniFatturazioneDocumento().select(id_fattura = testata.id)
        if dati_differita:
            for ddtt in dati_differita:
                ddt = TestataDocumento().getRecord(id=ddtt.id_ddt)
                file_conad.write("01")
                file_conad.write(str(dati_differita.index(ddtt)+1).zfill(5)) #numero progressivo
                file_conad.write(str(testata.numero).rjust(6)) #numero fattura
                file_conad.write(str(testata.data_documento.strftime('%y%m%d'))) #data fattura
                file_conad.write(str(ddt.numero).rjust(6)) #numero bolla
                file_conad.write(str(ddt.data_documento.strftime('%y%m%d')))
                file_conad.write("CodiceURBANI".ljust(15))
                file_conad.write(" ")
                file_conad.write(ddt.ragione_sociale_cliente[0:14].ljust(15))
                file_conad.write("6800".ljust(15))
                file_conad.write(" ".rjust(15)) #codice socio
                file_conad.write(" ")
                file_conad.write("F")
                file_conad.write("EUR")
                file_conad.write(" ".rjust(25))
                file_conad.write(" ".rjust(6)+"\n")
                for riga in ddt.righe:
                    if riga.id_articolo:
                        art = leggiArticolo(riga.id_articolo)
                        file_conad.write("02")
                        file_conad.write(str(dati_differita.index(ddtt) + 1).zfill(5))
                        file_conad.write(str(art["codice"]).rjust(15))
                        file_conad.write(str(art["denominazione"][0:26].replace("à", "a")).ljust(30))
                        file_conad.write(str(art["unitaBase"]).upper().rjust(2))
                        file_conad.write(str(mN(Decimal(riga.quantita * (riga.moltiplicatore or 1)), 2)).replace(".","").zfill(7))
                        file_conad.write(str(mN(Decimal(riga.valore_unitario_netto), 3)).replace(".","").zfill(9))
                        file_conad.write(str(mN(Decimal(riga.quantita or 0) * Decimal(riga.moltiplicatore or 1) * Decimal(riga.valore_unitario_netto or 0), 3)).replace(".","").zfill(9))
                        file_conad.write("".zfill(4))
                        file_conad.write(" ".rjust(1))
                        file_conad.write(str(mN(riga.percentuale_iva,0)).rjust(2))
                        file_conad.write(" ".rjust(1))
                        file_conad.write("1")
                        file_conad.write("".zfill(6))
                        file_conad.write(" ".rjust(2))
                        file_conad.write(" ")
                        file_conad.write(" ")
                        file_conad.write(" ")
                        file_conad.write("".zfill(5))
                        file_conad.write(" ")
                        file_conad.write(" ")
                        file_conad.write("".zfill(7))
                        file_conad.write(" ".rjust(3))
                        file_conad.write("".zfill(6))
                        file_conad.write(" ".rjust(6) + "\n")

        file_conad.close()


class TestBuildFileConad(unittest.TestCase):
    """Test per il modulo Trasferimento merce magazzino
    """
    numero = -1
    testata = None
    file_conad = None

    def setUp(self):
        testate = TestataDocumento().select(numero="1")
        if testate:
            self.testata = testate[0]
        self.file_conad = open("file_conad", "wb")

    def test_build_fileconad(self):
        """ build fileconad
        """
        generaFileConad(self.testata, self.file_conad)

if __name__ == '__main__':
    tests = ['test_build_fileconad']
    suite = unittest.TestSuite(map(TestBuildFileConad, tests))
    unittest.TextTestRunner(verbosity=2).run(suite)
