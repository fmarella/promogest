# -*- coding: utf-8 -*-

#    Copyright (C) 2005-2013 by Promotux
#                        di Francesco Meloni snc - http://www.promotux.it/

#    Author: Francesco Marella <francesco.marella@anche.no>

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
from sqlalchemy.orm import *
from promogest.Environment import *
from promogest.dao.Dao import Dao
from promogest.modules.ADR.dao.CategoriaTrasporto import CategoriaTrasporto
from promogest.modules.ADR.dao.CodiceClassificazione import CodiceClassificazione
from promogest.modules.ADR.dao.GruppoImballaggio import GruppoImballaggio
from promogest.modules.ADR.dao.ClassePericolo import ClassePericolo
from promogest.modules.ADR.dao.Galleria import Galleria

try:
    t_articolo_adr = Table('articolo_adr', params['metadata'],
                         schema=params['schema'], autoload=True)
except:

    t_articolo_adr = Table(
        'articolo_adr',
        params['metadata'],
        Column('id', Integer, primary_key=True),
        Column('id_articolo', Integer,
               ForeignKey(fk_prefix + 'articolo.id',
                          onupdate='CASCADE', ondelete='CASCADE')),
        Column('numero_un', String(20), nullable=True),
        Column('id_gruppo_imballaggio', Integer,
               ForeignKey(fk_prefix + 'gruppo_imballaggio.id',
                          onupdate="CASCADE", ondelete="RESTRICT")),
        Column('id_categoria_trasporto', Integer,
               ForeignKey(fk_prefix + 'categoria_trasporto.id',
                          onupdate='CASCADE', ondelete='RESTRICT')),
        Column('id_galleria', Integer,
               ForeignKey(fk_prefix + 'adr_galleria.id',
                          onupdate="CASCADE", ondelete="RESTRICT")),
        Column('id_classe', Integer,
               ForeignKey(fk_prefix + 'adr_classe_pericolo.id',
                          onupdate="CASCADE", ondelete="RESTRICT")),
        Column('id_codice_classificazione', Integer,
               ForeignKey(fk_prefix + 'codice_classificazione.id',
                          onupdate="CASCADE", ondelete="RESTRICT")),
        schema=params['schema'],
        useexisting=True,
        )
    t_articolo_adr.create(checkfirst=True)


class ArticoloADR(Dao):

    def __init__(self, req=None):
        Dao.__init__(self, entity=self)

    def filter_values(self, k, v):
        if k == 'id':
            dic = {k: t_articolo_adr.c.id==v}
        elif k == 'id_articolo':
            dic = {k: t_articolo_adr.c.id_articolo==v}
        return dic[k]

    @property
    def categoria_trasporto(self):
        a = CategoriaTrasporto().getRecord(id=self.id_categoria_trasporto)
        if a:
            return a.denominazione
        else:
            return _('categoria indeterminata')

    @property
    def quantita_massima_trasportabile(self):
        a = CategoriaTrasporto().getRecord(id=self.id_categoria_trasporto)
        if a:
            return a.quantita_massima_trasportabile
        else:
            return _('quantita massima trasportabile indeterminata')

    @property
    def coefficiente_moltiplicazione_virtuale(self):
        a = CategoriaTrasporto().getRecord(id=self.id_categoria_trasporto)
        if a:
            return a.coefficiente_moltiplicazione_virtuale
        else:
            return _('coefficiente moltiplicazione virtuale indeterminato')

    @property
    def codice_classificazione(self):
        a = CodiceClassificazione().getRecord(id=self.id_codice_classificazione)
        if a:
            return a.denominazione
        else:
            return ''

    @property
    def gruppo_imballaggio(self):
        a = GruppoImballaggio().getRecord(id=self.id_gruppo_imballaggio)
        if a:
            return a.denominazione
        else:
            return _('gruppo imballaggio indeterminato')

    @property
    def classe_pericolo(self):
        a = ClassePericolo().getRecord(id=self.id_classe)
        if a:
            return a.denominazione
        else:
            return ''

    @property
    def galleria(self):
        a = Galleria().getRecord(id=self.id_galleria)
        if a:
            return a.denominazione
        else:
            return ''

std_mapper = mapper(ArticoloADR, t_articolo_adr,
                    order_by=t_articolo_adr.c.id_articolo)
