# -*- coding: utf-8 -*-

# Promogest
#
# Copyright (C) 2007 by Promotux Informatica - http://www.promotux.it/
# Author: Francesco Meloni <francesco@promotux.it>

from sqlalchemy import *
from sqlalchemy.orm import *
from promogest.Environment import *
from Dao import Dao

class Role(Dao):
    """
    Role class provides to make a Users dao which include more used
    database functions
    """
    def __init__(self, arg=None,isList=False, id=None):
        Dao.__init__(self, entity=self.__class__, isList=isList, id=id)

    def filter_values(self,k,v):
        dic= {  'name' : role.c.name.ilike("%"+v+"%")}
        return  dic[k]

role=Table('role',
            params['metadata'],
            schema = params['mainSchema'],
            autoload=True)
std_mapper = mapper(Role, role, order_by=role.c.id)