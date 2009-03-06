#-*- coding: utf-8 -*-
#
# Promogest
#
# Copyright (C) 2005 by Promotux Informatica - http://www.promotux.it/
# Author: Francesco Meloni <francesco@promotux.it>


from sqlalchemy import Table
from sqlalchemy.orm import mapper, relation, join
from promogest.Environment import params, conf, modulesList
from Dao import Dao
from Magazzino import Magazzino
from ScontoRigaMovimento import ScontoRigaMovimento
from ScontoRigaDocumento import ScontoRigaDocumento
from Articolo import Articolo
from UnitaBase import UnitaBase
from Listino import Listino
from Multiplo import Multiplo
from Stoccaggio import Stoccaggio
from DaoUtils import scontiRigaMovimentoDel
from promogest.ui.utils import getScontiFromDao, getStringaSconti
if hasattr(conf, "SuMisura") and getattr(conf.SuMisura,'mod_enable') == "yes":
    #from promogest.modules.SuMisura.data.SuMisuraDb import *
    from promogest.modules.SuMisura.dao.MisuraPezzo import MisuraPezzo


class RigaMovimento(Dao):

    def __init__(self, arg=None):
        Dao.__init__(self, entity=self)
        self.__scontiRigaMovimento = None

    def __magazzino(self):
        if self.maga: return self.maga.denominazione
        else: return ""
    magazzino= property(__magazzino)

    def _getAliquotaIva(self):
        _denominazioneBreveAliquotaIva = Articolo().getRecord(id=self.id_articolo).denominazione_breve_aliquota_iva
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

    def _getStringaScontiRigaMovimento(self):
        (listSconti, applicazione) = getScontiFromDao(self._getScontiRigaMovimento(), self.applicazione_sconti)
        return getStringaSconti(listSconti)

    stringaSconti = property(_getStringaScontiRigaMovimento)

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

    if "SuMisura" in modulesList:
        def _getMisuraPezzo(self):
                    #if self.__dbMisuraPezzo is None:
            try:
                self.__dbMisuraPezzo = MisuraPezzo().select(idRiga=self.id)
                self.__misuraPezzo = self.__dbMisuraPezzo[:]
                return self.__misuraPezzo
            except:
                self.__misuraPezzo = []
                return self.__misuraPezzo

        def _setMisuraPezzo(self, value):
            self.__misuraPezzo = value
        misura_pezzo = property(_getMisuraPezzo, _setMisuraPezzo)

        def _altezza(self):
            if self.misura_pezzo:
                return self.misura_pezzo[0].altezza
            else:
                return ""
        altezza = property(_altezza)

        def _larghezza(self):
            if self.misura_pezzo:
                return self.misura_pezzo[0].larghezza
            else:
                return ""
        larghezza = property(_larghezza)

        def _moltiplicatore(self):
            if self.misura_pezzo:
                return self.misura_pezzo[0].moltiplicatore
            else:
                return ""
        pezzi_moltiplicatore = property(_moltiplicatore)


    def __unita_base(self):
        a =  params["session"].query(Articolo).with_parent(self).filter(self.arti.id_unita_base==UnitaBase.id).all()
        if not a:
            return a
        else:
            return a[0].den_unita.denominazione_breve
    unita_base = property(__unita_base)

    if hasattr(conf, "PromoWear") and getattr(conf.PromoWear,'mod_enable')=="yes":
        def _denominazione_gruppo_taglia(self):
            #if self.ATC: return self.ATC.denominazione or ""
            if self.arti:return self.arti.denominazione_gruppo_taglia
            #else: return ""
        denominazione_gruppo_taglia = property(_denominazione_gruppo_taglia)

        def _id_articolo_padre(self):
            #if self.ATC: return self.ATC.id_articolo_padre or None
            if self.arti:return self.arti.id_articolo_padre
        id_articolo_padre_taglia_colore=property(_id_articolo_padre)
        id_articolo_padre = property(_id_articolo_padre)

        def _id_gruppo_taglia(self):
            #if self.ATC: return self.ATC.id_gruppo_taglia or None
            if self.arti:return self.arti.id_gruppo_taglia
        id_gruppo_taglia=property(_id_gruppo_taglia)

        def _id_genere(self):
            #if self.ATC: return self.ATC.id_genere or None
            if self.arti:return self.arti.id_genere
            #else: return ""
        id_genere = property(_id_genere)

        def _id_stagione(self):
            if self.arti:return self.arti.id_stagione
        id_stagione = property(_id_stagione)

        def _id_anno(self):
            if self.arti:return self.arti.id_anno
        id_anno = property(_id_anno)

        def _denominazione_taglia(self):
            """ esempio di funzione  unita alla property """
            if self.arti:return self.arti.denominazione_taglia
        denominazione_taglia = property(_denominazione_taglia)

        def _denominazione_colore(self):
            """ esempio di funzione  unita alla property """
            if self.arti:return self.arti.denominazione_colore
        denominazione_colore = property(_denominazione_colore)

        def _anno(self):
            """ esempio di funzione  unita alla property """
            if self.arti:return self.arti.anno
        anno = property(_anno)

        def _stagione(self):
            """ esempio di funzione  unita alla property """
            if self.arti:return self.arti.stagione
        stagione = property(_stagione)

        def _genere(self):
            """ esempio di funzione  unita alla property """
            if self.arti:return self.arti.genere
        genere = property(_genere)


    def filter_values(self,k,v):
        dic= {  'idTestataMovimento' :riga_mov.c.id_testata_movimento ==v,}
        return  dic[k]

    def persist(self):

        params["session"].add(self)
        params["session"].commit()
        #creazione stoccaggio se non gia' presente
        stoccato = (Stoccaggio().count(idArticolo=self.id_articolo,
                                                idMagazzino=self.id_magazzino) > 0)
        if not(stoccato):
            daoStoccaggio = Stoccaggio()
            daoStoccaggio.id_articolo = self.id_articolo
            daoStoccaggio.id_magazzino = self.id_magazzino
            params["session"].add(daoStoccaggio)
            params["session"].commit()

        scontiRigaMovimentoDel(id=self.id)
        if self.scontiRigheMovimento:
            for value in self.scontiRigheMovimento:
                value.id_riga_movimento = self.id
                params["session"].add(value)
            params["session"].commit()

        #print "MAAAAAAAAAAAAAAAAAAA",modulesList
        if "SuMisura" in modulesList:
            #try:
            if self.__misuraPezzo:
                self.__misuraPezzo.id_riga = self.id
                params["session"].add(self.__misuraPezzo)
                params["session"].commit()
            #except:
                #print "errore nel salvataggio di misura pezzo"


riga=Table('riga', params['metadata'], schema = params['schema'], autoload=True)
riga_mov=Table('riga_movimento', params['metadata'],schema = params['schema'],autoload=True)

j = join(riga_mov, riga)

std_mapper = mapper(RigaMovimento, j,properties={
        'id':[riga_mov.c.id, riga.c.id],
        "maga":relation(Magazzino,primaryjoin=riga.c.id_magazzino==Magazzino.id),
        "arti":relation(Articolo,primaryjoin=riga.c.id_articolo==Articolo.id),
        "listi":relation(Listino,primaryjoin=riga.c.id_listino==Listino.id),
        "multi":relation(Multiplo,primaryjoin=riga.c.id_multiplo==Multiplo.id),
        "SCM":relation(ScontoRigaMovimento,primaryjoin = riga_mov.c.id==ScontoRigaMovimento.id_riga_movimento,
                        cascade="all, delete",
                        backref="RM"),
        }, order_by=riga_mov.c.id)

#if hasattr(conf, "SuMisura") and getattr(conf.SuMisura,'mod_enable') == "yes":
    ##from promogest.modules.SuMisura.data.SuMisuraDb import *
    #from promogest.modules.SuMisura.dao.MisuraPezzo import MisuraPezzo
    #std_mapper.add_property("sumi",relation(MisuraPezzo,primaryjoin=
                    #MisuraPezzo.id_riga==riga_mov.c.id,
                    #cascade="all, delete",
                    #backref="riga_mov"))