#!/usr/local/bin/python
# -*- coding: utf-8 -*-

#    Copyright (C) 2005-2012 by Promotux
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

import sys
import os
path = ".."
if path not in sys.path:
    sys.path.append(path)

from promogest import preEnv

preEnv.tipodbforce = "postgresql"
preEnv.aziendaforce = "urbani"
from promogest.Environment import params
from promogest.dao.TestataDocumento import TestataDocumento
from promogest.dao.Fornitura import Fornitura
from promogest.dao.RigaMovimento import RigaMovimento
from promogest.dao.RigaMovimentoFornitura import RigaMovimentoFornitura
from promogest.dao.NumeroLottoTemp import NumeroLottoTemp
from promogest.dao.ScontoFornitura import ScontoFornitura
from promogest.lib.utils import stringToDateTime, timeit


# Allora: vediamo di gestire il lavoro in TRE step distinti:
# 1) Aggiungiamo le forniture mancanti anche se prive di lotto
# 2) Aggiungiamo in rigamovimentoFornitura un riferimento per ogni articolo comprato
# 3) cerchiamo in lotto temp un riferimento ad una riga mov vendita, ricaviamo l'articolo
#    ed andiamo a piazzare il rif lotto alla fornitura libera, poi mettiamo il rif della riga movimento
#    nella rigaMovforni in modo da chiudere il tutto .....
# la % di correttezza secondo me è di circa l'80%


# PRIMO STEP
#seleziono tutti i documenti di acquisto possibili

testate_ddt = TestataDocumento().select(idOperazione="DDT acquisto", batchSize=None)
testate_fat = TestataDocumento().select(idOperazione="Fattura acquisto", batchSize=None)
docus = testate_ddt+testate_fat
#sommo le due liste

#ciclo nei documenti
num = len(docus)
#docus = []
for tt in docus:
    print "\n\nDOCUMENTI MANCANTI                            ", num - docus.index(tt)
    # Cerco il movimento collegato al documento
    t = tt.TM[0]
    #ciclo nelle righe
    for riga in t.righe:
        #verifico che la riga abbia un id_articolo ed un fornitore (potrebbe non essere necessario)
        if t.id_fornitore and riga.id_articolo:
            fors = Fornitura().select(
                                        idArticolo=riga.id_articolo,
                                        idFornitore=t.id_fornitore,
                                        dataFornitura=t.data_movimento,
                                        batchSize = None)
            daoFornitura = None
            if fors:
                daoFornitura = fors[0]
                v = "vecchia"
            else:
                daoFornitura = Fornitura()
                v = "nuova"

                daoFornitura.id_fornitore = t.id_fornitore
                daoFornitura.id_articolo = riga.id_articolo
                daoFornitura.data_fornitura = t.data_movimento
                if "_RigaMovimento__codiceArticoloFornitore" in riga.__dict__:
                    daoFornitura.codice_articolo_fornitore = riga.__dict__["_RigaMovimento__codiceArticoloFornitore"]
                daoFornitura.prezzo_lordo = riga.valore_unitario_lordo
                daoFornitura.prezzo_netto = riga.valore_unitario_netto
                daoFornitura.percentuale_iva = riga.percentuale_iva
                daoFornitura.applicazione_sconti = riga.applicazione_sconti
                sconti = []
                for s in riga.sconti:
                    daoSconto = ScontoFornitura()
                    daoSconto.id_fornitura = daoFornitura.id
                    daoSconto.valore = s.valore
                    daoSconto.tipo_sconto = s.tipo_sconto
                    sconti.append(daoSconto)

                daoFornitura.sconti = sconti
                print "FORNITURA", daoFornitura, v

                params["session"].add(daoFornitura)
                params["session"].commit()

            rmf = RigaMovimentoFornitura().select(idArticolo=riga.id_articolo, idRigaMovimentoAcquisto=riga.id,idFornitura=daoFornitura.id, batchSize=None)
            if not rmf:
                print " VECCHIA?"
                a = RigaMovimentoFornitura()
                a.id_articolo = riga.id_articolo
                a.id_riga_movimento_acquisto = riga.id
                a.id_fornitura = daoFornitura.id
                params["session"].add(a)
                params["session"].commit()



lt = NumeroLottoTemp().select(batchSize=None)
# id_riga_movimento_vendita_temp, lotto_temp
n = len(lt)
g = 0
for l in lt:
    print "\n\nLOTTI TEMPORANEI MANCANTI",  n-lt.index(l)
    rmf =  RigaMovimentoFornitura().select(idRigaMovimentoVendita=l.id_riga_movimento_vendita_temp)
    print "ESISTE UNA RIGA IN RIGAMOV FORNI", rmf
    if not rmf:
        print " ABBIAMO GIA QUESTI DATI DA METTERE", l.rigamovventemp.id_articolo, l.id_riga_movimento_vendita_temp
        #cerchiamo una fornitura precisa
        daoForn = Fornitura().select(idArticolo=l.rigamovventemp.id_articolo,
                                numeroLotto = l.lotto_temp,
                                batchSize = None)
        if daoForn:
            print "HAI BECCATO IL DATO", daoForn[0]
        if not daoForn:
            daoForn = Fornitura().select(idArticolo=l.rigamovventemp.id_articolo,
                                noLotto =True,
                                batchSize = None)
            print "DAO FORN", daoForn
            if daoForn:
                daoForn[0].numero_lotto = l.lotto_temp
                params["session"].add(daoForn[0])
                #params["session"].commit()

        if daoForn:
            a = RigaMovimentoFornitura()
            a.id_articolo = l.rigamovventemp.id_articolo
            a.id_riga_movimento_vendita = l.id_riga_movimento_vendita_temp
            a.id_fornitura = daoForn[0].id
            print "RIGA MOV FORNI DA AGGIUNGERE", a
            params["session"].add(a)
            #params["session"].commit()
            print " RIMUOVO 1", l
            params["session"].delete(l)
            g += 1
            #params["session"].commit()
            if g == 2000:
                params["session"].commit()
                g = 0
                print "\n\n ------------------------------------- SALVATO E AZZERO -----------------------------------\n\n"
    else:
        print " RIMUOVO 2", l
        params["session"].delete(l)
params["session"].commit()



