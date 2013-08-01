# -*- coding: utf-8 -*-

#    Copyright (C) 2005-2012
#by Promotux di Francesco Meloni snc - http://www.promotux.it/

# Author: Francesco Meloni <francesco@promotux.it>

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


from sqlalchemy import Table
from sqlalchemy.orm import mapper, join
from promogest.Environment import params
from promogest.dao.Dao import Dao


try:
    t_testata_scontrino_cliente=Table('testata_scontrino_cliente',
                                params['metadata'],
                                schema = params['schema'],
                                autoload=True)
except:
    #pass
    from data.testataScontrinoCliente import t_testata_scontrino_cliente

class TestataScontrinoCliente(Dao):

    def __init__(self, req=None):
        Dao.__init__(self, entity=self)

    def filter_values(self,k,v):
        if k == 'id':
            dic= { k :t_testata_scontrino_cliente.c.id == v}
        elif k== 'id_cliente':
            dic ={k:t_testata_scontrino_cliente.c.id_cliente==v}
        elif k== 'id_testata_scontrino':
            dic ={k:t_testata_scontrino_cliente.c.id_testata_scontrino==v}
        return  dic[k]



std_mapper = mapper(TestataScontrinoCliente,t_testata_scontrino_cliente,
                order_by=t_testata_scontrino_cliente.c.id)
