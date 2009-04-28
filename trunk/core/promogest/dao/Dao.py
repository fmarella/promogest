# -*- coding: utf-8 -*-

# Promogest
#
# Copyright (C) 2008 by Promotux Informatica - http://www.promotux.it/
# Author: Francesco Meloni <francesco@promotux.it>

import gtk
import datetime
from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.ext.serializer import loads, dumps
from promogest.Environment import *
from promogest.ui.GtkExceptionHandler import GtkExceptionHandler

class Dao(object):
    """
    Astrazione generica di ciò˛ che fu il vecchio dao basata su sqlAlchemy
    """
    def __init__(self, entity=None, exceptionHandler=None):
        self.session = params["session"]
        self.metadata = params["metadata"]
        self.numRecords = None
        self.DaoModule = entity.__class__
        self._exceptionHandler = exceptionHandler

    def getRecord(self,id=None):
        """ Restituisce un record ( necessita di un ID )"""
        if id:
            _record = self.session.query(self.DaoModule).get(id)
        else:
            return None
        return _record

    def select(self, orderBy=None, distinct=False, groupBy=None,join=None, offset=0,
                batchSize=20,complexFilter=None,isList = "all", **kwargs):
        """ 
        Funzione riscritta diverse volte, il vecchio sistema che
        permetteva di aggiungere a cascata nuove opzioni sembrava rallentare
        leggermente ...questo sistema meno elegante è invece più performante
        """
        filter1 = filter2 = None
        if complexFilter:
            filter1 = complexFilter
        else:
            filter2= self.prepareFilter(kwargs)
        filter = and_(filter1,filter2)
        #print filter
        try:
            if join and filter and orderBy:
                self.record= self.session.query(self.DaoModule).join(join).filter(filter).order_by(orderBy).limit(batchSize).offset(offset).all()
            elif filter and orderBy:
                self.record= self.session.query(self.DaoModule).filter(filter).order_by(orderBy).limit(batchSize).offset(offset).all()
            elif join and orderBy:
                self.record= self.session.query(self.DaoModule).join(join).order_by(orderBy).limit(batchSize).offset(offset).all()
            elif filter and join:
                self.record= self.session.query(self.DaoModule).join(join).filter(filter).limit(batchSize).offset(offset).all()
            elif filter:
                self.record= self.session.query(self.DaoModule).filter(filter).limit(batchSize).offset(offset).all()
            elif join:
                self.record= self.session.query(self.DaoModule).join(join).limit(batchSize).offset(offset).all()
            elif orderBy:
                self.record= self.session.query(self.DaoModule).order_by(orderBy).limit(batchSize).offset(offset).all()
            else:
                self.record= self.session.query(self.DaoModule).limit(batchSize).offset(offset).all()
            return self.record
        except Exception, e:
            self.raiseException(e)

    def count(self, complexFilter=None,distinct =None,**kwargs):
        """
        Restituisce il numero delle righe 
        """
        _numRecords = 0
        if complexFilter:
            filter = complexFilter
        else:
            filter= self.prepareFilter(kwargs)
        try:
            dao = self.session.query(self.DaoModule)
            if filter:
                dao = dao.filter(filter)
            if distinct:
                dao = dao.distinct()
            _numRecords = dao.count()
            if _numRecords > 0:
                self.numRecords = _numRecords
            return self.numRecords
        except Exception, e:
            self.raiseException(e)

    def persist(self,multiple=False, record=True):
        params["session"].add(self)
        self.saveAppLog(self)

    def save_update(self,multiple=False, record=True):
        params["session"].add(self)
        self.saveAppLog(self)

    def delete(self, multiple=False, record = True ):
        params['session'].delete(self)
        self.saveAppLog(self)

    def saveAppLog(self,dao):
        self.saveToAppLog(self)
#        self.commit()

    def commit(self):
        """ Salva i dati nel DB"""
        try:
            params["session"].commit()
            return 1
        except Exception,e:
            msg = """ATTENZIONE ERRORE
    Qui sotto viene riportato l'errore di sistema:
    %s
    ( normalmente il campo in errore è tra "virgolette")
    """ %e
            overDialog = gtk.MessageDialog(None, gtk.DIALOG_MODAL
                                                | gtk.DIALOG_DESTROY_WITH_PARENT,
                                                    gtk.MESSAGE_ERROR,
                                                    gtk.BUTTONS_CANCEL, msg)
            response = overDialog.run()
            overDialog.destroy()
            print "ERRORE", e
            ciccio= params["session"].rollback()
            print "CICCIO", ciccio
            return 0

    def saveToAppLog(self, status=True,action=None, value=None):
        """
        Salviamo l'operazione nella tabella di log con un oggetto 
        pickeld 
        """
        if params["session"].dirty:
            message = "UPDATE "+ self.__class__.__name__ 
        elif params["session"].new:
            message = "INSERT " + self.__class__.__name__
        elif params["session"].deleted:
            message = "DELETE "+ self.__class__.__name__ 
        else:
            message = "UNKNOWN ACTION"
        level = self.commit()
        if level:
            result = " CORRETTO"
        else:
            result = " ERRATO"
        registration_date = datetime.datetime.now()
#        schema_azienda = params['schema']
        id_utente = params['usernameLoggedList'][0]
        utentedb = params['usernameLoggedList'][3]
        utente = params['usernameLoggedList'][1]
        mapper = object_mapper(self)
        pk = mapper.primary_key_from_instance(self)
        completeMessage = message + " " +str(pk)
        appLogTable = Table('app_log', params['metadata'], autoload=True, schema=params['mainSchema'])
        #print "SEEEEEELF", self, self.__dict__, dumps(self)
        aplot = appLogTable.insert()
        #aplot.execute(
                    #id_utente = params['usernameLoggedList'][0],
                    #utentedb = params['usernameLoggedList'][1],
                    #schema_azienda = params['schema'],
                    #level = "I",
                    #message = completeMessage,
                    #value = level,
                    #registration_date = datetime.datetime.now(),
                    #object = dumps(self)
                #)
        print "[LOG] %s da %s in %s in data %s" %(completeMessage,utente, params['schema'] ,registration_date.strftime("%d/%m/%Y"))

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
                    if v:
                        if type(v)==list:
                            filter_parameters.append((v,k,"Lista"))
                        else:
                            filter_parameters.append((v,k,"s"))
            else:
                if value:
                    if type(value)==list:
                        filter_parameters.append((value,key,"Lista"))
                    else:
                        filter_parameters.append((value,key,"s"))
        if filter_parameters != []:
            if debugFilter:
                print "FILTER PARAM:",self.DaoModule.__name__, filter_parameters
            filter = self.getFilter(filter_parameters)
            return filter
        return

    def getFilter(self,filter_parameters):
        """ Send the filter dict to the function """
        filters = []
        for elem in filter_parameters:
            if elem[0] and elem[2]=="Lista":
                arg= self.filter_values(str(elem[1]+"List"),elem[0])
            elif elem[0]:
                arg= self.filter_values(str(elem[1]),elem[0])
            filters.append(arg)
        return and_(*filters)
