# -*- coding: utf-8 -*-

# Promogest
#
# Copyright (C) 2005 by Promotux Informatica - http://www.promotux.it/
# Author: Francesco Meloni <francesco@promotux.it>

from sqlalchemy import Table
from sqlalchemy.orm import mapper
from promogest.Environment import *
from Dao import Dao

class Language(Dao):

    def __init__(self, arg=None):
        Dao.__init__(self, entity=self)

    def filter_values(self,k,v):
        dic= {}
        return  dic[k]

lang=Table('language', params['metadata'],
    schema = params['mainSchema'],
    autoload=True)

std_mapper = mapper(Language, lang, order_by=lang.c.denominazione)

