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

articolo = Table('articolo', params['metadata'],schema = params['schema'],autoload=True)

#j = join(associazionearticolo, articolo)

std_mapper = mapper(AssociazioneArticoli, associazionearticolo, properties={
                "arto_padre":relation(Articolo,primaryjoin=
                    associazionearticolo.c.id_padre==Articolo.id, backref="asso_art_padre"),
                "arto_figlio":relation(Articolo,primaryjoin=
                    associazionearticolo.c.id_figlio==Articolo.id, backref="asso_art_figlio")},
                                            order_by=associazionearticolo.c.posizione)

