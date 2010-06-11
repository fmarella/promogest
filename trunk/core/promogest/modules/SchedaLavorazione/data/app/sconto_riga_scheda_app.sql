--
-- Copyright (C) 2005 by Promotux Informatica - http://www.promotux.it/
-- Author: Dr astico (Marco Pinna) <zoccolodignu@gmail.com>
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

sconto_riga_scheda  - Stored procedure applicativa

*/

DROP FUNCTION promogest.ScontoRigaSchedaSet(varchar, bigint, bigint, decimal(16,4), varchar, bigint);
CREATE OR REPLACE FUNCTION promogest.ScontoRigaSchedaSet(varchar, bigint, bigint, decimal(16,4), varchar, bigint) RETURNS promogest.resultid AS 
$$
    DECLARE
        -- Parametri contesto
        _schema                 ALIAS FOR $1;
        _idutente               ALIAS FOR $2;
        
        -- Parametri tabella
        _id                     ALIAS FOR $3;
        _valore                 ALIAS FOR $4;
        _tipo_sconto            ALIAS FOR $5;
        _id_riga_scheda      ALIAS FOR $6;

        schema_prec             varchar(2000);
        sql_command             varchar(2000);
        _ret                    promogest.resultid;
        _rec                    record;
    BEGIN
        -- Memorizza schema precedente
        schema_prec:= ARRAY_TO_STRING(CURRENT_SCHEMAS('t'),',');
    
        -- Imposta schema corrente
        sql_command:= 'SET SEARCH_PATH TO ' || _schema;
        EXECUTE sql_command;
        
        SELECT INTO _ret * FROM promogest.ScontoRigaSchedaInsUpd(_schema, _idutente, _id, _valore, _tipo_sconto, _id_riga_scheda); 
        
        -- Imposta schema precedente
        sql_command:= 'SET SEARCH_PATH TO ' || schema_prec;
        EXECUTE sql_command;
        
        RETURN _ret;
    END;
$$ LANGUAGE plpgsql;


DROP FUNCTION promogest.ScontoRigaSchedaDel(varchar, bigint, bigint);
CREATE OR REPLACE FUNCTION promogest.ScontoRigaSchedaDel(varchar, bigint, bigint) RETURNS promogest.resultid AS 
$$
    DECLARE
        -- Parametri contesto
        _schema                 ALIAS FOR $1;
        _idutente               ALIAS FOR $2;
        
        -- Parametri tabella
        _id_riga_scheda      ALIAS FOR $3;
        
        schema_prec             varchar(2000);
        sql_command             varchar(2000);
        _ret                    promogest.resultid;
        _rec                    record;
    BEGIN
        -- Memorizza schema precedente
        schema_prec:= ARRAY_TO_STRING(CURRENT_SCHEMAS('t'),',');
    
        -- Imposta schema corrente
        sql_command:= 'SET SEARCH_PATH TO ' || _schema;
        EXECUTE sql_command;

        DELETE FROM sconto WHERE id IN (SELECT id FROM sconti_righe_schede WHERE id_riga_scheda = _id_riga_scheda);
    
        -- DELETE FROM sconto WHERE sconto_riga_scheda.id_riga_scheda = _id_riga_scheda AND sconto.id = sconto_riga_scheda.id;

        -- Imposta schema precedente
        sql_command:= 'SET SEARCH_PATH TO ' || schema_prec;
        EXECUTE sql_command;
        
        RETURN _ret;
    END;
$$ LANGUAGE plpgsql;


DROP FUNCTION promogest.ScontiRigaSchedaDel(varchar, bigint, bigint);
CREATE OR REPLACE FUNCTION promogest.ScontiRigaSchedaDel(varchar, bigint, bigint) RETURNS promogest.resultid AS 
$$
    DECLARE
        -- Parametri contesto
        _schema                 ALIAS FOR $1;
        _idutente               ALIAS FOR $2;
        
        -- Parametri tabella
        _id_riga_scheda      ALIAS FOR $3;
        
        schema_prec             varchar(2000);
        sql_command             varchar(2000);
        _ret                    promogest.resultid;
        _rec                    record;
    BEGIN
        -- Memorizza schema precedente
        schema_prec:= ARRAY_TO_STRING(CURRENT_SCHEMAS('t'),',');
    
        -- Imposta schema corrente
        sql_command:= 'SET SEARCH_PATH TO ' || _schema;
        EXECUTE sql_command;

        DELETE FROM SCONTO WHERE id IN (SELECT id FROM sconti_righe_schede WHERE id_riga_scheda = _id_riga_scheda);
    
        -- DELETE FROM sconto WHERE sconto_riga_scheda.id_riga_scheda = _id_riga_scheda AND sconto.id = sconto_riga_scheda.id;

        -- Imposta schema precedente
        sql_command:= 'SET SEARCH_PATH TO ' || schema_prec;
        EXECUTE sql_command;
        
        RETURN _ret;
    END;
$$ LANGUAGE plpgsql;


DROP FUNCTION promogest.ScontoRigaSchedaGet(varchar, bigint, bigint);
DROP FUNCTION promogest.ScontoRigaSchedaSel(varchar, bigint, varchar, bigint, bigint, bigint);
DROP FUNCTION promogest.ScontoRigaSchedaSelCount(varchar, bigint, varchar, bigint, bigint, bigint);

DROP TYPE promogest.sconto_riga_scheda_type;
DROP TYPE promogest.sconto_riga_scheda_sel_count_type;

CREATE TYPE promogest.sconto_riga_scheda_type AS (
     id                 bigint
    ,valore             decimal(16,4)
    ,tipo_sconto        varchar(20)
    ,id_riga_scheda  bigint
);

CREATE TYPE promogest.sconto_riga_scheda_sel_count_type AS (
    count       bigint
);

CREATE OR REPLACE FUNCTION promogest.ScontoRigaSchedaGet(varchar, bigint, bigint) RETURNS SETOF promogest.sconto_riga_scheda_type AS 
$$
    DECLARE
        -- Parametri contesto
        _schema             ALIAS FOR $1;
        _idutente           ALIAS FOR $2;
        
        -- Parametri tabella
        _id                 ALIAS FOR $3;
        
        schema_prec         varchar(2000);
        sql_command         varchar(2000);
        v_row               record;
    BEGIN
        -- Memorizza schema precedente
        schema_prec:= ARRAY_TO_STRING(CURRENT_SCHEMAS('t'),',');
    
        -- Imposta schema corrente
        sql_command:= 'SET SEARCH_PATH TO ' || _schema;
        EXECUTE sql_command;
        
        FOR v_row IN SELECT * FROM v_sconto_riga_scheda WHERE id = _id LOOP
            RETURN NEXT v_row;
        END LOOP;

        -- Imposta schema precedente
        sql_command:= 'SET SEARCH_PATH TO ' || schema_prec;
        EXECUTE sql_command;

        RETURN;
    END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION promogest.ScontoRigaSchedaSel(varchar, bigint, varchar, bigint, bigint, bigint) RETURNS SETOF promogest.sconto_riga_scheda_type AS 
$$
    DECLARE
        -- Parametri contesto
        _schema                 ALIAS FOR $1;
        _idutente               ALIAS FOR $2;
        
        -- Parametri procedura
        _orderby                ALIAS FOR $3;
        _id_riga_scheda      ALIAS FOR $4;
        _offset                 ALIAS FOR $5;
        _count                  ALIAS FOR $6;
        
        schema_prec             varchar(2000);
        sql_statement           varchar(2000);
        sql_cond                varchar(2000);
        limitstring             varchar(500);
        _add                    varchar(500);
        OrderBy                 varchar(200);
        v_row                   record;
    BEGIN
        -- Memorizza schema precedente
        schema_prec:= ARRAY_TO_STRING(CURRENT_SCHEMAS('t'),',');
    
        -- Imposta schema corrente
        sql_statement:= 'SET SEARCH_PATH TO ' || _schema;
        EXECUTE sql_statement;

        sql_statement:= 'SELECT * FROM v_sconto_riga_scheda ';
        sql_cond:='';
        
        IF _orderby IS NULL THEN
            OrderBy = ' id_riga_scheda  ';
        ELSE
            OrderBy = _orderby;
        END IF;
        
        IF _id_riga_scheda IS NOT NULL THEN
            _add:= 'id_riga_scheda = ' || _id_riga_scheda;
            sql_cond:= promogest.sqlAddCondition(sql_cond,_add);
        ELSE            
            _add:= 'id_riga_scheda IS NULL ';
            sql_cond:= promogest.sqlAddCondition(sql_cond,_add);
        END IF;

        IF _offset IS NULL THEN
            limitstring:= '';
        ELSE
            limitstring:= ' LIMIT ' || _count || ' OFFSET  ' || _offset;
        END IF;
        
        IF sql_cond != '' THEN
            sql_statement:= sql_statement || ' WHERE ' || sql_cond || 'ORDER BY ' || OrderBy || limitstring;
        ELSE
            sql_statement:= sql_statement || ' ORDER BY ' || OrderBy || limitstring;
        END IF;

        FOR v_row IN EXECUTE sql_statement LOOP
            RETURN NEXT v_row;
        END LOOP;

        -- Imposta schema precedente
        sql_statement:= 'SET SEARCH_PATH TO ' || schema_prec;
        EXECUTE sql_statement;

        RETURN;
    END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION promogest.ScontoRigaSchedaSelCount(varchar, bigint, varchar, bigint, bigint, bigint) RETURNS SETOF promogest.sconto_riga_scheda_sel_count_type AS 
$$
    DECLARE
        -- Parametri contesto
        _schema                 ALIAS FOR $1;
        _idutente               ALIAS FOR $2;
        
        -- Parametri procedura
        _orderby                ALIAS FOR $3;
        _id_riga_scheda      ALIAS FOR $4;
        _offset                 ALIAS FOR $5;
        _count                  ALIAS FOR $6;
        
        schema_prec             varchar(2000);
        sql_statement           varchar(2000);
        sql_cond                varchar(2000);
        limitstring             varchar(500);
        _add                    varchar(500);
        OrderBy                 varchar(200);
        v_row                   record;
    BEGIN
        -- Memorizza schema precedente
        schema_prec:= ARRAY_TO_STRING(CURRENT_SCHEMAS('t'),',');
    
        -- Imposta schema corrente
        sql_statement:= 'SET SEARCH_PATH TO ' || _schema;
        EXECUTE sql_statement;

        sql_statement:= 'SELECT COUNT(id) FROM v_sconto_riga_scheda ';
        sql_cond:='';
        
        IF _id_riga_scheda IS NOT NULL THEN
            _add:= 'id_riga_scheda = ' || _id_riga_scheda;
            sql_cond:= promogest.sqlAddCondition(sql_cond,_add);
        ELSE            
            _add:= 'id_riga_scheda IS NULL ';
            sql_cond:= promogest.sqlAddCondition(sql_cond,_add);
        END IF;
        
        IF sql_cond != '' THEN
            sql_statement:= sql_statement || ' WHERE ' || sql_cond;
        END IF;

        FOR v_row IN EXECUTE sql_statement LOOP
            RETURN NEXT v_row;
        END LOOP;

        -- Imposta schema precedente
        sql_statement:= 'SET SEARCH_PATH TO ' || schema_prec;
        EXECUTE sql_statement;

        RETURN;
    END;
$$ LANGUAGE plpgsql;
