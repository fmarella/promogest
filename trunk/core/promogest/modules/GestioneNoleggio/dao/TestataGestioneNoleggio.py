# -*- coding: utf-8 -*-

# Promogest
#
# Copyright (C) 2005-2009 by Promotux Informatica - http://www.promotux.it/
# Author: Francesco Meloni <francesco@promotux.it>

from sqlalchemy import *
from sqlalchemy.orm import *
from promogest.Environment import *
from promogest.dao.Dao import Dao


try:
    testatadocumentonoleggio = Table('testata_documento_noleggio', params['metadata'],
                                schema = params['schema'], autoload=True)
except:
    testataDocumento=Table('testata_documento', params['metadata'],schema = params['schema'],autoload=True)

    if tipodb == "sqlite":
        testatadocumentoFK = 'testata_documento.id'
    else:
        testatadocumentoFK = params['schema']+'.testata_documento.id'

    testatadocumentonoleggio = Table('testata_documento_noleggio', params['metadata'],
                        Column('id',Integer,primary_key=True),
                        Column('id_testata_documento',Integer,ForeignKey(testatadocumentoFK,onupdate="CASCADE",ondelete="CASCADE"),primary_key=True),
                        Column('data_inizio_noleggio',DateTime, nullable=False),
                        Column('data_fine_noleggio',DateTime,nullable=False),
                        schema=params['schema'])
    testatadocumentonoleggio.create(checkfirst=True)


class TestataGestioneNoleggio(Dao):

    def __init__(self, arg=None):
        Dao.__init__(self, entity=self)

    def filter_values(self,k,v):
        if k == 'id':
            dic= {k:testatadocumentonoleggio.c.id ==v}
        elif k == 'idTestataDocumento':
            dic= {k:testatadocumentonoleggio.c.id_testata_documento==v}
        elif k == 'daData':
            dic = {k :testatadocumentonoleggio.c.data_inizio_noleggio >= v}
        elif k == 'aData':
            dic = {k:testatadocumentonoleggio.c.data_inizio_noleggio <= v}
        return  dic[k]

std_mapper = mapper(TestataGestioneNoleggio, testatadocumentonoleggio,properties={
        }, order_by=testatadocumentonoleggio.c.id)