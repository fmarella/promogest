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

from sqlalchemy import *
from sqlalchemy.orm import *
from promogest.Environment import *

from promogest.dao.Dao import Dao, Base
from promogest.dao.daoContatti.CategoriaContatto import CategoriaContatto



class ContattoCategoriaContatto(Base, Dao):
    try:
        __table__ = Table('contatto_categoria_contatto',
                                params['metadata'],
                                schema = params['schema'],
                                autoload=True,autoload_with=engine)
    except:
        from data.categoriaContatto import t_categoria_contatto
        from data.contattoCategoriaContatto import t_contatto_categoria_contatto
        __table__ = t_contatto_categoria_contatto

    categoria_con = relationship("CategoriaContatto",backref=backref("contatto_categoria_contatto"))

    __mapper_args__ = {
            "order_by":"id_contatto"
    }

    def __init__(self, req=None):
        Dao.__init__(self, entity=self)

    def filter_values(self,k,v):
        dic= {'idContatto':ContattoCategoriaContatto.__table__.c.id_contatto==v,
            'id':ContattoCategoriaContatto.__table__.c.id_contatto==v,
            'idCategoriaContatto':ContattoCategoriaContatto.__table__.c.id_categoria_contatto==v}
        return  dic[k]

    def _categoria_contatto(self):
        if self.categoria_con: return self.categoria_con.denominazione
        else: return ""
    categoria_contatto= property(_categoria_contatto)
