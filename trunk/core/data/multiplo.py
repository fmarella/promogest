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
from promogest.Environment import *

t_multiplo = Table('multiplo', params["metadata"],
        Column('id',Integer,primary_key=True),
        Column('denominazione_breve',String(50),nullable=False),
        Column('denominazione',String(200),nullable=False),
        Column('id_unita_base',Integer,ForeignKey(fk_prefix_main+'unita_base.id', onupdate="CASCADE", ondelete="RESTRICT")),
        Column('id_articolo',Integer,ForeignKey(fk_prefix+'articolo.id', onupdate="CASCADE", ondelete="RESTRICT")),
        Column('moltiplicatore',Numeric(15,6),nullable=False),
        UniqueConstraint('denominazione', 'denominazione_breve'),
        CheckConstraint("id_unita_base IS NULL AND id_articolo IS NOT NULL  OR  id_unita_base IS NOT NULL  AND id_articolo IS NULL"),
        schema=params["schema"]
        )
t_multiplo.create(checkfirst=True)
