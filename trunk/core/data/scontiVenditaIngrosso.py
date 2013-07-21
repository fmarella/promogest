# -*- coding: utf-8 -*-

#    Copyright (C) 2005-2013 by Promotux
#                        di Francesco Meloni snc - http://www.promotux.it/

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

class ScontiVenditaIngrossoDb(object):

    def __init__(self, schema = None,mainSchema=None, metadata=None, session=None,debug=False):
        self.metadata = metadata
        self.session_sl = session
        self.schema = schema
        self.debug = debug

    def create(self):

        listinoArticoloTable = Table('listino_articolo', self.metadata, autoload=True, schema=self.schema)
        scontoTable = Table('sconto', self.metadata, autoload=True, schema=self.schema)

        if self.schema:
            scontoFK =self.schema+'.sconto.id'
            listinoarticoloFKid_listino =self.schema+'.listino_articolo.id_listino'
            listinoarticoloFKid_articolo =self.schema+'.listino_articolo.id_articolo'
            listinoarticoloFKdatalistinoarticolo =self.schema+'.listino_articolo.data_listino_articolo'
        else:
            scontoFK ='sconto.id'
            listinoarticoloFKid_listino ='listino_articolo.id_listino'
            listinoarticoloFKid_articolo ='listino_articolo.id_articolo'
            listinoarticoloFKdatalistinoarticolo ='listino_articolo.data_listino_articolo'

        scontiVenditaIngrossoTable = Table('sconti_vendita_ingrosso', self.metadata,
                Column('id',Integer,ForeignKey(scontoFK,onupdate="CASCADE",ondelete="CASCADE"), primary_key=True),
                Column('id_listino',Integer),
                Column('id_articolo',Integer),
                Column('data_listino_articolo',DateTime),
                ForeignKeyConstraint(columns=("id_listino","id_articolo","data_listino_articolo"),
                                                refcolumns=(listinoarticoloFKid_listino,
                                                            listinoarticoloFKid_articolo,
                                                            listinoarticoloFKdatalistinoarticolo),
                                                onupdate="CASCADE", ondelete="CASCADE"),

                schema=self.schema
                )

        scontiVenditaIngrossoTable.create(checkfirst=True)

    def update(self, req=None, arg=None):
        pass

    def alter(self, req=None, arg=None):
        pass
