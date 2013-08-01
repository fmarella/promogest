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

from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy.orm import mapper, relation, backref
from promogest.Environment import params
from promogest.dao.Dao import Dao
from promogest.modules.Pagamenti.dao.TestataDocumentoScadenza import TestataDocumentoScadenza
from promogest.modules.PrimaNota.dao.RigaPrimaNota import RigaPrimaNota, rigaprimanota

rigaprimanotatestatadocumentoscadenza = Table('riga_primanota_testata_documento_scadenza',
                                                  params['metadata'],
                                                  schema=params['schema'],
                                                  autoload=True)



class RigaPrimaNotaTestataDocumentoScadenza(Dao):

    def __init__(self, req=None):
        Dao.__init__(self, entity=self)

    def filter_values(self, k, v):
        if k == "idRigaPrimaNota":
            dic = {k: rigaprimanotatestatadocumentoscadenza.c.id_riga_prima_nota == v}
        elif k == 'idTestataDocumentoScadenza':
            dic = {k: rigaprimanotatestatadocumentoscadenza.c.id_testata_documento_scadenza == v}
        return  dic[k]

std_mapper = mapper(RigaPrimaNotaTestataDocumentoScadenza,
                   rigaprimanotatestatadocumentoscadenza,
                   properties={
                    "tds" :relation(TestataDocumentoScadenza, backref="rpntds"),
                    "_rpn_": relation(RigaPrimaNota,
                        primaryjoin=rigaprimanotatestatadocumentoscadenza.c.id_riga_prima_nota==rigaprimanota.c.id),
                   },
                   order_by=rigaprimanotatestatadocumentoscadenza.c.id_riga_prima_nota)
