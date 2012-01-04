# -*- coding: utf-8 -*-

#    Copyright (C) 2005-2012 by Promotux
#                       di Francesco Meloni snc - http://www.promotux.it/

#    Author: Francesco Meloni  <francesco@promotux.it>
#    This file is part of Promogest.

#    Promogest is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 2 of the License, or
#    (at your option) any later version.

#    Promogest is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

#    You should have received a copy of the GNU General Public License
#    along with Promogest.  If not, see <http://www.gnu.org/licenses/>.


from sqlalchemy import *
from sqlalchemy.orm import *
from core.Environment import *
from Dao import Dao
from User import User

userTable = Table('utente', params['metadata'], autoload=True, schema=params['mainSchema'])

try:
    if params["tipo_db"] == "sqlite":
        utenteFK ='utente.id'
    else:
        utenteFK =params['mainSchema']+'.utente.id'


    olsline  = Table('ols_line', params["metadata"],
            Column('id',Integer,primary_key=True),
            Column('codice',String(10), unique=True, nullable=False),
            Column('data_registrazione',Date),
            Column("data_expire", Date),
            Column('active', Boolean, default=0),
            Column('spot', String(2000), nullable=False),
            Column('clicks', Integer, default=1),
            Column('ordine', Integer, unique=True, nullable=True),
            Column('id_user', Integer,ForeignKey(utenteFK)),
            #useexisting=True,
            schema = params['schema'])
    olsline.create(checkfirst=True)
except:
    olsline=Table('ols_line', params['metadata'],schema = params['schema'],autoload=True)


class OlsLine(Dao):

    def __init__(self, req= None,arg=None):
        Dao.__init__(self, entity=self)

    #@reconstructor
    #def init_on_load(self):
        #self.__dbcategorie = []
        #self.__categorie = []


    def filter_values(self, k,v):
        if k == "denomination":
            dic= { k : olsline.c.denomination.ilike("%"+v+"%")}
        elif k == "denominationEM":
            dic= { k : olsline.c.denomination == v}
        elif k == "codice":
            dic= { k : olsline.c.codice == v}
        elif k =="active":
            dic = { k :olsline.c.active ==v}
        return  dic[k]



std_mapper = mapper(OlsLine, olsline, properties={
            'user' : relation(User, backref="olsline"),
            #'lang' : relation(Language),
            #'categ':relation(SoftwareCategorySoftware,primaryjoin = software.c.id==SoftwareCategorySoftware.id_software, backref='sw'),
                }, order_by=olsline.c.ordine.asc())
