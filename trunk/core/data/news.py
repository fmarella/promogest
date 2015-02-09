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

from promogest.Environment import *

t_news= Table('news', params['metadata'],
        Column('id', Integer, primary_key=True),
        Column('title', String(200), nullable=False),
        Column('abstract', String(400), nullable=True),
        Column('body', Text, nullable=True),
        Column('source_url', String(400), nullable=True),
        Column('source_url_alt_text', String(400), nullable=True),
        Column('imagepath', String(400), nullable=True),
        Column('insert_date', DateTime, nullable=True),
        Column('publication_date', DateTime, nullable=True),
        Column('clicks', Integer),
        Column("permalink", String(500), nullable=True),
        Column('active', Boolean, default=0),
        Column('id_categoria', Integer,ForeignKey('{0}news_category.id'.format(fk_prefix))),
        Column('id_user', Integer,ForeignKey('{0}utente.id'.format(fk_prefix_main))),
        Column('id_language', Integer,ForeignKey('{0}language.id'.format(fk_prefix_main))),
        schema=params['schema'],
        extend_existing=True,
        )
t_news.create(checkfirst=True)
