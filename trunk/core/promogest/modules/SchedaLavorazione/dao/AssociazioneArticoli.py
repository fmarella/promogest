# -*- coding: utf-8 -*-
# Promogest
#
# Copyright (C) 2005 by Promotux Informatica - http://www.promotux.it/
# Author: Francesco Meloni <francesco@promotux.it>


from sqlalchemy import *
from sqlalchemy.orm import *
from promogest.Environment import *
from promogest.dao.Dao import Dao
from promogest.dao.Articolo import Articolo

class AssociazioneArticoli(Dao):

    def __init__(self, arg=None):
        Dao.__init__(self, entity=self)

    def persist(self):
        """
        Salva l'associazione nel database
        """
        if connection is None:
            if  self._connection is not None:
                self._connection.execStoredProcedure('AssociazioneArticoloSet',
                        (self.id ,self.id_associato, self.id_articolo, self.posizione))
            else:
                self.raiseException(NotImplementedError('Object is read-only '
                                                        + '(no connection has '
                                                        + 'been associated)'))
        else:
            connection.execStoredProcedure('AssociazioneArticoloSet',
                            (self.id ,self.id_associato, self.id_articolo, self.posizione))

    def delete(self, conn=None, son=False):
        if conn is not None:
            conn.execStoredProcedure(self._delSPName,
                                     (self.id,))
        else:
            if self._connection is None:
                self.raiseException(NotImplementedError('Object is read-only '
                                                        + '(no connection has '
                                                        + 'been associated)'))

            self._connection.execStoredProcedure(self._delSPName,
                                                 (self.id_articolo, son))

    def filter_values(self,k,v):
        if k == "id":
            dic= {k:associazionearticolo.c.id ==v}
        elif k=="nodo":
            dic= {k:None}
            #dic= {k:associazionearticolo.c.nodo ==v}
        return  dic[k]

associazionearticolo=Table('associazione_articolo', params['metadata'],
                                                    schema = params['schema'],
                                                    autoload=True)

std_mapper = mapper(AssociazioneArticoli, associazionearticolo, properties={},
                                            order_by=associazionearticolo.c.id)

