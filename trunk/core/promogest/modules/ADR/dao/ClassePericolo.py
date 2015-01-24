# -*- coding: utf-8 -*-

#    Copyright (C) 2005-2015 by Promotux
#                        di Francesco Meloni snc - http://www.promotux.it/

#    Author: Francesco Marella <francesco.marella@anche.no>
#    Author: Francesco Meloni <francesco@promotux.it>

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
from promogest.dao.Dao import Dao, Base

class ClassePericolo(Base, Dao):
    try:
        __table__ = Table('adr_classe_pericolo', params['metadata'], schema = params['schema'],autoload=True)

    except:
        __table__ = Table('adr_classe_pericolo', params["metadata"],
            Column('id',Integer, primary_key=True),
            Column('denominazione', String(10)),
            Column('descrizione', Text),
            schema = params['schema'])
    __mapper_args__ = {
        'order_by' : "denominazione"
    }

    def __init__(self, req= None, arg=None):
        Dao.__init__(self, entity=self)

    def filter_values(self,k,v):
        dic= {
            'denominazione': ClassePericolo.__table__.c.denominazione == v,
            'descrizione': ClassePericolo.__table__.c.descrizione == v,
                }
        return  dic[k]


_classi = [
    ('1',   _('Materie e oggetti esplosivi')),
    ('2',   _('Gas')),
    ('3',   _('Materie liquide infiammabili')),
    ('4.1', _('Materie solide infiammabili')),
    ('4.2', _('Materie soggette ad accensione spontanea')),
    ('4.3', _('Materie che a contatto con l\'acqua sviluppano gas infiammabili')),
    ('5.1', _('Materie carburenti')),
    ('5.2', _('Perossidi organici')),
    ('6.1', _('Materie tossiche')),
    ('6.2', _('Materie infettanti')),
    ('7',   _('Materie radioattive')),
    ('8',   _('Materie corrosive')),
    ('9',   _('Materie e oggetti pericolosi diversi')),]

f = ClassePericolo().select(denominazione="1")
if not f:
    for p in _classi:
        a = ClassePericolo()
        a.denominazione = p[0]
        a.descrizione = p[1]
        session.add(a)
    session.commit()
