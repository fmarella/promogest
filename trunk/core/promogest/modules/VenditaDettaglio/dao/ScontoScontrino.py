#-*- coding: utf-8 -*-
#
"""
 PromoGest  http://promogest.promotux.it
 Copyright (C) 2005-2010 by Promotux Informatica - http://www.promotux.it/
 Author: Francesco Meloni <francesco@promotux.it>
 License: GNU GPLv2
"""

from sqlalchemy import *
from sqlalchemy.orm import *
from promogest.Environment import *
from promogest.dao.Dao import Dao

class ScontoScontrino(Dao):

    def __init__(self, arg=None):
        Dao.__init__(self, entity=self)

    def filter_values(self, k,v):
        dic= {}
        return  dic[k]

sconto_scontrino=Table('sconto_scontrino',
            params['metadata'],
            schema = params['schema'],
            autoload=True)
std_mapper = mapper(ScontoScontrino, sconto_scontrino, order_by=sconto_scontrino.c.id)
