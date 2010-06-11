# -*- coding: utf-8 -*-

# Promogest
#
# Copyright (C) 2005-2008 by Promotux Informatica - http://www.promotux.it/
# Author: Francesco Meloni <francesco@promotux.it>

from sqlalchemy import *
from sqlalchemy.orm import *
from promogest.Environment import *



def getArticoloTagliaColoreExt(dao):
    """ Restituisce il Dao ArticoloTagliaColore collegato al Dao Articolo #"""
    #if self.__articoloTagliaColore is not None:
    #self.__articoloTagliaColore = None
    #try:
    dao.__articoloTagliaColore = ArticoloTagliaColore().getRecord(id=self.id)
    return dao.__articoloTagliaColore
    #except:
        #return False

def setArticoloTagliaColore(self, value):
    """ Imposta il Dao ArticoloTagliaColore collegato al Dao Articolo
    """
    self.__articoloTagliaColore = value
articoloTagliaColore = property(getArticoloTagliaColore, setArticoloTagliaColore)

def getArticoliTagliaColore(self, idGruppoTaglia=None, idTaglia=None, idColore=None):
    """ Restituisce una lista di Dao ArticoloTagliaColore figli del Dao Articolo """
    #from promogest.modules.PromoWear.dao.ArticoloTagliaColore import select
    articoli = []
    try:
        articolo_relato = ArticoloTagliaColore().getRecord(id=self.id)
        if not articolo_relato.id_articolo_padre:
            articoli = ArticoloTagliaColore().select(idArticoloPadre=articolo_relato.id_articolo,
                                                        idGruppoTaglia=idGruppoTaglia,
                                                        idTaglia=idTaglia,
                                                        idColore=idColore,
                                                        offset=None,
                                                        batchSize=None)
        else:
            articoli = ArticoloTagliaColore().select(idArticoloPadre=articolo_relato.id_articolo_padre,
                                                        idGruppoTaglia=idGruppoTaglia,
                                                        idTaglia=idTaglia,
                                                        idColore=idColore,
                                                        offset=None,
                                                        batchSize=None)
    except:
        print "FOR DEBUG ONLY getArticoliTagliaColore FAILED"
    return articoli
articoliTagliaColore = property(getArticoliTagliaColore)


def getArticoliVarianti(self):
    """ Restituisce una lista di Dao Articolo Varianti """
    articoli = []
    for art in self.getArticoliTagliaColore():
        articoli.append(Articolo().getRecord(id=art.id_articolo))
    return articoli
articoliVarianti = property(getArticoliVarianti)


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

def _denominazione_colore(self):
    """ esempio di funzione  unita alla property """
    if self.ATC :
        try:
            return self.ATC[0].denominazione_colore
        except:
            return self.ATC.denominazione_colore
denominazione_colore = property(_denominazione_colore)

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