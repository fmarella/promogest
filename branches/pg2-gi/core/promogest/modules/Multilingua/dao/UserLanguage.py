# -*- coding: utf-8 -*-

# Promogest
#
# Copyright (C) 2007-2008 by Promotux Informatica - http://www.promotux.it/
# Author: Francesco Meloni <francesco@promotux.it>
# Licenza: GNU GPLv2

from sqlalchemy import Table
from sqlalchemy.orm import mapper, relation
from promogest.Environment import params
from promogest.dao.Dao import Dao
from Language import Language
from promogest.dao.User import User

class UserLanguage(Dao):
    """ RoleAction class database functions  """
    def __init__(self, arg=None):
        Dao.__init__(self, entity=self)

    def filter_values(self,k,v):
        if k == 'idLanguage':
            dic = {k:userlanguage.c.id_language == v}
        elif k == 'idUser':
            dic = {k:userlanguage.c.id_user == v}
        return  dic[k]

userlanguage=Table('userlanguage',
                params['metadata'],
                schema = params['mainSchema'],
                autoload=True)
std_mapper = mapper(UserLanguage, userlanguage, properties={
            'lan':relation(Language, backref='userlanguage'),
            #'use':relation(User, backref='userrole'),
                }, order_by=userlanguage.c.id_language)



