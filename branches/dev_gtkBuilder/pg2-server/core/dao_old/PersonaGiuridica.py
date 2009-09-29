#-*- coding: utf-8 -*-
#
# Promogest - Janas
#
# Copyright (C) 2005 by Promotux Informatica - http://www.promotux.it/
# Author: Francesco Meloni <francesco@promotux.it>



from sqlalchemy import *
from sqlalchemy.orm import *
from core.Environment import *
from Dao import Dao
from core.dao.Regioni import Regioni
from core.dao.Province import Province

userTable = Table('utente',params['metadata'], autoload=True, schema=params['mainSchema'])
regioneTable  = Table('regione', params['metadata'], autoload=True, schema=params['mainSchema'])
provinciaTable  = Table('provincia', params['metadata'], autoload=True, schema=params['mainSchema'])

if tipo_db =="sqlite":
    utenteFK = 'utente.id'
    provinciaFK = 'provincia.id'
    regioneFK = 'regione.id'
else:
    utenteFK = params['mainSchema']+'.utente.id'
    provinciaFK = params['mainSchema']+'.provincia.id'
    regioneFK = params['mainSchema']+'.regione.id'

personaGiuridicaTable = Table('persona_giuridica', params['metadata'],
        Column('id', Integer, primary_key=True),
        Column('codice', String(50), nullable=True,),
        Column('ragione_sociale',String(200), nullable=True),
        Column('insegna',String(100), nullable=True),
        Column('cognome',String(70), nullable=True),
        Column('nome',String(70), nullable=True),
        Column('sede_operativa_indirizzo',String(300), nullable=True),
        Column('sede_operativa_cap',String(5), nullable=True),
        Column('id_sede_operativa_provincia',Integer,ForeignKey(provinciaFK),nullable=True),
        Column('id_sede_operativa_regione',Integer, ForeignKey(regioneFK),nullable=True),
        Column('sede_operativa_localita',String(200), nullable=True),
        Column('sede_legale_indirizzo',String(300), nullable=True),
        Column('sede_legale_cap',String(5), nullable=True),
        Column('id_sede_legale_provincia',Integer,ForeignKey(provinciaFK), nullable=True),
        Column('id_sede_legale_regione',Integer,ForeignKey(regioneFK), nullable=True),
        Column('sede_legale_localita',String(200), nullable=True),
        Column('nazione',String(100), nullable=True),
        Column('codice_fiscale',String(16), nullable=True),
        Column('partita_iva',String(11), nullable=True),
        Column('id_user',Integer, ForeignKey(utenteFK)),
        schema = params['schema']
        )
personaGiuridicaTable.create(checkfirst=True)


class PersonaGiuridica_(Dao):

    def __init__(self, arg=None):
        Dao.__init__(self, entity=self)

    def filter_values(self,k,v):
        dic= {}
        return  dic[k]

persona_giuridica=Table('persona_giuridica',
                params['metadata'],
                schema = params['schema'],
                autoload=True)

std_mapper = mapper(PersonaGiuridica_, persona_giuridica, order_by=persona_giuridica.c.id)
