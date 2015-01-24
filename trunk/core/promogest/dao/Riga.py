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
from promogest.dao.Dao import Dao, Base

from promogest.dao.Magazzino import Magazzino
from promogest.dao.Listino import Listino
from promogest.dao.Multiplo import Multiplo
from promogest.dao.Articolo import Articolo
from promogest.dao.UnitaBase import UnitaBase
from promogest.dao.AliquotaIva import AliquotaIva


class Riga(Base, Dao):
    """ Mapper to handle the Row Table """

    try:
        __table__ = Table('riga',
                   params['metadata'],
                   schema=params['schema'],
                   autoload=True)
    except:
        from data.riga import t_riga
        __table__ = t_riga

    __mapper_args__ = {
        'order_by' : "posizione"
    }

    maga = relationship("Magazzino")
    listi = relationship("Listino")
    multi = relationship("Multiplo")
    arti = relationship("Articolo")

    def __init__(self, req=None):
        Dao.__init__(self, entity=self)

    def filter_values(self,k,v):
        """ Filtro del Mapper Riga"""
        if k=='descrizione':
            dic= {k: Riga.__table__.c.descrizione.ilike("%" + v + "%")}
        elif k=="id_articolo":
            dic={k: Riga.__table__.c.id_articolo == v}
        elif k=="idMultiplo":
            dic={k: Riga.__table__.c.id_multiplo == v}
        elif k=="idMagazzino":
            dic={k: Riga.__table__.c.id_magazzino == v}
        return  dic[k]

    @property
    def magazzino(self):
        if self.maga: return self.maga.denominazione
        else: return ""

    @property
    def listino(self):
        if self.listi: return self.listi.denominazione
        else: return ""

    @property
    def multiplo(self):
        if self.multi: return self.multi.denominazione
        else: return ""
    @property
    def codice_articolo(self):
        if self.arti:return self.arti.codice
        else: return ""

    @property
    def aliquota(self):
        """ Relazione aggiunta successivamente, difficile metterla in FK """
        if self.id_iva:
            try:
                cache = CachedDaosDict()
                return cache['aliquotaiva'][self.id_iva][0].denominazione_breve or ""
            except:
                return AliquotaIva().getRecord(id=self.id_iva).denominazione_breve or ""
        else:
            return ""

    @property
    def unita_base(self):
        if self.arti: return self.arti.denominazione_breve_unita_base
        else: return ""

    if hasattr(conf, "PromoWear") and getattr(conf.PromoWear,'mod_enable')=="yes":
        @property
        def denominazione_gruppo_taglia(self):
            if self.arti:return self.arti.denominazione_gruppo_taglia

        def _id_articolo_padre(self):
            if self.arti:return self.arti.id_articolo_padre
        id_articolo_padre_taglia_colore=property(_id_articolo_padre)
        id_articolo_padre = property(_id_articolo_padre)

        @property
        def id_gruppo_taglia(self):
            if self.arti:return self.arti.id_gruppo_taglia
        @property
        def id_genere(self):
            if self.arti:return self.arti.id_genere
        @property
        def id_stagione(self):
            if self.arti:return self.arti.id_stagione
        @property
        def id_anno(self):
            if self.arti:return self.arti.id_anno
        @property
        def denominazione_taglia(self):
            if self.arti:return self.arti.denominazione_taglia
        @property
        def denominazione_colore(self):
            if self.arti:return self.arti.denominazione_colore
        @property
        def anno(self):
            if self.arti:return self.arti.anno
        @property
        def stagione(self):
            if self.arti:return self.arti.stagione
        @property
        def genere(self):
            if self.arti:return self.arti.genere
        @property
        def denominazione_modello(self):
            if self.arti:return self.arti.denominazione_modello


try:
    Riga.__table__.c.posizione
except:
    conn = engine.connect()
    ctx = MigrationContext.configure(conn)
    op = Operations(ctx)
    op.add_column('riga', Column('posizione', Integer),schema=params["schema"])

if tipodb=="sqlite":
    from promogest.dao.Multiplo import Multiplo
    a = session.query(Multiplo.id).all()
    b = session.query(Riga.id_multiplo).all()
    fixit =  list(set(b)-set(a))
    print "fixt-riga_multiplo", fixit
    for f in fixit:
        if f[0] != "None" and f[0] != None:
            aa = Riga().select(idMultiplo=f[0], batchSize=None)
            for a in aa:
                a.id_multiplo = None
                session.add(a)
            session.commit()
