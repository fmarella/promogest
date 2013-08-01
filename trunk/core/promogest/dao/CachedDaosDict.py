# -*- coding: utf-8 -*-

#    Copyright (C) 2005-2013 by Promotux
#                       di Francesco Meloni snc - http://www.promotux.it/

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

from promogest import Environment

class _CachedDaosDict(object):
    """
    """
    def __init__(self):
        self._dict = {}
        self._params = {}

    def add(self, klass, use_key='id', fetch_field=None):
        """
        """
        klass_name = str(klass.__name__).lower()
        self._params[klass_name] = {'use_key': use_key, 'fetch_field': fetch_field}
        result = Environment.session.query(getattr(klass, use_key), klass).all()
        subdict = {}
        for row in result:
            if not fetch_field:
                subdict[row[0]] = row[1]
            else:
                subdict[row[0]] = (row[1], getattr(row[1], fetch_field))
        self._dict[klass_name] = subdict

    def update(self, klass):
        """
        """
        klass_name = str(klass.__name__).lower()
        if klass_name not in self._dict:
            raise KeyError("'%s'" % klass_name)
        del self._dict[klass_name]
        self.add(klass, **self._params[klass_name])

    def __getitem__(self, obj):
        return self._dict[obj]

    def delete(self, obj):
        """
        """
        if obj not in self._dict:
            raise KeyError("'%s'" % obj)
        del self._dict[obj]

    def __repr__(self):
        return '<CachedDaosDict>'
_cachedobject = _CachedDaosDict()
def CachedDaosDict(): return _cachedobject

from promogest.dao.Operazione import Operazione
from promogest.dao.Pagamento import Pagamento
from promogest.dao.AliquotaIva import AliquotaIva
cache_obj = CachedDaosDict()
#Environment.cache_obj = cache_objj
cache_obj.add(Operazione, use_key='denominazione')
cache_obj.add(Pagamento, use_key='denominazione')
cache_obj.add(AliquotaIva, fetch_field='tipo_ali_iva')
