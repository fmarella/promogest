# -*- coding: utf-8 -*-

#    Copyright (C) 2005-2012 2011 by Promotux
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


from sqlalchemy import *
from sqlalchemy.orm import *
from promogest.Environment import params, conf, modulesList

try:
    t_riga_movimento = Table('riga_movimento',
                         params['metadata'],
                         schema=params['schema'],
                         autoload=True)
except:
    from data.rigaMovimento import t_riga_movimento

from Dao import Dao
from Magazzino import Magazzino
from ScontoRigaMovimento import ScontoRigaMovimento
from ScontoRigaDocumento import ScontoRigaDocumento
from Articolo import Articolo
from UnitaBase import UnitaBase
from Listino import Listino
from Multiplo import Multiplo
from Stoccaggio import Stoccaggio
from Riga import Riga, t_riga
from promogest.lib.utils import getScontiFromDao, getStringaSconti, posso

if hasattr(conf, "SuMisura") and getattr(conf.SuMisura,'mod_enable') == "yes":
    #from promogest.modules.SuMisura.data.SuMisuraDb import *
    from promogest.modules.SuMisura.dao.MisuraPezzo import MisuraPezzo


class RigaMovimento(Dao):

    def __init__(self, req=None):
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
        if self.rig : return self.rig.unita_base
        else: return ""
    unita_base = property(__unita_base)



    def _getScontiRigaMovimento(self):

        if self.id:
            self.__dbScontiRigaMovimentoPart=self.SCM

            #self.__dbScontiRigaDocumentoPart = params["session"].query(ScontoRigaDocumento).filter_by(id_riga_documento=self.id).all()
            self.__dbScontiRigaDocumentoPart = []
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

    def _getCodiceArticoloFornitore(self):
        #FIXME: controllare
        self.__codiceArticoloFornitore = None
        #self.__codiceArticoloFornitore = self.arti.codice_articolo_fornitore
        return self.__codiceArticoloFornitore

    def _setCodiceArticoloFornitore(self, value):
        self.__codiceArticoloFornitore = value

    codiceArticoloFornitore = property(_getCodiceArticoloFornitore, _setCodiceArticoloFornitore)

    def _lottotemp(self):
        if hasattr(self, "NLT"):
            if self.NLT:
                return self.NLT[0].lotto_temp
        else:
            return ""
    numero_lotto_temp = property(_lottotemp)


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



    if (hasattr(conf, "GestioneNoleggio") and getattr(conf.GestioneNoleggio,'mod_enable')=="yes") or ("GestioneNoleggio" in modulesList):
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

        def _modello(self):
            """ esempio di funzione  unita alla property """
            if self.rig:return self.rig.denominazione_modello
        denominazione_modello = property(_modello)


    def filter_values(self,k,v):
        if k == 'idTestataMovimento':
            dic= {k: t_riga_movimento.c.id_testata_movimento ==v}
        elif k =="idArticolo":
            dic= {k: t_riga.c.id_articolo == v}
        return  dic[k]

    #def scontiRigaMovimentoDel(self,id=None):
        #"""
        #Cancella gli sconti legati ad una riga movimento
        #"""
        #row = ScontoRigaMovimento().select(idRigaMovimento= id,
                                            #offset = None,
                                            #batchSize = None)
        #if row:
            #for r in row:
                #params['session'].delete(r)
            #params["session"].commit()
            #return True

    def persist(self,sm=False):

        params["session"].add(self)
        #params["session"].commit()
        #creazione stoccaggio se non gia' presente
        stoccato = (Stoccaggio().count(idArticolo=self.id_articolo,
                                                idMagazzino=self.id_magazzino) > 0)
        if not stoccato:
            daoStoccaggio = Stoccaggio()
            daoStoccaggio.id_articolo = self.id_articolo
            daoStoccaggio.id_magazzino = self.id_magazzino
            params["session"].add(daoStoccaggio)
            #params["session"].commit()
        if (hasattr(conf, "GestioneNoleggio") and getattr(conf.GestioneNoleggio,'mod_enable')=="yes") or ("GestioneNoleggio" in modulesList):

            nr = NoleggioRiga()
            nr.coeficente = self.coeficente_noleggio
            nr.prezzo_acquisto = self.prezzo_acquisto_noleggio
            if str(self.isrent).upper().strip() == "True".upper().strip():
                nr.isrent = True
            else:
                nr.isrent = False
            nr.id_riga = self.id
            nr.persist()
        #self.scontiRigaMovimentoDel(id=self.id)
        if self.scontiRigheMovimento:
            if not self.id:
                params["session"].commit()
            for value in self.scontiRigheMovimento:
                value.id_riga_movimento = self.id
                #value.persist()
                params["session"].add(value)
        #params["session"].commit()
        if sm:
            #try:
            if self.__misuraPezzo:
                self.__misuraPezzo[0].id_riga = self.id
                self.__misuraPezzo[0].persist()
            #except:
                #print "errore nel salvataggio di misura pezzo"
            self.__misuraPezzo = []
        #params["session"].commit()


std_mapper = mapper(RigaMovimento, join(t_riga_movimento, t_riga),
    properties={
        'id':[t_riga_movimento.c.id, t_riga.c.id],
        "rig":relation(Riga,primaryjoin = t_riga_movimento.c.id==t_riga.c.id, backref="RM"),
        'totaleRiga': column_property(t_riga.c.quantita * t_riga.c.moltiplicatore * t_riga.c.valore_unitario_netto ),
        'totaleRigaLordo': column_property(t_riga.c.quantita * t_riga.c.moltiplicatore * t_riga.c.valore_unitario_lordo ),
        #"arti":relation(Articolo,primaryjoin=t_riga.c.id_articolo==Articolo.id),
        #"listi":relation(Listino,primaryjoin=t_riga.c.id_listino==Listino.id),
        #"multi":relation(Multiplo,primaryjoin=t_riga.c.id_multiplo==Multiplo.id),
        "SCM":relation(ScontoRigaMovimento,primaryjoin = t_riga_movimento.c.id==ScontoRigaMovimento.id_riga_movimento,
                        cascade="all, delete",
                        backref="RM"),
    },
    order_by=t_riga.c.posizione)

if (hasattr(conf, "GestioneNoleggio") and getattr(conf.GestioneNoleggio,'mod_enable')=="yes") or ("GestioneNoleggio" in modulesList):
    from promogest.modules.GestioneNoleggio.dao.NoleggioRiga import NoleggioRiga
    std_mapper.add_property("NR",relation(NoleggioRiga,primaryjoin=NoleggioRiga.id_riga==t_riga.c.id,cascade="all, delete",backref="RM",uselist=False))
