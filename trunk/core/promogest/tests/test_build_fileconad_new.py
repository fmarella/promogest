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
from parser import myparse


def generaFileConad(testata):
    """
    """
    if testata:
        #Scriviamo la testata della fattura
        dati_differita = InformazioniFatturazioneDocumento().select(id_fattura = testata.id)
        if dati_differita:
            for ddtt in dati_differita:
                ddt = TestataDocumento().getRecord(id=ddtt.id_ddt)

                dati = {
                    'testata': {
                        'numero_progressivo': str(dati_differita.index(ddtt) + 1),
                        'numero_fattura': str(testata.numero),
                        'data_fattura': testata.data_documento,
                        'numero_bolla': str(ddt.numero),
                        'data_bolla': ddt.data_documento,
                        'codice_fornitore': 'CodiceURBANI',
                        'codice_cliente': ddt.ragione_sociale_cliente[0:14],
                    },
                    'dettaglio': []
                }


                for riga in ddt.righe:
                    if riga.id_articolo:
                        art = leggiArticolo(riga.id_articolo)
                        dati['dettaglio'].append(
                            {
                                'numero_progressivo':str(dati_differita.index(ddtt) + 1),
                                'codice_articolo': str(art["codice"]),
                                'descrizione': str(art["denominazione"][0:26].replace("à", "a")),
                                'unita_misura': str(art["unitaBase"]).upper(),
                                'qta_fatturata': str(mN(Decimal(riga.quantita * (riga.moltiplicatore or 1)), 2)),
                                'prezzo_unitario': str(mN(Decimal(riga.valore_unitario_netto), 3)),
                                'importo_totale': str(mN(Decimal(riga.quantita or 0) * Decimal(riga.moltiplicatore or 1) * Decimal(riga.valore_unitario_netto or 0), 3)),
                                'aliquota_iva': str(mN(riga.percentuale_iva,0))
                            })
            return dati


class TestBuildFileConad(unittest.TestCase):
    """Test per il modulo Trasferimento merce magazzino
    """
    numero = -1
    testata = None
    file_conad = None
    infile = None

    def setUp(self):
        testate = TestataDocumento().select(numero="1")
        if testate:
            self.testata = testate[0]
        self.file_conad = open("file_conad", "wb")
        self.infile = open('tracciato_conad.xml', 'r')

    def test_build_fileconad(self):
        """ build fileconad
        """
        dati = generaFileConad(self.testata)
        myparse(self.infile, dati, self.file_conad)

if __name__ == '__main__':
    tests = ['test_build_fileconad']
    suite = unittest.TestSuite(map(TestBuildFileConad, tests))
    unittest.TextTestRunner(verbosity=2).run(suite)
