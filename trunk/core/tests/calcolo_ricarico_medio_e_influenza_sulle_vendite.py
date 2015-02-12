# -*- coding: utf-8 -*-

#    Copyright (C) 2005-2013 by Promotux
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


import random
import unittest
import os
import sys
from datetime import datetime
path = ".."
if path not in sys.path:
    sys.path.append(path)
#from promogest import preEnv

#preEnv.tipodbforce = "sqlite"
#preEnv.aziendaforce = "urbani"
#from promogest.buildEnv import set_configuration
from promogest import Environment

from sqlalchemy import func
from promogest.dao.Operazione import Operazione
from promogest.dao.TestataMovimento import TestataMovimento
from promogest.dao.TestataDocumento import TestataDocumento
from promogest.dao.RigaMovimento import RigaMovimento
from promogest.dao.RigaDocumento import RigaDocumento
from promogest.dao.Riga import Riga
from promogest.dao.Magazzino import Magazzino
from promogest.dao.Articolo import Articolo
from promogest.dao.Cliente import Cliente
from promogest.dao.CategoriaArticolo import CategoriaArticolo
from promogest.dao.CategoriaCliente import CategoriaCliente
from promogest.dao.UnitaBase import *
from promogest.lib.utils import *
from promogest.lib.relativedelta import relativedelta

class TestCalcoloMedioInfluenzaSulleVendite(unittest.TestCase):

    def setUp(self):
        self.codiceArticolo = "22 A"
        self.annoScorso = 2012
        self.idMagazzino = 1
        self.idArticolo = []

    def test_calcolo_ricarico_medio_e_influenza_sulle_vendite(self):
        idsCliente = []
        idsArticoli = []
        artiID = []
        intervallo = ''
        self.res = []
        # Prelevo i dati dalla ui
        daData = stringToDate("01/01/2000")
        aData = stringToDate("20/02/2015")
        print("HIHIHIHIHIHIHIHIHIHIHI", daData, aData)

        catesCli = CategoriaCliente().select(batchSize=10)
        idcates = [x.id for x in catesCli]
        # print("IDCATESSSS", idcates)
        cateClienteDen = [x.denominazione for x in catesCli]
        idsCliente = []
        for d in idcates:
            clie = Cliente().select(idCategoria=d, batchSize=None)
            # print("CLIEEEEEEEEEEEEEEE", clie)
            for c in clie:
                idsCliente.append(c.id)

        clienti2 = Cliente().select(batchSize=50)
        # print " CLIENTIIIIIIIIIIIIIIIIIIIII", clienti2
        for c in clienti2:
            if c not in idsCliente:
                idsCliente.append(c.id)

        catesArt = CategoriaArticolo().select(batchSize=1)
        idcatesa = [x.id for x in catesArt]
        cateArticoloDen = [x.denominazione for x in catesArt]

        # inizializzo un po' di variabili e dizionari
        quantitaVendutaDict = {}
        quantitaAcquistata = 0
        quantitaAcquistataTotale = 0
        valoreAcquistoDict = {}
        valoreAcquisto = 0
        quantitaVenduta = 0
        quantitaVendutaTotale = 0
        valoreAcquistoTotale = 0
        valoreVenditaDict = {}
        valoreVendita = 0
        valoreVenditaTotale = Decimal("0")
        ricaricomedioDict = {}
        incidenzaAcquistoDict = {}
        incidenzaVenditaDict = {}

        # smisto i dati  secondo categoriaArticolo
        # print " ID CATEGORIE", idcatesa, idsCliente, daData, aData
        for arto in idcatesa:
            # INIZIO livello categoria
            nomeCategoria = CategoriaArticolo().getRecord(id=arto)
            articoli = Articolo().select(idCategoria=arto,
                                         batchSize=None)
            print "ARTICOLI IN QUELLA CATEGORIA", len(articoli)
            for art in articoli:
                # INIZIO livello articolo
                # print "INIZIO AD ELABORARE L'ARTICOLO ", art.id
                quantitaVendutaUNO = 0
                quantitaVendutaTotaleUNO = 0
                quantitaAcquistataUNO = 0
                quantitaAcquistataTotaleUNO = 0
                # tutte le righe movimento per la vendita
                # print(idsCliente,daData, aData,art.id)
                righeArticoloMovimentate = Environment.params["session"] \
                    .query(RigaMovimento) \
                    .filter(TestataMovimento.id_cliente.in_(idsCliente)) \
                    .filter(
                    RigaMovimento.id_testata_movimento == TestataMovimento.id) \
                    .filter(Riga.id == RigaMovimento.id) \
                    .filter(Riga.id_articolo == art.id) \
                    .all()

                # .filter(TestataMovimento.data_movimento.between(daData, aData)) \
                # .filter(Riga.id_magazzino.in_(self.magazzinoId)) \
                print "RIGHE DI MOVIMENTO VENDITA", righeArticoloMovimentate
                for rig in righeArticoloMovimentate:
                    # Quanti ne ho venduti IN TOTALE

                    quantitaVendutaUNO += rig.quantita
                    quantitaVendutaTotaleUNO += rig.quantita
                    quantitaVendutaTotale += rig.quantita

                    quantitaAcquistataUNO = 0
                    rigaArticoloMovimentata = Environment.params["session"] \
                        .query(RigaMovimento) \
                        .filter(TestataMovimento.data_movimento.between(
                        daData + relativedelta(months=-4), aData)) \
                        .filter(TestataMovimento.id_cliente == None) \
                        .filter(TestataMovimento.id_fornitore != None) \
                        .filter(
                        RigaMovimento.id_testata_movimento == TestataMovimento.id) \
                        .filter(Riga.id == RigaMovimento.id) \
                        .filter(Riga.id_articolo == art.id) \
                        .all()
                    # .filter(Riga.id_magazzino.in_(self.magazzinoId)) \
                    if not rigaArticoloMovimentata:
                        forni = leggiFornitura(art.id)
                        valoreAcquisto += (
                            forni["prezzoNetto"] * quantitaVendutaUNO)
                        valoreAcquistoTotale += (
                            forni["prezzoNetto"] * quantitaVendutaUNO)
                        print " PREZZO DA FORNITURA"
                    else:
                        #                        for r in rigaArticoloMovimentata:
                        valoreAcquisto += (rigaArticoloMovimentata[
                                               0].valore_unitario_netto * quantitaVendutaUNO)
                        valoreAcquistoTotale += (rigaArticoloMovimentata[
                                                     0].valore_unitario_netto * quantitaVendutaUNO)

                        quantitaAcquistataUNO += rigaArticoloMovimentata[
                            0].quantita
                        quantitaAcquistataTotaleUNO += rigaArticoloMovimentata[
                            0].quantita
                        #                        quantitaAcquistataTotale += r[0].quantita
                    print " VALORE ACQUISTO", valoreAcquisto

                    ope = leggiOperazione(rig.testata_movimento.operazione)
                    if ope["fonteValore"] == "vendita_iva":
                        # devo scorporare l'iva dal prezzo finale di vendita
                        imponibile = Decimal(str(
                            float(rig.valore_unitario_netto) / (
                                1 + float(rig.percentuale_iva) / 100)))
                    elif ope["fonteValore"] == "vendita_senza_iva":
                        imponibile = Decimal(
                            str(float(rig.valore_unitario_netto)))
                    else:
                        print "TIPO DI FONTE VALORE PER LA VENDITA NN RICONOSCIUTO"
                    valoreVendita += (imponibile * quantitaVendutaUNO)
                    valoreVenditaTotale += (imponibile * quantitaVendutaUNO)



                    # QUESTO LIVELLO ARTICOLO

                    # if quantitaVendutaTotaleUNO <= quantitaAcquistataTotaleUNO:
                    #     print "ARTICOLO %s OK", str(art.id), quantitaVendutaTotaleUNO,quantitaAcquistataTotaleUNO
                    # else:
                    #     print " SERVE TROVARE UN PREZZO ACQUISTO", str(art.id),quantitaVendutaTotaleUNO,quantitaAcquistataTotaleUNO

            # Questo livello categoria
            quantitaVenduta = +quantitaVendutaTotale
            if valoreAcquisto != 0:
                ricaricomedioDict[nomeCategoria.denominazione] = ((
                                                                      valoreVendita - valoreAcquisto ) / valoreAcquisto) * 100
            else:
                ricaricomedioDict[nomeCategoria.denominazione] = 0
            quantitaVendutaDict[
                nomeCategoria.denominazione] = quantitaVenduta or Decimal("0")
            valoreAcquistoDict[
                nomeCategoria.denominazione] = valoreAcquisto or Decimal("0")
            valoreVenditaDict[
                nomeCategoria.denominazione] = valoreVendita or Decimal("0")
            quantitaVenduta = 0
            valoreAcquisto = 0
            valoreVendita = 0
        # Questo livello fuori da tutto
        for k, v in valoreVenditaDict.items():
            if v:
                incidenzaVenditaDict[k] = v * 100 / valoreVenditaTotale
            else:
                incidenzaVenditaDict[k] = 0
        for k, v in valoreAcquistoDict.items():
            if v:
                incidenzaAcquistoDict[k] = v * 100 / valoreAcquistoTotale
            else:
                incidenzaAcquistoDict[k] = 0

        pageData = {
            "file": "statistica_ricarico_medio_e_influenza_vendite.html",
            "categorieArticolo": cateArticoloDen,
            "quantitaVendutaDict": quantitaVendutaDict,
            "valoreAcquistoDict": valoreAcquistoDict,
            "valoreVenditaDict": valoreVenditaDict,
            "ricaricomedioDict": ricaricomedioDict,
            "incidenzaVenditaDict": incidenzaVenditaDict,
            "incidenzaAcquistoDict": incidenzaAcquistoDict,
            "quantitaVendutaTotale": quantitaVendutaTotale,
            "valoreAcquistoTotale": valoreAcquistoTotale,
            "valoreVenditaTotale": valoreVenditaTotale,
            "daData": self.da_data_entry.get_text(),
            "aData": self.a_data_entry.get_text(),
            # "produttore": produt,
            "cateclienti": cateClienteDen,
            # "magazzini": self.magazzinoDen,
            "nomestatistica": self.nome_stat}




suite = unittest.TestLoader().loadTestsFromTestCase(TestCalcoloMedioInfluenzaSulleVendite)
unittest.TextTestRunner(verbosity=2).run(suite)


#                .filter(TestataMovimento.operazione.in_(Environment.solo_acquisto_con_DDT))\
#.filter(Riga.valore_unitario_netto!=0)\