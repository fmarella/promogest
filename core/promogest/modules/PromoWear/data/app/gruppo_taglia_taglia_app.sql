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
-- MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
-- GNU General Public License for more details.
--
-- You should have received a copy of the GNU General Public License
-- along with this program; if not, write to the Free Software
-- Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.

/*

GruppoTaglia<->Taglia  - Stored procedure applicativa

*/

DROP FUNCTION promogest.GruppoTagliaTagliaSet(varchar, bigint, bigint, bigint);
DROP FUNCTION promogest.GruppoTagliaTagliaSet(varchar, bigint, bigint, bigint, bigint);
CREATE OR REPLACE FUNCTION promogest.GruppoTagliaTagliaSet(varchar, bigint, bigint, bigint, bigint) RETURNS promogest.resultid AS '
    DECLARE
        -- Parametri contesto
        _schema                     ALIAS FOR $1;
        _idutente                   ALIAS FOR $2;
        
        -- Parametri tabella
        _id_gruppo_taglia           ALIAS FOR $3;
        _id_taglia                  ALIAS FOR $4;
        _ordine                     ALIAS FOR $5;

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
        
        SELECT INTO _ret * FROM promogest.GruppoTagliaTagliaInsUpd(_schema, _idutente, _id_gruppo_taglia, _id_taglia, _ordine);
        
        -- Imposta schema precedente
        sql_command:= \'SET SEARCH_PATH TO \' || schema_prec;
        EXECUTE sql_command;
        
        RETURN _ret;
    END;
' LANGUAGE plpgsql;


DROP FUNCTION promogest.GruppoTagliaTagliaDel(varchar, bigint, bigint, bigint);
CREATE OR REPLACE FUNCTION promogest.GruppoTagliaTagliaDel(varchar, bigint, bigint, bigint) RETURNS promogest.resultid AS '
    DECLARE
        -- Parametri contesto
        _schema                     ALIAS FOR $1;
        _idutente                   ALIAS FOR $2;
        
        -- Parametri tabella
        _id_gruppo_taglia           ALIAS FOR $3;
        _id_taglia                  ALIAS FOR $4;
        
        schema_prec                 varchar(2000);
        sql_command                 varchar(2000);
        _ret                        promogest.resultid;
        _rec                        record;
        logid                       bigint;

    BEGIN
        -- Memorizza schema precedente
        schema_prec:= ARRAY_TO_STRING(CURRENT_SCHEMAS(\'t\'),\',\');
    
        -- Imposta schema corrente
        sql_command:= \'SET SEARCH_PATH TO \' || _schema;
        EXECUTE sql_command;

        DELETE FROM gruppo_taglia_taglia WHERE id_gruppo_taglia = _id_gruppo_taglia AND id_taglia = _id_taglia;

        IF FOUND THEN
            PERFORM promogest.LogSet(_idutente, _schema, \'I\',\'GruppoTagliaTagliaDel\',\'Deleted gruppo_taglia_taglia\' ,NULL,NULL);
            SELECT 1 INTO _ret;
        ELSE
            PERFORM promogest.LogSet(_idutente, _schema, \'E\',\'GruppoTagliaTagliaDel\',\'gruppo_taglia_taglia not found\',NULL,NULL);
            RAISE WARNING\'gruppo_taglia_taglia not found: \';
            logid := CURRVAL(\'promogest.application_log_id_seq\');
            SELECT INTO _ret -logid;
        END IF;
        
        -- Imposta schema precedente
        sql_command:= \'SET SEARCH_PATH TO \' || schema_prec;
        EXECUTE sql_command;
        
        RETURN _ret;
    END;
' LANGUAGE plpgsql;

DROP FUNCTION promogest.GruppoTagliaTagliaGet(varchar, bigint, bigint, bigint);
DROP FUNCTION promogest.GruppoTagliaTagliaSel(varchar, bigint, varchar,  bigint, bigint, bigint, bigint);
DROP FUNCTION promogest.GruppoTagliaTagliaSelCount(varchar, bigint, varchar,  bigint, bigint, bigint, bigint);

DROP TYPE promogest.gruppo_taglia_taglia_type;
DROP TYPE promogest.gruppo_taglia_taglia_sel_type;
DROP TYPE promogest.gruppo_taglia_taglia_sel_count_type;

CREATE TYPE promogest.gruppo_taglia_taglia_type AS (
     id_gruppo_taglia                       bigint
    ,id_taglia                              bigint
    ,ordine                                 bigint
);

CREATE TYPE promogest.gruppo_taglia_taglia_sel_type AS (
     id_gruppo_taglia                       bigint
    ,id_taglia                              bigint
    ,ordine                                 bigint
    ,denominazione_breve_gruppo_taglia      varchar
    ,denominazione_gruppo_taglia            varchar
    ,denominazione_breve_taglia             varchar
    ,denominazione_taglia                   varchar
);

CREATE TYPE promogest.gruppo_taglia_taglia_sel_count_type AS (
    count       bigint
);

CREATE OR REPLACE FUNCTION promogest.GruppoTagliaTagliaGet(varchar, bigint, bigint, bigint) RETURNS SETOF promogest.gruppo_taglia_taglia_type AS '
    DECLARE
        -- Parametri contesto
        _schema                 ALIAS FOR $1;
        _idutente               ALIAS FOR $2;
        
        -- Parametri tabella
        _id_gruppo_taglia       ALIAS FOR $3;
        _id_taglia              ALIAS FOR $4;
        
        schema_prec             varchar(2000);
        sql_command             varchar(2000);
        v_row                   record;
    BEGIN
        -- Memorizza schema precedente
        schema_prec:= ARRAY_TO_STRING(CURRENT_SCHEMAS(\'t\'),\',\');
    
        -- Imposta schema corrente
        sql_command:= \'SET SEARCH_PATH TO \' || _schema;
        EXECUTE sql_command;
        
        FOR v_row IN SELECT * FROM gruppo_taglia_taglia WHERE id_gruppo_taglia = _id_gruppo_taglia AND id_taglia = _id_taglia LOOP
            RETURN NEXT v_row;
        END LOOP;

        -- Imposta schema precedente
        sql_command:= \'SET SEARCH_PATH TO \' || schema_prec;
        EXECUTE sql_command;

        RETURN;
    END;
' LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION promogest.GruppoTagliaTagliaSel(varchar, bigint, varchar, bigint, bigint, bigint, bigint) RETURNS SETOF promogest.gruppo_taglia_taglia_sel_type AS '
    DECLARE
        -- Parametri contesto
        _schema                 ALIAS FOR $1;
        _idutente               ALIAS FOR $2;
        
        -- Parametri procedura
        _orderby                ALIAS FOR $3;
        _id_gruppo_taglia       ALIAS FOR $4;
        _id_taglia              ALIAS FOR $5;
        _offset                 ALIAS FOR $6;
        _count                  ALIAS FOR $7;
        
        schema_prec             varchar(2000);
        sql_statement           varchar(2000);
        sql_cond                varchar(2000);
        limitstring             varchar(500);
        _add                    varchar(500);
        OrderBy                 varchar(200);
        v_row record;
    BEGIN
        -- Memorizza schema precedente
        schema_prec:= ARRAY_TO_STRING(CURRENT_SCHEMAS(\'t\'),\',\');
    
        -- Imposta schema corrente
        sql_statement:= \'SET SEARCH_PATH TO \' || _schema;
        EXECUTE sql_statement;

        sql_statement:= \'SELECT * FROM v_gruppo_taglia_taglia \';
        sql_cond:=\'\';
        
        IF _orderby IS NULL THEN
            OrderBy = \'id_gruppo_taglia, ordine, id_taglia \';
        ELSE
            OrderBy = _orderby;
        END IF;
        
        IF _id_gruppo_taglia IS NOT NULL THEN
            _add:= \' id_gruppo_taglia = \' || _id_gruppo_taglia;
            sql_cond:= promogest.sqlAddCondition(sql_cond,_add);
        END IF;
        
        IF _id_taglia IS NOT NULL THEN
            _add:= \' id_taglia = \' || _id_taglia;
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

CREATE OR REPLACE FUNCTION promogest.GruppoTagliaTagliaSelCount(varchar, bigint, varchar,  bigint, bigint, bigint, bigint) RETURNS SETOF promogest.gruppo_taglia_taglia_sel_count_type AS '
    DECLARE
        -- Parametri contesto
        _schema                 ALIAS FOR $1;
        _idutente               ALIAS FOR $2;
        
        -- Parametri procedura
        _orderby                ALIAS FOR $3;
        _id_gruppo_taglia       ALIAS FOR $4;
        _id_taglia              ALIAS FOR $5;
        _offset                 ALIAS FOR $6;
        _count                  ALIAS FOR $7;
        
        schema_prec             varchar(2000);
        sql_statement           varchar(2000);
        sql_cond                varchar(2000);
        limitstring             varchar(500);
        _add                    varchar(500);
        OrderBy                 varchar(200);
        v_row record;
    BEGIN
        -- Memorizza schema precedente
        schema_prec:= ARRAY_TO_STRING(CURRENT_SCHEMAS(\'t\'),\',\');
    
        -- Imposta schema corrente
        sql_statement:= \'SET SEARCH_PATH TO \' || _schema;
        EXECUTE sql_statement;

        sql_statement:= \'SELECT COUNT(*) FROM v_gruppo_taglia_taglia \';
        sql_cond:=\'\';
        
        IF _id_gruppo_taglia IS NOT NULL THEN
            _add:= \'id_gruppo_taglia = \' || _id_gruppo_taglia;
            sql_cond:= promogest.sqlAddCondition(sql_cond,_add);
        END IF;
        
        IF _id_taglia IS NOT NULL THEN
            _add:= \'id_taglia = \' || _id_gruppo_taglia;
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
