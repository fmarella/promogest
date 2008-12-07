#-*- coding: utf-8 -*-
#
# Promogest
#
# Copyright (C) 2005 by Promotux Informatica - http://www.promotux.it/
# Author: Dario Fadda <dario@promotux.it>
# Author: Francesco Meloni <francesco@promotux.it>

from sqlalchemy import *
from sqlalchemy.orm import *
from promogest.Environment import *
from Dao import Dao

class ScontoRigaNoleggio(Dao):

    def __init__(self, arg=None):
        Dao.__init__(self, entity=self)

    def filter_values(self, k,v):
        dic= {  'id' : sconto_riga_noleggio.c.id==v,
        }
        return  dic[k]


sconto_riga_noleggio=Table('sconto_riga_noleggio',
            params['metadata'],
            schema = params['schema'],
            autoload=True)
std_mapper = mapper(ScontoRigaNoleggio, sconto_riga_noleggio)

