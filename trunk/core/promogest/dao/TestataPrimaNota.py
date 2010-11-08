# -*- coding: utf-8 -*-

#    Copyright (C) 2005, 2006, 2007 2008, 2009, 2010 by Promotux
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


from sqlalchemy import *
from sqlalchemy.orm import *
from promogest.Environment import *
from Dao import Dao
from DaoUtils import *
from promogest.ui.utils import numeroRegistroGet
from promogest.ui.utils import *


try:
    testataprimanota=Table('testata_prima_nota',
            params['metadata'],
            schema = params['schema'],
            autoload=True)
except:
    testataprimanota = Table('testata_prima_nota', params["metadata"],
            Column('id', Integer, primary_key=True),
            Column('numero', Integer, nullable=False),
            Column('note', Text, nullable=True),
            Column('data_inizio', DateTime, nullable=True),
            Column('data_fine', DateTime, nullable=True),
            schema=params["schema"],
            useexisting=True)
    testataprimanota.create(checkfirst=True)

from promogest.dao.RigaPrimaNota import RigaPrimaNota

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
        self.__dbRighePrimaNota = object_session(self).query(RigaPrimaNota)\
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
        elif k == 'datafinecheck':
            dic = {k:testataprimanota.c.data_fine == None}
        elif k == 'datafine':
            dic = {k:testataprimanota.c.data_fine == v}
        elif k == 'numero':
            dic = {k:testataprimanota.c.numero == v}
        elif k == 'daDataInizio':
            dic = {k:testataprimanota.c.data_inizio >= v}
        elif k== 'aDataInizio':
            dic = {k:testataprimanota.c.data_inizio <= v}
        elif k == 'daDataFine':
            dic = {k:testataprimanota.c.data_fine >= v}
        elif k== 'aDataFine':
            dic = {k:testataprimanota.c.data_fine <= v}
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
                "totale" : totale,
                "tot_entrate" :tot_entrate,
                "tot_uscite": tot_uscite,
                "tot_entrate_banca" :tot_entrate_banca,
                "tot_entrate_cassa":tot_entrate_cassa,
                "tot_uscite_banca":tot_uscite_banca,
                "tot_uscite_cassa":tot_uscite_cassa
                }
        return totali
    totali = property(__TotalePrimaNota)

    def persist(self):
        """ cancellazione righe associate alla testata """
        pg2log.info("DENTRO IL TESTATA PRIMA NOTA CASSA")
        params["session"].add(self)
        params["session"].commit()
        if self.__righePrimaNota:
            for riga in self.__righePrimaNota:
                riga.id_testata_prima_nota = self.id
                riga.persist()
        self.__righePrimaNota = []

std_mapper = mapper(TestataPrimaNota, testataprimanota,properties={
        "rigatest": relation(RigaPrimaNota,primaryjoin=
                testataprimanota.c.id==RigaPrimaNota.id_testata_prima_nota,
                cascade="all, delete",
                backref="tprimanota")},
                order_by=testataprimanota.c.id)
