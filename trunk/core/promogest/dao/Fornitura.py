# -*- coding: utf-8 -*-

#    Copyright (C) 2005-2015 by Promotux
#                       di Francesco Meloni snc - http://www.promotux.it/

#    Author: Francesco Meloni  <francesco@promotux.it>
#    Author: Francesco Marella <francesco.marella@anche.no>

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
from promogest.dao.Multiplo import Multiplo
from promogest.dao.ScontoFornitura import ScontoFornitura
from promogest.dao.Fornitore import Fornitore


class Fornitura(Base, Dao):
    try:
        __table__ = Table('fornitura',
                    params['metadata'],
                    schema=params['schema'],
                    autoload=True)
    except:
        from data.personaGiuridica import t_persona_giuridica
        from data.fornitore import t_fornitore
        from data.fornitura import t_fornitura
        __table__ = t_fornitura

    multi = relationship("Multiplo")
    sconto_fornitura = relationship("ScontoFornitura", backref="fornitura")
    forni = relationship("Fornitore")

    def __init__(self, req=None):
        Dao.__init__(self, entity=self)
        self.__scontiFornitura = None

    def sconti():
        doc = "The sconti property."
        def fget(self):
            self.__dbScontiFornitura = self.sconto_fornitura
            self.__scontiFornitura = self.__dbScontiFornitura[:]
            return self.__scontiFornitura
        def fset(self, value):
            self.__scontiFornitura = value
        def fdel(self):
            del self._scontiFornitura
        return locals()
    sconti = property(**sconti())

    @property
    def fornitore(self):
        if self.forni:
            return self.forni.ragione_sociale or ""

    @property
    def codice_fornitore(self):
        if self.forni:
            return self.forni.codice or ""

    @property
    def codice_articolo(self):
        if self.arti:
            return self.arti.codice or ""

    @property
    def articolo(self):
        if self.arti:
            return self.arti.denominazione or ""

    @property
    def multiplo(self):
        if self.multi:
            return self.multi.denominazione_breve or ""


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
            if self.arti: return self.arti.denominazione_taglia
        @property
        def denominazione_colore(self):
            if self.arti: return self.arti.denominazione_colore
        @property
        def anno(self):
            if self.arti: return self.arti.anno

        @property
        def stagione(self):
            if self.arti: return self.arti.stagione

        @property
        def genere(self):
            if self.arti:return self.arti.genere

    def filter_values(self,k,v):
        if k == 'codiceArticoloFornitore':
            dic = {k: Fornitura.__table__.c.codice_articolo_fornitore.ilike("%"+v+"%")}
        elif k == 'codiceArticoloFornitoreEM' or k == "codiceArticoloFornitoreEsatto":
            dic = {k: Fornitura.__table__.c.codice_articolo_fornitore == v}
        elif k == 'idFornitore':
            dic= {k: Fornitura.__table__.c.id_fornitore ==v}
        elif k == 'idFornitoreList':
            dic= {k: Fornitura.__table__.c.id_fornitore.in_(v)}
        elif k == 'idArticolo':
            dic = {k: Fornitura.__table__.c.id_articolo==v}
        elif k == 'idArticoloList':
            dic = {k: Fornitura.__table__.c.id_articolo.in_(v)}
        elif k == 'daDataPrezzo':
            dic = {k: Fornitura.__table__.c.data_prezzo >= v}
        elif k == 'dataPrezzo':
            dic = {k: Fornitura.__table__.c.data_prezzo == v}
        elif k == 'dataFornitura':
            dic = {k: Fornitura.__table__.c.data_fornitura == v}
        elif k == 'aDataPrezzo':
            dic = {k: Fornitura.__table__.c.data_prezzo <= v}
        elif k == 'daDataFornitura':
            dic = {k: Fornitura.__table__.c.data_fornitura >= v}
        elif k == 'aDataFornitura':
            dic = {k: Fornitura.__table__.c.data_fornitura <= v}
        elif k == 'numeroLotto':
            dic = {k: Fornitura.__table__.c.numero_lotto == v}
        elif k == 'noLotto':
            dic = {k: Fornitura.__table__.c.numero_lotto == None}
        return dic[k]

    def scontiFornituraDel(self, idDao):
        aa = ScontoFornitura().select(idFornitura = idDao.id, batchSize=None)
        if aa:
            for a in aa:
                session.delete(a)
            session.commit()

    def persist(self):
        try:
            session.add (self)
            session.commit()
            self.scontiFornituraDel(self)
            if self.__scontiFornitura is not None:
                for sco in self.__scontiFornitura:
                    sco.id_fornitura = self.id
                    sco.persist()
        except:
            session.rollback()
