# -*- coding: utf-8 -*-

# Promogest - Janas
#
# Copyright (C) 2007-2008 by Promotux Informatica - http://www.promotux.it/
# Author: Francesco Meloni <francesco@promotux.it>
# Licenza: GNU GPLv2

from sqlalchemy import *
from sqlalchemy.orm import *
from promogest.Environment import *
from promogest.dao.Dao import Dao


try:
    sectionuser=Table('section_user', params['metadata'], schema = params['schema'],autoload=True)
except:
    sectionuser = Table('section_user', params['metadata'],
            Column('id_utente',Integer,primary_key=True),
            Column('name_section',String(50),primary_key=True),
            schema=params['schema'])
    sectionuser.create(checkfirst=True)

class SectionUser(Dao):
    """ SectionUser class database functions  """
    def __init__(self, req=None):
        Dao.__init__(self, entity=self)

    def filter_values(self,k,v):
        if k == 'id_utente':
            dic = {k:sectionuser.c.id_utente == v}
        elif k == 'id_section':
            dic = {k:sectionuser.c.id_section == v}
        return  dic[k]

std_mapper = mapper(SectionUser, sectionuser, order_by=sectionuser.c.name_section)
