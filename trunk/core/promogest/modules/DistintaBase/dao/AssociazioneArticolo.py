# -*- coding: utf-8 -*-

# Promogest
#
# Copyright (C) 2005 by Promotux Informatica - http://www.promotux.it/
# Author: Francesco Meloni <francesco@promotux.it>

from sqlalchemy import *
from sqlalchemy.orm import *
from promogest.Environment import *
from promogest.dao.Dao import Dao

class AssociazioneArticolo(Dao):
    """
    Rappresenta un raggruppamento di articoli relazionati ad un unico articolo "padre"
    """
    def __init__(self, arg=None):
        Dao.__init__(self, entity=self)


    def filter_values(self,k,v):
        if k =='idFiglio':
            dic= {k:associazionearticolo.c.id_articolo ==v}
        elif k == "idPadre":
            dic = {k:associazionearticolo.c.id_padre ==v}
        return  dic[k]

associazionearticolo=Table('associazione_articolo',params['metadata'],schema = params['schema'],autoload=True)

std_mapper = mapper(AssociazioneArticolo, associazionearticolo, order_by=associazionearticolo.c.id)
