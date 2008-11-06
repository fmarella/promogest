#-*- coding: utf-8 -*-
#
# Promogest
#
# Copyright (C) 2005 by Promotux Informatica - http://www.promotux.it/
# Author: Francesco Meloni <francesco@promotux.it>


from promogest.lib.sqlalchemy import *
from promogest.lib.sqlalchemy.orm import *
from promogest.Environment import *
from promogest import Environment
from Dao import Dao
from Riga import Riga
from Magazzino import Magazzino
from ScontoRigaMovimento import ScontoRigaMovimento
from ScontoRigaDocumento import ScontoRigaDocumento
from Articolo import Articolo
from UnitaBase import UnitaBase
from Listino import Listino
from AliquotaIva import AliquotaIva
from Multiplo import Multiplo
from Stoccaggio import Stoccaggio
from DaoUtils import *
from Fornitura import Fornitura
if hasattr(conf, "SuMisura"):
    if getattr(conf.SuMisura,'mod_enable','yes'):
        from promogest.modules.SuMisura.dao.MisuraPezzo import MisuraPezzo


class RigaMovimento(Dao):

    def __init__(self, arg=None,isList=False, id=None):
        Dao.__init__(self, entity=self.__class__, isList=isList, id=id)
        self.__scontiRigaMovimento = None

    def __magazzino(self):
        if self.maga: return self.maga.denominazione
        else: return ""
    magazzino= property(__magazzino)

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

    def __listino(self):
        if self.listi: return self.listi.denominazione
        else: return ""
    listino= property(__listino)

    def __multiplo(self):
        if self.multi: return self.multi.denominazione
        else: return ""
    multiplo = property(__multiplo)

    def __codiceArticolo(self):
        if self.arti:return self.arti.codice
        else: return ""
    codice_articolo= property(__codiceArticolo)

    def _getScontiRigaMovimento(self):

        if self.id:
            self.__dbScontiRigaMovimentoPart = params["session"].query(ScontoRigaMovimento).filter_by(id_riga_movimento=self.id).all()
            self.__dbScontiRigaDocumentoPart = params["session"].query(ScontoRigaDocumento).filter_by(id_riga_documento=self.id).all()
            self.__dbScontiRigaMovimento = self.__dbScontiRigaMovimentoPart + self.__dbScontiRigaDocumentoPart
            self.__scontiRigaMovimento = self.__dbScontiRigaMovimento[:]
        else:
            self.__scontiRigaMovimento = []
        return self.__scontiRigaMovimento

    def _setScontiRigaMovimento(self, value):
        self.__scontiRigaMovimento = value

    sconti = property(_getScontiRigaMovimento, _setScontiRigaMovimento)

    def _getTotaleRiga(self):
        # Il totale e' ivato o meno a seconda del prezzo
        totaleRiga = float(self.quantita) * float(self.moltiplicatore) * float(self.valore_unitario_netto)
        return totaleRiga

    totaleRiga = property(_getTotaleRiga, )


    def _getCodiceArticoloFornitore(self):
        #FIXME: controllare
        self.__codiceArticoloFornitore = None
        #self.__codiceArticoloFornitore = self.arti.codice_articolo_fornitore
        return self.__codiceArticoloFornitore

    def _setCodiceArticoloFornitore(self, value):
        self.__codiceArticoloFornitore = value

    codiceArticoloFornitore = property(_getCodiceArticoloFornitore, _setCodiceArticoloFornitore)

    #if "SuMisura" in Environment.modulesList:
    def _getMisuraPezzo(self):
                #if self.__dbMisuraPezzo is None:
        try:
            self.__dbMisuraPezzo = MisuraPezzo(isList=True).select(idRiga=self.id)
            self.__misuraPezzo = self.__dbMisuraPezzo[:]
            return self.__misuraPezzo
        except:
            self.__misuraPezzo = []
            return self.__misuraPezzo

    def _setMisuraPezzo(self, value):
            self.__misuraPezzo = value

    misura_pezzo = property(_getMisuraPezzo, _setMisuraPezzo)

    def __unita_base(self):
        a =  params["session"].query(Articolo).with_parent(self).filter(self.arti.id_unita_base==UnitaBase.id).all()
        if not a:
            return a
        else:
            return a[0].den_unita.denominazione_breve
    unita_base = property(__unita_base)

    def filter_values(self,k,v):
        dic= {  'idTestataMovimento' :riga_mov.c.id_testata_movimento ==v,}
        return  dic[k]

    def persist(self, scontiRigaMovimento=None):
        #print " UN PASSO ALLA VOLTA ....SIAMO DENTRO IL PERSIST DI RIGAMOVIMENTO", self
        params["session"].add(self)
        params["session"].commit()

        #creazione stoccaggio se non gia' presente
        stoccato = (Stoccaggio(isList=True).count(idArticolo=self.id_articolo,
                                                   idMagazzino=self.id_magazzino) > 0)
        if not(stoccato):
            daoStoccaggio = Stoccaggio().getRecord()
            daoStoccaggio.id_articolo = self.id_articolo
            daoStoccaggio.id_magazzino = self.id_magazzino
            daoStoccaggio.persist()

        scontiRigaMovimentoDel(id=self.id)
        if scontiRigaMovimento:
            for key,value in scontiRigaMovimento.items():
                if key==self:
                    for v in value:
                        v.id_riga_movimento = self.id
                        params["session"].add(v)
                        params["session"].commit()

        if "SuMisura" in modulesList:
            try:
                mp = MisuraPezzo(id=self.id).getRecord()
                mp.delete()
            except:
                pass
            print "MISURA PEZZOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO", self.__misuraPezzo
            if self.__misuraPezzo:
        #if type(self.__misuraPezzo) == list:
            #if self.__misuraPezzo != []:
                #self.__misuraPezzo[-1].id_riga = self.id
                #self.__misuraPezzo[-1].persist()
        #else:
                self.__misuraPezzo.id_riga = self.id
                params["session"].add(self.__misuraPezzo)
                params["session"].commit()
                #self.__misuraPezzo.persist()
        #FIXME: VERIFICAREEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE

        params["session"].flush()

riga=Table('riga',
        params['metadata'],
        schema = params['schema'],
        autoload=True)

riga_mov=Table('riga_movimento',
                params['metadata'],
                schema = params['schema'],
                autoload=True)

j = join(riga_mov, riga)

std_mapper = mapper(RigaMovimento, j,properties={
        'id':[riga_mov.c.id, riga.c.id],
        "maga":relation(Magazzino,primaryjoin=riga.c.id_magazzino==Magazzino.id),
        "arti":relation(Articolo,primaryjoin=riga.c.id_articolo==Articolo.id),
        "listi":relation(Listino,primaryjoin=riga.c.id_listino==Listino.id),
        "multi":relation(Multiplo,primaryjoin=riga.c.id_multiplo==Multiplo.id),
        }, order_by=riga_mov.c.id)



