--
-- Copyright (C) 2005 by Promotux Informatica - http://www.promotux.it/
-- Author: Andrea Argiolas <andrea@promotux.it>
--
-- This program is free software; you can redistribute it and/or
-- modify it under the terms of the GNU General Public License
-- as published by the Free Software Foundation; either version 2
-- of the License, or (at your option) any later version.
--
-- This program is distributed in the hope that it will be useful,
-- but WITHOUT ANY WARRANTY; without even the implied warranty of
-- MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
-- GNU General Public License for more details.
--
-- You should have received a copy of the GNU General Public License
-- along with this program; if not, write to the Free Software
-- Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.

/*

Inventario  - Stored procedure applicativa

*/


DROP FUNCTION promogest.InventarioSet(varchar, bigint, bigint, integer, bigint, bigint, decimal(16,4), decimal(16,4), date);
CREATE OR REPLACE FUNCTION promogest.InventarioSet(varchar, bigint, bigint, integer, bigint, bigint, decimal(16,4), decimal(16,4), date) RETURNS promogest.resultid AS '
    DECLARE
        -- Parametri contesto
        _schema                         ALIAS FOR $1;
        _idutente                       ALIAS FOR $2;
        
        -- Parametri tabella
        _id                             ALIAS FOR $3;
        _anno                           ALIAS FOR $4;
        _id_magazzino                   ALIAS FOR $5;
        _id_articolo                    ALIAS FOR $6;
        _quantita                       ALIAS FOR $7;
        _valore_unitario                ALIAS FOR $8;
        _data_aggiornamento             ALIAS FOR $9;

        schema_prec                     varchar(2000);
        sql_command                     varchar(2000);
        _ret                            promogest.resultid;
        _rec                            record;
    BEGIN
        -- Memorizza schema precedente
        schema_prec:= ARRAY_TO_STRING(CURRENT_SCHEMAS(\'t\'),\',\');
    
        -- Imposta schema corrente
        sql_command:= \'SET SEARCH_PATH TO \' || _schema;
        EXECUTE sql_command;
        
        SELECT INTO _ret * FROM promogest.InventarioInsUpd(_schema, _idutente, _id, _anno, _id_magazzino, _id_articolo, _quantita, _valore_unitario, _data_aggiornamento);
        sql_command:= \'SET SEARCH_PATH TO \' || schema_prec;
        EXECUTE sql_command;
        
        RETURN _ret;
    END;
' LANGUAGE plpgsql;


DROP FUNCTION promogest.InventarioDel(varchar, bigint, bigint);
CREATE OR REPLACE FUNCTION promogest.InventarioDel(varchar, bigint, bigint) RETURNS promogest.resultid AS '
    DECLARE
        -- Parametri contesto
        _schema                 ALIAS FOR $1;
        _idutente               ALIAS FOR $2;
        
        -- Parametri tabella
        _id                     ALIAS FOR $3;
        
        schema_prec             varchar(2000);
        sql_command             varchar(2000);
        _ret                    promogest.resultid;
        _rec                    record;
    BEGIN
        -- Memorizza schema precedente
        schema_prec:= ARRAY_TO_STRING(CURRENT_SCHEMAS(\'t\'),\',\');
    
        -- Imposta schema corrente
        sql_command:= \'SET SEARCH_PATH TO \' || _schema;
        EXECUTE sql_command;
        
        SELECT INTO _ret * FROM promogest.ObjectDel(_schema, _idutente, \'inventario\', _id, \'id\');
        
        -- Imposta schema precedente
        sql_command:= \'SET SEARCH_PATH TO \' || schema_prec;
        EXECUTE sql_command;
        
        RETURN _ret;
    END;
' LANGUAGE plpgsql;


DROP FUNCTION promogest.InventarioGet(varchar, bigint, bigint);
DROP FUNCTION promogest.InventarioSel(varchar, bigint, varchar, integer, bigint, bigint, date, date, bigint, bigint);
DROP FUNCTION promogest.InventarioSelCount(varchar, bigint, varchar, integer, bigint, bigint, date, date, bigint, bigint);


DROP TYPE promogest.inventario_type;
DROP TYPE promogest.inventario_sel_type;
DROP TYPE promogest.inventario_sel_count_type;

CREATE TYPE promogest.inventario_type AS (
     id                                 bigint
    ,anno                               integer
    ,id_magazzino                       bigint
    ,id_articolo                        bigint
    ,quantita                           decimal(16,4)
    ,valore_unitario                    decimal(16,4)
    ,data_aggiornamento                 date
);

CREATE TYPE promogest.inventario_sel_type AS (
     id                                 bigint
    ,anno                               integer
    ,id_magazzino                       bigint
    ,id_articolo                        bigint
    ,quantita                           decimal(16,4)
    ,valore_unitario                    decimal(16,4)
    ,data_aggiornamento                 date
    ,magazzino                          varchar
    ,codice_articolo                    varchar
    ,articolo                           varchar
    ,produttore                         varchar
    ,codice_a_barre                     varchar
    ,codice_articolo_fornitore          varchar
    ,id_aliquota_iva                    bigint
    ,denominazione_breve_aliquota_iva   varchar
    ,denominazione_aliquota_iva         varchar
    ,percentuale_aliquota_iva           decimal
    ,id_famiglia_articolo               bigint
    ,denominazione_breve_famiglia       varchar
    ,denominazione_famiglia             varchar
    ,id_categoria_articolo              bigint
    ,denominazione_breve_categoria      varchar
    ,denominazione_categoria            varchar
    ,id_unita_base                      bigint
    ,denominazione_breve_unita_base     varchar
    ,denominazione_unita_base           varchar
    ,id_articolo_padre                  bigint
    ,id_gruppo_taglia                   bigint
    ,denominazione_breve_gruppo_taglia  varchar
    ,denominazione_gruppo_taglia        varchar
    ,id_taglia                          bigint
    ,denominazione_breve_taglia         varchar
    ,denominazione_taglia               varchar
    ,id_colore                          bigint
    ,denominazione_breve_colore         varchar
    ,denominazione_colore               varchar
    ,id_anno                            bigint
    ,anno_abbigliamento                 varchar
    ,id_stagione                        bigint
    ,stagione_abbigliamento             varchar
    ,id_genere                          bigint
    ,genere_abbigliamento               varchar
);

CREATE TYPE promogest.inventario_sel_count_type AS (
    count       bigint
);


CREATE OR REPLACE FUNCTION promogest.InventarioGet(varchar, bigint, bigint) RETURNS SETOF promogest.inventario_type AS '
    DECLARE
        -- Parametri contesto
        _schema                 ALIAS FOR $1;
        _idutente               ALIAS FOR $2;
        
        -- Parametri tabella
        _id                     ALIAS FOR $3;
        
        schema_prec             varchar(2000);
        sql_command             varchar(2000);
        v_row                   record;
    BEGIN
        -- Memorizza schema precedente
        schema_prec:= ARRAY_TO_STRING(CURRENT_SCHEMAS(\'t\'),\',\');
    
        -- Imposta schema corrente
        sql_command:= \'SET SEARCH_PATH TO \' || _schema;
        EXECUTE sql_command;
        
        FOR v_row IN SELECT * FROM inventario WHERE id = _id LOOP
            RETURN NEXT v_row;
        END LOOP;
                                    
        -- Imposta schema precedente
        sql_command:= \'SET SEARCH_PATH TO \' || schema_prec;
        EXECUTE sql_command;

        RETURN;
    END;
' LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION promogest.InventarioSel(varchar, bigint, varchar, integer, bigint, bigint, date, date, bigint, bigint) RETURNS SETOF promogest.inventario_sel_type AS '
    DECLARE
        -- Parametri contesto
        _schema                         ALIAS FOR $1;
        _idutente                       ALIAS FOR $2;
        
        -- Parametri procedura
        _orderby                        ALIAS FOR $3;
        _anno                           ALIAS FOR $4;
        _id_magazzino                   ALIAS FOR $5;
        _id_articolo                    ALIAS FOR $6;
        _da_data_aggiornamento          ALIAS FOR $7;
        _a_data_aggiornamento           ALIAS FOR $8;
        _offset                         ALIAS FOR $9;
        _count                          ALIAS FOR $10;
        
        schema_prec                     varchar(2000);
        sql_statement                   varchar(2000);
        sql_cond                        varchar(2000);
        limitstring                     varchar(500);
        _add                            varchar(500);
        OrderBy                         varchar(200);
        v_row                           record;
        _tablename                      varchar;
    BEGIN
        -- Memorizza schema precedente
        schema_prec:= ARRAY_TO_STRING(CURRENT_SCHEMAS(\'t\'),\',\');
    
        -- Imposta schema corrente
        sql_statement:= \'SET SEARCH_PATH TO \' || _schema;
        EXECUTE sql_statement;

        sql_statement:= \'SELECT I.id, I.anno, I.id_magazzino, I.id_articolo, I.quantita, I.valore_unitario, I.data_aggiornamento, I.magazzino, I.codice_articolo, I.articolo, I.produttore, I.codice_a_barre, I.codice_articolo_fornitore, I.id_aliquota_iva, I.denominazione_breve_aliquota_iva, I.denominazione_aliquota_iva, I.percentuale_aliquota_iva, I.id_famiglia_articolo, I.denominazione_breve_famiglia, I.denominazione_famiglia, I.id_categoria_articolo, I.denominazione_breve_categoria, I.denominazione_categoria, I.id_unita_base, I.denominazione_breve_unita_base, I.denominazione_unita_base,I.id_articolo_padre, I.id_gruppo_taglia, I.denominazione_breve_gruppo_taglia, I.denominazione_gruppo_taglia, I.id_taglia, I.denominazione_breve_taglia, I.denominazione_taglia, I.id_colore, I.denominazione_breve_colore, I.denominazione_colore, I.id_anno, I.anno_abbigliamento, I.id_stagione, I.stagione_abbigliamento, I.id_genere, I.genere_abbigliamento FROM v_inventario_completa I \';
        sql_cond:=\'\';

        IF _orderby IS NULL THEN
            OrderBy = \'I.magazzino, I.codice_articolo \';
        ELSE
            OrderBy = _orderby;
        END IF;

        IF _anno IS NOT NULL THEN
            _add:= \'I.anno = \' || _anno;
            sql_cond:= promogest.sqlAddCondition(sql_cond,_add);
        END IF;

        IF _id_magazzino IS NOT NULL THEN
            _add:= \'I.id_magazzino = \' || _id_magazzino;
            sql_cond:= promogest.sqlAddCondition(sql_cond,_add);
        END IF;

        IF _id_articolo IS NOT NULL THEN
            _add:= \'I.id_articolo = \' || _id_articolo;
            sql_cond:= promogest.sqlAddCondition(sql_cond,_add);
        ELSE
            SELECT INTO _tablename * FROM promogest.ArticoloFilteredExists(_schema, _idutente);
            IF _tablename <> \'\' THEN
                sql_statement:= sql_statement || \' INNER JOIN \' || _tablename || \' A ON I.id_articolo = A.id\';
            END IF;
        END IF;

        IF _da_data_aggiornamento IS NOT NULL THEN
            _add:= \'I.data_aggiornamento >= \' || QUOTE_LITERAL(_da_data_aggiornamento);
            sql_cond:= promogest.sqlAddCondition(sql_cond,_add);
        END IF;

        IF _a_data_aggiornamento IS NOT NULL THEN
            _add:= \'I.data_aggiornamento <= \' || QUOTE_LITERAL(_a_data_aggiornamento);
            sql_cond:= promogest.sqlAddCondition(sql_cond,_add);
        END IF;
        
        IF _offset IS NULL THEN
            limitstring:= \'\';
        ELSE
            limitstring:= \' LIMIT \' || _count || \' OFFSET  \' || _offset;
        END IF;
        
        IF sql_cond != \'\' THEN
            sql_statement:= sql_statement || \' WHERE \' || sql_cond || \'ORDER BY \' || OrderBy || limitstring;
        ELSE
            sql_statement:= sql_statement || \' ORDER BY \' || OrderBy || limitstring;
        END IF;

        FOR v_row IN EXECUTE sql_statement LOOP
            RETURN NEXT v_row;
        END LOOP;

        -- Imposta schema precedente
        sql_statement:= \'SET SEARCH_PATH TO \' || schema_prec;
        EXECUTE sql_statement;

        RETURN;
    END;
' LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION promogest.InventarioSelCount(varchar, bigint, varchar, integer, bigint, bigint, date, date, bigint, bigint) RETURNS SETOF promogest.inventario_sel_count_type AS '
    DECLARE
        -- Parametri contesto
        _schema                         ALIAS FOR $1;
        _idutente                       ALIAS FOR $2;
        
        -- Parametri procedura
        _orderby                        ALIAS FOR $3;
        _anno                           ALIAS FOR $4;
        _id_magazzino                   ALIAS FOR $5;
        _id_articolo                    ALIAS FOR $6;
        _da_data_aggiornamento          ALIAS FOR $7;
        _a_data_aggiornamento           ALIAS FOR $8;
        _offset                         ALIAS FOR $9;
        _count                          ALIAS FOR $10;
        
        schema_prec                     varchar(2000);
        sql_statement                   varchar(2000);
        sql_cond                        varchar(2000);
        limitstring                     varchar(500);
        _add                            varchar(500);
        OrderBy                         varchar(200);
        v_row                           record;
        _tablename                      varchar;
    BEGIN
        -- Memorizza schema precedente
        schema_prec:= ARRAY_TO_STRING(CURRENT_SCHEMAS(\'t\'),\',\');
    
        -- Imposta schema corrente
        sql_statement:= \'SET SEARCH_PATH TO \' || _schema;
        EXECUTE sql_statement;

        sql_statement:= \'SELECT COUNT(I.id) FROM inventario I \';
        sql_cond:=\'\';

        IF _anno IS NOT NULL THEN
            _add:= \'I.anno = \' || _anno;
            sql_cond:= promogest.sqlAddCondition(sql_cond,_add);
        END IF;

        IF _id_magazzino IS NOT NULL THEN
            _add:= \'I.id_magazzino = \' || _id_magazzino;
            sql_cond:= promogest.sqlAddCondition(sql_cond,_add);
        END IF;

        IF _id_articolo IS NOT NULL THEN
            _add:= \'I.id_articolo = \' || _id_articolo;
            sql_cond:= promogest.sqlAddCondition(sql_cond,_add);
        ELSE
            SELECT INTO _tablename * FROM promogest.ArticoloFilteredExists(_schema, _idutente);
            IF _tablename <> \'\' THEN
                sql_statement:= sql_statement || \' INNER JOIN \' || _tablename || \' A ON I.id_articolo = A.id\';
            END IF;
        END IF;
        
        IF _da_data_aggiornamento IS NOT NULL THEN
            _add:= \'I.data_aggiornamento >= \' || QUOTE_LITERAL(_da_data_aggiornamento);
            sql_cond:= promogest.sqlAddCondition(sql_cond,_add);
        END IF;

        IF _a_data_aggiornamento IS NOT NULL THEN
            _add:= \'I.data_aggiornamento <= \' || QUOTE_LITERAL(_a_data_aggiornamento);
            sql_cond:= promogest.sqlAddCondition(sql_cond,_add);
        END IF;
        
        IF _offset IS NULL THEN
            limitstring:= \'\';
        ELSE
            limitstring:= \' LIMIT \' || _count || \' OFFSET  \' || _offset;
        END IF;
        
        IF sql_cond != \'\' THEN
            sql_statement:= sql_statement || \' WHERE \' || sql_cond;
        END IF;

        FOR v_row IN EXECUTE sql_statement LOOP
            RETURN NEXT v_row;
        END LOOP;

        -- Imposta schema precedente
        sql_statement:= \'SET SEARCH_PATH TO \' || schema_prec;
        EXECUTE sql_statement;

        RETURN;
    END;
' LANGUAGE plpgsql;


DROP FUNCTION promogest.InventarioFill(varchar, bigint, integer);
CREATE OR REPLACE FUNCTION promogest.InventarioFill(varchar, bigint, integer) RETURNS VOID AS '
    DECLARE
        -- Parametri contesto
        _schema                         ALIAS FOR $1;
        _idutente                       ALIAS FOR $2;
        
        -- Parametri tabella
        _anno                           ALIAS FOR $3;
        
        schema_prec                     varchar(2000);
        sql_statement                   varchar(2000);
        _tablename                      varchar;
        _count                          bigint;
        _anno_prec                      integer;
    BEGIN
        -- Memorizza schema precedente
        schema_prec:= ARRAY_TO_STRING(CURRENT_SCHEMAS(\'t\'),\',\');

        -- Imposta schema corrente
        sql_statement:= \'SET SEARCH_PATH TO \' || _schema;
        EXECUTE sql_statement;

        SELECT INTO _anno_prec (_anno - 1);
        sql_statement:= \'INSERT INTO inventario (anno, id_magazzino, id_articolo, quantita, valore_unitario, data_aggiornamento) 
                            (SELECT \' || _anno || \', M.id, A.id, G.giacenza, NULL, CURRENT_TIMESTAMP 
                             FROM magazzino M CROSS JOIN articolo A 
                             LEFT OUTER JOIN (SELECT R.id_magazzino, R.id_articolo, SUM( CASE O.segno WHEN \'\'-\'\' THEN (-R.quantita * R.moltiplicatore) WHEN \'\'+\'\' THEN (R.quantita * R.moltiplicatore) END ) AS giacenza 
                                              FROM riga_movimento RM 
                                              INNER JOIN riga R ON RM.id = R.id 
                                              INNER JOIN testata_movimento TM ON RM.id_testata_movimento = TM.id 
                                              INNER JOIN promogest.operazione O ON TM.operazione = O.denominazione  
                                              WHERE DATE_PART(\'\'year\'\', TM.data_movimento) = \' || _anno_prec || \' 
                                              GROUP BY id_magazzino, id_articolo) G ON M.id = G.id_magazzino AND A.id = G.id_articolo 
                             WHERE A.cancellato <> True)\';
        EXECUTE sql_statement;

        -- Imposta schema precedente
        sql_statement:= \'SET SEARCH_PATH TO \' || schema_prec;
        EXECUTE sql_statement;
    END;
' LANGUAGE plpgsql;


DROP FUNCTION promogest.InventarioUpd(varchar, bigint, integer);
CREATE OR REPLACE FUNCTION promogest.InventarioUpd(varchar, bigint, integer) RETURNS VOID AS '
    DECLARE
        -- Parametri contesto
        _schema                         ALIAS FOR $1;
        _idutente                       ALIAS FOR $2;
        
        -- Parametri tabella
        _anno                           ALIAS FOR $3;
        
        schema_prec                     varchar(2000);
        sql_statement                   varchar(2000);
        _tablename                      varchar;
        _count                          bigint;
    BEGIN
        -- Memorizza schema precedente
        schema_prec:= ARRAY_TO_STRING(CURRENT_SCHEMAS(\'t\'),\',\');

        -- Imposta schema corrente
        sql_statement:= \'SET SEARCH_PATH TO \' || _schema;
        EXECUTE sql_statement;

        sql_statement:= \'INSERT INTO inventario (anno, id_magazzino, id_articolo, quantita, valore_unitario, data_aggiornamento) 
                            (SELECT \' || _anno || \', M.id, A.id, NULL, NULL, NULL 
                             FROM magazzino M CROSS JOIN articolo A 
                             WHERE (M.id, A.id) NOT IN (SELECT I.id_magazzino, I.id_articolo FROM INVENTARIO I WHERE I.anno = \' || _anno || \')
                                   AND A.cancellato <> True)\';
        EXECUTE sql_statement;

        -- Imposta schema precedente
        sql_statement:= \'SET SEARCH_PATH TO \' || schema_prec;
        EXECUTE sql_statement;
    END;
' LANGUAGE plpgsql;


DROP FUNCTION promogest.InventarioPrezzoAcquistoUltimoUpd(varchar, bigint, integer);
DROP FUNCTION promogest.InventarioPrezzoAcquistoUltimoUpd(varchar, bigint, integer, bigint);
CREATE OR REPLACE FUNCTION promogest.InventarioPrezzoAcquistoUltimoUpd(varchar, bigint, integer, bigint) RETURNS void AS '
    DECLARE
        -- Parametri contesto
        _schema                         ALIAS FOR $1;
        _idutente                       ALIAS FOR $2;

        _anno                           ALIAS FOR $3;
        _id_magazzino                   ALIAS FOR $4;

        schema_prec                     varchar(2000);
        sql_statement                   varchar(2000);
        _anno_prec                      integer;
    BEGIN
        -- Memorizza schema precedente
        schema_prec:= ARRAY_TO_STRING(CURRENT_SCHEMAS(\'t\'),\',\');

        -- Imposta schema corrente
        sql_statement:= \'SET SEARCH_PATH TO \' || _schema;
        EXECUTE sql_statement;

        SELECT INTO _anno_prec (_anno - 1);

        BEGIN
            sql_statement:= \'DROP TABLE valorizzazione_tmp;\';
            EXECUTE sql_statement;
        EXCEPTION
            WHEN undefined_table THEN
                RAISE NOTICE \'Error dropping tmp table\';
        END;

        sql_statement:= \'CREATE TEMPORARY TABLE valorizzazione_tmp AS 
                                (SELECT R.id_magazzino, R.id_articolo, 
                                 MAX(R.valore_unitario_netto) AS prezzo, 
                                 MAX(TM.data_movimento) AS data
                                 FROM riga_movimento RM INNER JOIN riga R ON RM.id = R.id 
                                 INNER JOIN testata_movimento TM ON RM.id_testata_movimento = TM.id 
                                 INNER JOIN promogest.operazione O ON TM.operazione = O.denominazione 
                                 WHERE (R.valore_unitario_netto <> 0 AND O.segno = \'\'+\'\' AND
                                        DATE_PART(\'\'year\'\', TM.data_movimento) = \' || _anno_prec || \' AND 
                                        R.id_magazzino = \' || _id_magazzino || \') 
                                 GROUP BY R.id_magazzino, R.id_articolo) \';
        EXECUTE sql_statement;

        sql_statement:= \'UPDATE inventario SET valore_unitario = (SELECT prezzo FROM valorizzazione_tmp T WHERE inventario.id_magazzino = T.id_magazzino AND inventario.id_articolo = T.id_articolo) WHERE anno = \' || _anno || \' AND (valore_unitario IS NULL OR valore_unitario = 0)\';
        EXECUTE sql_statement;

        -- Imposta schema precedente
        sql_statement:= \'SET SEARCH_PATH TO \' || schema_prec;
        EXECUTE sql_statement;
    END;
' LANGUAGE plpgsql;


DROP FUNCTION promogest.InventarioPrezzoVenditaUltimoUpd(varchar, bigint, integer);
DROP FUNCTION promogest.InventarioPrezzoVenditaUltimoUpd(varchar, bigint, integer, bigint);
CREATE OR REPLACE FUNCTION promogest.InventarioPrezzoVenditaUltimoUpd(varchar, bigint, integer, bigint) RETURNS void AS '
    DECLARE
        -- Parametri contesto
        _schema                         ALIAS FOR $1;
        _idutente                       ALIAS FOR $2;

        _anno                           ALIAS FOR $3;
        _id_magazzino                   ALIAS FOR $4;

        schema_prec                     varchar(2000);
        sql_statement                   varchar(2000);
        _anno_prec                      integer;
    BEGIN
        -- Memorizza schema precedente
        schema_prec:= ARRAY_TO_STRING(CURRENT_SCHEMAS(\'t\'),\',\');

        -- Imposta schema corrente
        sql_statement:= \'SET SEARCH_PATH TO \' || _schema;
        EXECUTE sql_statement;

        SELECT INTO _anno_prec (_anno - 1);

        BEGIN
            sql_statement:= \'DROP TABLE valorizzazione_tmp;\';
            EXECUTE sql_statement;
        EXCEPTION
            WHEN undefined_table THEN
                RAISE NOTICE \'Error dropping tmp table\';
        END;

        sql_statement:= \'CREATE TEMPORARY TABLE valorizzazione_tmp AS 
                                (SELECT R.id_magazzino, R.id_articolo, 
                                 MAX(R.valore_unitario_netto) AS prezzo, 
                                 MAX(TM.data_movimento) AS data
                                 FROM riga_movimento RM INNER JOIN riga R ON RM.id = R.id 
                                 INNER JOIN testata_movimento TM ON RM.id_testata_movimento = TM.id 
                                 INNER JOIN promogest.operazione O ON TM.operazione = O.denominazione 
                                 WHERE (R.valore_unitario_netto <> 0 AND O.segno = \'\'-\'\' AND
                                        DATE_PART(\'\'year\'\', TM.data_movimento) = \' || _anno_prec || \' AND 
                                        R.id_magazzino = \' || _id_magazzino || \') 
                                 GROUP BY R.id_magazzino, R.id_articolo) \';
        EXECUTE sql_statement;

        sql_statement:= \'UPDATE inventario SET valore_unitario = (SELECT prezzo FROM valorizzazione_tmp T WHERE inventario.id_magazzino = T.id_magazzino AND inventario.id_articolo = T.id_articolo) WHERE anno = \' || _anno || \' AND (valore_unitario IS NULL OR valore_unitario = 0)\';
        EXECUTE sql_statement;

        -- Imposta schema precedente
        sql_statement:= \'SET SEARCH_PATH TO \' || schema_prec;
        EXECUTE sql_statement;
    END;
' LANGUAGE plpgsql;


DROP FUNCTION promogest.InventarioPrezzoAcquistoMedioUpd(varchar, bigint, integer);
DROP FUNCTION promogest.InventarioPrezzoAcquistoMedioUpd(varchar, bigint, integer, bigint);
CREATE OR REPLACE FUNCTION promogest.InventarioPrezzoAcquistoMedioUpd(varchar, bigint, integer, bigint) RETURNS void AS '
    DECLARE
        -- Parametri contesto
        _schema                         ALIAS FOR $1;
        _idutente                       ALIAS FOR $2;

        _anno                           ALIAS FOR $3;
        _id_magazzino                   ALIAS FOR $4;

        schema_prec                     varchar(2000);
        sql_statement                   varchar(2000);
        _anno_prec                      integer;
    BEGIN
        -- Memorizza schema precedente
        schema_prec:= ARRAY_TO_STRING(CURRENT_SCHEMAS(\'t\'),\',\');

        -- Imposta schema corrente
        sql_statement:= \'SET SEARCH_PATH TO \' || _schema;
        EXECUTE sql_statement;

        SELECT INTO _anno_prec (_anno - 1);

        BEGIN
            sql_statement:= \'DROP TABLE valorizzazione_tmp;\';
            EXECUTE sql_statement;
        EXCEPTION
            WHEN undefined_table THEN
                RAISE NOTICE \'Error dropping tmp table\';
        END;

        sql_statement:= \'CREATE TEMPORARY TABLE valorizzazione_tmp AS 
                                (SELECT R.id_magazzino, R.id_articolo, 
                                 AVG(R.valore_unitario_netto) AS prezzo
                                 FROM riga_movimento RM INNER JOIN riga R ON RM.id = R.id 
                                 INNER JOIN testata_movimento TM ON RM.id_testata_movimento = TM.id 
                                 INNER JOIN promogest.operazione O ON TM.operazione = O.denominazione 
                                 WHERE (R.valore_unitario_netto <> 0 AND O.segno = \'\'+\'\' AND
                                        DATE_PART(\'\'year\'\', TM.data_movimento) = \' || _anno_prec || \' AND 
                                        R.id_magazzino = \' || _id_magazzino || \') 
                                 GROUP BY R.id_magazzino, R.id_articolo) \';
        EXECUTE sql_statement;

        sql_statement:= \'UPDATE inventario SET valore_unitario = (SELECT prezzo FROM valorizzazione_tmp T WHERE inventario.id_magazzino = T.id_magazzino AND inventario.id_articolo = T.id_articolo) WHERE anno = \' || _anno || \' AND (valore_unitario IS NULL OR valore_unitario = 0)\';
        EXECUTE sql_statement;

        -- Imposta schema precedente
        sql_statement:= \'SET SEARCH_PATH TO \' || schema_prec;
        EXECUTE sql_statement;
    END;
' LANGUAGE plpgsql;


DROP FUNCTION promogest.InventarioPrezzoVenditaMedioUpd(varchar, bigint, integer);
DROP FUNCTION promogest.InventarioPrezzoVenditaMedioUpd(varchar, bigint, integer, bigint);
CREATE OR REPLACE FUNCTION promogest.InventarioPrezzoVenditaMedioUpd(varchar, bigint, integer, bigint) RETURNS void AS '
    DECLARE
        -- Parametri contesto
        _schema                         ALIAS FOR $1;
        _idutente                       ALIAS FOR $2;

        _anno                           ALIAS FOR $3;
        _id_magazzino                   ALIAS FOR $4;

        schema_prec                     varchar(2000);
        sql_statement                   varchar(2000);
        _anno_prec                      integer;
    BEGIN
        -- Memorizza schema precedente
        schema_prec:= ARRAY_TO_STRING(CURRENT_SCHEMAS(\'t\'),\',\');

        -- Imposta schema corrente
        sql_statement:= \'SET SEARCH_PATH TO \' || _schema;
        EXECUTE sql_statement;

        SELECT INTO _anno_prec (_anno - 1);

        BEGIN
            sql_statement:= \'DROP TABLE valorizzazione_tmp;\';
            EXECUTE sql_statement;
        EXCEPTION
            WHEN undefined_table THEN
                RAISE NOTICE \'Error dropping tmp table\';
        END;

        sql_statement:= \'CREATE TEMPORARY TABLE valorizzazione_tmp AS 
                                (SELECT R.id_magazzino, R.id_articolo, 
                                 AVG(R.valore_unitario_netto) AS prezzo
                                 FROM riga_movimento RM INNER JOIN riga R ON RM.id = R.id 
                                 INNER JOIN testata_movimento TM ON RM.id_testata_movimento = TM.id 
                                 INNER JOIN promogest.operazione O ON TM.operazione = O.denominazione 
                                 WHERE (R.valore_unitario_netto <> 0 AND O.segno = \'\'-\'\' AND
                                        DATE_PART(\'\'year\'\', TM.data_movimento) = \' || _anno_prec || \' AND 
                                        R.id_magazzino = \' || _id_magazzino || \') 
                                 GROUP BY R.id_magazzino, R.id_articolo) \';
        EXECUTE sql_statement;

        sql_statement:= \'UPDATE inventario SET valore_unitario = (SELECT prezzo FROM valorizzazione_tmp T WHERE inventario.id_magazzino = T.id_magazzino AND inventario.id_articolo = T.id_articolo) WHERE anno = \' || _anno || \' AND (valore_unitario IS NULL OR valore_unitario = 0)\';
        EXECUTE sql_statement;

        -- Imposta schema precedente
        sql_statement:= \'SET SEARCH_PATH TO \' || schema_prec;
        EXECUTE sql_statement;
    END;
' LANGUAGE plpgsql;
