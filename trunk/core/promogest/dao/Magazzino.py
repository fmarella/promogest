#-*- coding: utf-8 -*-
#
"""
 Promogest
 Copyright (C) 2005-2008 by Promotux Informatica - http://www.promotux.it/
 Author: Francesco Meloni <francesco@promotux.it>
 License: GNU GPLv2
"""

from sqlalchemy import *
from sqlalchemy.orm import *
from promogest.Environment import *
from Dao import Dao


magazzinoTable=Table('magazzino',params['metadata'],schema = params['schema'],autoload=True)
if "magazzino.pvcode" not in str(magazzinoTable.columns):
    print "AGGIUNGO LA COLONNA PVCODE"
    conn = params["engine"].connect()
    trans = conn.begin()
    conn.execute("ALTER TABLE "+ params['schema']+".magazzino"+" ADD COLUMN pvcode varchar(3);")
    trans.commit()

class Magazzino(Dao):

    def __init__(self, arg=None):
        Dao.__init__(self, entity=self)

    def filter_values(self,k,v):
        dic= {  'denominazione' : magazzino.c.denominazione.ilike("%"+v+"%")}
        return  dic[k]

magazzino=Table('magazzino',params['metadata'],schema = params['schema'],autoload=True)

std_mapper = mapper(Magazzino, magazzino, order_by=magazzino.c.id)
