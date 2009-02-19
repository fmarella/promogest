# -*- coding: utf-8 -*-
# Promogest
#
# Copyright (C) 2005 by Promotux Informatica - http://www.promotux.it/
# Author: Dr astico (Pinna Marco) <zoccolodignu@gmail.com>

"""
CREATE TABLE colori_stampa (
    id                      BIGSERIAL   NOT NULL PRIMARY KEY
    ,denominazione          VARCHAR(50) NOT NULL
    ,UNIQUE (id, denominazione)
);
"""
from sqlalchemy import *
from sqlalchemy.orm import *
from promogest.Environment import *
from promogest.dao.Dao import Dao


class ColoreStampa(Dao):

    def __init__(self, arg=None):
        Dao.__init__(self, entity=self)

    def filter_values(self,k,v):
        dic= {'id':coloristampa.c.id ==v}
        return  dic[k]

coloristampa=Table('colore_stampa',
                        params['metadata'],
                        schema = params['schema'],
                        autoload=True)

std_mapper = mapper(ColoreStampa, coloristampa, order_by=coloristampa.c.id)
