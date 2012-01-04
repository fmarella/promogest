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
from promogest.Environment import *
from promogest.dao.Dao import Dao
from promogest.dao.Riga import Riga

class MisuraPezzo(Dao):
    """ User class provides to make a Users dao which include more used"""

    def __init__(self, req=None):
        Dao.__init__(self, entity=self)

    def filter_values(self,k,v):
        dic= {  'idRiga' : misurapezzo.c.id_riga ==v}
        return  dic[k]

misurapezzo=Table('misura_pezzo',
        params['metadata'],
        schema = params['schema'],
        autoload=True)

std_mapper = mapper(MisuraPezzo, misurapezzo, properties={
        "rig":relation(Riga,primaryjoin=Riga.id==misurapezzo.c.id_riga, backref=backref("sumi")),

}, order_by=misurapezzo.c.id)

#if hasattr(conf, "SuMisura") and getattr(conf.SuMisura,'mod_enable') == "yes":
    ##from promogest.modules.SuMisura.data.SuMisuraDb import *
    ##print "CI PASSIIIIIIIIIIIIIIIIIIIIIIIIII"
    #from promogest.modules.SuMisura.dao.MisuraPezzo import MisuraPezzo
    #std_mapper.add_property("sumi",relation(MisuraPezzo,primaryjoin=
                    #MisuraPezzo.id_riga==riga.c.id,
                    #cascade="all, delete",
                    #backref="riga_mov"))
