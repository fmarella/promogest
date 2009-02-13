#-*- coding: utf-8 -*-
#
# Promogest
#
# Copyright (C) 2005 by Promotux Informatica - http://www.promotux.it/
# Author: Francesco Meloni <francesco@promotux.it>

from sqlalchemy import Table
from sqlalchemy.orm import mapper
from promogest.Environment import params
from Dao import Dao

class Riga(Dao):
    """ Mapper to handle the Row Table """
    def __init__(self, arg=None):
        Dao.__init__(self, entity=self)

    def filter_values(self,k,v):
        """ Filtro del Mapper Riga"""
        if k=='descrizione':
            dic= {  k : riga.c.descrizione.ilike("%"+v+"%")}
        elif k=="id_articolo":
            dic={k:riga.c.id_articolo==v}
        return  dic[k]

riga=Table('riga', params['metadata'],schema = params['schema'],autoload=True)
std_mapper = mapper(Riga, riga, properties={}, order_by=riga.c.id)