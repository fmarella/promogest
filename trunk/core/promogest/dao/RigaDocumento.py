# -*- coding: utf-8 -*-

# Promogest
#
# Copyright (C) 2005 by Promotux Informatica - http://www.promotux.it/
# Author: Andrea Argiolas <andrea@promotux.it>


from sqlalchemy import *
from sqlalchemy.orm import *
from promogest.Environment import params, modulesList, conf
from Dao import Dao
from UnitaBase import UnitaBase
from ScontoRigaDocumento import ScontoRigaDocumento
from ScontoRigaMovimento import ScontoRigaMovimento
from Articolo import Articolo
from AliquotaIva import AliquotaIva
from Magazzino import Magazzino
from Listino import Listino
from Multiplo import Multiplo
from DaoUtils import scontiRigaDocumentoDel
from Riga import Riga

if "SuMisura" in modulesList:
    from promogest.modules.SuMisura.dao.MisuraPezzo import MisuraPezzo
from promogest.ui.utils import *

class RigaDocumento(Dao):
    """ User class provides to make a Users dao which include more used"""

    def __init__(self, arg=None):
        Dao.__init__(self, entity=self)
        self.valueList = []
        self.__misuraPezzo = None
        self.__dbMisuraPezzo = None
        self.misura_pezzo2 = None
        # usata per mantenere il valore del codice articolo fornitore proveniente da un
        # documento o movimento di carico, per salvare la fornitura
        self.__codiceArticoloFornitore = None
        self.__coeficente_noleggio = None
        self.__prezzo_acquisto_noleggio = None
        self.__isrent = None
        #pass

    @reconstructor
    def init_on_load(self):
        self.__dbMisuraPezzo = None
        self.misura_pezzo = None
        self.__misuraPezzo = None
        self.__coeficente_noleggio = None
        self.__prezzo_acquisto_noleggio = None
        self.__isrent = None


    #def _getAliquotaIva(self):
        ## Restituisce la denominazione breve dell'aliquota iva
        #_denominazioneBreveAliquotaIva = '%2.0f' % (self.percentuale_iva or 0)
        #daoArticolo = Articolo().getRecord(id=self.id_articolo)
        #if daoArticolo is not None:
            #if daoArticolo.id_aliquota_iva is not None:
                #daoAliquotaIva = AliquotaIva().getRecord(id=daoArticolo.id_aliquota_iva)
                #if daoAliquotaIva is not None:
                    #_denominazioneBreveAliquotaIva = daoAliquotaIva.denominazione_breve or ''
        #if (_denominazioneBreveAliquotaIva == '0' or _denominazioneBreveAliquotaIva == '00'):
            #_denominazioneBreveAliquotaIva = ''
        #return _denominazioneBreveAliquotaIva

    #aliquota = property(_getAliquotaIva, )


    def __aliquota(self):
        if self.rig: return self.rig.aliquota
        else: return ""
    aliquota= property(__aliquota)

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
        if self.rig: return self.rig.magazzino
        else: return ""
    magazzino= property(__magazzino)

    def __listino(self):
        if self.rig: return self.rig.listino
        else: return ""
    listino= property(__listino)

    def __multiplo(self):
        if self.rig: return self.rig.multiplo
        else: return ""
    multiplo = property(__multiplo)

    #def __unita_base(self):
        #a =  params["session"].query(UnitaBase).filter(and_(riga.c.id_articolo == Articolo.id,  Articolo.id_unita_base==UnitaBase.id)).all()
        #if not a:
            #return a
        #else:
            #return a[0].denominazione_breve
    #unita_base = property(__unita_base)
    def __unita_base(self):
        #a =  params["session"].query(Articolo).with_parent(self).filter(self.arti.id_unita_base==UnitaBase.id).all()
        #if not a:
            #return a
        #else:
            #return a[0].den_unita.denominazione_breve
        if self.rig : return self.rig.unita_base
        else: return ""
    unita_base = property(__unita_base)

    def __codiceArticolo(self):
        if self.rig:return self.rig.codice_articolo
        else: return ""
    codice_articolo= property(__codiceArticolo)

    if hasattr(conf, "GestioneNoleggio") and getattr(conf.GestioneNoleggio,'mod_enable')=="yes":

        def _get_coeficente_noleggio(self):
            if not self.__coeficente_noleggio:
                if self.NR:
                    self.__coeficente_noleggio =  self.NR.coeficente
                else:
                    self.__coeficente_noleggio =  0
            return self.__coeficente_noleggio
        def _set_coeficente_noleggio(self, value):
            self.__coeficente_noleggio = value
        coeficente_noleggio = property(_get_coeficente_noleggio, _set_coeficente_noleggio)

        def _get_prezzo_acquisto_noleggio(self):
            if not self.__prezzo_acquisto_noleggio:
                if self.NR:
                    self.__prezzo_acquisto_noleggio =  self.NR.prezzo_acquisto
                else:
                    self.__prezzo_acquisto_noleggio =  0
            return self.__prezzo_acquisto_noleggio
        def _set_prezzo_acquisto_noleggio(self, value):
            self.__prezzo_acquisto_noleggio = value
        prezzo_acquisto_noleggio = property(_get_prezzo_acquisto_noleggio, _set_prezzo_acquisto_noleggio)

        def _get_isrent(self):
            if not self.__isrent:
                if self.NR:
                    self.__isrent =  self.NR.isrent
                else:
                    self.__isrent =  True
            return self.__isrent
        def _set_isrent(self, value):
            self.__isrent = value
        isrent = property(_get_isrent, _set_isrent)


    if hasattr(conf, "SuMisura") and getattr(conf.SuMisura,'mod_enable')=="yes":
        def _getMisuraPezzo(self):
            if not self.__misuraPezzo and self.id:
                self.__dbMisuraPezzo = MisuraPezzo().select(idRiga=self.id)
                self.__misuraPezzo = self.__dbMisuraPezzo[:]
            return self.__misuraPezzo

        def _setMisuraPezzo(self, value):
            self.__misuraPezzo = value
        misura_pezzo = property(_getMisuraPezzo, _setMisuraPezzo)

        def _altezza(self):
            misure = self._getMisuraPezzo()
            if misure:
                return misure[0].altezza
            else:
                return ""
        altezza = property(_altezza)

        def _larghezza(self):
            misure = self._getMisuraPezzo()
            if misure:
                return misure[0].larghezza
            else:
                return ""
        larghezza = property(_larghezza)

        def _moltiplicatore(self):
            if self.misura_pezzo:
                return self.misura_pezzo[0].moltiplicatore
            else:
                return ""
        pezzi_moltiplicatore = property(_moltiplicatore)


    def _getScontiRigaDocumento(self):
        #FIXME : il sistema originale aveva una UNION di due view fatte su mov e doc per cui avevano due campi
        # movimento e riga documento con l'id della riga a cui si riferivano ...
        # noi non avendo la union al momento facciamo due query ed appendiamo le liste
        self.__dbScontiRigaMovimentoPart = params["session"].query(ScontoRigaMovimento).filter_by(id_riga_movimento=self.id).all()
        self.__dbScontiRigaDocumentoPart = params["session"].query(ScontoRigaDocumento).filter_by(id_riga_documento=self.id).all()
        self.__dbScontiRigaDocumento = self.__dbScontiRigaMovimentoPart + self.__dbScontiRigaDocumentoPart
        self.__scontiRigaDocumento = self.__dbScontiRigaDocumento[:]
        return self.__scontiRigaDocumento

    def _setScontiRigaDocumento(self, value):

        self.__scontiRigaDocumento = value

    sconti = property(_getScontiRigaDocumento, _setScontiRigaDocumento)

    def filter_values(self,k,v):
        dic= {  'idTestataDocumento' : riga_doc.c.id_testata_documento==v }
        return  dic[k]

    def persist(self):

        #salvataggio riga
        params["session"].add(self)
        params["session"].commit()
        if hasattr(conf, "SuMisura") and getattr(conf.SuMisura,'mod_enable')=="yes":
            if self.__misuraPezzo:
                self.__misuraPezzo[0].id_riga = self.id
                self.__misuraPezzo[0].persist()

        if hasattr(conf, "GestioneNoleggio") and getattr(conf.GestioneNoleggio,'mod_enable')=="yes":
        #if self.__coeficente_noleggio and self.__prezzo_acquisto_noleggio:
            nr = NoleggioRiga()
            nr.coeficente = self.coeficente_noleggio
            nr.prezzo_acquisto = self.prezzo_acquisto_noleggio
            if str(self.isrent).upper().strip() == "True".upper().strip():
                nr.isrent = True
            else:
                nr.isrent = False
            nr.id_riga = self.id
            nr.persist()

        scontiRigaDocumentoDel(id=self.id)
        if self.scontiRigaDocumento:
            for value in self.scontiRigaDocumento:
                value.id_riga_documento = self.id
                params["session"].add(value)
        params["session"].commit()
        self.__dbMisuraPezzo = []
riga=Table('riga', params['metadata'],schema = params['schema'], autoload=True)
riga_doc=Table('riga_documento',params['metadata'],schema = params['schema'],autoload=True)

j = join(riga_doc, riga)

std_mapper = mapper(RigaDocumento, j,properties={
        'id':[riga_doc.c.id, riga.c.id],
        "rig":relation(Riga,primaryjoin = riga_doc.c.id==riga.c.id, backref="RD"),
        #"maga":relation(Magazzino,primaryjoin=riga.c.id_magazzino==Magazzino.id),
        #"arti":relation(Articolo,primaryjoin=riga.c.id_articolo==Articolo.id),
        #"listi":relation(Listino,primaryjoin=riga.c.id_listino==Listino.id),
        "multi":relation(Multiplo,primaryjoin=riga.c.id_multiplo==Multiplo.id),
        "SCD":relation(ScontoRigaDocumento,primaryjoin = riga_doc.c.id==ScontoRigaDocumento.id_riga_documento, cascade="all, delete", backref="RD"),
            },order_by=riga_doc.c.id)

if hasattr(conf, "GestioneNoleggio") and getattr(conf.GestioneNoleggio,'mod_enable')=="yes":
    from promogest.modules.GestioneNoleggio.dao.NoleggioRiga import NoleggioRiga
    std_mapper.add_property("NR",relation(NoleggioRiga,primaryjoin=NoleggioRiga.id_riga==riga.c.id,cascade="all, delete",backref="RD",uselist=False))
