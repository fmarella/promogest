# -*- coding: utf-8 -*-

#    Copyright (C) 2005-2012 by Promotux
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

try:
    t_fornitura = Table('fornitura',
                    params['metadata'],
                    schema=params['schema'],
                    autoload=True)
except:
    from data.personaGiuridica import t_persona_giuridica
    from data.fornitore import t_fornitore
    from data.fornitura import t_fornitura

from promogest.dao.Dao import Dao
from Multiplo import Multiplo, t_multiplo
from ScontoFornitura import ScontoFornitura
from Fornitore import Fornitore, t_fornitore
#from promogest.lib.migrate import *


class Fornitura(Dao):

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
        def _denominazione_gruppo_taglia(self):
            if self.arti:return self.arti.denominazione_gruppo_taglia
        denominazione_gruppo_taglia = property(_denominazione_gruppo_taglia)

        def _id_articolo_padre(self):
            if self.arti:return self.arti.id_articolo_padre
        id_articolo_padre_taglia_colore=property(_id_articolo_padre)
        id_articolo_padre = property(_id_articolo_padre)

        def _id_gruppo_taglia(self):
            if self.arti:return self.arti.id_gruppo_taglia
        id_gruppo_taglia=property(_id_gruppo_taglia)

        def _id_genere(self):
            if self.arti:return self.arti.id_genere
            id_genere = property(_id_genere)

        def _id_stagione(self):
            if self.arti:return self.arti.id_stagione
        id_stagione = property(_id_stagione)

        def _id_anno(self):
            if self.arti:return self.arti.id_anno
        id_anno = property(_id_anno)

        @property
        def denominazione_taglia(self):
            if self.arti:
                return self.arti.denominazione_taglia

        @property
        def denominazione_colore(self):
            if self.arti:
                return self.arti.denominazione_colore

        @property
        def anno(self):
            if self.arti:
                return self.arti.anno

        @property
        def stagione(self):
            if self.arti:
                return self.arti.stagione

        @property
        def genere(self):
            if self.arti:return self.arti.genere

    def filter_values(self,k,v):
        if k == 'codiceArticoloFornitore':
            dic = {k: t_fornitura.c.codice_articolo_fornitore.ilike("%"+v+"%")}
        elif k == 'codiceArticoloFornitoreEM' or k == "codiceArticoloFornitoreEsatto":
            dic = {k: t_fornitura.c.codice_articolo_fornitore == v}
        elif k == 'idFornitore':
            dic= {k: t_fornitura.c.id_fornitore ==v}
        elif k == 'idFornitoreList':
            dic= {k: t_fornitura.c.id_fornitore.in_(v)}
        elif k == 'idArticolo':
            dic = {k: t_fornitura.c.id_articolo==v}
        elif k == 'idArticoloList':
            dic = {k: t_fornitura.c.id_articolo.in_(v)}
        elif k == 'daDataPrezzo':
            dic = {k: t_fornitura.c.data_prezzo >= v}
        elif k == 'dataPrezzo':
            dic = {k: t_fornitura.c.data_prezzo == v}
        elif k == 'dataFornitura':
            dic = {k: t_fornitura.c.data_fornitura == v}
        elif k == 'aDataPrezzo':
            dic = {k: t_fornitura.c.data_prezzo <= v}
        elif k == 'daDataFornitura':
            dic = {k: t_fornitura.c.data_fornitura >= v}
        elif k == 'aDataFornitura':
            dic = {k: t_fornitura.c.data_fornitura <= v}
        elif k == 'numeroLotto':
            dic = {k: t_fornitura.c.numero_lotto == v}
        elif k == 'noLotto':
            dic = {k: t_fornitura.c.numero_lotto == None}
        return dic[k]

    def scontiFornituraDel(self, idDao):
        aa = ScontoFornitura().select(idFornitura = idDao.id, batchSize=None)
        if aa:
            for a in aa:
                session.delete(a)
            session.commit()

    def persist(self):
        session.add (self)
        session.commit()
        self.scontiFornituraDel(self)
        if self.__scontiFornitura is not None:
            for sco in self.__scontiFornitura:
                sco.id_fornitura = self.id
                sco.persist()



#if "numero_lotto" not in [c.name for c in t_fornitura.columns]:
    #col = Column('numero_lotto', String(200))
    #col.create(t_fornitura)
#if "data_scadenza" not in [c.name for c in t_fornitura.columns]:
    #col = Column('data_scadenza', DateTime)
    #col.create(t_fornitura)
#if "data_produzione" not in [c.name for c in t_fornitura.columns]:
    #col = Column('data_produzione', DateTime)
    #col.create(t_fornitura)

std_mapper = mapper(Fornitura, t_fornitura,
    properties={
        "multi": relation(Multiplo,
            primaryjoin=t_fornitura.c.id_multiplo==t_multiplo.c.id),
        "sconto_fornitura": relation(ScontoFornitura, backref="fornitura"),
        "forni" : relation(Fornitore,
            primaryjoin=t_fornitura.c.id_fornitore==t_fornitore.c.id),
    },
    order_by=[t_fornitura.c.data_fornitura, t_fornitura.c.id_fornitore])
