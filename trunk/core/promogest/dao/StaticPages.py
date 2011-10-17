# -*- coding: utf-8 -*-

# Promogest - Janas
#
# Copyright (C) 2005 by Promotux Informatica - http://www.promotux.it/
# Author: Francesco Meloni <francesco@promotux.it>

from sqlalchemy import *
from sqlalchemy.orm import *
from core.Environment import *
from Dao import Dao
from Language import Language
from User import User

languageTable = Table('language', params['metadata'], autoload=True, schema=params['mainSchema'])
userTable = Table('utente', params['metadata'], autoload=True, schema=params['mainSchema'])

if params["tipo_db"] == "sqlite":
    utenteFK ='utente.id'
    languageFK = 'language.id'
else:
    utenteFK =params['mainSchema']+'.utente.id'
    languageFK =params['mainSchema']+'.language.id'

pagesTable= Table('static_page', params['metadata'],
        Column('id', Integer, primary_key=True),
        Column('title', String(200), nullable=False),
        Column('abstract', String(400), nullable=True),
        Column('body', Text, nullable=True),
        Column('imagepath', String(400), nullable=True),
        Column('publication_date', DateTime, nullable=True),
        Column('clicks', Integer),
        Column("permalink", String(500), nullable=True),
        Column('active', Boolean, default=0),
        Column('id_user', Integer,ForeignKey(utenteFK)),
        Column('id_language', Integer,ForeignKey(languageFK)),
        schema=params['schema']
        )
pagesTable.create(checkfirst=True)

class StaticPages(Dao):

    def __init__(self, req=None):
        Dao.__init__(self, entity=self)

    def filter_values(self,k,v):
        if k=='id_language':
            dic= {  k : staticpage.c.id_language == v}
        elif k == "titlePage":
            dic = { k: staticpage.c.title==v }
        elif k == "permalink":
            dic = { k: staticpage.c.permalink==v }
        return  dic[k]

staticpage=Table('static_page',params['metadata'],schema = params['schema'],autoload=True)

std_mapper = mapper(StaticPages, staticpage, properties = {
        'lang' : relation(Language),
        'user' : relation(User) })
