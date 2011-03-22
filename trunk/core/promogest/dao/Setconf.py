#-*- coding: utf-8 -*-
#
# Promogest - Janas
#
# Copyright (C) 2005-2010 by Promotux Informatica - http://www.promotux.it/
# Author: Francesco Meloni <francesco@promotux.it>

from sqlalchemy import *
from sqlalchemy.orm import *
from Dao import Dao
from promogest.Environment import *


try:
    setconf=Table('setconf', params['metadata'],schema = params['schema'],autoload=True)
except:
    setconf  = Table('setconf', params["metadata"],
            Column('id',Integer,primary_key=True),
            Column('key',String(50), nullable=False),
            Column('description',String(200), nullable=True),
            Column('value',String(2000)),
            Column('section',String(50), nullable=False),
            Column('tipo_section',String(50)),
            Column('tipo',String(50)),
            Column('date', DateTime, nullable=True),
            Column('active', Boolean, default=True),
            Column('visible', Boolean, default=True),
            UniqueConstraint('key', "section"),
            schema = params['schema'])
    setconf.create(checkfirst=True)

class SetConf(Dao):

    def __init__(self, req= None, arg=None):
        Dao.__init__(self, entity=self)

    def filter_values(self, k, v):
        if k == "description":
            dic= { k : setconf.c.description.ilike("%"+v+"%")}
        elif k == "value":
            dic= { k : setconf.c.value == v}
        elif k == "body":
            dic= { k : setconf.c.body.ilike("%"+v+"%")}
        elif k == "section":
            dic= { k : setconf.c.section == v}
        elif k == "key":
            dic= { k : setconf.c.key == v}
        elif k == 'searchkey':
            dic = {k:or_(setconf.c.key.ilike("%"+v+"%"),
                        setconf.c.value.ilike("%"+v+"%"),
                        setconf.c.description.ilike("%"+v+"%"))}
        elif k =="active":
            dic = { k :setconf.c.active ==v}
        elif k =="visible":
            dic = { k :setconf.c.visible ==v}
        return  dic[k]

std_mapper = mapper(SetConf, setconf, order_by=setconf.c.key)

bb = SetConf().select(key="articolo_struttura_codice", section="Articoli")
if not bb:
    kbb = SetConf()
    kbb.key = "articolo_struttura_codice"
    kbb.value ="ART000000"
    kbb.section = "Articoli"
    kbb.tipo_section = "Generico"
    kbb.description = "Articolo struttura codice"
    kbb.active = True
    kbb.tipo = "str"
    kbb.date = datetime.datetime.now()
    session.add(kbb)
bb = SetConf().select(key="articolo_codice_upper", section="Articoli")
if not bb:
    kbb = SetConf()
    kbb.key = "articolo_codice_upper"
    kbb.value ="True"
    kbb.section = "Articoli"
    kbb.tipo_section = "Generico"
    kbb.description = "Articolo struttura codice"
    kbb.active = True
    kbb.tipo = "bool"
    kbb.date = datetime.datetime.now()
    session.add(kbb)
bb = SetConf().select(key="articolo_immagini", section="Articoli")
if not bb:
    kbb = SetConf()
    kbb.key = "articolo_immagini"
    kbb.value ="True"
    kbb.section = "Articoli"
    kbb.tipo_section = "Generico"
    kbb.description = "Articolo visualizzazione immagini"
    kbb.active = True
    kbb.tipo = "bool"
    kbb.date = datetime.datetime.now()
    session.add(kbb)


bb = SetConf().select(key="cliente_struttura_codice", section="Clienti")
if not bb:
    kbb = SetConf()
    kbb.key = "cliente_struttura_codice"
    kbb.value ="CLI000000"
    kbb.section = "Clienti"
    kbb.tipo_section = "Generico"
    kbb.description = "Cliente struttura codice"
    kbb.active = True
    kbb.tipo = "str"
    kbb.date = datetime.datetime.now()
    session.add(kbb)
bb = SetConf().select(key="cliente_codice_upper", section="Clienti")
if not bb:
    kbb = SetConf()
    kbb.key = "cliente_codice_upper"
    kbb.value ="True"
    kbb.section = "Clienti"
    kbb.tipo_section = "Generico"
    kbb.description = "Clienti codice upper"
    kbb.active = True
    kbb.tipo = "bool"
    kbb.date = datetime.datetime.now()
    session.add(kbb)
bb = SetConf().select(key="cliente_nome_cognome", section="Clienti")
if not bb:
    kbb = SetConf()
    kbb.key = "cliente_nome_cognome"
    kbb.value ="False"
    kbb.section = "Clienti"
    kbb.tipo_section = "Generico"
    kbb.description = "Visualizza nome cognome"
    kbb.active = True
    kbb.tipo = "bool"
    kbb.date = datetime.datetime.now()
    session.add(kbb)

session.commit()
