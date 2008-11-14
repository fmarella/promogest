#-*- coding: utf-8 -*-
#
"""
 Promogest - promoCMS
 Copyright (C) 2007-2008 by Promotux Informatica - http://www.promotux.it/
# Author: JJDaNiMoTh <jjdanimoth@gmail.com>
 license: GPL see LICENSE file
"""

from sqlalchemy import *
from sqlalchemy.orm import *
from promogest.Environment import *
from promogest.dao.Dao import Dao
from promogest.dao.Immagine import Immagine
from promogest.dao.UnitaBase import UnitaBase
from promogest.dao.FamigliaArticolo import FamigliaArticolo
from promogest.dao.AliquotaIva import AliquotaIva
from promogest.dao.CategoriaArticolo import CategoriaArticolo
from promogest.dao.CodiceABarreArticolo import CodiceABarreArticolo
from promogest.dao.Imballaggio import Imballaggio
from promogest.dao.StatoArticolo import StatoArticolo
from promogest.ui.utils import idArticoloFromFornitura, codeIncrement
from promogest.modules.PromoWear.dao.Colore import Colore
from promogest.modules.PromoWear.dao.Taglia import Taglia
from promogest.modules.PromoWear.dao.ArticoloTagliaColore import ArticoloTagliaColore
from promogest.modules.PromoWear.dao.AnnoAbbigliamento import AnnoAbbigliamento
from promogest.modules.PromoWear.dao.GruppoTaglia import GruppoTaglia
from promogest.modules.PromoWear.dao.StagioneAbbigliamento import StagioneAbbigliamento
from promogest.modules.PromoWear.dao.GenereAbbigliamento import GenereAbbigliamento
        #import promogest.modules.PromoWear.dao.Taglia

class Articolo(Dao):

    def __init__(self, arg=None,isList=False, id=None):
        Dao.__init__(self, entity=self.__class__, isList=isList, id=id)
        self.__articoloTagliaColore = None

    def _codice_a_barre(self):
        """ esempio di funzione  unita alla property """
        try:
            # cerco la situazione ottimale, un articolo ha un codice ed è primario
            try:
                a =  params["session"].query(CodiceABarreArticolo.codice).with_parent(self).filter(and_(articolo.c.id==CodiceABarreArticolo.id_articolo,
                            CodiceABarreArticolo.primario==True)).one()
                return a[0]
            except:
                a =  params["session"].query(CodiceABarreArticolo.codice).with_parent(self).filter(articolo.c.id==CodiceABarreArticolo.id_articolo).one()
                return a[0]
        except:
            return ""
    codice_a_barre = property(_codice_a_barre)

    def _codice_articolo_fornitore(self):
        if self.artic: return self.artic.codice_articolo_fornitore
        else: return ""
    codice_articolo_fornitore= property(_codice_articolo_fornitore)

    def _codice_a_barre_all(self):
        """ esempio di funzione  unita alla property """
        a =  params["session"].query(CodiceABarreArticolo).with_parent(self).filter(and_(articolo.c.id==CodiceABarreArticolo.id_articolo)).all()
        if not a:
            return a
        else:
            return a[0].codice
    codice_a_barre_all = property(_codice_a_barre_all)

    def _imballaggio(self):
        if self.imba: return self.imba.denominazione
        else: return ""
    imballaggio= property(_imballaggio)

    def _getImmagine(self):
        if self.image:
            self._url_immagine= self.image.filename
        else:
            self._url_immagine = ""
        return self._url_immagine

    def _setImmagine(self, value):
        self._url_immagine = value
    url_immagine= property(_getImmagine, _setImmagine)

    def _denominazione_famiglia(self):
        if self.den_famiglia :return self.den_famiglia.denominazione
        else : return ""
    denominazione_famiglia= property(_denominazione_famiglia)

    def _denominazione_breve_famiglia(self):
        if self.den_famiglia:return self.den_famiglia.denominazione_breve
        else: return ""
    denominazione_breve_famiglia= property(_denominazione_breve_famiglia)

    def _denominazione_breve_aliquota_iva(self):
        if self.ali_iva :return self.ali_iva.denominazione_breve
        else: return ""
    denominazione_breve_aliquota_iva= property(_denominazione_breve_aliquota_iva)

    def _denominazione_aliquota_iva(self):
        if self.ali_iva :return self.ali_iva.denominazione
        else: return ""
    denominazione_aliquota_iva= property(_denominazione_aliquota_iva)

    def _percentuale_aliquota_iva(self):
        if self.ali_iva :return self.ali_iva.percentuale
        else: return ""
    percentuale_aliquota_iva= property(_percentuale_aliquota_iva)

    def _denominazione_breve_categoria(self):
        if self.den_categoria: return self.den_categoria.denominazione_breve
        else: return ""
    denominazione_breve_categoria = property(_denominazione_breve_categoria)

    def _denominazione_categoria(self):
        if self.den_categoria: return self.den_categoria.denominazione
        else: return ""
    denominazione_categoria = property(_denominazione_categoria)

    def _denominazione_breve_unita_base(self):
        if self.den_unita:return self.den_unita.denominazione_breve
        else: return ""
    denominazione_breve_unita_base= property(_denominazione_breve_unita_base)

    def _denominazione_unita_base(self):
        if self.den_unita:return self.den_unita.denominazione
        else: return ""
    denominazione_unita_base= property(_denominazione_unita_base)

    def _stato_articolo(self):
        if self.sa: return self.sa.denominazione
        else: return ""
    stato_articolo= property(_stato_articolo)

    def getArticoloTagliaColore(self):
        """ Restituisce il Dao ArticoloTagliaColore collegato al Dao Articolo #"""
        #if self.__articoloTagliaColore is not None:
        #self.__articoloTagliaColore = None
        try:
            self.__articoloTagliaColore = ArticoloTagliaColore(isList=True).select(idArticolo=self.id,
                                                                                    offset=None,
                                                                                    batchSize=None)[0]
            return self.__articoloTagliaColore
        except Exception:
            print "Errore in getArticoloTagliaColore"

    def setArticoloTagliaColore(self, value):
        """
        Imposta il Dao ArticoloTagliaColore collegato al Dao Articolo
        """
        print "VALUEEEEEEEEE articoloTagliaColore " , value
        self.__articoloTagliaColore = value

    articoloTagliaColore = property(getArticoloTagliaColore, setArticoloTagliaColore)

    def getArticoloTagliaColoreCompleto(self):
        """
        Restituisce il Dao ArticoloTagliaColore collegato al Dao Articolo
        con le chiavi esterne risolte
        """
        #if self.id is None:
            #return None
        #try:
            #from promogest.modules.PromoWear.dao.ArticoloTagliaColore import select
        articolo = ArticoloTagliaColore(isList=True).select(idArticolo=self.id,
                                                            offset=None,
                                                            batchSize=None)
        if articolo:
            return articolo[0] or None
        #return articolo[0]
        #else:
            #return None
        #except Exception:
            #print "errore in getArticolOTagliaColoreCompleto"
            #return None

    articoloTagliaColoreCompleto = property(getArticoloTagliaColoreCompleto)

    def getArticoliTagliaColore(self, idGruppoTaglia=None, idTaglia=None, idColore=None):
        """ Restituisce una lista di Dao ArticoloTagliaColore figli del Dao Articolo """
        #from promogest.modules.PromoWear.dao.ArticoloTagliaColore import select
        articoli = ArticoloTagliaColore(isList=True).select(idArticoloPadre=self.id,
                                                            idGruppoTaglia=idGruppoTaglia,
                                                            idTaglia=idTaglia,
                                                            idColore=idColore,
                                                            offset=None,
                                                            batchSize=None)
        return articoli
    articoliTagliaColore = property(getArticoliTagliaColore)

    def _getTaglie(self):
        """ Restituisce una lista di Dao Taglia relativi alle taglie di tutti i Dao
            ArticoloTagliaColore figli del Dao Articolo  """
        idTaglie = set(a.id_taglia for a in self.articoliTagliaColore)
        return [Taglia(id=idt).getRecord() for idt in idTaglie]

    taglie = property(_getTaglie)


    def _getColori(self):
        """
        Restituisce una lista di Dao Colore relativi ai colori di tutti i Dao
        ArticoloTagliaColore figli del Dao Articolo
        """

        idColori = set(a.id_colore for a in self.articoliTagliaColore)
        return [Colore(id=idc).getRecord() for idc in idColori]

    colori = property(_getColori)


    #def _denominazione_gruppo_taglia(self):
        #if self.ATC: return self.ATC.denominazione or ""
    #denominazione_gruppo_taglia = property(_denominazione_gruppo_taglia)

    def _id_articolo_padre(self):
        if self.ATC: return self.ATC.id_articolo_padre or None
    id_articolo_padre_taglia_colore=property(_id_articolo_padre)
    id_articolo_padre = property(_id_articolo_padre)

    def _id_gruppo_taglia(self):
        if self.ATC: return self.ATC.id_gruppo_taglia or None
    id_gruppo_taglia=property(_id_gruppo_taglia)

    def _id_genere(self):
        if self.ATC: return self.ATC.id_genere or None
        #else: return ""
    id_genere = property(_id_genere)

    def _id_stagione(self):
        if self.ATC: return self.ATC.id_stagione or None
    id_stagione = property(_id_stagione)

    def _id_anno(self):
        if self.ATC: return self.ATC.id_anno or ""
    id_anno = property(_id_anno)


    def _denominazione_gruppo_taglia(self):
        """ esempio di funzione  unita alla property """
        if self.ATC :
            try:
                return self.ATC[0].denominazione_gruppo_taglia
            except:
                return self.ATC.denominazione_gruppo_taglia
    denominazione_gruppo_taglia = property(_denominazione_gruppo_taglia)


    def _denominazione_taglia(self):
        """ esempio di funzione  unita alla property """
        if self.ATC :
            try:
                return self.ATC[0].denominazione_taglia
            except:
                return self.ATC.denominazione_taglia
    denominazione_taglia = property(_denominazione_taglia)

    def _denominazione_colore(self):
        """ esempio di funzione  unita alla property """
        if self.ATC :
            try:
                return self.ATC[0].denominazione_colore
            except:
                return self.ATC.denominazione_colore
    denominazione_colore = property(_denominazione_colore)

    def _anno(self):
        """ esempio di funzione  unita alla property """
        if self.ATC :
            try:
                return self.ATC[0].anno
            except:
                return self.ATC.anno
    anno = property(_anno)

    def _stagione(self):
        """ esempio di funzione  unita alla property """
        if self.ATC :
            try:
                return self.ATC[0].stagione
            except:
                return self.ATC.stagione
    stagione = property(_stagione)

    def _genere(self):
        """ esempio di funzione  unita alla property """
        if self.ATC :
            try:
                return self.ATC[0].genere
            except:
                return self.ATC.genere
    genere = property(_genere)

    def isArticoloPadre(self):
        """ Dice se l'articolo e' un articolo padre """

        articolo = self.getArticoloTagliaColore()
        if articolo is not None:
            return (articolo.id_articolo_padre is None)
        else:
            return False

    def filter_values(self,k,v):
        if k == "codice":
            dic = {k:articolo.c.codice.ilike("%"+v+"%")}
        elif k == 'denominazione':
            dic = {k:articolo.c.denominazione.ilike("%"+v+"%")}
        elif k == 'codiceABarre':
            dic = {k:and_(articolo.c.id==CodiceABarreArticolo.id_articolo,CodiceABarreArticolo.codice.like("%"+v+"%"))}
        elif k== 'codiceArticoloFornitore':
            dic = {k:and_(articolo.c.id==fornitura.c.id_articolo,fornitura.c.codice_articolo_fornitore.like("%"+v+"%"))}
        elif k == 'produttore':
            dic = {k:articolo.c.produttore.ilike("%"+v+"%")}
        elif k=='idFamiglia':
            dic = {k:articolo.c.id_famiglia_articolo ==v}
        elif k == 'idCategoria':
            dic = {k:articolo.c.id_categoria_articolo ==v}
        elif k == 'idStato':
            dic= {k:articolo.c.id_stato_articolo == v}
        elif k == 'cancellato':
            dic = {k:or_(articolo.c.cancellato != v)}
        elif k == 'figliTagliaColore':
            dic = {k:None}
        elif k == 'idTaglia':
            dic = {k:articolotagliacolore.c.id_taglia==v}
        elif k == 'idGruppoTaglia':
            dic = {k:articolotagliacolore.c.id_gruppo_taglia ==v}
        elif k == 'padriTagliaColore':
            dic = {k:None}
        elif k == 'idColore':
            dic = {k:articolotagliacolore.c.id_colore ==v}
        elif k == 'idStagione':
            dic = {k:articolotagliacolore.c.id_stagione ==v}
        elif k == 'idAnno':
            dic = {k:articolotagliacolore.c.id_anno ==v}
        elif k == 'idGenere':
            dic = {k:articolotagliacolore.c.id_genere ==v}
        return  dic[k]


    def persist(self):
        params["session"].add(self)
        params["session"].commit()
        #salvataggio , immagine ....per il momento viene gestita una immagine per articolo ...
        #in seguito sarà l'immagine a comandare non l'articolo
        try:
            if self._url_immagine and Immagine(id=self.id_immagine).getRecord():
                img = Immagine(id=self.id_immagine).getRecord()
                img.filename=self._url_immagine
                img.id_famiglia = self.id_famiglia_articolo
                self.id_immagine = self.id
                params["session"].add(img)
                params["session"].add(self)
                params["session"].commit()
            elif self._url_immagine:
                img = Immagine().getRecord()
                img.id=self.id
                img.filename=self._url_immagine
                img.id_famiglia = self.id_famiglia_articolo
                self.id_immagine = self.id
                params["session"].add(img)
                params["session"].add(self)
                params["session"].commit()
            elif not self._url_immagine and Immagine(id=self.id_immagine).getRecord():
                img = Immagine(id=self.id_immagine).getRecord()
                self.id_immagine = None
                img.delete()
        except:
            pass
            #print "nessuna immagine associata all'articolo"
        if self.__articoloTagliaColore:
            self.__articoloTagliaColore.id=self.id
            params["session"].add(self.__articoloTagliaColore)
            params["session"].commit()



            print "qui c'è del lavoro da fareeeeeeeeeeeeeeeeeeeeeeeeeeeee"
        params["session"].flush()


#def getByCodice(connection, codice):
    #""" Restituisce il risultato di una ricerca per codice """
    #res = connection.execStoredProcedure('ArticoloGetByCodice', (codice,))
    #if len(res) > 0:
        #return Articolo(connection, res[0]['id'])
        #else:
            #return None


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
    """ Restituisce il codice progressivo per un nuovo articolo """

    lunghezzaProgressivo = 0
    lunghezzaCodiceFamiglia = 0
    numeroFamiglie = 0
    codice = ''
    if hasattr(conf,'Articoli'):
        if hasattr(conf.Articoli,'lunghezza_progressivo'):
            lunghezzaProgressivo = int(conf.Articoli.lunghezza_progressivo)
        if lunghezzaProgressivo > 0:
            if isNuovoCodiceByFamiglia():
                lunghezzaCodiceFamiglia = int(conf.Articoli.lunghezza_codice_famiglia)
                numeroFamiglie = int(conf.Articoli.numero_famiglie)
            try:
                codicesel  = select([func.max(Articolo.codice)]).execute().fetchall()
                codice = codeIncrement(codicesel[0][0])
            except:
                pass
            try:
                if codice == "" and hasattr(conf.Articoli,'struttura_codice'):
                    codice = codeIncrement(conf.Articoli.struttura_codice)
            except:
                pass
    return codice

def getArticoliAssociati(connection, id):
    res = connection.execStoredProcedure('ArticoliAssociatiGet',(codice,))
    if len(res) > 0:
        article_list =[]
        for r in res:
            article_list.append(Articolo(connection,r['id']))
        print 'Done. Found '+str(len(res))+' associated articles in databse.'
        return (len(res))

def setArticoliAssociati(connection, article, data):
    if len (data) > 0:
        for article2 in data:
            connection.execStoredProcedure('ArticoliAssociatiSet', (article1.id, article2.id))
        return true
    else:
        return None

def delArticoliAssociati(connection, articolo1, articolo2):
    connection.execStoredProcedure('ArticoliAssociatiDel', (article1.id,article2.id))


fornitura = Table('fornitura', params['metadata'], schema = params['schema'], autoload=True)
articolo = Table('articolo', params['metadata'],schema = params['schema'], autoload=True)
articolotagliacolore = Table('articolo_taglia_colore',params['metadata'],schema = params['schema'],autoload=True)


#j = articolo.outerjoin(articolotagliacolore, onclause=articolotagliacolore.c.id_articolo==articolo.c.id)



std_mapper = mapper(Articolo,articolo,properties={
            "cod_barre":relation(CodiceABarreArticolo,primaryjoin=
                and_(articolo.c.id==CodiceABarreArticolo.id_articolo)),
            "imba":relation(Imballaggio,primaryjoin=
                and_(articolo.c.id_imballaggio==Imballaggio.id), backref="articolo"),
            #"stato_articolo":relation(StatoArticolo, backref="articolo"),
            "ali_iva" : relation(AliquotaIva,primaryjoin=
                and_(articolo.c.id_aliquota_iva==AliquotaIva.id)),
            "den_famiglia":relation(FamigliaArticolo,primaryjoin= articolo.c.id_famiglia_articolo==FamigliaArticolo.id),
            "den_categoria":relation(CategoriaArticolo,primaryjoin=
                and_(articolo.c.id_categoria_articolo==CategoriaArticolo.id)),
            "den_unita":relation(UnitaBase,primaryjoin= (articolo.c.id_unita_base==UnitaBase.id)),
            "image":relation(Immagine,primaryjoin= (articolo.c.id_immagine==Immagine.id)),
            "sa":relation(StatoArticolo,primaryjoin=(articolo.c.id_stato_articolo==StatoArticolo.id)),
            #"articoloTagliaColore":relation(ArticoloTagliaColore),
            "ATC":relation(ArticoloTagliaColore,primaryjoin=(articolo.c.id==ArticoloTagliaColore.id_articolo),uselist=False),
            }, order_by=articolo.c.id)


    #def delete(self):
        #"""
        #Elimina fisicamente o logicamente un articolo
        #"""

        #def isMovimentato(id):
            #""" Verifica se l'articolo e' presente almeno una riga di movimento/documento """
            #queryString = ('SELECT COUNT(*) FROM ' +
                        #Environment.connection._schemaAzienda + '.riga ' +
                        #'WHERE id_articolo = ' + str(id))
            #argList = []
            #self._connection._cursor.execute(queryString, argList)
            #res = Environment.connection._cursor.fetchall()

            #return res[0][0] > 0


        #conn = conn or self._connection

        ##if conn is None:
        ##    conn = Environment.connection

        #if conn is None:
            #self.raiseException(NotImplementedError('Object is read-only '
                                                    #+ '(no connection has '
                                                    #+ 'been associated)'))

        ## se l'articolo e' presente tra le righe di un movimento o documento
        ## si esegue la cancellazione logica, altrimenti fisica

        #conn.startTransaction()

        #try:
            #articolo = ArticoloPromowear(conn, self.id)
            #articoliTagliaColore = self.articoliTagliaColore
            #if self.isArticoloPadre():
                #movimentato = isMovimentato(self.id)
                #for atc in articoliTagliaColore:
                    #movimentato or isMovimentato(atc.id_articolo)

                ## se il padre o almeno una delle varianti e' movimentata si elimina logicamente
                #if movimentato:

                    #articolo.cancellato = True
                    #articolo.persist(conn=conn)

                    #for atc in articoliTagliaColore:
                        #articolo = atc.articolo()
                        #articolo.cancellato = True
                        #articolo.persist(conn=conn)
                #else:
                    #for atc in articoliTagliaColore:
                        #articolo = atc.articolo()
                        #articolo.delete(conn=conn)

                    #Dao.Dao.delete(self, conn=conn)
            #else:
                #movimentato = isMovimentato(self.id)
                ## se la variante e' movimentata si elimina logicamente
                #if movimentato:
                    #articolo.cancellato = True
                    #articolo.persist(conn=conn)
                #else:
                    #Dao.Dao.delete(self, conn=conn)
        #except:
            #conn.abortTransaction()
            #raise

        #conn.commitTransaction()
