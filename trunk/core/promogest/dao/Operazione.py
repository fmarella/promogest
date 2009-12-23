#-*- coding: utf-8 -*-
#
# Promogest
#
# Copyright (C) 2005 by Promotux Informatica - http://www.promotux.it/
# Author: Francesco Meloni <francesco@promotux.it>


from sqlalchemy import *
from sqlalchemy.orm import *
from promogest.Environment import *
from Dao import Dao

class Operazione(Dao):

    def __init__(self, arg=None):
        Dao.__init__(self, entity=self)

    def filter_values(self,k,v):
        if k == 'denominazione':
            dic= { k: operazione.c.denominazione.ilike("%"+v+"%")}
        elif k== 'denominazioneEM':
            dic= { k: operazione.c.denominazione == (v).strip()}
        elif k=="tipoOperazione":
            dic = {k:operazione.c.tipo_operazione==v}
        elif k=="segno":
            dic = {k: operazione.c.segno ==v}
        elif k=="tipoPersonaGiuridica":
            dic = {k: operazione.c.tipo_persona_giuridica ==v}
        return  dic[k]

operazione=Table('operazione',params['metadata'],schema = params['mainSchema'],autoload=True)

std_mapper = mapper(Operazione, operazione, order_by=operazione.c.denominazione)
