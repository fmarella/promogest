# -*- coding: utf-8 -*-

#    Copyright (C) 2005-2013 by Promotux
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

import os
import sys
from optparse import OptionParser

path = ".."
if path not in sys.path:
    sys.path.append(path)

from promogest.dao.Operazione import Operazione
from promogest.dao.Setting import Setting


class creaNuovoTipoDocumento():

    def __init__(self):
        parser = OptionParser()
        debug_help = """Crea un nuovo tipo di documento
si usa lanciando lo script  --nome nome documento da fare

es: python creaNuovoTipoDocumento -- nome "Fattura vendita A"
"""
        parser.add_option("-n", "--nome",
                                action="store",
                                help=debug_help,
                                default="False",
                                type="string",
                                dest="do")
        (options, args) = parser.parse_args()
        print "AAAAAAAAAAAAAA", options
        if options.do:
            self.do(options.do)

    def do(self, nome=False):
        """        "Vendita dettaglio";"-";"vendita_iva";"cliente";
        """
        print "NOME", nome
        lettere = ["A","B","C","D","E","F","G","H"]
        for l in lettere:
            ce = Operazione().getRecord(id="Fattura vendita "+l)
            if not ce:
                a = Operazione()
                a.denominazione = "Fattura vendita "+l
                a.segno = "-"
                a.fonte_valore =  "vendita_iva"
                a.tipo_persona_giuridica = "cliente"
                #a.tipo_operazione =
                a.persist()
                print "NON CE", ce
            else:
                print "OK","Fattura vendita "+l
            cc = Setting().getRecord(id="Fattura vendita "+l+".registro")
            # "Fattura vendita.registro";"Registro associato alle fatture vendita";"registro_fattura_vendita"
            if not cc:
                a = Setting()
                a.key = "Fattura vendita "+l+".registro"
                a.description = "Registro associato alle fatture vendita "+l
                a.value = "registro_fattura_vendita_"+l.lower()
                a.persist()
                print "NON CE", cc
            else:
                print "OK","Registro Fattura vendita "+l

            cc = Setting().getRecord(id="registro_fattura_vendita_"+l.lower() + ".rotazione")
            # "registro_fattura_vendita.rotazione";"Tipologia di rotazione del registro_fattura_vendita";"annuale"
            if not cc:
                a = Setting()
                a.key = "registro_fattura_vendita_"+l.lower() + ".rotazione"
                a.description = "Tipologia di rotazione del registro_fattura_vendita "+l
                a.value = "annuale"
                a.persist()
                print "NON CE", cc
            else:
                print "OK","Rotazione Fattura vendita "+l




#s= select([operazione.c.denominazione]).execute().fetchall()
#if (u'Buono visione merce',) not in s or s==[]:
    #tipo = operazione.insert()
    #tipo.execute(denominazione='Buono visione merce',
                #segno='-',
                #fonte_valore= "vendita_senza_iva",
                #tipo_persona_giuridica = "cliente")

#setting = Table('setting', meta, schema = schemadest, autoload=True)
#s= select([setting.c.key]).execute().fetchall()
#if (u'Buono visione merce.registro',) not in s or s==[]:
    #tipo = setting.insert()
    #tipo.execute(key='Buono visione merce.registro',
                #description='Registro associato ai buoni visione merce',
                #value= "registro_buono_visione_merce")
    #tipo.execute(key='registro_buono_visione_merce.rotazione',
                #description='Tipologia di rotazione del registro_buono_visione_merce',
                #value= "annuale")
#if __name__ == '__main__':
creaNuovoTipoDocumento()
