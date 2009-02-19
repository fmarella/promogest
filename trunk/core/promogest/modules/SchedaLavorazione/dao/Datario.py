# -*- coding: utf-8 -*-
# Promogest
#
# Copyright (C) 2005 by Promotux Informatica - http://www.promotux.it/
# Author: Francesco Meloni <francesco@promotux.it>

from sqlalchemy import *
from sqlalchemy.orm import *
from promogest.Environment import *
from promogest.dao.Dao import Dao


class Datario(Dao):

    def __init__(self, arg=None):
        Dao.__init__(self, entity=self)

    def filter_values(self,k,v):
        if k == "id":
            dic= {k:datario.c.id ==v}
        elif k== "idScheda":
            dic= {k:datario.c.id_scheda==v}
        return  dic[k]

datario=Table('datario',params['metadata'],schema = params['schema'],autoload=True)

std_mapper = mapper(Datario, datario, properties={
                        }, order_by = datario.c.id)