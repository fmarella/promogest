# -*- coding: utf-8 -*-

#    Copyright (C) 2005, 2006, 2007 2008, 2009, 2010, 2011 by Promotux
#                        di Francesco Meloni snc - http://www.promotux.it/

#    Author: Francesco Meloni <francesco@promotux.it>

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

try:
    ritenutaaccontoriga = Table('ritenuta_acconto_riga', params['metadata'],
                                    schema = params['schema'], autoload=True)
except:
    rigaTable = Table('riga', params['metadata'], autoload=True, schema=params['schema'])

    if tipodb == "sqlite":
        rigaFK = 'riga.id'
    else:
        rigaFK = params['schema']+'.riga.id'

    ritenutaaccontoriga = Table('ritenuta_acconto_riga', params['metadata'],
                        Column('id',Integer,primary_key=True),
                        Column('provvigionale', Boolean,nullable=False),
                        Column('ritenuta_percentuale',Numeric(8,4),nullable=True),
                        Column('rivalsa_percentuale',Numeric(8,4),nullable=True),
                        Column('id_riga',Integer,ForeignKey(rigaFK, onupdate="CASCADE", ondelete="RESTRICT"),nullable=False),
                        UniqueConstraint('id_riga'),
                        schema=params['schema'])
    ritenutaaccontoriga.create(checkfirst=True)

class RigaRitenutaAcconto(Dao):
    """ TABELLA:  ritenuta_acconto_riga,
    """
    def __init__(self, arg=None):
        Dao.__init__(self, entity=self)

    def filter_values(self,k,v):
        if k == 'id':
            dic= {k:ritenutaaccontoriga.c.id ==v}
        return  dic[k]

std_mapper = mapper(RigaRitenutaAcconto, ritenutaaccontoriga,properties={
                    }, order_by=ritenutaaccontoriga.c.id)
