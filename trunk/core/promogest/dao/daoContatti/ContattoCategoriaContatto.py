# -*- coding: utf-8 -*-

#    Copyright (C) 2005-2012
#by Promotux di Francesco Meloni snc - http://www.promotux.it/

# Author: Francesco Meloni <francesco@promotux.it>

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
from sqlalchemy.orm import mapper, relation, backref
from promogest.Environment import params
from promogest.dao.daoContatti.CategoriaContatto import CategoriaContatto
from promogest.dao.Dao import Dao

class ContattoCategoriaContatto(Dao):

    def __init__(self, req=None):
        Dao.__init__(self, entity=self)

    def filter_values(self,k,v):
        dic= {'idContatto':contatto_categoria_contatto.c.id_contatto==v,
            'id':contatto_categoria_contatto.c.id_contatto==v,
            'idCategoriaContatto':contatto_categoria_contatto.c.id_categoria_contatto==v}
        return  dic[k]

    def _categoria_contatto(self):
        if self.categoria_con: return self.categoria_con.denominazione
        else: return ""
    categoria_contatto= property(_categoria_contatto)

contatto_categoria_contatto=Table('contatto_categoria_contatto',
                            params['metadata'],
                            schema = params['schema'],
                            autoload=True)

std_mapper= mapper(ContattoCategoriaContatto, contatto_categoria_contatto,properties={
"categoria_con":relation(CategoriaContatto,backref=backref("contatto_categoria_contatto"))},
                    order_by=contatto_categoria_contatto.c.id_contatto)
