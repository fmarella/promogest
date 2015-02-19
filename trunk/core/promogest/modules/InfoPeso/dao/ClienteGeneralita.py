# -*- coding: utf-8 -*-

#    Copyright (C) 2005-2015 by Promotux
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
from promogest.dao.DaoUtils import *
from promogest.lib.utils import *
from promogest.dao.Cliente import Cliente

try:
    clientegeneralita = Table('cliente_generalita',
            params['metadata'],
            schema = params['schema'],
            autoload=True)
except:
    clienteTable = Table('cliente', params['metadata'], autoload=True, schema=params['schema'])

    if params["tipo_db"] == "sqlite":
        clienteFK ='cliente.id'
    else:
        clienteFK = params['schema']+'.cliente.id'

    clientegeneralita = Table('cliente_generalita', params["metadata"],
            Column('id', Integer, primary_key=True),
            Column('id_cliente', Integer,ForeignKey(clienteFK,onupdate="CASCADE",ondelete="CASCADE")),
            Column('data_nascita', DateTime, nullable=True),
            Column('altezza', Numeric(16,4), nullable=True),
            Column('genere', String(10), nullable=True),
            schema=params["schema"],
            useexisting=True)
    clientegeneralita.create(checkfirst=True)

class ClienteGeneralita(Dao):

    def __init__(self, req=None):
        Dao.__init__(self, entity=self)

    @property
    def cliente(self):
        """ esempio di funzione  unita alla property """
        cli=  Cliente().getRecord(id=self.id_cliente)
        if cli:
            return cli.ragione_sociale
        else:
            return ""

    def filter_values(self,k,v):
        if k == 'idCliente':
            dic = {k:clientegeneralita.c.id_cliente == v}
        return  dic[k]

std_mapper = mapper(ClienteGeneralita, clientegeneralita,properties={
        "CLI": relation(Cliente,primaryjoin=
                clientegeneralita.c.id_cliente==Cliente.id,
                cascade="all, delete")},
                order_by=clientegeneralita.c.id)
