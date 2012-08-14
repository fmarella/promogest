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

riga_primanotaTable = Table('riga_prima_nota',
                            params['metadata'],
                            autoload=True,
                            schema=params['schema'])
testata_documento_scadenzaTable = Table('testata_documento_scadenza',
                                      params['metadata'],
                                      schema=params['schema'],
                                      autoload=True)

try:
    rigaprimanotatestatadocumentoscadenza = Table('riga_primanota_testata_documento_scadenza',
                                                  params['metadata'],
                                                  schema=params['schema'],
                                                  autoload=True)
except:
    if params["tipo_db"] == "sqlite":
        rigaprimanotaFK = 'riga_prima_nota.id'
        testatadocumentoscadenzaFK = 'testata_documento_scadenza.id'
    else:
        rigaprimanotaFK = params['schema'] + '.riga_prima_nota.id'
        testatadocumentoscadenzaFK = params['schema'] + '.testata_documento_scadenza.id'

    rigaprimanotatestatadocumentoscadenza = Table('riga_primanota_testata_documento_scadenza',
                                                  params["metadata"],
                                                  Column('id', Integer, primary_key=True),
                                                  Column('id_riga_prima_nota',
                                                         Integer,
                                                         ForeignKey(rigaprimanotaFK),
                                                         nullable=False),
                                                  Column('id_testata_documento_scadenza',
                                                         Integer,
                                                         ForeignKey(testatadocumentoscadenzaFK),
                                                         nullable=False),
                                                  schema=params["schema"],
                                                  useexisting=True)

    rigaprimanotatestatadocumentoscadenza.create(checkfirst=True)


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
                    "tds" :relation(TestataDocumentoScadenza, cascade="all, delete", backref="rpntds")
                   },
                   order_by=rigaprimanotatestatadocumentoscadenza.c.id_riga_prima_nota)
