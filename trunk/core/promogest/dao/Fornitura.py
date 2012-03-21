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

from sqlalchemy import *
from sqlalchemy.orm import *
from promogest.Environment import *
from Dao import Dao
from Multiplo import Multiplo, multiplo
from ScontoFornitura import ScontoFornitura
from Fornitore import Fornitore, fornitore
from migrate import *


class Fornitura(Dao):

    def __init__(self, req=None):
        Dao.__init__(self, entity=self)

    def _getScontiFornitura(self):
        self.__dbScontiFornitura = self.sconto_fornitura
        self.__scontiFornitura = self.__dbScontiFornitura[:]
        return self.__scontiFornitura

    def _setScontiFornitura(self, value):
        self.__scontiFornitura = value

    sconti = property(_getScontiFornitura, _setScontiFornitura)

    def _fornitore(self):
        if self.forni: return self.forni.ragione_sociale or ""
    fornitore= property(_fornitore)

    def _codice_fornitore(self):
        if self.forni: return self.forni.codice or ""
    codice_fornitore= property(_codice_fornitore)

    def _codiceArticolo(self):
        if self.arti: return self.arti.codice or ""
    codice_articolo= property(_codiceArticolo)

    def _denoArticolo(self):
        if self.arti: return self.arti.denominazione or ""
    articolo= property(_denoArticolo)

    def _multiplo(self):
        if self.multi: return self.multi.denominazione_breve or ""
    multiplo= property(_multiplo)


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

        def _denominazione_taglia(self):
            if self.arti:return self.arti.denominazione_taglia
        denominazione_taglia = property(_denominazione_taglia)

        def _denominazione_colore(self):
            if self.arti:return self.arti.denominazione_colore
        denominazione_colore = property(_denominazione_colore)

        def _anno(self):
            if self.arti:return self.arti.anno
        anno = property(_anno)

        def _stagione(self):
            if self.arti:return self.arti.stagione
        stagione = property(_stagione)

        def _genere(self):
            if self.arti:return self.arti.genere
        genere = property(_genere)



    def filter_values(self,k,v):
        if k == 'codiceArticoloFornitore':
            dic = {k:fornitura.c.codice_articolo_fornitore.ilike("%"+v+"%")}
        elif k == 'codiceArticoloFornitoreEM' or k == "codiceArticoloFornitoreEsatto":
            dic = {k:fornitura.c.codice_articolo_fornitore == v}
        elif k== 'idFornitore':
            dic= {k:fornitura.c.id_fornitore ==v}
        elif k== 'idFornitoreList':
            dic= {k:fornitura.c.id_fornitore.in_(v)}
        elif k == 'idArticolo':
            dic = {k:fornitura.c.id_articolo==v}
        elif k == 'idArticoloList':
            dic = {k:fornitura.c.id_articolo.in_(v)}
        elif k == 'daDataPrezzo':
            dic = {k:fornitura.c.data_prezzo >= v}
        elif k == 'dataPrezzo':
            dic = {k:fornitura.c.data_prezzo == v}
        elif k == 'dataFornitura':
            dic = {k:fornitura.c.data_fornitura == v}
        elif k == 'aDataPrezzo':
            dic = {k:fornitura.c.data_prezzo <= v}
        elif k == 'daDataFornitura':
            dic= {k:fornitura.c.data_fornitura >= v}
        elif k == 'aDataFornitura':
            dic = {k:fornitura.c.data_fornitura <= v}
        return  dic[k]

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

fornitura=Table('fornitura', params['metadata'], schema = params['schema'], autoload=True)

if "numero_lotto" not in [c.name for c in fornitura.columns]:
    col = Column('numero_lotto', String(200))
    col.create(fornitura)
if "data_scadenza" not in [c.name for c in fornitura.columns]:
    col = Column('data_scadenza', DateTime)
    col.create(fornitura)
if "data_produzione" not in [c.name for c in fornitura.columns]:
    col = Column('data_produzione', DateTime)
    col.create(fornitura)

std_mapper = mapper(Fornitura,fornitura, properties={
        "multi": relation(Multiplo,primaryjoin=fornitura.c.id_multiplo==multiplo.c.id),
        "sconto_fornitura": relation(ScontoFornitura, backref="fornitura"),
        "forni" : relation(Fornitore,primaryjoin=fornitura.c.id_fornitore==fornitore.c.id),
        #"arti" : relation(Articolo,primaryjoin=fornitura.c.id_articolo==Articolo.id, backref=backref("artic", uselist=False)),
                }, order_by=[fornitura.c.data_fornitura,fornitura.c.id_fornitore])
