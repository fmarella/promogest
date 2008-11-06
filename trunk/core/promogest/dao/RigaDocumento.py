# -*- coding: iso-8859-15 -*-

# Promogest
#
# Copyright (C) 2005 by Promotux Informatica - http://www.promotux.it/
# Author: Andrea Argiolas <andrea@promotux.it>


from promogest.lib.sqlalchemy import *
from promogest.lib.sqlalchemy.orm import *
from promogest.Environment import *
from Dao import Dao
from Riga import Riga
from UnitaBase import UnitaBase
import ScontoRigaDocumento
from ScontoRigaDocumento import ScontoRigaDocumento
from ScontoRigaMovimento import ScontoRigaMovimento
from ScontoRigaMovimento import *
from ScontoRigaDocumento import *
from Articolo import Articolo
from AliquotaIva import AliquotaIva
from Magazzino import Magazzino
from Listino import Listino
from Multiplo import Multiplo
from DaoUtils import *

if "SuMisura" in modulesList:
    from promogest.modules.SuMisura.dao.MisuraPezzo import MisuraPezzo
    import promogest.modules.SuMisura.dao.MisuraPezzo
from promogest.ui.utils import *

class RigaDocumento(Dao):
    """ User class provides to make a Users dao which include more used"""

    def __init__(self, arg=None,isList=False, id=None):
        Dao.__init__(self, entity=self.__class__, isList=isList, id=id)
        self.valueList = []
        if "SuMisura" in modulesList:
            self.__misuraPezzo = None
            self.__dbMisuraPezzo = None

        # usata per mantenere il valore del codice articolo fornitore proveniente da un
        # documento o movimento di carico, per salvare la fornitura
        self.__codiceArticoloFornitore = None
        #pass

    def _getAliquotaIva(self):
        # Restituisce la denominazione breve dell'aliquota iva
        _denominazioneBreveAliquotaIva = '%2.0f' % (self.percentuale_iva or 0)
        daoArticolo = Articolo(id=self.id_articolo).getRecord()
        if daoArticolo is not None:
            if daoArticolo.id_aliquota_iva is not None:
                daoAliquotaIva = AliquotaIva(id=daoArticolo.id_aliquota_iva).getRecord()
                if daoAliquotaIva is not None:
                    _denominazioneBreveAliquotaIva = daoAliquotaIva.denominazione_breve or ''
        if (_denominazioneBreveAliquotaIva == '0' or _denominazioneBreveAliquotaIva == '00'):
            _denominazioneBreveAliquotaIva = ''
        return _denominazioneBreveAliquotaIva

    aliquota = property(_getAliquotaIva, )

    def _getStringaScontiRigaDocumento(self):
        (listSconti, applicazione) = getScontiFromDao(self._getScontiRigaDocumento(), self.applicazione_sconti)
        return getStringaSconti(listSconti)

    stringaSconti = property(_getStringaScontiRigaDocumento)

    def _getCodiceArticoloFornitore(self):
        self.__codiceArticoloFornitore = None
        return self.__codiceArticoloFornitore

    def _setCodiceArticoloFornitore(self, value):
        self.__codiceArticoloFornitore = value

    codiceArticoloFornitore = property(_getCodiceArticoloFornitore, _setCodiceArticoloFornitore)

    def _getTotaleRiga(self):
        # Il totale e' ivato o meno a seconda del prezzo
        totaleRiga = float(self.quantita) * float(self.moltiplicatore) * float(self.valore_unitario_netto)
        return totaleRiga

    totaleRiga = property(_getTotaleRiga, )

    def __magazzino(self):
        if self.maga: return self.maga.denominazione
        else: return ""
    magazzino= property(__magazzino)

    def __listino(self):
        if self.listi: return self.listi.denominazione
        else: return ""
    listino= property(__listino)

    def __multiplo(self):
        if self.multi: return self.multi.denominazione
        else: return ""
    multiplo = property(__multiplo)

    def __unita_base(self):
        a =  params["session"].query(Articolo).with_parent(self).filter(Articolo.id_unita_base==UnitaBase.id).all()
        if not a:
            return a
        else:
            return a[0].denominazione_breve
    unita_base = property(__unita_base)

    def __codiceArticolo(self):
        """ esempio di funzione  unita alla property """
        a =  params["session"].query(Articolo).with_parent(self).filter(RigaDocumento.id_articolo==Articolo.id).all()
        if not a:
            return a
        else:
            return a[0].codice
    codice_articolo= property(__codiceArticolo)

    def _getMisuraPezzo(self):
                #if self.__dbMisuraPezzo is None:
        try:
            self.__dbMisuraPezzo = MisuraPezzo(isList=True).select(idRiga=self.id)
            self.__misuraPezzo = self.__dbMisuraPezzo[:]
        except:
            self.__misuraPezzo = []
        #print "valueeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee_setMisuraPezzouno  ", self.__misuraPezzo
        return self.__misuraPezzo

    def _setMisuraPezzo(self, value):
        #print "valueeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee_setMisuraPezzodue  ", value
        self.__misuraPezzo = value
        Environment.TRENINO["misuraPezzo"] = value

    misura_pezzo = property(_getMisuraPezzo, _setMisuraPezzo)

    def _getScontiRigaDocumento(self):
        #FIXME : il sistema originale aveva una UNION di due view fatte su mov e doc per cui avevano due campi
        # movimento e riga documento con l'id della riga a cui si riferivano ...
        # noi non avendo la union al momento facciamo due query ed appendiamo le liste
        self.__dbScontiRigaMovimentoPart = params["session"].query(ScontoRigaMovimento).filter_by(id_movimento=self.id).all()
        self.__dbScontiRigaDocumentoPart = params["session"].query(ScontoRigaDocumento).filter_by(id_documento=self.id).all()
        self.__dbScontiRigaDocumento = self.__dbScontiRigaMovimentoPart + self.__dbScontiRigaDocumentoPart
        self.__scontiRigaDocumento = self.__dbScontiRigaDocumento[:]
        return self.__scontiRigaDocumento


    def _setScontiRigaDocumento(self, value):

        self.__scontiRigaDocumento = value
        #print "VALUEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE", value, Environment.scontiRigaDocumentoList

    sconti = property(_getScontiRigaDocumento, _setScontiRigaDocumento)


    def filter_values(self,k,v):
        dic= {  'idTestataDocumento' : riga_doc.c.id_testata_documento==v }
        return  dic[k]

    def persist(self):

        #salvataggio riga
        params["session"].add(self)
        params["session"].commit()
        #params["session"].flush()

        if "SuMisura" in modulesList:
            mp = MisuraPezzo(id=self.id).getRecord()
            try:
                mp.delete()
            except:
                pass
            #conn.execStoredProcedure('MisuraPezzoDel', (self.id, ))
            print "MISURA PEZZOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO", self.__misuraPezzo
            if Environment.TRENINO["misuraPezzo"]:
        #if type(self.__misuraPezzo) == list:
            #if self.__misuraPezzo != []:
                #self.__misuraPezzo[-1].id_riga = self.id
                #self.__misuraPezzo[-1].persist()
        #else:
                self.__misuraPezzo.id_riga = self.id
                self.__misuraPezzo.persist()
                Environment.TRENINO["misuraPezzo"]  = None


        if Environment.TRENINO["scontiRigaDocumento"]:
            scontiRigaDocumentoDel(id=self.id)

            for rigasconto in Environment.TRENINO["scontiRigaDocumento"]:
                #annullamento id dello sconto
                rigasconto._resetId()
                #associazione allo sconto della riga
                rigasconto.id_riga_documento = self.id
                #salvataggio sconto
                #rigasconto.persist()
                params["session"].add(rigasconto)
                params["session"].commit()
                #params["session"].add(self.rowScontiToSave[i])
        params["session"].commit()
        params["session"].flush()
            #self.__scontiRigaDocumento[i].persist()

riga=Table('riga',
        params['metadata'],
        schema = params['schema'],
        autoload=True)


riga_doc=Table('riga_documento',
            params['metadata'],
            schema = params['schema'],
            autoload=True)

j = join(riga_doc, riga)

std_mapper = mapper(RigaDocumento, j,properties={
        'id':[riga_doc.c.id, riga.c.id],
        "maga":relation(Magazzino,primaryjoin=riga.c.id_magazzino==Magazzino.id),
        "arti":relation(Articolo,primaryjoin=riga.c.id_articolo==Articolo.id),
        "listi":relation(Listino,primaryjoin=riga.c.id_listino==Listino.id),
        "multi":relation(Multiplo,primaryjoin=riga.c.id_multiplo==Multiplo.id),},
                order_by=riga_doc.c.id)
