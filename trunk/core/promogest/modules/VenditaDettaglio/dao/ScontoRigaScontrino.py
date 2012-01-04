# -*- coding: utf-8 -*-

#    Copyright (C) 2005-2012  by Promotux
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
from sqlalchemy.orm import *
from promogest.Environment import *
from promogest.dao.Dao import Dao
from promogest.modules.VenditaDettaglio.dao.ScontoScontrino import ScontoScontrino
from promogest.modules.VenditaDettaglio.ui.VenditaDettaglioUtils import scontoRigaScontrinoDel


class ScontoRigaScontrino(Dao):

    def __init__(self, req=None):
        Dao.__init__(self, entity=self)

    def filter_values(self,k,v):
        dic= {'id':sconto_riga_scontrino.c.id ==v,
        'idRigaScontrino':sconto_riga_scontrino.c.id_riga_scontrino==v,}
        return  dic[k]


sconto_riga_scontrino=Table('sconto_riga_scontrino',
                            params['metadata'],
                            schema = params['schema'],
                            autoload=True)


sconto_scontrino = Table('sconto_scontrino',
                                params['metadata'],
                                schema = params['schema'],
                                autoload=True)

j = join(sconto_scontrino, sconto_riga_scontrino)

std_mapper = mapper(ScontoRigaScontrino,j, properties={
            'id':[sconto_scontrino.c.id, sconto_riga_scontrino.c.id],
            }, order_by=sconto_riga_scontrino.c.id)
