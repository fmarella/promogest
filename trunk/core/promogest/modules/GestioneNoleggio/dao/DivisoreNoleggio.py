# -*- coding: utf-8 -*-

# Promogest
#
# Copyright (C) 2005-2008 by Promotux Informatica - http://www.promotux.it/
# Author: Francesco Meloni <francesco@promotux.it>

from sqlalchemy import *
from sqlalchemy.orm import *
from promogest.Environment import *
from promogest.dao.Dao import Dao

class DivisoreNoleggio(Dao):

    def __init__(self, arg=None):
        Dao.__init__(self, entity=self)


    def filter_values(self,k,v):
        if k =='idDivisoreNoleggio':
            dic= {k:divisorenoleggio.c.id_articolo ==v}
        elif k == "idValue":
            dic = {k:divisorenoleggio.c.value ==v}
        return  dic[k]

divisorenoleggio=Table('divisore_noleggio',params['metadata'],schema = params['schema'],autoload=True)

std_mapper = mapper(DivisoreNoleggio, divisorenoleggio, order_by=divisorenoleggio.c.value)