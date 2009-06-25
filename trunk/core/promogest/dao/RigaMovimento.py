#-*- coding: utf-8 -*-
#
# Promogest
#
# Copyright (C) 2005 by Promotux Informatica - http://www.promotux.it/
# Author: Francesco Meloni <francesco@promotux.it>


from sqlalchemy import *
from sqlalchemy.orm import *
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
from Riga import Riga
from promogest.ui.utils import getScontiFromDao, getStringaSconti, tempo

if hasattr(conf, "SuMisura") and getattr(conf.SuMisura,'mod_enable') == "yes":
    #from promogest.modules.SuMisura.data.SuMisuraDb import *
    from promogest.modules.SuMisura.dao.MisuraPezzo import MisuraPezzo


class RigaMovimento(Dao):

    def __init__(self, arg=None):
        Dao.__init__(self, entity=self)
        self.__scontiRigaMovimento = None
        self.__dbMisuraPezzo = None
        self.__misuraPezzo = None
        self.__coeficente_noleggio = None
        self.__prezzo_acquisto_noleggio = None
        self.__isrent = None

    @reconstructor
    def init_on_load(self):
        self.__dbMisuraPezzo = None
        self.__misuraPezzo = None
        self.__coeficente_noleggio = None
        self.__prezzo_acquisto_noleggio = None
        self.__isrent = None

    #def _getAliquotaIva(self):
        #_denominazioneBreveAliquotaIva = Articolo().getRecord(id=self.id_articolo).denominazione_breve_aliquota_iva
        #return _denominazioneBreveAliquotaIva
    #aliquota = property(_getAliquotaIva, )
    def __aliquota(self):
        if self.rig: return self.rig.aliquota
        else: return ""
    aliquota= property(__aliquota)

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

    def __codiceArticolo(self):
        if self.rig:return self.rig.codice_articolo
        else: return ""
    codice_articolo= property(__codiceArticolo)

    def __unita_base(self):
        #a =  params["session"].query(Articolo).with_parent(self).filter(self.arti.id_unita_base==UnitaBase.id).all()
        #if not a:
            #return a
        #else:
            #return a[0].den_unita.denominazione_breve
        if self.rig : return self.rig.unita_base
        else: return ""
    unita_base = property(__unita_base)



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




    if hasattr(conf, "SuMisura") and getattr(conf.SuMisura,'mod_enable')=="yes":
        def _getMisuraPezzo(self):
            if self.__misuraPezzo is None:
                self.__dbMisuraPezzo = MisuraPezzo().select(idRiga=self.id)
                self.__misuraPezzo = self.__dbMisuraPezzo[:]
                return self.__misuraPezzo
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


    if hasattr(conf, "PromoWear") and getattr(conf.PromoWear,'mod_enable')=="yes":
        def _denominazione_gruppo_taglia(self):
            if self.rig:return self.rig.denominazione_gruppo_taglia
        denominazione_gruppo_taglia = property(_denominazione_gruppo_taglia)

        def _id_articolo_padre(self):
            if self.rig:return self.rig.id_articolo_padre
        id_articolo_padre_taglia_colore=property(_id_articolo_padre)
        id_articolo_padre = property(_id_articolo_padre)

        def _id_gruppo_taglia(self):
            #if self.ATC: return self.ATC.id_gruppo_taglia or None
            if self.rig:return self.rig.id_gruppo_taglia
        id_gruppo_taglia=property(_id_gruppo_taglia)

        def _id_genere(self):
            #if self.ATC: return self.ATC.id_genere or None
            if self.rig:return self.rig.id_genere
            #else: return ""
        id_genere = property(_id_genere)

        def _id_stagione(self):
            if self.rig:return self.rig.id_stagione
        id_stagione = property(_id_stagione)

        def _id_anno(self):
            if self.rig:return self.rig.id_anno
        id_anno = property(_id_anno)

        def _denominazione_taglia(self):
            """ esempio di funzione  unita alla property """
            if self.rig:return self.rig.denominazione_taglia
        denominazione_taglia = property(_denominazione_taglia)

        def _denominazione_colore(self):
            """ esempio di funzione  unita alla property """
            if self.rig:return self.rig.denominazione_colore
        denominazione_colore = property(_denominazione_colore)

        def _anno(self):
            """ esempio di funzione  unita alla property """
            if self.rig:return self.rig.anno
        anno = property(_anno)

        def _stagione(self):
            """ esempio di funzione  unita alla property """
            if self.rig:return self.rig.stagione
        stagione = property(_stagione)

        def _genere(self):
            """ esempio di funzione  unita alla property """
            if self.rig:return self.rig.genere
        genere = property(_genere)


    def filter_values(self,k,v):
        dic= {  'idTestataMovimento' :riga_mov.c.id_testata_movimento ==v,}
        return  dic[k]

    def persist(self):

        params["session"].add(self)
        params["session"].commit()
        #creazione stoccaggio se non gia' presente
        print "DOPO Commit Riga movimento", tempo()
        stoccato = (Stoccaggio().count(idArticolo=self.id_articolo,
                                                idMagazzino=self.id_magazzino) > 0)
        if not stoccato:
            daoStoccaggio = Stoccaggio()
            daoStoccaggio.id_articolo = self.id_articolo
            daoStoccaggio.id_magazzino = self.id_magazzino
            params["session"].add(daoStoccaggio)
            params["session"].commit()
        print "DOPO Stoccato", tempo()
        if hasattr(conf, "GestioneNoleggio") and getattr(conf.GestioneNoleggio,'mod_enable')=="yes":
        #if self.__coeficente_noleggio and self.__prezzo_acquisto_noleggio:
            nr = NoleggioRiga()
            nr.coeficente = self.coeficente_noleggio
            nr.prezzo_acquisto = self.prezzo_acquisto_noleggio
            if str(self.isrent).upper().strip() == "True".upper().strip():
                print " QUINDI SEI QUI"
                nr.isrent = True
            else:
                nr.isrent = False
            nr.id_riga = self.id
            nr.persist()
        print "Prima di scontiRigaMovimentoDel", tempo()
        scontiRigaMovimentoDel(id=self.id)
        print "Dopo di scontiRigaMovimentoDel", tempo()
        if self.scontiRigheMovimento:
            for value in self.scontiRigheMovimento:
                value.id_riga_movimento = self.id
                value.persist()
                #params["session"].add(value)
            #params["session"].commit()
        print "DOPO sconti riga movimento persist", tempo()
        #print "MAAAAAAAAAAAAAAAAAAA",modulesList
        if "SuMisura" in modulesList:
            #try:
            if self.__misuraPezzo:
                self.__misuraPezzo[0].id_riga = self.id
                self.__misuraPezzo[0].persist()
            #except:
                #print "errore nel salvataggio di misura pezzo"
            self.__misuraPezzo = []


riga=Table('riga', params['metadata'], schema = params['schema'], autoload=True)
riga_mov=Table('riga_movimento', params['metadata'],schema = params['schema'],autoload=True)

j = join(riga_mov, riga)

std_mapper = mapper(RigaMovimento, j,properties={
        'id':[riga_mov.c.id, riga.c.id],
        "rig":relation(Riga,primaryjoin = riga_mov.c.id==riga.c.id, backref="RM"),
        #"arti":relation(Articolo,primaryjoin=riga.c.id_articolo==Articolo.id),
        #"listi":relation(Listino,primaryjoin=riga.c.id_listino==Listino.id),
        #"multi":relation(Multiplo,primaryjoin=riga.c.id_multiplo==Multiplo.id),
        "SCM":relation(ScontoRigaMovimento,primaryjoin = riga_mov.c.id==ScontoRigaMovimento.id_riga_movimento,
                        cascade="all, delete",
                        backref="RM"),
        }, order_by=riga_mov.c.id)

if hasattr(conf, "GestioneNoleggio") and getattr(conf.GestioneNoleggio,'mod_enable')=="yes":
    from promogest.modules.GestioneNoleggio.dao.NoleggioRiga import NoleggioRiga
    std_mapper.add_property("NR",relation(NoleggioRiga,primaryjoin=NoleggioRiga.id_riga==riga.c.id,cascade="all, delete",backref="RM",uselist=False))
