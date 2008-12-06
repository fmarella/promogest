#-*- coding: utf-8 -*-
#
# Promogest
#
# Copyright (C) 2005 by Promotux Informatica - http://www.promotux.it/
# Author: Francesco Meloni <francesco@promotux.it>


from sqlalchemy import *
from sqlalchemy.orm import *
from promogest.Environment import *
from CategoriaContatto import CategoriaContatto
from Dao import Dao

class ContattoCategoriaContatto(Dao):

    def __init__(self, arg=None,isList=False):
        Dao.__init__(self, entity=self.__class__, isList=isList)

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



