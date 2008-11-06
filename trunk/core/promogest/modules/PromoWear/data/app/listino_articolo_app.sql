--
-- Copyright (C) 2005 by Promotux Informatica - http://www.promotux.it/
-- Author: Alessandro Scano <alessandro@promotux.it>
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

ListinoArticolo  - Stored procedure applicativa

*/

DROP FUNCTION promogest.ListinoArticoloSet(varchar, bigint, bigint, bigint, decimal(16,4), decimal(16,4), decimal(16,4), timestamp, boolean) CASCADE;
CREATE OR REPLACE FUNCTION promogest.ListinoArticoloSet(varchar, bigint, bigint, bigint, decimal(16,4), decimal(16,4), decimal(16,4), timestamp, boolean) RETURNS promogest.resultid AS '
    DECLARE
        -- Parametri contesto
        _schema                     ALIAS FOR $1;
        _idutente                   ALIAS FOR $2;

        -- Parametri tabella
        _id_listino                 ALIAS FOR $3;
        _id_articolo                ALIAS FOR $4;
        _prezzo_dettaglio           ALIAS FOR $5;
        _prezzo_ingrosso            ALIAS FOR $6;
        _ultimo_costo               ALIAS FOR $7;
        _data_listino_articolo      ALIAS FOR $8;
        _listino_attuale            ALIAS FOR $9;

        schema_prec                 varchar(2000);
        sql_command                 varchar(2000);
        _ret                        promogest.resultid;
        _rec                        record;
    BEGIN
        -- Memorizza schema precedente
        schema_prec:= ARRAY_TO_STRING(CURRENT_SCHEMAS(\'t\'),\',\');

        -- Imposta schema corrente
        sql_command:= \'SET SEARCH_PATH TO \' || _schema;
        EXECUTE sql_command;

        SELECT INTO _ret * FROM promogest.ListinoArticoloInsUpd(_schema, _idutente, _id_listino, _id_articolo, _prezzo_dettaglio, _prezzo_ingrosso, _ultimo_costo, _listino_attuale);

        -- Imposta schema precedente
        sql_command:= \'SET SEARCH_PATH TO \' || schema_prec;
        EXECUTE sql_command;

        RETURN _ret;
    END;
' LANGUAGE plpgsql;


DROP FUNCTION promogest.ListinoArticoloDel(varchar, bigint, bigint, bigint) CASCADE;
CREATE OR REPLACE FUNCTION promogest.ListinoArticoloDel(varchar, bigint, bigint, bigint) RETURNS promogest.resultid AS '
    DECLARE
        -- Parametri contesto
        _schema                 ALIAS FOR $1;
        _idutente               ALIAS FOR $2;

        -- Parametri tabella
        _id_listino             ALIAS FOR $3;
        _id_articolo            ALIAS FOR $4;

        schema_prec             varchar(2000);
        sql_command             varchar(2000);
        _ret                    promogest.resultid;
        _rec                    record;
        logid                   bigint;
    BEGIN
        -- Memorizza schema precedente
        schema_prec:= ARRAY_TO_STRING(CURRENT_SCHEMAS(\'t\'),\',\');

        -- Imposta schema corrente
        sql_command:= \'SET SEARCH_PATH TO \' || _schema;
        EXECUTE sql_command;

        UPDATE listino_articolo SET listino_attuale = \'f\' WHERE id_listino = _id_listino AND id_articolo = _id_articolo AND listino_attuale = \'t\';

        IF FOUND THEN
            PERFORM promogest.LogSet(_idutente, _schema, \'I\',\'ListinoArticoloDel\',\'Deleted listino_articolo\' ,NULL,NULL);
            SELECT 1 INTO _ret;
        ELSE
            PERFORM promogest.LogSet(_idutente, _schema, \'E\',\'ListinoArticoloDel\',\'listino_articolo not found\',NULL,NULL);
            RAISE WARNING\'listino_articolo not found: \';
            logid := CURRVAL(\'promogest.application_log_id_seq\');
            SELECT INTO _ret -logid;
        END IF;

        -- Imposta schema precedente
        sql_command:= \'SET SEARCH_PATH TO \' || schema_prec;
        EXECUTE sql_command;

        RETURN _ret;
    END;
' LANGUAGE plpgsql;

DROP FUNCTION promogest.ListinoArticoloGet(varchar, bigint, bigint, bigint) CASCADE;
DROP FUNCTION promogest.ListinoArticoloSel(varchar, bigint, varchar, bigint, bigint, boolean, date, date, bigint, bigint) CASCADE;
DROP FUNCTION promogest.ListinoArticoloSelCount(varchar, bigint, varchar, bigint, bigint, boolean, date, date, bigint, bigint) CASCADE;

DROP TYPE promogest.listino_articolo_type;
DROP TYPE promogest.listino_articolo_sel_type;
DROP TYPE promogest.listino_articolo_sel_count_type;

CREATE TYPE promogest.listino_articolo_type AS (
     id_listino                 bigint
    ,id_articolo                bigint
    ,prezzo_dettaglio           decimal(16,4)
    ,prezzo_ingrosso            decimal(16,4)
    ,ultimo_costo               decimal(16,4)
    ,data_listino_articolo      timestamp
    ,listino_attuale            boolean
);

CREATE TYPE promogest.listino_articolo_sel_type AS (
     id_listino                             bigint
    ,id_articolo                            bigint
    ,data_listino_articolo                  timestamp
    ,listino_attuale                        boolean
    ,denominazione                          varchar
    ,prezzo_dettaglio                       decimal(16,4)
    ,prezzo_ingrosso                        decimal(16,4)
    ,ultimo_costo                           decimal(16,4)
    ,data_listino                           timestamp
    ,codice_articolo                        varchar
    ,articolo                               varchar
    ,aliquota_iva                           varchar
    ,percentuale_iva                        decimal(8,4)
    ,id_articolo_padre                      bigint
    ,id_gruppo_taglia                       bigint
    ,id_taglia                              bigint
    ,id_colore                              bigint
    ,id_anno                                bigint
    ,id_stagione                            bigint
    ,id_genere                              bigint
    ,denominazione_breve_gruppo_taglia      varchar
    ,denominazione_gruppo_taglia            varchar
    ,denominazione_breve_taglia             varchar
    ,denominazione_taglia                   varchar
    ,denominazione_breve_colore             varchar
    ,denominazione_colore                   varchar
    ,anno                                   varchar
    ,stagione                               varchar
    ,genere                                 varchar
);

CREATE TYPE promogest.listino_articolo_sel_count_type AS (
    count       bigint
);

CREATE OR REPLACE FUNCTION promogest.ListinoArticoloGet(varchar, bigint, bigint, bigint) RETURNS SETOF promogest.listino_articolo_type AS '
    DECLARE
        -- Parametri contesto
        _schema                 ALIAS FOR $1;
        _idutente               ALIAS FOR $2;

        -- Parametri tabella
        _id_listino             ALIAS FOR $3;
        _id_articolo            ALIAS FOR $4;

        schema_prec             varchar(2000);
        sql_command             varchar(2000);
        v_row                   record;
    BEGIN
        -- Memorizza schema precedente
        schema_prec:= ARRAY_TO_STRING(CURRENT_SCHEMAS(\'t\'),\',\');

        -- Imposta schema corrente
        sql_command:= \'SET SEARCH_PATH TO \' || _schema;
        EXECUTE sql_command;

        FOR v_row IN SELECT * FROM listino_articolo WHERE id_articolo = _id_articolo AND id_listino = _id_listino AND listino_attuale = \'t\' LOOP
            RETURN NEXT v_row;
        END LOOP;

        -- Imposta schema precedente
        sql_command:= \'SET SEARCH_PATH TO \' || schema_prec;
        EXECUTE sql_command;

        RETURN;
    END;
' LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION promogest.ListinoArticoloSel(varchar, bigint, varchar, bigint, bigint, boolean, date, date, bigint, bigint) RETURNS SETOF promogest.listino_articolo_sel_type AS '
    DECLARE
        -- Parametri contesto
        _schema                 ALIAS FOR $1;
        _idutente               ALIAS FOR $2;

        -- Parametri procedura
        _orderby                ALIAS FOR $3;
        _id_listino             ALIAS FOR $4;
        _id_articolo            ALIAS FOR $5;
        _listino_attuale        ALIAS FOR $6;
        _da_data_listino        ALIAS FOR $7;
        _a_data_listino         ALIAS FOR $8;
        _offset                 ALIAS FOR $9;
        _count                  ALIAS FOR $10;

        schema_prec             varchar(2000);
        sql_statement           varchar(2000);
        sql_cond                varchar(2000);
        limitstring             varchar(500);
        _add                    varchar(500);
        OrderBy                 varchar(200);
        v_row                   record;
        _tablename              varchar;
    BEGIN
        -- Memorizza schema precedente
        schema_prec:= ARRAY_TO_STRING(CURRENT_SCHEMAS(\'t\'),\',\');

        -- Imposta schema corrente
        sql_statement:= \'SET SEARCH_PATH TO \' || _schema;
        EXECUTE sql_statement;

        sql_statement:= \'SELECT L.* FROM v_listino_articolo_completa L \';
        sql_cond:=\'\';

        IF _orderby IS NULL THEN
            OrderBy = \'L.denominazione \';
        ELSE
            OrderBy = _orderby;
        END IF;

        IF _id_articolo IS NOT NULL THEN
            _add:= \'L.id_articolo = \' || _id_articolo;
            sql_cond:= promogest.sqlAddCondition(sql_cond,_add);
        ELSE
            SELECT INTO _tablename * FROM promogest.ArticoloFilteredExists(_schema, _idutente);
            IF _tablename <> \'\' THEN
                sql_statement:= sql_statement || \' INNER JOIN \' || _tablename || \' AF ON L.id_articolo = AF.id\';
            END IF;
        END IF;

        IF _id_listino IS NOT NULL THEN
            _add:= \'L.id_listino = \' || _id_listino;
            sql_cond:= promogest.sqlAddCondition(sql_cond,_add);
        END IF;

        IF _listino_attuale IS NOT NULL THEN
            IF _listino_attuale = True THEN
                _add:= \'L.listino_attuale = \'\'t\'\'\';
                sql_cond:= promogest.sqlAddCondition(sql_cond,_add);
            ELSE
                IF _listino_attuale = False THEN
                    _add:= \'L.listino_attuale = \'\'f\'\'\';
                    sql_cond:= promogest.sqlAddCondition(sql_cond,_add);
                END IF;
            END IF;
        END IF;

        IF _da_data_listino IS NOT NULL THEN
            _add:= \'L.data_listino >= \' || QUOTE_LITERAL(_da_data_listino);
            sql_cond:= promogest.sqlAddCondition(sql_cond,_add);
        END IF;

        IF _a_data_listino IS NOT NULL THEN
            _add:= \'L.data_listino <= \' || QUOTE_LITERAL(_a_data_listino);
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

CREATE OR REPLACE FUNCTION promogest.ListinoArticoloSelCount(varchar, bigint, varchar,  bigint, bigint, boolean, date, date, bigint, bigint) RETURNS SETOF promogest.listino_articolo_sel_count_type AS '
    DECLARE
        -- Parametri contesto
        _schema                 ALIAS FOR $1;
        _idutente               ALIAS FOR $2;

        -- Parametri procedura
        _orderby                ALIAS FOR $3;
        _id_listino             ALIAS FOR $4;
        _id_articolo            ALIAS FOR $5;
        _listino_attuale        ALIAS FOR $6;
        _da_data_listino        ALIAS FOR $7;
        _a_data_listino         ALIAS FOR $8;
        _offset                 ALIAS FOR $9;
        _count                  ALIAS FOR $10;

        schema_prec             varchar(2000);
        sql_statement           varchar(2000);
        sql_cond                varchar(2000);
        limitstring             varchar(500);
        _add                    varchar(500);
        OrderBy                 varchar(200);
        v_row                   record;
        _tablename              varchar;
    BEGIN
        -- Memorizza schema precedente
        schema_prec:= ARRAY_TO_STRING(CURRENT_SCHEMAS(\'t\'),\',\');

        -- Imposta schema corrente
        sql_statement:= \'SET SEARCH_PATH TO \' || _schema;
        EXECUTE sql_statement;

        sql_statement:= \'SELECT count(L.id_listino) FROM v_listino_articolo_completa L \';
        sql_cond:=\'\';

        IF _id_articolo IS NOT NULL THEN
            _add:= \'L.id_articolo = \' || _id_articolo;
            sql_cond:= promogest.sqlAddCondition(sql_cond,_add);
        ELSE
            SELECT INTO _tablename * FROM promogest.ArticoloFilteredExists(_schema, _idutente);
            IF _tablename <> \'\' THEN
                sql_statement:= sql_statement || \' INNER JOIN \' || _tablename || \' AF ON L.id_articolo = AF.id\';
            END IF;
        END IF;

        IF _id_listino IS NOT NULL THEN
            _add:= \'L.id_listino = \' || _id_listino;
            sql_cond:= promogest.sqlAddCondition(sql_cond,_add);
        END IF;

        IF _listino_attuale IS NOT NULL THEN
            IF _listino_attuale = True THEN
                _add:= \'L.listino_attuale = \'\'t\'\'\';
                sql_cond:= promogest.sqlAddCondition(sql_cond,_add);
            ELSE
                IF _listino_attuale = False THEN
                    _add:= \'L.listino_attuale = \'\'f\'\'\';
                    sql_cond:= promogest.sqlAddCondition(sql_cond,_add);
                END IF;
            END IF;
        END IF;

        IF _da_data_listino IS NOT NULL THEN
            _add:= \'L.data_listino >= \' || QUOTE_LITERAL(_da_data_listino);
            sql_cond:= promogest.sqlAddCondition(sql_cond,_add);
        END IF;

        IF _a_data_listino IS NOT NULL THEN
            _add:= \'L.data_listino <= \' || QUOTE_LITERAL(_a_data_listino);
            sql_cond:= promogest.sqlAddCondition(sql_cond,_add);
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
