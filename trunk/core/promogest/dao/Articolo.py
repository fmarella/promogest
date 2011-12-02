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

from promogest.ui.utils import codeIncrement, tempo, posso
from sqlalchemy import *
from sqlalchemy.orm import *
from promogest.Environment import *
from Dao import Dao
from promogest.dao.DaoUtils import giacenzaArticolo
from promogest import Environment
from promogest.modules.GestioneKit.dao.ArticoloKit import ArticoloKit
from Imballaggio import Imballaggio
from AliquotaIva import AliquotaIva
from StatoArticolo import StatoArticolo
#from Immagine import Immagine
from UnitaBase import UnitaBase
from FamigliaArticolo import FamigliaArticolo
from CategoriaArticolo import CategoriaArticolo
from CodiceABarreArticolo import CodiceABarreArticolo
from Fornitura import Fornitura
from Multiplo import Multiplo
from promogest.ui.utils import codeIncrement

if hasattr(conf, "PromoWear") and getattr(conf.PromoWear,'mod_enable')=="yes":
    from promogest.modules.PromoWear.dao.Colore import Colore
    from promogest.modules.PromoWear.dao.Taglia import Taglia
    from promogest.modules.PromoWear.dao.ArticoloTagliaColore import ArticoloTagliaColore
    from promogest.modules.PromoWear.dao.AnnoAbbigliamento import AnnoAbbigliamento
    from promogest.modules.PromoWear.dao.GruppoTaglia import GruppoTaglia
    from promogest.modules.PromoWear.dao.StagioneAbbigliamento import StagioneAbbigliamento
    from promogest.modules.PromoWear.dao.GenereAbbigliamento import GenereAbbigliamento

if posso("ADR"):
    from promogest.modules.ADR.dao.ArticoloADR import ArticoloADR



class Articolo(Dao):

    def __init__(self, req=None):
        Dao.__init__(self, entity=self)
        self.__articoloTagliaColore = None
        self.__codibar = None

    @reconstructor
    def init_on_load(self):
        self.__codibar = None
        self.__articoloTagliaColore = None

    def cod_bar(self):
        if not self.__codibar:
            self.__codibar = params["session"].query(CodiceABarreArticolo).with_parent(self).filter(articolo.c.id==CodiceABarreArticolo.id_articolo)
        return self.__codibar

    @property
    def codice_a_barre(self):
        """ esempio di funzione  unita alla property """
        que = self.cod_bar()
        try:
            # cerco la situazione ottimale, un articolo ha un codice ed è primario
            try:
                a =  que.filter(CodiceABarreArticolo.primario==True).one()
                return a.codice
            except:
                a =  que.one()
                return a.codice
        except:
            return ""

    def getGiacenza(self):
        giace =giacenzaArticolo(year=Environment.workingYear,
                                        idArticolo=self.id,
                                        allMag=True)[0]
        return giace
#        return 0
#    giacenza = property(_setGiacenzaArticolo)



    @property
    def codice_articolo_fornitore(self):
        codi = []
        if self.fornitur:
            for f in self.fornitur:
                if not f.codice_articolo_fornitore in codi and f.codice_articolo_fornitore is not None:
                    codi.append(f.codice_articolo_fornitore)
            if len(codi)>1:
#                print "STRANAMENTE CI SONO PI§ CODICI FORNITORE PER QUESTO ARTICOLO"
                return codi[-1] or ""
            elif len(codi)==1:
                return codi[0]
            else:
                return ""
#            return forni.codice_articolo_fornitore or ""


    @property
    def articoli_kit(self):
        arti =ArticoloKit().select(idArticoloWrapper=self.id,batchSize=None)
        return arti

    @property
    def componente_in_kit(self):
        #from promogest.modules.GestioneKit.dao.ArticoloKit import ArticoloKit
        arti =ArticoloKit().select(idArticoloFiller=self.id,batchSize=None)
        return arti

    def _sm(self):
        if self.stoccaggio:
            return self.stoccaggio[0].scorta_minima
        return 0
    sm = property(_sm)

    @property
    def imballaggio(self):
        if self.imba: return self.imba.denominazione
        else: return ""


    def _getImmagine(self):
        self._url_immagine = ""
        return self._url_immagine
        if self.image:
            self._url_immagine= self.image.filename
        else:
            self._url_immagine = ""
        return self._url_immagine

    def _setImmagine(self, value):
        self._url_immagine = value
    url_immagine= property(_getImmagine, _setImmagine)

    @property
    def denominazione_famiglia(self):
        if self.den_famiglia :return self.den_famiglia.denominazione
        else : return ""


    @property
    def denominazione_breve_famiglia(self):
        if self.den_famiglia:return self.den_famiglia.denominazione_breve
        else: return ""

    @property
    def denominazione_breve_aliquota_iva(self):
        if self.ali_iva :return self.ali_iva.denominazione_breve
        else: return ""

    @property
    def id_tipo_aliquota_iva(self):
        if self.ali_iva :return self.ali_iva.id_tipo
        else: return 1

    @property
    def denominazione_aliquota_iva(self):
        if self.ali_iva :return self.ali_iva.denominazione
        else: return ""

    @property
    def percentuale_aliquota_iva(self):
        if self.ali_iva :return self.ali_iva.percentuale
        else: return ""

    @property
    def denominazione_breve_categoria(self):
        if self.den_categoria: return self.den_categoria.denominazione_breve
        else: return ""

    @property
    def denominazione_categoria(self):
        if self.den_categoria: return self.den_categoria.denominazione
        else: return ""

    @property
    def denominazione_breve_unita_base(self):
        if self.den_unita:return self.den_unita.denominazione_breve
        else: return ""

    @property
    def denominazione_unita_base(self):
        if self.den_unita:return self.den_unita.denominazione
        else: return ""

    @property
    def stato_articolo(self):
        if self.sa: return self.sa.denominazione
        else: return ""


    def _impegnatoSuLavorazione(self):
        from promogest.modules.SchedaLavorazione.dao.SchedaOrdinazione import SchedaOrdinazione
        from promogest.modules.SchedaLavorazione.dao.RigaSchedaOrdinazione import RigaSchedaOrdinazione
        from promogest.dao.Riga import Riga
        if self.codice not in ["Stampa", "z-CONTR","z-BONIFICO"]:
            year = Environment.workingYear
            t=0
            part= Environment.params["session"]\
                .query(Riga.quantita)\
                .filter(and_(SchedaOrdinazione.fattura!=True,
                            Riga.id==RigaSchedaOrdinazione.id,
                                RigaSchedaOrdinazione.id_scheda == SchedaOrdinazione.id,
                                Riga.id_articolo==self.id,
                                )).all()
            for r in part:
                t +=r[0]
            return t
    #impegnato_su_lavorazione = property(_impegnatoSuLavorazione)



    if hasattr(conf, "PromoWear") and getattr(conf.PromoWear,'mod_enable')=="yes":


        def getArticoloTagliaColore(self):
            """ Restituisce il Dao ArticoloTagliaColore collegato al Dao Articolo #"""
            self.__articoloTagliaColore = ArticoloTagliaColore().getRecord(id=self.id)
            return self.__articoloTagliaColore

        def setArticoloTagliaColore(self, value):
            """ Imposta il Dao ArticoloTagliaColore collegato al Dao Articolo
            """
            self.__articoloTagliaColore = value
        articoloTagliaColore = property(getArticoloTagliaColore, setArticoloTagliaColore)

        def getArticoliTagliaColore(self, idGruppoTaglia=None, idTaglia=None, idColore=None, order=None):
            """ Restituisce una lista di Dao ArticoloTagliaColore figli del Dao Articolo """
            #from promogest.modules.PromoWear.dao.ArticoloTagliaColore import select
            articoli = []
            try:
                articolo_relato = ArticoloTagliaColore().getRecord(id=self.id)
                if order =="Colore":
                    orderBy = ArticoloTagliaColore.id_colore.asc()
                elif order =="Taglia":
                    orderBy = ArticoloTagliaColore.id_taglia.asc()
                elif order =="ColoreDESC":
                    orderBy = ArticoloTagliaColore.id_colore.desc()
                elif order =="TagliaDESC":
                    orderBy = ArticoloTagliaColore.id_taglia.desc()
                else:
                    orderBy = None
                if not articolo_relato.id_articolo_padre:
                    articoli = ArticoloTagliaColore().select(idArticoloPadre=articolo_relato.id_articolo,
                                                                idGruppoTaglia=idGruppoTaglia,
                                                                idTaglia=idTaglia,
                                                                idColore=idColore,
                                                                offset=None,
                                                                batchSize=None,
                                                                orderBy=orderBy)
                else:
                    articoli = ArticoloTagliaColore().select(idArticoloPadre=articolo_relato.id_articolo_padre,
                                                                idGruppoTaglia=idGruppoTaglia,
                                                                idTaglia=idTaglia,
                                                                idColore=idColore,
                                                                offset=None,
                                                                batchSize=None,
                                                                orderBy=orderBy)
            except:
                #print "FOR DEBUG ONLY getArticoliTagliaColore FAILED"
                pass
            return articoli
        articoliTagliaColore = property(getArticoliTagliaColore)


        def _getArticoliVarianti(self,order=None):
            """ Restituisce una lista di Dao Articolo Varianti """
            return [Articolo().getRecord(id=art.id_articolo) for art in self.getArticoliTagliaColore(order=order)]
        articoliVarianti = property(_getArticoliVarianti)


        def _getTaglie(self):
            """ Restituisce una lista di Dao Taglia relativi alle taglie di tutti i Dao
                ArticoloTagliaColore figli del Dao Articolo  """
            idTaglie = set(a.id_taglia for a in self.articoliTagliaColore)
            return [Taglia().getRecord(id=idt) for idt in idTaglie]

        taglie = property(_getTaglie)


        def _getColori(self):
            """ Restituisce una lista di Dao Colore relativi ai colori di tutti i Dao
                ArticoloTagliaColore figli del Dao Articolo """
            idColori = set(a.id_colore for a in self.articoliTagliaColore)
            return [Colore().getRecord(id=idc) for idc in idColori]

        colori = property(_getColori)

        def _id_articolo_padre(self):
            if self.ATC: return self.ATC.id_articolo_padre or None
        id_articolo_padre_taglia_colore=property(_id_articolo_padre)
        id_articolo_padre = property(_id_articolo_padre)

        def _id_articolo(self):
            # we need it to see if this is ia tagliacolore simple article without father or variant
            if self.ATC: return self.ATC.id_articolo or None
        id_articolo_taglia_colore=property(_id_articolo)

        def _id_gruppo_taglia(self):
            if self.ATC: return self.ATC.id_gruppo_taglia or None
        id_gruppo_taglia=property(_id_gruppo_taglia)

        def _id_taglia(self):
            if self.ATC: return self.ATC.id_taglia or None
        id_taglia=property(_id_taglia)

        def _id_colore(self):
            if self.ATC: return self.ATC.id_colore or None
        id_colore=property(_id_colore)

        def _id_modello(self):
            if self.ATC: return self.ATC.id_modello or None
        id_modello=property(_id_modello)

        def _id_genere(self):
            if self.ATC: return self.ATC.id_genere or None
            #else: return ""
        id_genere = property(_id_genere)

        def _id_stagione(self):
            if self.ATC: return self.ATC.id_stagione or None
        id_stagione = property(_id_stagione)

        @property
        def id_anno(self):
            if self.ATC: return self.ATC.id_anno or ""

        @property
        def denominazione_gruppo_taglia(self):
            """ esempio di funzione  unita alla property """
            if self.ATC :
                try:
                    return self.ATC[0].denominazione_gruppo_taglia
                except:
                    return self.ATC.denominazione_gruppo_taglia

        @property
        def denominazione_taglia(self):
            """ esempio di funzione  unita alla property """
            if self.ATC :
                try:
                    return self.ATC[0].denominazione_taglia
                except:
                    return self.ATC.denominazione_taglia
            else:
                return ""

        @property
        def denominazione_breve_taglia(self):
            """ esempio di funzione  unita alla property """
            if self.ATC :
                try:
                    return self.ATC[0].denominazione_breve_taglia
                except:
                    return self.ATC.denominazione_breve_taglia

        def _denominazione_colore(self):
            """ esempio di funzione  unita alla property """
            if self.ATC :
                try:
                    return self.ATC[0].denominazione_colore
                except:
                    return self.ATC.denominazione_colore
        denominazione_colore = property(_denominazione_colore)

        def _denominazione_breve_colore(self):
            """ esempio di funzione  unita alla property """
            if self.ATC :
                try:
                    return self.ATC[0].denominazione_breve_colore
                except:
                    return self.ATC.denominazione_breve_colore
        denominazione_breve_colore = property(_denominazione_colore)

        def _denominazione_modello(self):
            """ esempio di funzione  unita alla property """
            if self.ATC :
                try:
                    return self.ATC[0].denominazione_modello
                except:
                    return self.ATC.denominazione_modello
        denominazione_modello = property(_denominazione_modello)

        @property
        def anno(self):
            """ esempio di funzione  unita alla property """
            if self.ATC :
                try:
                    return self.ATC[0].anno
                except:
                    return self.ATC.anno

        @property
        def stagione(self):
            """ esempio di funzione  unita alla property """
            if self.ATC :
                try:
                    return self.ATC[0].stagione
                except:
                    return self.ATC.stagione

        @property
        def genere(self):
            """ esempio di funzione  unita alla property """
            if self.ATC :
                try:
                    return self.ATC[0].genere
                except:
                    return self.ATC.genere

        def isArticoloPadre(self):
            """ Dice se l'articolo e' un articolo padre """

            articolo = self.getArticoloTagliaColore()
            if articolo is not None:
                return (articolo.id_articolo_padre is None)
            else:
                return False

    if (hasattr(conf, "GestioneNoleggio") and getattr(conf.GestioneNoleggio,'mod_enable')=="yes") or ("GestioneNoleggio" in modulesList):

        @property
        def divisore_noleggio(self):
            """ esempio di funzione  unita alla property """
            if self.APGN :return self.APGN.divisore_noleggio_value
            else: return ""


    if hasattr(conf, "DistintaBase") and getattr(conf.DistintaBase,'mod_enable')=="yes":
        """ necessario questo if"""
        @property
        def articoliAss(self):
            """ esempio di funzione  unita alla property """
            arts = AssociazioneArticolo().select(idPadre=self.id,
                                                offset=None,
                                                batchSize=None
                                                )
            return arts

        @property
        def isNode(self):
            art = AssociazioneArticolo().select(idPadre=self.id,
                                                idFiglio = self.id,
                                                offset=None,
                                                batchSize=None)
            if art:return True
            else: return False

    def persist(self):
        params["session"].add(self)
        #params["session"].commit()
        self.save_update()
        #salvataggio , immagine ....per il momento viene gestita una immagine per articolo ...
        #in seguito sarà l'immagine a comandare non l'articolo
        try:
            if self._url_immagine and Immagine().getRecord(id=self.id_immagine):
                img = Immagine().getRecord(id=self.id_immagine)
                img.filename=self._url_immagine
                img.id_famiglia = self.id_famiglia_articolo
                self.id_immagine = self.id
                params["session"].add(img)
                self.save_update()
                params["session"].add(self)
                self.save_update()
            elif self._url_immagine:
                img = Immagine()
                img.id=self.id
                img.filename=self._url_immagine
                img.id_famiglia = self.id_famiglia_articolo
                self.id_immagine = self.id
                params["session"].add(img)
                self.saveToAppLog(img)
                params["session"].add(self)
                self.saveToAppLog(self)
            elif not self._url_immagine and Immagine().getRecord(id=self.id_immagine):
                img = Immagine().getRecord(id=self.id_immagine)
                self.id_immagine = None
                img.delete()
        except:
            pass
        if posso("GN"):
            if self.divisore_noleggio_value_set and self.id:
                div_nol = ArticoloGestioneNoleggio().getRecord(id=self.id)
                if div_nol:
                        div_nol.divisore_noleggio_value = self.divisore_noleggio_value_set
                        params["session"].add(div_nol)
                else:
                    div_nol = ArticoloGestioneNoleggio()
                    div_nol.id_articolo = self.id
                    div_nol.divisore_noleggio_value = self.divisore_noleggio_value_set
                    params["session"].add(div_nol)

        if posso("PW"):
            try:
                if self.__articoloTagliaColore:
                    isTc = ArticoloTagliaColore().getRecord(id=self.id)
                    if isTc:
                        isTc.delete()
                    self.__articoloTagliaColore.id_articolo=self.id
                    params["session"].add(self.__articoloTagliaColore)
                    self.save_update()
                    if self.isArticoloPadre():
                        for var in self.getArticoliTagliaColore():
                            var.id_genere = self.__articoloTagliaColore.id_genere
                            var.id_anno = self.__articoloTagliaColore.id_anno
                            var.id_stagione = self.__articoloTagliaColore.id_stagione
                            var.id_modello = self.__articoloTagliaColore.id_modello
                            params["session"].add(var)
                        #self.saveToAppLog(var)
            except:
                print "ARTICOLO NORMALE SENZA TAGLIE O COLORI"

        if posso("ADR"):
            if self.articoloADR and self.id:
                articoloADR = ArticoloADR().select(id_articolo=self.id)
                if articoloADR:
                        articoloADR[0].delete()
                self.articoloADR.id_articolo = self.id
                params["session"].add(self.articoloADR)
                self.save_update()

        params["session"].commit()

    def delete(self):
        # se l'articolo e' presente tra le righe di un movimento o documento
        # si esegue la cancellazione logica
        from promogest.dao.ListinoArticolo import ListinoArticolo
        from promogest.dao.Inventario import Inventario
        from Riga import Riga
        res = Riga().select(id_articolo=self.id)
        inv = Inventario().select(idArticolo=self.id)
        sc = None
        if posso("VD"):
            from promogest.modules.VenditaDettaglio.dao.RigaScontrino import RigaScontrino
            sc = RigaScontrino().select(idArticolo= self.id)
        if res or inv:
            daoArticolo = Articolo().getRecord(id=self.id)
            daoArticolo.cancellato = True
            params["session"].add(daoArticolo)
        elif sc:
            daoArticolo = Articolo().getRecord(id=self.id)
            daoArticolo.cancellato = True
            params["session"].add(daoArticolo)
        else:
            if posso("PW"):
                atc = ArticoloTagliaColore().getRecord(id=self.id)
                if atc:
                    atc.delete()
            if posso('ADR'):
                artADR = ArticoloADR().select(id_articolo=self.id)
                if artADR:
                    params["session"].delete(artADR[0])
            params["session"].delete(self)
        la = ListinoArticolo().select(idArticolo= self.id)
        if la:
            for l in la:
                l.delete()
#        try:
        if posso("GN"):
            from promogest.modules.GestioneNoleggio.dao.ArticoloGestioneNoleggio import ArticoloGestioneNoleggio
            artGN = ArticoloGestioneNoleggio().select(idArticolo=self.id)
            if artGN:
                params["session"].delete(artGN[0])
        params["session"].commit()
        Environment.pg2log.info("DELETE ARTICOLO" )
#        except:
#            print " ATTENZIONE CANCELLAZIONE ARTICOLO NON  RIUSCITA"

    def filter_values(self,k,v):
        if k == "codice":
            dic = {k:articolo.c.codice.ilike("%"+v+"%")}
        elif k == "codicesatto" or k == "codiceEM":
            dic = {k:articolo.c.codice == v}
        elif k == 'denominazione':
            dic = {k:articolo.c.denominazione.ilike("%"+v+"%")}
        elif k == 'codiceABarre':
            dic = {k:and_(articolo.c.id==CodiceABarreArticolo.id_articolo,CodiceABarreArticolo.codice.ilike("%"+v+"%"))}
        elif k == 'codiceABarreEM':
            dic = {k:and_(articolo.c.id==CodiceABarreArticolo.id_articolo,CodiceABarreArticolo.codice ==v)}
        elif k== 'codiceArticoloFornitore':
            dic = {k:and_(articolo.c.id==fornitura.c.id_articolo,fornitura.c.codice_articolo_fornitore.ilike("%"+v+"%"))}
        elif k== 'codiceArticoloFornitoreEM':
            dic = {k:and_(articolo.c.id==fornitura.c.id_articolo,fornitura.c.codice_articolo_fornitore == v)}
        elif k == 'produttore':
            dic = {k:articolo.c.produttore.ilike("%"+v+"%")}
        elif k=='idFamiglia':
            dic = {k:articolo.c.id_famiglia_articolo ==v}
        elif k=='idAliquotaIva':
            dic = {k:articolo.c.id_aliquota_iva ==v}
        elif k == 'idCategoria':
            dic = {k:articolo.c.id_categoria_articolo ==v}
        elif k == 'idCategoriaList':
            dic = {k:articolo.c.id_categoria_articolo.in_(v)}
        elif k == 'idStato':
            dic= {k:articolo.c.id_stato_articolo == v}
        elif k == 'cancellato':
            dic = {k:or_(articolo.c.cancellato != v)}
        elif k == 'idArticolo':
            dic = {k:or_(articolo.c.id == v)}
        elif k == "listinoFissato":
            dic = {k:and_(listinoarticolo.c.id_articolo == articolo.c.id, listinoarticolo.c.id_listino == v)}
        elif posso("PW"):
            if k == 'figliTagliaColore':
                dic = {k:and_(articolo.c.id==ArticoloTagliaColore.id_articolo, ArticoloTagliaColore.id_articolo_padre==None)}
            elif k == 'idTaglia':
                dic = {k:and_(articolo.c.id==ArticoloTagliaColore.id_articolo, ArticoloTagliaColore.id_taglia==v)}
            elif k == 'idModello':
                dic = {k:and_(articolo.c.id==ArticoloTagliaColore.id_articolo, ArticoloTagliaColore.id_modello==v)}
            elif k == 'idGruppoTaglia':
                dic = {k:and_(articolo.c.id==ArticoloTagliaColore.id_articolo, ArticoloTagliaColore.id_gruppo_taglia ==v)}
            elif k == 'padriTagliaColore':
                dic = {k:and_(articolo.c.id==ArticoloTagliaColore.id_articolo, ArticoloTagliaColore.id_articolo_padre!=None)}
            elif k == 'idColore':
                dic = {k:and_(articolo.c.id==ArticoloTagliaColore.id_articolo, ArticoloTagliaColore.id_colore ==v)}
            elif k == 'idStagione':
                dic = {k:and_(articolo.c.id==ArticoloTagliaColore.id_articolo, ArticoloTagliaColore.id_stagione ==v)}
            elif k == 'idAnno':
                dic = {k:and_(articolo.c.id==ArticoloTagliaColore.id_articolo, ArticoloTagliaColore.id_anno == v)}
            elif k == 'idGenere':
                dic = {k:and_(articolo.c.id==ArticoloTagliaColore.id_articolo, ArticoloTagliaColore.id_genere ==v)}
        elif posso("SL"):
            if k =="node":
                dic = {k: and_(AssociazioneArticolo.id_padre==articolo.c.id,
                        AssociazioneArticolo.id_figlio ==articolo.c.id)}
        return  dic[k]

listinoarticolo=Table('listino_articolo',params['metadata'],schema = params['schema'],autoload=True)
fornitura=Table('fornitura',params['metadata'],schema = params['schema'],autoload=True)
articolo=Table('articolo', params['metadata'],schema = params['schema'],autoload=True)
unita_b=Table('unita_base', params['metadata'],schema = params['mainSchema'],autoload=True)
imballo=Table('imballaggio', params['metadata'],schema = params['schema'],autoload=True)
codb=Table('codice_a_barre_articolo', params['metadata'],schema = params['schema'],autoload=True)
aliva=Table('aliquota_iva', params['metadata'],schema = params['schema'],autoload=True)
catearti=Table('categoria_articolo', params['metadata'],schema = params['schema'],autoload=True)
famiarti=Table('famiglia_articolo', params['metadata'],schema = params['schema'],autoload=True)
statoart=Table('stato_articolo', params['metadata'],schema = params['mainSchema'],autoload=True)
img=Table('image', params['metadata'],schema = params['schema'],autoload=True)

std_mapper = mapper(Articolo,articolo,
            properties=dict(
                        cod_barre = relation(CodiceABarreArticolo,primaryjoin=
                                articolo.c.id==codb.c.id_articolo, backref="arti", cascade="all, delete"),
                        imba = relation(Imballaggio,primaryjoin=articolo.c.id_imballaggio==imballo.c.id),
                        ali_iva =  relation(AliquotaIva,primaryjoin=
                                (articolo.c.id_aliquota_iva==aliva.c.id)),
                        den_famiglia = relation(FamigliaArticolo,primaryjoin= articolo.c.id_famiglia_articolo==famiarti.c.id),
                        den_categoria = relation(CategoriaArticolo,primaryjoin=
                                    (articolo.c.id_categoria_articolo==catearti.c.id)),
                        den_unita = relation(UnitaBase,primaryjoin=articolo.c.id_unita_base==unita_b.c.id),
                        #image = relation(Immagine,primaryjoin= articolo.c.id_immagine==img.c.id,
                                            #cascade="all, delete",
                                            #backref="arti"),
                        sa = relation(StatoArticolo,primaryjoin=(articolo.c.id_stato_articolo==statoart.c.id)),
                        fornitur = relation(Fornitura,primaryjoin=(fornitura.c.id_articolo==articolo.c.id), backref="arti"),
                        multi = relation(Multiplo,primaryjoin=(Multiplo.id_articolo==articolo.c.id),backref="arti")
                        ), order_by=articolo.c.codice)
if hasattr(conf, "PromoWear") and getattr(conf.PromoWear,'mod_enable')=="yes":
    from promogest.modules.PromoWear.dao.ArticoloTagliaColore import ArticoloTagliaColore
    std_mapper.add_property("ATC",relation(ArticoloTagliaColore,primaryjoin=(articolo.c.id==ArticoloTagliaColore.id_articolo),backref="ARTI",uselist=False))
if hasattr(conf, "DistintaBase") and getattr(conf.DistintaBase,'mod_enable')=="yes":
    from promogest.modules.DistintaBase.dao.AssociazioneArticolo import AssociazioneArticolo
    std_mapper.add_property("AAPadre",relation(AssociazioneArticolo,primaryjoin=(articolo.c.id==AssociazioneArticolo.id_padre),backref="ARTIPADRE"))
    std_mapper.add_property("AAFiglio",relation(AssociazioneArticolo,primaryjoin=(articolo.c.id==AssociazioneArticolo.id_figlio),backref="ARTIFIGLIO"))
if (hasattr(conf, "GestioneNoleggio") and getattr(conf.GestioneNoleggio,'mod_enable')=="yes") or ("GestioneNoleggio"in modulesList):
    from promogest.modules.GestioneNoleggio.dao.ArticoloGestioneNoleggio import ArticoloGestioneNoleggio
    std_mapper.add_property("APGN",relation(ArticoloGestioneNoleggio,primaryjoin=(articolo.c.id==ArticoloGestioneNoleggio.id_articolo),backref="ARTI",uselist=False))

if (hasattr(conf, "ADR") and getattr(conf.ADR, 'mod_enable') == "yes") or ("ADR" in modulesList):
    from promogest.modules.ADR.dao.ArticoloADR import ArticoloADR
    std_mapper.add_property("APADR",
                            relation(ArticoloADR,
                                     primaryjoin=(articolo.c.id==ArticoloADR.id_articolo),
                                     backref="ARTI",
                                     uselist=False))


def isNuovoCodiceByFamiglia():
    """ Indica se un nuovo codice articolo dipende dalla famiglia o meno """
    dependsOn = False

    if hasattr(conf,'Articoli'):
        if hasattr(conf.Articoli,'numero_famiglie'):
            if hasattr(conf.Articoli,'lunghezza_codice_famiglia'):
                dependsOn = ((int(conf.Articoli.lunghezza_codice_famiglia) > 0) and
                            (int(conf.Articoli.numero_famiglie) > 0))
    return dependsOn

def getNuovoCodiceArticolo(idFamiglia=None):
    """ Restituisce il codice progressivo per un nuovo articolo
        05/03/2011: rivista e semplificata, forse troppo però adesso
        è velocissima
    """

    lunghezzaProgressivo = 0
    lunghezzaCodiceFamiglia = 0
    numeroFamiglie = 0
    codice = ''
    try:

        art = session.query(Articolo.codice).order_by(desc(Articolo.id)).limit(500).all()
        #art.reverse()
        #print art
        for q in art:
            codice = codeIncrement(q[0])
            if not codice or Articolo().select(codicesatto=codice):
                continue
            else:
                #if not Articolo().select(codicesatto=codice):
                return codice
    except:
        pass
    try:
        if not codice:
            from promogest.ui.utils import setconf
            dd = setconf("Articoli", "articolo_struttura_codice")
            codice = codeIncrement(dd)
    except:
        pass
    return codice
