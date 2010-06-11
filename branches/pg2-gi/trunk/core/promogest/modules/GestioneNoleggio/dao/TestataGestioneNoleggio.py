# -*- coding: utf-8 -*-

# Promogest
#
# Copyright (C) 2005-2009 by Promotux Informatica - http://www.promotux.it/
# Author: Francesco Meloni <francesco@promotux.it>

from sqlalchemy import *
from sqlalchemy.orm import *
from promogest.Environment import *
from promogest.dao.Dao import Dao

class TestataGestioneNoleggio(Dao):

    def __init__(self, arg=None):
        Dao.__init__(self, entity=self)

    #def _getRigheScontrino(self):
        #self.__dbRigheScontrino = RigaScontrino().select(idTestataScontrino=self.id, batchSize=None)
        #self.__righeScontrino = self.__dbRigheScontrino[:]
        #return self.__righeScontrino

    #def _setRigheScontrino(self, value):
        #self.__righeScontrino = value

    #righe = property(_getRigheScontrino, _setRigheScontrino)

    #def _dataMovimento(self):
        #if self.testatamovimento: return self.testatamovimento.data_movimento
        #else: return ""
    #data_movimento=property(_dataMovimento)

    #def _numeroMovimento(self):
        #if self.testatamovimento: return self.testatamovimento.numero
        #else: return ""
    #numero_movimento=property(_numeroMovimento)

    #def _getScontiTestataScontrino(self):
        #if self.id:
            #self.__dbScontiTestataScontrino = ScontoTestataScontrino().select(join = ScontoTestataScontrino.TS,
                                                                                #idScontoTestataScontrino=self.id,
                                                                                #batchSize=None)
            #self.__scontiTestataScontrino = self.__dbScontiTestataScontrino
        #else:
            #self.__scontiTestataScontrino = []
        #return self.__scontiTestataScontrino

    #def _setScontiTestataScontrino(self, value):
        #self.__scontiTestataScontrino = value
    #sconti = property(_getScontiTestataScontrino, _setScontiTestataScontrino)

    #def _getStringaScontiTestataDocumento(self):
        #(listSconti, applicazione) = getScontiFromDao(self._getScontiTestataDocumento(), self.applicazione_sconti)
        #return getStringaSconti(listSconti)
    #stringaSconti = property(_getStringaScontiTestataDocumento)

    def filter_values(self,k,v):
        if k == 'id':
            dic= {k:testatadocumentonoleggio.c.id ==v}
        elif k == 'idTestataDocumento':
            dic= {k:testatadocumentonoleggio.c.id_testata_documento==v}
        elif k == 'daData':
            dic = {k :testatadocumentonoleggio.c.data_inizio_noleggio >= v}
        elif k == 'aData':
            dic = {k:testatadocumentonoleggio.c.data_inizio_noleggio <= v}
        return  dic[k]

    #def persist(self, chiusura=False):

        ##salvataggio testata scontrino
        #params['session'].add(self)
        #params['session'].commit()

        ##se siamo in chiusura fiscale non serve che vengano toccati i dati delle righe
        #if not chiusura:
            #if self.__righeScontrino:
                ##rigaScontrinoDel(id=self.id)

                ##cancellazione righe associate alla testata
                #for riga in self.__righeScontrino:
                    ##annullamento id della riga
                    #riga._resetId()
                    ##associazione alla riga della testata
                    #riga.id_testata_scontrino = self.id
                    ##salvataggio riga
                    #riga.persist()
        #params['session'].flush()


testataDocumento=Table('testata_documento', params['metadata'],schema = params['schema'],autoload=True)
testataDocumentoNoleggioTable = Table('testata_documento_noleggio', params['metadata'],
                    Column('id',Integer,primary_key=True),
                    Column('id_testata_documento',Integer,ForeignKey(params['schema']+'.testata_documento.id',onupdate="CASCADE",ondelete="CASCADE"),primary_key=True),
                    Column('data_inizio_noleggio',DateTime, nullable=False),
                    Column('data_fine_noleggio',DateTime,nullable=False),
                    schema=params['schema'])
testataDocumentoNoleggioTable.create(checkfirst=True)

testatadocumentonoleggio = Table('testata_documento_noleggio', params['metadata'],
                                schema = params['schema'], autoload=True)


std_mapper = mapper(TestataGestioneNoleggio, testatadocumentonoleggio,properties={
        }, order_by=testatadocumentonoleggio.c.id)