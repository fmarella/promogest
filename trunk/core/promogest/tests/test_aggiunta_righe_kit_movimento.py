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
from promogest.dao.TestataMovimento import TestataMovimento
from promogest.dao.RigaMovimento import RigaMovimento
from promogest.dao.Articolo import Articolo
from promogest.modules.GestioneKit.dao.ArticoloKit import ArticoloKit
from promogest.ui.utils import *

#mi serve un movimento di tipo trasferimento merce magazzino

class TestTestataMovimento(unittest.TestCase):
    """Test per il modulo Trasferimento merce magazzino
    """
    numero = -1
    print azienda

    def setUp(self):
        testate = TestataMovimento().select(idOperazione="Carico da composizione kit")
        if testate:
            self.tm = testate[0]
            print self.tm.__dict__
        self.righeMovimento = []


    def aggiungi_riga(self, art, riga):
        a = leggiArticolo(art.id_articolo_filler)
        print "KIT", a["denominazione"], art.id_articolo_filler, art.quantita
        r = RigaMovimento()
        r.valore_unitario_netto = 0
        r.valore_unitario_lordo = 0
        r.quantita = -1*(art.quantita*riga.quantita)
        r.moltiplicatore = 1
        r.applicazione_sconti = riga.applicazione_sconti
        r.sconti = []
        r.percentuale_iva = a["percentualeAliquotaIva"]
        r.descrizione  = a["denominazione"]
        r.id_articolo = art.id_articolo_filler
        r.id_magazzino = riga.id_magazzino
        r.id_multiplo = riga.id_multiplo
        r.id_listino = riga.id_listino
        r.id_iva = a["idAliquotaIva"]
        r.id_riga_padre = riga.id_riga_padre
        r.scontiRigheMovimento = []
        return r





    def test_composizione_kit_movimento(self):
        """ Do something interesting here...
        """
        if self.tm.operazione == "Carico da composizione kit":
            print " **************** DEVO AGGIUNGERE IN NEGATIVO LE RIGHE KIT *****************"
            righeMov = []
            lista = []

            def gira(arti):
                aa=ArticoloKit().select(idArticoloWrapper=arti)
                if aa:
                    for a in aa:
                        print "A",leggiArticolo(a.id_articolo_wrapper)["denominazione"], leggiArticolo(a.id_articolo_filler)["denominazione"]
                        bb=ArticoloKit().select(idArticoloWrapper=a.id_articolo_wrapper)
                        if bb:
                            lista.append(a.id_articolo_filler)
                            gira(a.id_articolo_filler)

                return lista

            print "NUMERO RIGHE                                               ", len(self.tm.righe)
            for riga in self.tm.righe:
                print leggiArticolo(riga.id_articolo)["denominazione"]

                gira(riga.id_articolo)
                for l in lista:
                    print "OKKKKKKKKKKKKKKKKKKKKKKKKKKK", leggiArticolo(l)["denominazione"]

            self.righeMovimento = self.righeMovimento+righeMov
            print "NUMERO RIGHE DEFINITIVO                                   ", len(self.righeMovimento)
            for rigadef in self.righeMovimento:
                print rigadef.descrizione, rigadef.quantita




if __name__ == '__main__':
    tests = ['test_composizione_kit_movimento']
    suite = unittest.TestSuite(map(TestTestataMovimento, tests))
    unittest.TextTestRunner(verbosity=2).run(suite)
