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

        if tipodb == "sqlite":
            articoloFK = 'articolo.id'
        else:
            articoloFK = params['schema']+'.articolo.id'

        articoloGestioneleggioTable = Table('articolo_gestione_noleggio', params['metadata'],
                            Column('id_articolo',Integer,ForeignKey(articoloFK,onupdate="CASCADE",ondelete="CASCADE"),primary_key=True),
                            Column('divisore_noleggio_value',Numeric(4), nullable=False),
                            schema=params['schema'])
        articoloGestioneleggioTable.create(checkfirst=True)


        testataDocumento=Table('testata_documento', params['metadata'],schema = params['schema'],autoload=True)

        if tipodb == "sqlite":
            testatadocumentoFK = 'testata_documento.id'
        else:
            testatadocumentoFK = params['schema']+'.testata_documento.id'

        testataDocumentoNoleggioTable = Table('testata_documento_noleggio', params['metadata'],
                            Column('id_testata_documento',Integer,ForeignKey(testatadocumentoFK,onupdate="CASCADE",ondelete="CASCADE"),primary_key=True),
                            Column('data_inizio_noleggio',DateTime, nullable=False),
                            Column('data_fine_noleggio',DateTime,nullable=False),
                            schema=params['schema'])
        testataDocumentoNoleggioTable.create(checkfirst=True)
        conf.GestioneNoleggio.primoavvio = "no"
        conf.save()
