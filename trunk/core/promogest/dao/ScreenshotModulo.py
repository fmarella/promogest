#-*- coding: utf-8 -*-
#
# Promogest - Janas
#
# Copyright (C) 2005 by Promotux Informatica - http://www.promotux.it/
# Author: Francesco Meloni <francesco@promotux.it>

from sqlalchemy import *
from sqlalchemy.orm import *
from core.Environment import *
from core.dao.Modulo import Modulo
from Dao import Dao

moduloTable = Table('modulo', params["metadata"], autoload=True, schema=params["schema"])

if tipo_db == "sqlite":
    moduloFK= 'modulo.id'
else:
    moduloFK = params["schema"]+'.modulo.id'

recapitoTable = Table('screenshot_modulo', params["metadata"],
        Column('id', Integer, primary_key=True),
        Column('testo_alternativo', String(150), nullable=False),
        Column('imagepath',String(300), nullable=False),
        Column('id_modulo',Integer ,ForeignKey(moduloFK,onupdate="CASCADE",ondelete="CASCADE"),nullable=False),
        schema=self.schema
        )
recapitoTable.create(checkfirst=True)


class ScreenShotModulo(Dao):

    def __init__(self, req= None,arg=None):
        Dao.__init__(self, entity=self)

    def filter_values(k,v):
        dic= {
            'idModulo':screenshotmodulo.c.id_modulo == v,
                }
        return  dic[k]

screenshotmodulo=Table('screenshot_modulo', params['metadata'],schema = params['schema'],autoload=True)
std_mapper = mapper(ScreenShotModulo, screenshotmodulo)