# -*- coding: utf-8 -*-

# Promogest
#
# Copyright (C) 2005 by Promotux Informatica - http://www.promotux.it/
# Author: francesco Meloni <francesco@promotux.it>

from sqlalchemy import *
from sqlalchemy.orm import *
from promogest.Environment import *
from promogest.dao.Dao import Dao

if hasattr(conf, 'GestioneNoleggio'):
    if conf.GestioneNoleggio.primoavvio=="yes":
        """ tabelle schema principale """

        articolo=Table('articolo', params['metadata'],schema = params['schema'],autoload=True)
        articoloGestioneleggioTable = Table('articolo_gestione_noleggio', params['metadata'],
                            Column('id_articolo',Integer,ForeignKey(params['schema']+'.articolo.id',onupdate="CASCADE",ondelete="CASCADE"),primary_key=True),
                            Column('divisore_noleggio_value',Numeric(4), nullable=False),
                            schema=params['schema'])
        articoloGestioneleggioTable.create(checkfirst=True)


        testataDocumento=Table('testata_documento', params['metadata'],schema = params['schema'],autoload=True)
        testataDocumentoNoleggioTable = Table('testata_documento_noleggio', params['metadata'],
                            Column('id_testata_documento',Integer,ForeignKey(params['schema']+'.testata_documento.id',onupdate="CASCADE",ondelete="CASCADE"),primary_key=True),
                            Column('data_inizio_noleggio',DateTime, nullable=False),
                            Column('data_fine_noleggio',DateTime,nullable=False),
                            schema=params['schema'])
        testataDocumentoNoleggioTable.create(checkfirst=True)
        conf.GestioneNoleggio.primoavvio = "yes"
        conf.save()
