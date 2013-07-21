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

class ArticleDb(object):

    def __init__(self, schema = None, mainSchema=None, metadata=None, session=None,debug=False):
        self.metadata = metadata
        self.schema = schema
        self.mainSchema = mainSchema
        self.debug = debug

    def create(self):

        aliquota_ivaTable = Table('aliquota_iva',self.metadata, autoload=True, schema=self.schema)
        categoria_articoloTable = Table('categoria_articolo',self.metadata, autoload=True,schema=self.schema)
        famiglia_articoloTable = Table('famiglia_articolo',self.metadata, autoload=True,schema=self.schema)
        imageTable = Table('image', self.metadata, autoload=True,schema=self.schema)
        imballaggioTable = Table('imballaggio', self.metadata, autoload=True,schema=self.schema)
        unita_baseTable = Table('unita_base', self.metadata, autoload=True,schema=self.mainSchema)
        statoArticoloTable = Table('stato_articolo', self.metadata, autoload=True,schema=self.mainSchema)

        if self.mainSchema:
            statoarticoloFK =self.mainSchema+'.stato_articolo.id'
            unitabseFK =self.mainSchema+'.unita_base.id'
        else:
            statoarticoloFK ='stato_articolo.id'
            unitabseFK ='unita_base.id'

        if self.schema:
            aliquotaivaFK =self.schema+'.aliquota_iva.id'
            categoriaarticoloFK =self.schema+'.categoria_articolo.id'
            famigliaarticoloFK=self.schema+'.famiglia_articolo.id'
            imageFK =self.schema+'.image.id'
            imballaggioFK =self.schema+'.imballaggio.id'
        else:
            aliquotaivaFK = 'aliquota_iva.id'
            categoriaarticoloFK ='categoria_articolo.id'
            famigliaarticoloFK='famiglia_articolo.id'
            imageFK ='image.id'
            imballaggioFK ='imballaggio.id'

        articleTable= Table('articolo', self.metadata,
            Column('id', Integer, primary_key=True),
            Column('codice', String(50), nullable=False, unique=True),
            Column('denominazione', String(300), nullable=False),
            Column('id_aliquota_iva', Integer, ForeignKey(aliquotaivaFK,onupdate="CASCADE",ondelete="RESTRICT")),
            Column('id_famiglia_articolo', Integer, ForeignKey(famigliaarticoloFK,onupdate="CASCADE",ondelete="RESTRICT")),
            Column('id_categoria_articolo', Integer, ForeignKey(categoriaarticoloFK,onupdate="CASCADE",ondelete="RESTRICT")),
            Column('id_immagine', Integer,ForeignKey(imageFK,onupdate="CASCADE",ondelete="RESTRICT")),
            Column('id_unita_base', Integer, ForeignKey(unitabseFK,onupdate="CASCADE",ondelete="RESTRICT")),
            Column('id_stato_articolo', Integer, ForeignKey(statoarticoloFK,onupdate="CASCADE",ondelete="RESTRICT")),
            Column('produttore', String(150), nullable=True),
            Column('unita_dimensioni', String(20), nullable=True),
            Column('lunghezza', Float, nullable=True),
            Column('larghezza', Float, nullable=True),
            Column('altezza', Float, nullable=True),
            Column('unita_volume', String(20), nullable=True),
            Column('volume', String(20), nullable=True),
            Column('unita_peso', String(20), nullable=True),
            Column('peso_lordo', Float, nullable=True),
            Column('id_imballaggio', Integer, ForeignKey(imballaggioFK,onupdate="CASCADE",ondelete="RESTRICT")),
            Column('peso_imballaggio', Float, nullable=True),
            Column('stampa_etichetta', Boolean, default=0),
            Column('codice_etichetta', String(50), nullable=True),
            Column('descrizione_etichetta', String(200), nullable=True),
            Column('stampa_listino', Boolean, default=0),
            Column('descrizione_listino', String(200), nullable=True),
            Column('aggiornamento_listino_auto', Boolean, default=0),
            Column('timestamp_variazione', DateTime, nullable=True),
            Column('note', Text, nullable=True),
            Column('contenuto', Text, nullable=True),
            Column('cancellato', Boolean, nullable=True, default=False),
            Column('sospeso', Boolean, nullable=True, default=False),
            Column('quantita_minima',Float),
            schema=self.schema
                )
        articleTable.create(checkfirst=True)
        return

    def update(self, req=None, arg=None, listino=None):
        pass

    def alter(self, req=None, arg=None):
        pass
