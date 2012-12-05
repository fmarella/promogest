# -*- coding: utf-8 -*-

#    Copyright (C) 2005-2012 by Promotux
#                        di Francesco Meloni snc - http://www.promotux.it/

#    Author: Francesco Meloni <francesco@promotux.it>
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

from sqlalchemy import Table
from sqlalchemy.orm import mapper, relation
from promogest.Environment import params, conf
from UnitaBase import UnitaBase
from Dao import Dao


class Multiplo(Dao):

    def __init__(self, req=None):
        Dao.__init__(self, entity=self)

    def filter_values(self,k,v):
        if k == 'idArticolo':
            dic = {k : t_multiplo.c.id_articolo==v}
        elif k == 'idUnitaBase':
            dic = {k: t_multiplo.c.id_unita_base==v}
        elif k == 'denominazione':
            dic = {k: t_multiplo.c.denominazione.ilike("%"+v+"%")}
        return dic[k]

    @property
    def unita_base(self):
        if self.uniba:
            return self.uniba.denominazione
        else:
            return ""

    @property
    def articolo(self):
        if self.arti:
            return self.arti.denominazione
        else:
            return ""

    if hasattr(conf, "PromoWear") and getattr(conf.PromoWear,'mod_enable')=="yes":
        @property
        def denominazione_gruppo_taglia(self):
            if self.arti:
                return self.arti.denominazione_gruppo_taglia

        def _id_articolo_padre(self):
            if self.arti:
                return self.arti.id_articolo_padre
        id_articolo_padre_taglia_colore = property(_id_articolo_padre)
        id_articolo_padre = property(_id_articolo_padre)

        @property
        def id_gruppo_taglia(self):
            if self.arti:
                return self.arti.id_gruppo_taglia

        @property
        def id_genere(self):
            if self.arti:
                return self.arti.id_genere

        @property
        def id_stagione(self):
            if self.arti:
                return self.arti.id_stagione

        @property
        def id_anno(self):
            if self.arti:
                return self.arti.id_anno

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
            if self.arti:
                return self.arti.genere

t_multiplo = Table('multiplo',
                   params['metadata'],
                   schema=params['schema'],
                   autoload=True)

std_mapper = mapper(Multiplo, t_multiplo, properties={
        "uniba":relation(UnitaBase, primaryjoin=t_multiplo.c.id_unita_base==UnitaBase.id),
        #"arti":relation(Articolo,primaryjoin=multiplo.c.id_articolo==Articolo.id)
    }, order_by=t_multiplo.c.id)
