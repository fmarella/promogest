# -*- coding: utf-8 -*-

#    Copyright (C) 2005-2015 by Promotux
#                       di Francesco Meloni snc - http://www.promotux.it/

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
from sqlalchemy.orm import *
from promogest.Environment import *
from promogest.dao.Dao import Dao, Base

class FamigliaArticolo(Base, Dao):
    try:
        __table__ = Table('famiglia_articolo', params['metadata'],
                                    schema=params['schema'], autoload=True)
    except:
        from data.famigliaArticolo import t_famiglia_articolo
        __table__ = t_famiglia_articolo

    children = relationship("FamigliaArticolo", backref=backref('parent',
                                            remote_side="FamigliaArticolo.id"))
    __mapper_args__ = {
        "order_by":"codice"
    }

    def __init__(self, req=None):
        Dao.__init__(self, entity=self)

    def filter_values(self,k,v):
        if k == 'denominazione':
            dic= {k : FamigliaArticolo.__table__.c.denominazione.ilike("%"+v+"%")}
        elif k == "idPadre":
            dic= {k : FamigliaArticolo.__table__.c.id_padre == v}
        elif k == "codice":
            dic= {k : FamigliaArticolo.__table__.c.codice == v}
        elif k == "visible":
            dic= {k : FamigliaArticolo.__table__.c.visible == v}
        elif k == "denominazioneBreve":
            dic= {k : FamigliaArticolo.__table__.c.denominazione_breve.ilike("%"+v+"%")}
        return  dic[k]

    def preSave(self):
        famiglie_articolo = None
        return True

    def fathers(self):
        ok = params['session'].query(FamigliaArticolo).filter(and_(FamigliaArticolo.id_padre==None)).all()
        return ok
