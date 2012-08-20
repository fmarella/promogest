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

import datetime
from sqlalchemy import *
from sqlalchemy.orm import *
from promogest.Environment import *
from promogest.dao.Dao import Dao
from promogest.dao.DaoUtils import *
from promogest.lib.utils import *


try:
    testataprimanota = Table('testata_prima_nota',
        params['metadata'],
        schema = params['schema'],
        autoload=True)
except:
    testataprimanota = Table('testata_prima_nota',
        params["metadata"],
        Column('id', Integer, primary_key=True),
        Column('numero', Integer, nullable=False),
        Column('note', Text, nullable=True),
        Column('data_inizio', DateTime, nullable=True),
        Column('data_fine', DateTime, nullable=True),
        schema=params["schema"],
        useexisting=True)
    testataprimanota.create(checkfirst=True)

from promogest.modules.PrimaNota.dao.RigaPrimaNota import RigaPrimaNota

class TestataPrimaNota(Dao):

    def __init__(self, req=None):
        Dao.__init__(self, entity=self)
        self.__righePrimaNota = []
        self.__dbRighePrimaNota = []

    @reconstructor
    def init_on_load(self):
        self.__righePrimaNota = []
        self.__dbRighePrimaNota = []

    def _getRighePrimanota(self):
#        if not self.__righePrimaNota:
        self.__dbRighePrimaNota = session.query(RigaPrimaNota)\
                                            .with_parent(self)\
                                            .filter_by(id_testata_prima_nota=self.id)\
                                            .all()
        self.__righePrimaNota = self.__dbRighePrimaNota[:]
        return self.__righePrimaNota

    def _setRighePrimaNota(self, value):
        self.__righePrimaNota = value

    righeprimanota = property(_getRighePrimanota, _setRighePrimaNota)

    def ultimaNota(self):
        a = select([func.max(testataprimanota.c.data_fine)]).execute().fetchall()
        if a:
            return a[0][0]
        else:
            return None

    def filter_values(self,k,v):
        if k == 'daNumero':
            dic = {k:testataprimanota.c.numero >= v}
        elif k == 'aNumero':
            dic = {k:testataprimanota.c.numero <= v}
        elif k == 'numero':
            dic = {k:testataprimanota.c.numero == v}
        elif k == 'daDataInizio':
            dic = {k:testataprimanota.c.data_inizio >= v}
        elif k== 'aDataInizio':
            dic = {k:testataprimanota.c.data_inizio <= v}
        elif k== 'tipoCassa':
            dic = {k:and_(testataprimanota.c.id== RigaPrimaNota.id_testata_prima_nota,
                            RigaPrimaNota.tipo !="cassa")}
        elif k== 'denominazione':
            dic = {k:and_(testataprimanota.c.id== RigaPrimaNota.id_testata_prima_nota,
                            RigaPrimaNota.denominazione.ilike("%"+v+"%"))}
        elif k== 'tipoBanca':
            dic = {k:and_(testataprimanota.c.id== RigaPrimaNota.id_testata_prima_nota,
                            RigaPrimaNota.tipo !="banca")}
        elif k== 'idBanca':
            dic = {k:and_(testataprimanota.c.id== RigaPrimaNota.id_testata_prima_nota,
                            RigaPrimaNota.id_banca ==v)}
        elif k== 'segnoEntrate':
            dic = {k:and_(testataprimanota.c.id== RigaPrimaNota.id_testata_prima_nota,
                            RigaPrimaNota.segno !="entrata")}
        elif k== 'segnoUscite':
            dic = {k:and_(testataprimanota.c.id== RigaPrimaNota.id_testata_prima_nota,
                            RigaPrimaNota.segno !="uscita")}
        return  dic[k]

    def righePrimaNotaDel(self,id=None):
        """ Cancella le righe associate ad una prima nota
        """
        row = RigaPrimaNota().select(idTestataPrimaNota= id,
                                    offset = None,
                                    batchSize = None)
        if row:
            for r in row:
                params['session'].delete(r)
            params["session"].commit()
        return True

    def __TotalePrimaNota(self):
        totale = 0
        tot_entrate = 0
        tot_uscite = 0
        tot_entrate_cassa = 0
        tot_entrate_banca = 0
        tot_uscite_cassa = 0
        tot_uscite_banca = 0
        for riga in self.righeprimanota:
            if riga.segno == "entrata":
                totale += riga.valore
                tot_entrate += riga.valore
                if riga.tipo == "cassa":
                    tot_entrate_cassa += riga.valore
                else:
                    tot_entrate_banca += riga.valore
            else:
                totale -= riga.valore
                tot_uscite -= riga.valore
                if riga.tipo == "cassa":
                    tot_uscite_cassa -= riga.valore
                else:
                    tot_uscite_banca -= riga.valore
        totali = {
                "totale": totale,
                "tot_entrate": tot_entrate,
                "tot_uscite": tot_uscite,
                "tot_entrate_banca": tot_entrate_banca,
                "tot_entrate_cassa": tot_entrate_cassa,
                "tot_uscite_banca": tot_uscite_banca,
                "tot_uscite_cassa": tot_uscite_cassa
                }
        return totali
    totali = property(__TotalePrimaNota)

    def delete(self):
        from RigaPrimaNotaTestataDocumentoScadenza import RigaPrimaNotaTestataDocumentoScadenza
        row = RigaPrimaNota().select(idTestataPrimaNota= self.id,
                                    offset = None,
                                    batchSize = None)
        if row:
            for r in row:
                rpntdsc = RigaPrimaNotaTestataDocumentoScadenza().select(idRigaPrimaNota=r.id, batchSize=None)
                if rpntdsc:
                    for rr in rpntdsc:
                        params['session'].delete(rr)
                        params["session"].commit()
                params['session'].delete(r)
                params["session"].commit()
        params['session'].delete(self)
        params["session"].commit()


    def persist(self):
        """ salvataggio righe associate alla testata """
        pg2log.info("DENTRO IL TESTATA PRIMA NOTA CASSA")
        if not self.data_inizio:
            self.data_inizio = datetime.datetime.now()
        if not self.numero:
            self.numero = getNuovoNumero(self.data_inizio)
        params["session"].add(self)
        params["session"].commit()
        if self.__righePrimaNota:
            for riga in self.__righePrimaNota:
                riga.id_testata_prima_nota = self.id
                riga.persist()
        self.__righePrimaNota = []

def getNuovoNumero(data_inizio):
    anno = data_inizio.year
    num = Environment.session.query(func.max(TestataPrimaNota.numero)).filter((and_(TestataPrimaNota.data_inizio.between(datetime.date(int(anno), 1, 1), datetime.date(int(anno) + 1, 1, 1))))).one()[0]
    numero = 1
    if num:
        numero = num + 1
    return numero

std_mapper = mapper(TestataPrimaNota, testataprimanota,
    properties={
        "rigatest": relation(RigaPrimaNota,
            primaryjoin=testataprimanota.c.id==RigaPrimaNota.id_testata_prima_nota,
            foreign_keys=[RigaPrimaNota.id_testata_prima_nota],
            cascade="all, delete")
    },
    order_by=testataprimanota.c.numero.desc())
