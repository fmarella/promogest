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

from sqlalchemy import Table
from sqlalchemy.orm import mapper
from migrate import *
from promogest.Environment import *
from promogest.dao.Dao import Dao
from promogest.dao.DaoUtils import get_columns
from promogest.dao.CachedDaosDict import CachedDaosDict
from promogest.dao.Magazzino import Magazzino
from promogest.dao.Listino import Listino
from promogest.dao.Multiplo import Multiplo
from promogest.dao.Articolo import Articolo
from promogest.dao.UnitaBase import UnitaBase
from promogest.dao.AliquotaIva import AliquotaIva

t_riga = Table('riga',
               params['metadata'],
               schema=params['schema'],
               autoload=True)

columns_t_riga = get_columns(t_riga)

if "id_iva" not in columns_t_riga:
    delete_pickle()
    col = Column('id_iva', Integer)
    col.create(t_riga)

if "posizione" not in columns_t_riga:
    delete_pickle()
    col = Column('posizione', Integer)
    col.create(t_riga)

if "id_riga_padre" not in columns_t_riga:
    delete_pickle()
    col = Column('id_riga_padre', Integer)
    col.create(t_riga)

class Riga(Dao):
    """ Mapper to handle the Row Table """
    def __init__(self, req=None):
        Dao.__init__(self, entity=self)

    def filter_values(self,k,v):
        """ Filtro del Mapper Riga"""
        if k=='descrizione':
            dic= {k: t_riga.c.descrizione.ilike("%"+v+"%")}
        elif k=="id_articolo":
            dic={k: t_riga.c.id_articolo==v}
        return  dic[k]

    def __magazzino(self):
        if self.maga: return self.maga.denominazione
        else: return ""
    magazzino= property(__magazzino)

    def __listino(self):
        if self.listi: return self.listi.denominazione
        else: return ""
    listino= property(__listino)

    def __multiplo(self):
        if self.multi: return self.multi.denominazione
        else: return ""
    multiplo = property(__multiplo)

    def __codiceArticolo(self):
        if self.arti:return self.arti.codice
        else: return ""
    codice_articolo= property(__codiceArticolo)

    def _getAliquotaIva(self):
        if self.id_iva:
            cache = CachedDaosDict()
            return cache['aliquotaiva'][self.id_iva][0].denominazione_breve or ""
        else:
            return ""
    aliquota = property(_getAliquotaIva)

    def __unita_base(self):

        if self.arti: return self.arti.denominazione_breve_unita_base
        else: return ""
    unita_base = property(__unita_base)

    if hasattr(conf, "PromoWear") and getattr(conf.PromoWear,'mod_enable')=="yes":
        def _denominazione_gruppo_taglia(self):
            #if self.ATC: return self.ATC.denominazione or ""
            if self.arti:return self.arti.denominazione_gruppo_taglia
            #else: return ""
        denominazione_gruppo_taglia = property(_denominazione_gruppo_taglia)

        def _id_articolo_padre(self):
            #if self.ATC: return self.ATC.id_articolo_padre or None
            if self.arti:return self.arti.id_articolo_padre
        id_articolo_padre_taglia_colore=property(_id_articolo_padre)
        id_articolo_padre = property(_id_articolo_padre)

        def _id_gruppo_taglia(self):
            #if self.ATC: return self.ATC.id_gruppo_taglia or None
            if self.arti:return self.arti.id_gruppo_taglia
        id_gruppo_taglia=property(_id_gruppo_taglia)

        def _id_genere(self):
            #if self.ATC: return self.ATC.id_genere or None
            if self.arti:return self.arti.id_genere
            #else: return ""
        id_genere = property(_id_genere)

        def _id_stagione(self):
            if self.arti:return self.arti.id_stagione
        id_stagione = property(_id_stagione)

        def _id_anno(self):
            if self.arti:return self.arti.id_anno
        id_anno = property(_id_anno)

        def _denominazione_taglia(self):
            """ esempio di funzione  unita alla property """
            if self.arti:return self.arti.denominazione_taglia
        denominazione_taglia = property(_denominazione_taglia)

        def _denominazione_colore(self):
            """ esempio di funzione  unita alla property """
            if self.arti:return self.arti.denominazione_colore
        denominazione_colore = property(_denominazione_colore)

        def _anno(self):
            """ esempio di funzione  unita alla property """
            if self.arti:return self.arti.anno
        anno = property(_anno)

        def _stagione(self):
            """ esempio di funzione  unita alla property """
            if self.arti:return self.arti.stagione
        stagione = property(_stagione)

        def _genere(self):
            """ esempio di funzione  unita alla property """
            if self.arti:return self.arti.genere
        genere = property(_genere)

        def _modello(self):
            """ esempio di funzione  unita alla property """
            if self.arti:return self.arti.denominazione_modello
        denominazione_modello = property(_modello)

std_mapper = mapper(Riga, t_riga, properties={
            "maga":relation(Magazzino,primaryjoin=t_riga.c.id_magazzino==Magazzino.id),
            "listi":relation(Listino,primaryjoin=t_riga.c.id_listino==Listino.id),
            "multi":relation(Multiplo,primaryjoin=t_riga.c.id_multiplo==Multiplo.id),
            "arti":relation(Articolo,primaryjoin=t_riga.c.id_articolo==Articolo.id),
}, order_by=t_riga.c.posizione)
