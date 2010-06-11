#-*- coding: utf-8 -*-
#
# Promogest
#
# Copyright (C) 2005 by Promotux Informatica - http://www.promotux.it/
# Author: Francesco Meloni <francesco@promotux.it>


from sqlalchemy import *
from sqlalchemy.orm import *
from promogest.Environment import *
from promogest.dao.Dao import Dao
#from promogest.modules.VenditaDettaglio.dao.TestataScontrino import TestataScontrino


class CCardType(Dao):

    def __init__(self, arg=None):
        Dao.__init__(self, entity=self)

    def filter_values(self,k,v):
        dic= {  'denominazione' : c_card_type.c.denominazione.ilike("%"+v+"%")}
        return  dic[k]

c_card_type =Table('credit_card_type',
            params['metadata'],
            schema = params['schema'],
            autoload=True)

std_mapper = mapper(CCardType, c_card_type, order_by=c_card_type.c.id,properties={
#        "tesscon":relation(TestataScontrino,primaryjoin=(TestataScontrino.id_ccardtype==c_card_type.c.id), backref="cctypee")

        })
