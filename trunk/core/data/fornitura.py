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

t_fornitura = Table('fornitura', params["metadata"],
        Column('id',Integer,primary_key=True),
        Column('codice_articolo_fornitore',String(100),nullable=True),
        Column('prezzo_lordo',Numeric(16,4),nullable=False),
        Column('prezzo_netto',Numeric(16,4),nullable=False),
        Column('applicazione_sconti',String(20),nullable=True),
        Column('scorta_minima',Integer,nullable=True),
        Column('tempo_arrivo_merce',Integer,nullable=True),
        Column('fornitore_preferenziale',Boolean,nullable=True, default=False),
        Column('percentuale_iva',Numeric(8,4),nullable=True),
        Column('data_fornitura',DateTime,nullable=True),
        Column('data_prezzo',DateTime,nullable=True),
        Column('numero_lotto', String(200)),
        Column('data_scadenza', DateTime),
        Column('data_produzione', DateTime),
        #chiavi esterne
        Column('id_fornitore',Integer,ForeignKey(fk_prefix+'fornitore.id', onupdate="CASCADE", ondelete="RESTRICT")),
        Column('id_articolo',Integer,ForeignKey(fk_prefix+'articolo.id', onupdate="CASCADE", ondelete="CASCADE")),
        Column('id_multiplo',Integer,ForeignKey(fk_prefix+'multiplo.id', onupdate="CASCADE", ondelete="RESTRICT")),
        UniqueConstraint('id_fornitore', 'id_articolo', 'data_prezzo'),
        CheckConstraint( "applicazione_sconti = 'scalare' or applicazione_sconti = 'non scalare'" ),
        schema=params["schema"],
        extend_existing=True
        )
t_fornitura.create(checkfirst=True)
