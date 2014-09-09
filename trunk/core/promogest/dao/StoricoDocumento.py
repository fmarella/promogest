# -*- coding: utf-8 -*-

# Copyright (C) 2005-2014 by Promotux
# di Francesco Meloni snc - http://www.promotux.it/

# Author: Francesco Marella <francesco.marella@anche.no>

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

import datetime
from sqlalchemy import Table, Column, Integer, ForeignKey, DateTime, and_, Text
from sqlalchemy.orm import mapper, relation, backref
from sqlalchemy.orm.exc import NoResultFound

from promogest.Environment import params, fk_prefix, session, delete_pickle, restart_program
from promogest.dao.Dao import Dao
from promogest.dao.TestataDocumento import t_testata_documento, TestataDocumento
from promogest.lib.utils import messageInfo

NEUTRO = 0
ASCALARE = 1
STATO = (
    (0, 'Neutro'),
    (1, 'A scalare')
)

try:
    t_storico_documento = Table('storico_documento', params['metadata'], schema=params['schema'], autoload=True)

except:
    session.close()
    t_storico_documento = Table('storico_documento', params["metadata"],
                                Column('id', Integer, primary_key=True),
                                Column('padre', Integer, ForeignKey(fk_prefix + 'testata_documento.id')),
                                Column('figlio', Integer, ForeignKey(fk_prefix + 'testata_documento.id')),
                                Column('data_creazione', DateTime, nullable=True),
                                Column('ultima_modifica', DateTime, nullable=True),
                                Column('data_chiusura', DateTime, nullable=True),
                                Column('stato', Integer, nullable=True),
                                Column('tipo', Integer, nullable=True, default=NEUTRO),
                                Column('note', Text, nullable=True),
                                schema=params['schema'],
                                extend_existing=True)

    t_storico_documento.create(checkfirst=True)
    delete_pickle()
    messageInfo(msg="HO AGGIUNTO LA TABELLA STORICO DOCUMENTI, RIAVVIO IL PROMOGEST")
    restart_program()

class StoricoDocumento(Dao):
    def __init__(self, req=None, arg=None):
        Dao.__init__(self, entity=self)

    def filter_values(self, k, v):
        dic = {
            'padre': t_storico_documento.c.padre == v,
            'figlio': t_storico_documento.c.figlio == v,
        }
        return dic[k]

    def fathers(self):
        return params['session'].query(StoricoDocumento).filter(and_(StoricoDocumento.padre == None)).all()


std_mapper = mapper(StoricoDocumento, t_storico_documento)
    # ,
    #                 properties = {
    #                     'children': relation(StoricoDocumento,
    #                                          backref=backref('parent'), remote_side=[t_testata_documento.c.id])
    #                 })

def add_relazione(padre_id, figlio_id):
    '''
    Aggiunge una relazione tra due documenti nello storico
    :param padre_id: ID del documento padre
    :param figlio_id: ID del documento figlio
    :return: None
    '''
    storico = None
    try:
        storico = session.query(StoricoDocumento).filter(and_(StoricoDocumento.padre==padre_id, StoricoDocumento.figlio==None)).one()
    except NoResultFound:
        pass
    # relazione documento da duplicare e duplicato: padre -> figlio
    if not storico:
        storico = StoricoDocumento()
        storico.padre = padre_id
        storico.data_creazione = datetime.date.today()
    storico.figlio = figlio_id
    storico.ultima_modifica = datetime.date.today()
    storico.persist()
    # relazione sul nuovo documento: padre -> nessuno figlio
    storico2 = StoricoDocumento()
    storico2.padre = figlio_id
    storico2.figlio = None
    storico2.data_creazione = datetime.date.today()
    storico2.ultima_modifica = datetime.date.today()
    storico2.persist()

def get_padre(doc_id):
    '''
    Ritorna il documento padre del documento fornito
    :param doc_id: ID del documento di cui si vuole conoscere il padre
    :return: il padre del documento
    '''
    if doc_id:
        try:
            obj = session.query(StoricoDocumento).filter(StoricoDocumento.figlio==doc_id).one()
            return TestataDocumento().getRecord(id=obj.padre)
        except NoResultFound:
            return


def get_figli(doc_id):
    '''
    Ritorna tutti i documenti figli del documento fornito
    :param doc_id: ID del documento di cui si vogliono conoscere i figli
    :return: i documenti figli
    '''
    if doc_id:
        objs = session.query(StoricoDocumento).filter(StoricoDocumento.padre==doc_id).all()
        docs = []
        for obj in objs:
            docs.append(TestataDocumento().getRecord(obj.figlio))
        return docs

def rimuovi_da_storico(doc_id):
    '''
    Rimuove il documento dallo storico
    :param doc_id: ID del documento che si vuole rimuovere dallo storico
    :return: None
    '''
    if doc_id:
        try:
            obj = session.query(StoricoDocumento).filter(and_(StoricoDocumento.padre==doc_id, StoricoDocumento.figlio==None)).one()
            session.delete(obj)
        except NoResultFound:
            pass
        try:
            obj = session.query(StoricoDocumento).filter(StoricoDocumento.figlio==doc_id).one()
            session.delete(obj)
        except NoResultFound:
            pass
