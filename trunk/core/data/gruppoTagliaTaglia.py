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

t_gruppo_taglia_taglia = Table('gruppo_taglia_taglia', params['metadata'],
        Column('id_gruppo_taglia',Integer,
                    ForeignKey(fk_prefix + "gruppo_taglia.id",
                            onupdate="CASCADE",
                            ondelete="RESTRICT"),
                    primary_key=True),
        Column('id_taglia',Integer,
                    ForeignKey(fk_prefix + "taglia.id",
                            onupdate="CASCADE",
                            ondelete="RESTRICT"),
                    primary_key=True),
        Column('ordine',Integer,nullable=False),
        schema=params["schema"])
t_gruppo_taglia_taglia.create(checkfirst=True)
