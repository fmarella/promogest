# -*- coding: utf-8 -*-
# Promogest
#
# Copyright (C) 2005-2009 by Promotux Informatica - http://www.promotux.it/

from sqlalchemy import *
from sqlalchemy.orm import *
from promogest.Environment import *
from promogest.dao.Dao import Dao

class ContattoScheda(Dao):

    def __init__(self, arg=None):
        Dao.__init__(self, entity=self)

    def filter_values(self,k,v):
        if k == "id":
            dic= {k:contattoscheda.c.id ==v}
        elif k== "idScheda":
            dic= {k:contattoscheda.c.id_scheda==v}
        return  dic[k]

contattoscheda=Table('contatti_schede',params['metadata'],schema = params['schema'],
                                                                    autoload=True)

std_mapper = mapper(ContattoScheda, contattoscheda, order_by=contattoscheda.c.id)
