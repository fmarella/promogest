#-*- coding: utf-8 -*-
#
# Promogest
#
# Copyright (C) 2005 by Promotux Informatica - http://www.promotux.it/
# Author: Francesco Meloni <francesco@promotux.it>


from sqlalchemy import *
from sqlalchemy.orm import *
from promogest.Environment import *
from Dao import Dao

class PersonaGiuridica_(Dao):

    def __init__(self, arg=None):
        Dao.__init__(self, entity=self)

    def filter_values(self,k,v):
        dic= {}
        return  dic[k]

persona_giuridica=Table('persona_giuridica',
                params['metadata'],
                schema = params['schema'],
                autoload=True)

std_mapper = mapper(PersonaGiuridica_, persona_giuridica, order_by=persona_giuridica.c.id)
