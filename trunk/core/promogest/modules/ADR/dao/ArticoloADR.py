# -*- coding: utf-8 -*-

#    Copyright (C) 2005, 2006, 2007 2008, 2009, 2010, 2011 by Promotux
#                        di Francesco Meloni snc - http://www.promotux.it/

#    Author: Francesco Marella <francesco.marella@gmail.com>

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
from migrate import *
from promogest.modules.ADR.dao.CategoriaTrasporto import CategoriaTrasporto
from promogest.modules.ADR.dao.CodiceClassificazione import CodiceClassificazione
from promogest.modules.ADR.dao.GruppoImballaggio import GruppoImballaggio
from promogest.modules.ADR.dao.ClassePericolo import ClassePericolo
from promogest.modules.ADR.dao.Galleria import Galleria

try:
    articolo_adr = Table('articolo_adr', params['metadata'],
                         schema=params['schema'], autoload=True)
except:
    articolo = Table('articolo', params['metadata'],
                     schema=params['schema'], autoload=True)

    if tipodb == 'sqlite':
        articoloFK = 'articolo.id'
        categoria_trasportoFK = 'categoria_trasporto.id'
        codice_classificazioneFK = 'codice_classificazione.id'
        gruppo_imballaggioFK = 'gruppo_imballaggio.id'
        classeFK = 'adr_classe_pericolo.id'
        galleriaFK = 'adr_galleria.id'
    else:
        articoloFK = params['schema'] + '.articolo.id'
        categoria_trasportoFK = params['schema'] \
            + '.categoria_trasporto.id'
        codice_classificazioneFK = params['schema'] \
            + '.codice_classificazione.id'
        gruppo_imballaggioFK = params['schema'] \
            + '.gruppo_imballaggio.id'
        classeFK = params['schema'] + '.adr_classe_pericolo.id'
        galleriaFK = params['schema'] + '.adr_galleria.id'

    articolo_adr = Table(
        'articolo_adr',
        params['metadata'],
        Column('id', Integer, primary_key=True),
        Column('id_articolo', Integer, ForeignKey(articoloFK,
               onupdate='CASCADE', ondelete='CASCADE')),
        Column('numero_un', String(20), nullable=True),
        Column('id_gruppo_imballaggio', Integer,
               ForeignKey(gruppo_imballaggioFK, onupdate="CASCADE",
               ondelete="RESTRICT")),
        Column('id_categoria_trasporto', Integer,
               ForeignKey(categoria_trasportoFK, onupdate='CASCADE',
               ondelete='RESTRICT')),
        Column('id_galleria', Integer,
               ForeignKey(galleriaFK, onupdate="CASCADE",
               ondelete="RESTRICT")),
        Column('id_classe', Integer,
               ForeignKey(classeFK, onupdate="CASCADE",
               ondelete="RESTRICT")),
        Column('id_codice_classificazione', Integer,
               ForeignKey(codice_classificazioneFK, onupdate="CASCADE",
               ondelete="RESTRICT")),
        schema=params['schema'],
        useexisting=True,
        )
    articolo_adr.create(checkfirst=True)


class ArticoloADR(Dao):

    def __init__(self, req=None):
        Dao.__init__(self, entity=self)

    def filter_values(self, k, v):
        if k == 'id':
            dic = {k: articolo_adr.c.id == v}
        elif k == 'id_articolo':
            dic = {k: articolo_adr.c.id_articolo == v}
        return dic[k]

    def _categoriaTrasporto(self):
        a = \
            CategoriaTrasporto().getRecord(id=self.id_categoria_trasporto)
        if a:
            return a.denominazione
        else:
            return _('categoria indeterminata')
    categoria_trasporto = property(_categoriaTrasporto)

    def _quantita_massima_trasportabile(self):
        a = \
            CategoriaTrasporto().getRecord(id=self.id_categoria_trasporto)
        if a:
            return a.quantita_massima_trasportabile
        else:
            return _('quantita massima trasportabile indeterminata')
    quantita_massima_trasportabile = property(_quantita_massima_trasportabile)

    def _coefficiente_moltiplicazione_virtuale(self):
        a = \
            CategoriaTrasporto().getRecord(id=self.id_categoria_trasporto)
        if a:
            return a.coefficiente_moltiplicazione_virtuale
        else:
            return _('coefficiente moltiplicazione virtuale indeterminato')
    coefficiente_moltiplicazione_virtuale = property(_coefficiente_moltiplicazione_virtuale)

    def _codiceClassificazione(self):
        a = \
            CodiceClassificazione().getRecord(id=self.id_codice_classificazione)
        if a:
            return a.denominazione
        else:
            return ''
    codice_classificazione = property(_codiceClassificazione)

    def _gruppoImballaggio(self):
        a = \
            GruppoImballaggio().getRecord(id=self.id_gruppo_imballaggio)
        if a:
            return a.denominazione
        else:
            return _('gruppo imballaggio indeterminato')
    gruppo_imballaggio = property(_gruppoImballaggio)

    def _classePericolo(self):
        a = \
            ClassePericolo().getRecord(id=self.id_classe)
        if a:
            return a.denominazione
        else:
            return ''
    classe_pericolo = property(_classePericolo)

    def _galleria(self):
        a = \
            Galleria().getRecord(id=self.id_galleria)
        if a:
            return a.denominazione
        else:
            return ''
    galleria = property(_galleria)


std_mapper = mapper(ArticoloADR, articolo_adr, properties={},
                    order_by=articolo_adr.c.id_articolo)
