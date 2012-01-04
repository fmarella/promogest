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
from promoCMS.Environment import *
from Dao import Dao
from Language import Language
from StaticPages import StaticPages

class StaticMenu(Dao):

    def __init__(self,req=None, arg=None,isList=False, id=None):
        Dao.__init__(self, entity=self.__class__, isList=isList, id=id)

    def filter_values(self, k,v):
        if k == 'id_language':
            dic= {  k : staticmenu.c.id_language == v}
        elif k =='id_languageList':
            dic= {  k : staticmenu.c.id_language.in_(v)}
        return  dic[k]

    def _permalink(self):
        if self.page :return self.page.permalink or ""

    permalink = property(_permalink)
staticmenu= Table('static_menu',params['metadata'],schema = params['schema'],autoload=True)

std_mapper=mapper(StaticMenu, staticmenu,
        properties={
        "lang":relation(Language,backref="static_menu"),
        "page":relation(StaticPages,backref="static_menu")})
