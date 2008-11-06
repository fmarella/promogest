# -*- coding: iso-8859-15 -*-

"""
 Promogest
 Copyright (C) 2005-2008 by Promotux Informatica - http://www.promotux.it/
 Author: Francesco Meloni <francesco@promotux.it>
 Author: Andrea Argiolas <andrea@promotux.it>
 License: GNU GPLv2
"""

import datetime
from sqlalchemy import *
from sqlalchemy.orm import *
from promogest.Environment import *
from Dao import Dao
from Articolo import Articolo
from Magazzino import Magazzino
from DaoUtils import giacenzaSel

class Stoccaggio(Dao):
    """ User class provides to make a Users dao which include more used"""

    def __init__(self, arg=None,isList=False, id=None):
        Dao.__init__(self, entity=self.__class__, isList=isList, id=id)

    def _getTotaliOperazioniMovimento(self):
        self.__dbTotaliOperazioniMovimento = giacenzaSel(year=workingYear, idMagazzino= self.id_magazzino, idArticolo=self.id_articolo)
        self.__totaliOperazioniMovimento = self.__dbTotaliOperazioniMovimento[:]

        return self.__totaliOperazioniMovimento

    def _setTotaliOperazioniMovimento(self, value):
        self.__totaliOperazioniMovimento = value

    totaliOperazioniMovimento = property(_getTotaliOperazioniMovimento,
                                         _setTotaliOperazioniMovimento)

    def _getGiacenza(self):
        totaliOperazioniMovimento = self.totaliOperazioniMovimento
        totGiacenza = 0

        for t in totaliOperazioniMovimento:
            totGiacenza += (t['giacenza'] or 0)
            #totGiacenza += (t[4] or 0)
        return totGiacenza

    giacenza = property(_getGiacenza, )

    def _getValoreGiacenza(self):
        totaliOperazioniMovimento = self.totaliOperazioniMovimento
        totValoreGiacenza = 0

        for t in totaliOperazioniMovimento:
            totValoreGiacenza += (t['valore'] or 0)
            #totValoreGiacenza += (t[5] or 0)
        return totValoreGiacenza

    valoreGiacenza = property(_getValoreGiacenza, )

    def _codiceArticolo(self):
        if self.arti: return self.arti.codice
        else: return ""
    codice_articolo= property(_codiceArticolo)

    def _denoArticolo(self):
        if self.arti: return self.arti.denominazione
        else: return ""
    articolo= property(_denoArticolo)


    def _magazzino(self):
        if self.arti: return self.maga.denominazione
        else: return ""
    magazzino= property(_magazzino)

    def filter_values(self,k,v):
        if k== 'idArticolo':
            dic= {k:stoc.c.id_articolo == v}
        elif k == 'idMagazzino':
            dic = {k:stoc.c.id_magazzino == v}
        return  dic[k]

stoc=Table('stoccaggio',
            params['metadata'],
            schema = params['schema'],
            autoload=True)

std_mapper = mapper(Stoccaggio, stoc, properties={
        "arti" : relation(Articolo,primaryjoin=
                stoc.c.id_articolo==Articolo.id, backref="stoccaggio"),
        "maga" : relation(Magazzino,primaryjoin=
                stoc.c.id_magazzino==Magazzino.id, backref="stoccaggio"),
        }, order_by=stoc.c.id)


"""
BEGIN
        -- Memorizza schema precedente
        schema_prec:= ARRAY_TO_STRING(CURRENT_SCHEMAS(\'t\'),\',\');

        -- Imposta schema corrente
        sql_statement:= \'SET SEARCH_PATH TO \' || _schema;
        EXECUTE sql_statement;

        IF _id_articolo IS NULL THEN
            sql_statement:= \'SELECT RD.id_articolo, O.denominazione, SUM( CASE O.segno WHEN \'\'-\'\' THEN (-RD.quantita * RD.moltiplicatore) WHEN \'\'+\'\' THEN (RD.quantita * RD.moltiplicatore) END ) AS giacenza, SUM(( CASE O.segno WHEN \'\'-\'\' THEN (-RD.quantita * RD.moltiplicatore) WHEN \'\'+\'\' THEN (RD.quantita * moltiplicatore) END ) * RD.valore_unitario_netto) AS valore
                                FROM riga_movimento RM
                                INNER JOIN riga RD ON RM.id = RD.id
                                INNER JOIN testata_movimento TM ON RM.id_testata_movimento = TM.id
                                INNER JOIN promogest.operazione O ON TM.operazione = O.denominazione
                                WHERE DATE_PART(\'\'year\'\', TM.data_movimento) = \' || _anno;
            IF _id_magazzino IS NOT NULL THEN
                sql_statement:= sql_statement || \' AND id_magazzino = \' || _id_magazzino;
            END IF;
            sql_statement:= sql_statement || \' GROUP BY id_articolo, O.denominazione \';
        ELSE
            sql_statement:= \'SELECT CAST(\' || QUOTE_LITERAL(_id_articolo) || \' AS bigint) AS articolo, O.denominazione, SUM( CASE O.segno WHEN \'\'-\'\' THEN (-RD.quantita * RD.moltiplicatore) WHEN \'\'+\'\' THEN (RD.quantita * RD.moltiplicatore) END ) AS giacenza, SUM(( CASE O.segno WHEN \'\'-\'\' THEN (-RD.quantita * RD.moltiplicatore) WHEN \'\'+\'\' THEN (RD.quantita * RD.moltiplicatore) END ) * RD.valore_unitario_netto) AS valore
                                FROM riga_movimento RM
                                INNER JOIN riga RD ON RM.id = RD.id
                                INNER JOIN testata_movimento TM ON RM.id_testata_movimento = TM.id
                                INNER JOIN promogest.operazione O ON TM.operazione = O.denominazione
                                WHERE DATE_PART(\'\'year\'\', TM.data_movimento) = \' || _anno || \' AND id_articolo = \' || _id_articolo;
            IF _id_magazzino IS NOT NULL THEN
                sql_statement:= sql_statement || \' AND id_magazzino = \' || _id_magazzino;
            END IF;
            sql_statement:= sql_statement || \' GROUP BY O.denominazione \';
        END IF;

        sql_cond:=\'\';
        IF _orderby IS NULL THEN
            OrderBy = \' O.denominazione \';
        ELSE
            OrderBy = _orderby;
        END IF;

        IF sql_cond != \'\' THEN
            sql_statement:= sql_statement || \' WHERE \' || sql_cond || \' ORDER BY \' || OrderBy;
        ELSE
            sql_statement:= sql_statement || \' ORDER BY \' || OrderBy;
        END IF;

        FOR v_row IN EXECUTE sql_statement LOOP
            RETURN NEXT v_row;
        END LOOP;

        -- Imposta schema precedente
        sql_statement:= \'SET SEARCH_PATH TO \' || schema_prec;
        EXECUTE sql_statement;

        RETURN;
    END;
"""