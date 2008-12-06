# -*- coding: utf-8 -*-

# Promogest
#
# Copyright (C) 2005 by Promotux Informatica - http://www.promotux.it/
# Author: Alessandro Scano <alessandro@promotux.it>


from sqlalchemy import *
from sqlalchemy.orm import *
from promogest.Environment import *
from promogest.dao.Dao import Dao


class ChiusuraFiscale(Dao):

    def __init__(self, arg=None,isList=False):
        Dao.__init__(self, entity=self.__class__, isList=isList)

    def filter_values(self,k,v):
        dic= {'id':chiusura_fiscale.c.id ==v,
        "dataChiusura": chiusura_fiscale.c.data_chiusura ==v,
                        }
        return  dic[k]

chiusura_fiscale=Table('chiusura_fiscale',
                    params['metadata'],
                    schema = params['schema'],
                    autoload=True)

std_mapper = mapper(ChiusuraFiscale, chiusura_fiscale,properties={
        #"testatamovimento": relation(TestataMovimento,primaryjoin=
                #(testata_scontrino.c.id_testata_movimento==TestataMovimento.id), backref="testata_scontrino"),
        }, order_by=chiusura_fiscale.c.id)