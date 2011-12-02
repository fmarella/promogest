# -*- coding: utf-8 -*-

#    Copyright (C) 2005, 2006, 2007 2008, 2009, 2010 by Promotux
#                       di Francesco Meloni snc - http://www.promotux.it/

#    Author: Francesco Meloni  <francesco@promotux.it>
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
import hashlib
import sqlalchemy
from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.ext.serializer import loads, dumps
from promogest.Environment import *
from promogest.ui.GtkExceptionHandler import GtkExceptionHandler
from promogest.dao.DaoUtils import ckd

class Dao(object):
    """
    Astrazione generica di ciò˛ che fu il vecchio dao basata su sqlAlchemy
    """
    def __init__(self, entity=None, exceptionHandler=None):
        self._session = params["session"]
#        self._metadata = params["metadata"]
        self._numRecords = None
        self._DaoModule = entity.__class__
        self._exceptionHandler = exceptionHandler

    def getRecord(self,id=None):
        """ Restituisce un record ( necessita di un ID )"""
        if id:
            _record = self._session.query(self._DaoModule).get(id)
        else:
            return None
        return _record

    def select(self, orderBy=None, distinct=None, groupBy=None,join=None, offset=0,
                batchSize=20,complexFilter=None,isList = "all", **kwargs):
        """
        Funzione riscritta diverse volte, il vecchio sistema che
        permetteva di aggiungere a cascata nuove opzioni sembrava rallentare
        leggermente ...questo sistema meno elegante è invece più performante
        tornati al sistema iniziale che invece non penalizza le prestazioni
        ed è molto più flessibile
        """
        filter1 = filter2 = None
        if sqlalchemy.__version__ > 0.6:
            if complexFilter is not None:
                filter1 = complexFilter
            else:
                filter2= self.prepareFilter(kwargs)
        else:
            if complexFilter:
                filter1 = complexFilter
            else:
                filter2= self.prepareFilter(kwargs)
        filter = and_(filter1,filter2)
        #print filter
#        try:
#            if join and filter and orderBy:
#                self.record= self._session.query(self._DaoModule).join(join).filter(filter).order_by(orderBy).limit(batchSize).offset(offset).all()
#            elif filter and orderBy:
#                self.record= self._session.query(self._DaoModule).filter(filter).order_by(orderBy).limit(batchSize).offset(offset).all()
#            elif join and orderBy:
#                self.record= self._session.query(self._DaoModule).join(join).order_by(orderBy).limit(batchSize).offset(offset).all()
#            elif filter and join:
#                self.record= self._session.query(self._DaoModule).join(join).filter(filter).limit(batchSize).offset(offset).all()
#            elif filter:
#                self.record= self._session.query(self._DaoModule).filter(filter).limit(batchSize).offset(offset).all()
#            elif join:
#                self.record= self._session.query(self._DaoModule).join(join).limit(batchSize).offset(offset).all()
#            elif orderBy:
#                self.record= self._session.query(self._DaoModule).order_by(orderBy).limit(batchSize).offset(offset).all()
#            else:
#                self.record= self._session.query(self._DaoModule).limit(batchSize).offset(offset).all()
#            return self.record
#        except Exception, e:
#            self.raiseException(e)

#        try:
        self.record= self._session.query(self._DaoModule)
        if sqlalchemy.__version__ > 0.6:
            if join is not None:
                self.record = self.record.join(join)
            if filter is not None:
                self.record = self.record.filter(filter)
            if orderBy is not None:
                self.record = self.record.order_by(orderBy)
            if batchSize is not None:
                self.record = self.record.limit(batchSize)
            if distinct is not None:
                self.record = self.record.distinct(distinct)
            if offset is not None and offset is not 0:
                self.record = self.record.offset(offset)
            if groupBy is not None:
                self.record = self.record.group_by(groupBy)
#            else:
#                if join:
#                    self.record = self.record.join(join)
#                if filter:
#                    self.record = self.record.filter(filter)
#                if orderBy:
#                    self.record = self.record.order_by(orderBy)
#                if batchSize:
#                    self.record = self.record.limit(batchSize)
#                if distinct:
#                    self.record = self.record.distinct(distinct)
#                if offset:
#                    self.record = self.record.offset(offset)
#                if groupBy:
#                    self.record = self.record.group_by(groupBy)
        return self.record.all()
#        except Exception, e:
#            self.raiseException(e)



    def count(self, complexFilter=None,distinct =None,**kwargs):
        """
        Restituisce il numero delle righe
        """
        __numRecords = 0
        if sqlalchemy.__version__ > 0.6:
            if complexFilter is not None:
                filter = complexFilter
            else:
                filter= self.prepareFilter(kwargs)
        else:
            if complexFilter:
                filter = complexFilter
            else:
                filter= self.prepareFilter(kwargs)
        try:
            dao = self._session.query(self._DaoModule)
            if sqlalchemy.__version__ > 0.6:
                if filter is not None:
                    dao = dao.filter(filter)
                if distinct is not None:
                    dao = dao.distinct()
            else:
                if filter:
                    dao = dao.filter(filter)
                if distinct:
                    dao = dao.distinct()
            __numRecords = dao.count()
            if __numRecords > 0:
                self._numRecords = __numRecords
            return self._numRecords
        except Exception, e:
            self.raiseException(e)

    def persist(self,multiple=False, record=True):
        if self.dd(self.__class__.__name__):
            params["session"].add(self)
            self.saveAppLog(self)
        else:
            return

    def save_update(self,multiple=False, record=True):
        params["session"].add(self)
        self.saveAppLog(self)

    def add(self,multiple=False, record=True):
        params["session"].add(self)
        self.saveAppLog(self)

    def delete(self, multiple=False, record = True ):
        params['session'].delete(self)
        self.saveAppLog(self)

    def saveAppLog(self,dao):
        self.saveToAppLog(self)
#        self.commit()

    def rollback(self):
        params["session"].rollback()

    def ckdd(self, dao):
        return ckd(dao)

    def commit(self):
        """ Salva i dati nel DB"""
        if not params["session"].deleted and not self.ckdd(self):
            return
        try:
            params["session"].commit()
            return 1
        except Exception,e:
            msg = """ATTENZIONE ERRORE NEL SALVATAGGIO
    Qui sotto viene riportato l'errore di sistema:

    ( normalmente il campo in errore è tra "virgolette")

    %s

    L'errore può venire causato da un campo fondamentale
    mancante, da un codice già presente, si invita a
    rincontrollare i campi e riprovare
    Grazie!
    """ %e
            messageInfoEnv(msg=msg)
            pg2log.info("ERRORE IN DAO COMMIT  "+str(e))
            params["session"].rollback()
#            params["session"].clear()
#            Session = scoped_session(sessionmaker(bind=engine))
#            _session = Session()
#            params["session"] = _session
            return 0

    def dd(self,clase):
#        clasemd5 = hashlib.md5(clase).hexdigest()
        return True
#        if clasemd5 in mm:
##            print "OLLELLE OLLALLA", self.count()
#            if hashlib.md5(str(self.count())).hexdigest() == mm[clasemd5]:
#                from promogest.ui.utils import fenceDialog
#                fenceDialog()



    def saveToAppLog(self, status=True,action=None, value=None):
        """
        Salviamo l'operazione nella tabella di log con un oggetto
        pickeld
        """
#        if params["session"].dirty:
#            message = "UPDATE;"+ self.__class__.__name__
#        elif params["session"].new:
#            message = "INSERT;" + self.__class__.__name__
#        elif params["session"].deleted:
#            message = "DELETE;"+ self.__class__.__name__
#        else:
#            message = "UNKNOWN ACTION;"
        return self.commit()

    def _resetId(self):
        """
        Riporta l'id a None
        """
        self.id = None

    def sameRecord(self, dao):
        """
        Check whether this Dao represents the same SQL DBMS record of
        the given Dao
        """
        if dao and self:
            return (self.__hash__ == dao.__hash__ )
        return True

    def dictionary(self, complete=False):
        """
        Return a dictionary containing DAO data.  'complete' tells
        whether we should return *all* the data, even the one that's
        not SQL-related
        """
        sqlDict = {}
        for k in self.__dict__.keys():
            sqlDict[k] = getattr(self, k)

        if not complete:
            return sqlDict

        props = {}
        for att in self.__class__.__dict__.keys():
            if isinstance(getattr(self.__class__, att), property):
                value = getattr(self.__class__, att).__get__(self)
                if isinstance(value, list):
                    # Let's recurse
                    value = [d.dictionary(complete=complete) for d in value
                             if isinstance(d, Dao)]
                    #if isinstance(value, Dao):
                    for xx in value:
                        for k,v in xx.items():
                            if isinstance(v.__class__, Dao):
                                xx[k] = v
                props[att] = value

        attrs = {}
        for att in (x for x in self.__dict__.keys() if x not in sqlDict.keys()):
            # Let's filter boring stuff
            if '__' in att: # Private data
                continue
            elif att[0]=='_':
                continue
            attrs[att] = getattr(self, att)

        sqlDict.update(props)
        sqlDict.update(attrs)

        relat = []
        try:
            for a in self._DaoModule._sa_class_manager.mapper.iterate_properties:
                if a.__class__.__name__ =="RelationshipProperty":
                    relat.append(a.__dict__["key"])
            for q in relat:
                if q in sqlDict:
                    del sqlDict[q]
        except:
            pass

        return sqlDict

    def resolveProperties(self):
        """
        Resolve all the object properties.  This method expects all
        the properties to keep an internal cache that will avoid
        further SQL DBMS accesses.
        """
        pass

    def raiseException(self, exception):
        """
        Pump an exception instance or type through the object exception
        handler (if any)
        """
        #if self._exceptionHandler is not None:
        print exception
        GtkExceptionHandler().handle(exception)

        # Now let's raise the exception, in order to stop further processing
        #raise exception

    def prepareFilter(self, kwargs):
        """
        Take filter data from the gui and build the dictionary for the filter
        """
        filter_parameters = []
        for key,value in kwargs.items():
            if str(key).upper() =="filterDict".upper():
                for k,v in value.items():
                    if v is not None:
                        if type(v)==list:
                            filter_parameters.append((v,k,"Lista"))
                        else:
                            filter_parameters.append((v,k,"s"))
            else:
                if type(value)==list:
                    filter_parameters.append((value,key,"Lista"))
                elif type(value) ==bool:
                    filter_parameters.append((bool(value),key,"s"))
                elif value:
                    filter_parameters.append((value,key,"s"))
        if filter_parameters != []:
            if debugFilter:
                print "FILTER PARAM:",self._DaoModule.__name__, filter_parameters
            filter = self.getFilter(filter_parameters)
            return filter
        return

    def getFilter(self,filter_parameters):
        """ Send the filter dict to the function """
        filters = []
        for elem in filter_parameters:
            if elem[0] is not None and elem[2]=="Lista":
                arg= self.filter_values(str(elem[1]+"List"),elem[0])
                filters.append(arg)
            elif elem[0] or type(elem[0])==bool:
                arg= self.filter_values(str(elem[1]),elem[0])
                filters.append(arg)
        return and_(*filters)