# -*- coding: utf-8 -*-

#    Copyright (C) 2005-2015 by Promotux
#                        di Francesco Meloni snc - http://www.promotux.it/

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

from sqlalchemy import *
from sqlalchemy.orm import *
from promogest.Environment import *
from Dao import Dao
from RigaMovimento import RigaMovimento
from Fornitore import Fornitore
from Cliente import Cliente
from Fornitura import Fornitura

class TestataNoleggio(Dao):

    def __init__(self, req=None):
        Dao.__init__(self, entity=self)


    def _getRigheNoleggio(self):
        #if self.__dbRigheMovimento is None:
        self.__dbRigheNoleggio = params['session']\
                                        .query(RigaNoleggio)\
                                        .with_parent(self)\
                                        .filter_by(id_testata_noleggio=self.id)\
                                        .all()
        #if self.__righeMovimento is None:
        self.__righeNoleggio = self.__dbRigheNoleggio[:]
        return self.__righeNoleggio

    def _setRigheNoleggio(self, value):
        self.__righeNoleggio = value

    righe = property(_getRigheNoleggio, _setRigheNoleggio)

    def _ragioneSocialeFornitore(self):
        """ propery ragione sociale fornitore"""
        a = params['session'].query(Fornitore).with_parent(self).filter_by(id=self.id_fornitore).all()
        if not a:
            return a
        else:
            return a[0].ragione_sociale
    ragione_sociale_fornitore = property(_ragioneSocialeFornitore)

    def _ragioneSocialeCliente(self):
        """ property ragione sociale cliente """
        a = params['session'].query(Cliente).with_parent(self).filter_by(id=self.id_cliente).all()
        if not a:
            return a
        else:
            return a[0].ragione_sociale
    ragione_sociale_cliente= property(_ragioneSocialeCliente)

    def filter_values(self,k,v):
        dic= {  'daNumero': self.numero >= v,
                'aNumero':self.numero <= v,
                'daParte':self.parte >= v,
                'aParte' :self.parte <= v,
                'daData':self.data_movimento >= v,
                'aData': self.data_movimento <= v,
                'idOperazione': self.operazione == v,
                'idMagazzino': self.id.in_(select([RigaNoleggio.id_testata_noleggio],RigaNoleggio.id_magazzino== v)),
                'idCliente': self.id_cliente == v,
                'idFornitore': self.id_fornitore == v,
                'dataMovimento': self.data_movimento == v,
                'registroNumerazione': self.registro_numerazione==v,
            }
        return  dic[k]

    def subPersist(self):
        """cancellazione righe associate alla testata
            conn.execStoredProcedure('RigheMovimentoDel',(self.id, ))"""
        def righeNoleggioDel(id=None):
            """Cancella le righe associate ad un movimento"""
            row = RigaNoleggio().select(idTestataNoleggio = id)

            for r in row:
                r.delete()
            return
        righeNoleggioDel(id=self.id)
        if self.__righeNoleggio is not None:
            for riga in self.__righeNoleggio:
                #annullamento id della riga
                riga._resetId()
                #associazione alla riga della testata
                riga.id_testata_noleggio = self.id
                #salvataggio riga
                riga.persist()
                if self.id_fornitore is not None:
                    """aggiornamento forniture
                        cerca la fornitura relativa al fornitore
                        con data <= alla data del movimento"""
                    sconti = []
                    for s in riga.sconti:
                        daoSconto = ScontoFornitura()
                        daoSconto.id_fornitura = daoFornitura.id
                        daoSconto.valore = s.valore
                        daoSconto.tipo_sconto = s.tipo_sconto
                        sconti.append(daoSconto)

                    daoFornitura.sconti = sconti
                    daoFornitura.persist()

testata_nol=Table('testata_noleggio',
                    params['metadata'],
                    schema = params['schema'],
                    autoload=True)
std_mapper = mapper(TestataNoleggio, testata_nol,properties={
        "rigamov": relation(RigaNoleggio, backref="testata_noleggio"),
        "fornitore": relation(Fornitore, backref="testata_noleggio"),
        "cliente": relation(Cliente, backref="testata_noleggio"),
        }
        )

sel_mapper = std_mapper
total_mapper = std_mapper
