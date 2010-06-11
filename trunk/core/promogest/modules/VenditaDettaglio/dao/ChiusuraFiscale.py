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

    def __init__(self, arg=None):
        Dao.__init__(self, entity=self)

    def filter_values(self,k,v):
        if k == 'dataChiusura':
            dic= {k: chiusura_fiscale.c.data_chiusura ==v}
        elif k == 'idMagazzino':
            dic = {k: chiusura_fiscale.c.id_magazzino == v}
        elif k == 'idPuntoCassa':
            dic = {k: chiusura_fiscale.c.id_pos == v}
        return  dic[k]

chiusura_fiscale=Table('chiusura_fiscale',
                    params['metadata'],
                    schema = params['schema'],
                    autoload=True)

std_mapper = mapper(ChiusuraFiscale, chiusura_fiscale,properties={
        #"testatamovimento": relation(TestataMovimento,primaryjoin=
                #(testata_scontrino.c.id_testata_movimento==TestataMovimento.id), backref="testata_scontrino"),
        }, order_by=chiusura_fiscale.c.id)
