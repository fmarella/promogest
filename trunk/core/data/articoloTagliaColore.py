# -*- coding: utf-8 -*-

#    Copyright (C) 2005-2015 by Promotux
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
from promogest.Environment import *

t_articolo_taglia_colore = Table('articolo_taglia_colore', params['metadata'],
            Column('id_articolo',Integer,ForeignKey(fk_prefix+"articolo.id",onupdate="CASCADE",ondelete="CASCADE"),primary_key=True),
            Column('id_articolo_padre',Integer,ForeignKey(fk_prefix+"articolo.id",onupdate="CASCADE",ondelete="CASCADE")),
            Column('id_gruppo_taglia',Integer,ForeignKey(fk_prefix+'gruppo_taglia.id',onupdate="CASCADE",ondelete="CASCADE")),
            Column('id_taglia',Integer,ForeignKey(fk_prefix+"taglia.id",onupdate="CASCADE",ondelete="CASCADE")),
            Column('id_colore',Integer,ForeignKey(fk_prefix+"colore.id",onupdate="CASCADE",ondelete="CASCADE")),
            Column('id_anno',Integer,ForeignKey(fk_prefix_main+"anno_abbigliamento.id",onupdate="CASCADE",ondelete="CASCADE")),
            Column('id_stagione',Integer,ForeignKey(fk_prefix+'stagione_abbigliamento.id',onupdate="CASCADE",ondelete="CASCADE")),
            Column('id_genere',Integer,ForeignKey(fk_prefix+'genere_abbigliamento.id',onupdate="CASCADE",ondelete="CASCADE")),
            Column('id_modello',Integer,ForeignKey(fk_prefix+'modello.id',onupdate="CASCADE",ondelete="CASCADE")),
            UniqueConstraint('id_articolo_padre', 'id_gruppo_taglia', "id_taglia", "id_colore"),
            ForeignKeyConstraint(['id_gruppo_taglia', 'id_taglia'],[fk_prefix+'gruppo_taglia_taglia.id_gruppo_taglia',fk_prefix+'gruppo_taglia_taglia.id_taglia']),
            schema=params['schema'])
t_articolo_taglia_colore.create(checkfirst=True)
