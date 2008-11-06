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

Codice a Barre Articolo  - Stored procedure applicativa

*/

DROP FUNCTION promogest.CodiceABarreArticoloSet(varchar, bigint, bigint, varchar, bigint, boolean);
CREATE OR REPLACE FUNCTION promogest.CodiceABarreArticoloSet(varchar, bigint, bigint, varchar, bigint, boolean) RETURNS promogest.resultid AS '
    DECLARE
        -- Parametri contesto
        _schema             ALIAS FOR $1;
        _idutente           ALIAS FOR $2;
        
        -- Parametri tabella
        _id                 ALIAS FOR $3;
        _codice             ALIAS FOR $4;
        _id_articolo        ALIAS FOR $5;
        _primario           ALIAS FOR $6;
        schema_prec         varchar(2000);
        sql_command         varchar(2000);
        _ret                promogest.resultid;
        _rec                record;
        _oldcountprimary    integer;
    BEGIN
        -- Memorizza schema precedente
        schema_prec:= ARRAY_TO_STRING(CURRENT_SCHEMAS(\'t\'),\',\');
    
        -- Imposta schema corrente
        sql_command:= \'SET SEARCH_PATH TO \' || _schema;
        EXECUTE sql_command;

        -- Check codice primario
        IF _primario = \'t\' THEN
            SELECT COUNT(*) INTO _oldcountprimary FROM codice_a_barre_articolo WHERE id_articolo = _id_articolo AND primario;
            IF _oldcountprimary > 0 THEN
                -- Disattivo vecchi primari
                UPDATE codice_a_barre_articolo SET primario = \'f\' WHERE id_articolo = _id_articolo AND primario;
            END IF;
        END IF;
        
        SELECT INTO _ret * FROM promogest.CodiceABarreArticoloInsUpd(_schema, _idutente, _id, _codice, _id_articolo, _primario); 
        
        -- Imposta schema precedente
        sql_command:= \'SET SEARCH_PATH TO \' || schema_prec;
        EXECUTE sql_command;
        
        RETURN _ret;
    END;
' LANGUAGE plpgsql;


DROP FUNCTION promogest.CodiceABarreArticoloDel(varchar, bigint, bigint);
CREATE OR REPLACE FUNCTION promogest.CodiceABarreArticoloDel(varchar, bigint, bigint) RETURNS promogest.resultid AS '
    DECLARE
        -- Parametri contesto
        _schema             ALIAS FOR $1;
        _idutente           ALIAS FOR $2;
        
        -- Parametri tabella
        _id                 ALIAS FOR $3;
        schema_prec         varchar(2000);
        sql_command         varchar(2000);
        _ret                promogest.resultid;
        _rec                record;
    BEGIN
        -- Memorizza schema precedente
        schema_prec:= ARRAY_TO_STRING(CURRENT_SCHEMAS(\'t\'),\',\');
    
        -- Imposta schema corrente
        sql_command:= \'SET SEARCH_PATH TO \' || _schema;
        EXECUTE sql_command;
        
        SELECT INTO _ret * FROM promogest.ObjectDel(_schema, _idutente, \'codice_a_barre_articolo\', _id, \'id\');
        
        -- Imposta schema precedente
        sql_command:= \'SET SEARCH_PATH TO \' || schema_prec;
        EXECUTE sql_command;
        
        RETURN _ret;
    END;
' LANGUAGE plpgsql;

DROP FUNCTION promogest.CodiceABarreArticoloGet(varchar, bigint, bigint);
DROP FUNCTION promogest.CodiceABarreArticoloSel(varchar, bigint, varchar, bigint, varchar, bigint, bigint);
DROP FUNCTION promogest.CodiceABarreArticoloSelCount(varchar, bigint, varchar, bigint, varchar, bigint, bigint);

DROP TYPE promogest.codice_a_barre_articolo_type;
DROP TYPE promogest.codice_a_barre_articolo_sel_count_type;

CREATE TYPE promogest.codice_a_barre_articolo_type AS (
     id                 bigint
    ,codice             varchar
    ,id_articolo        bigint
    ,primario           boolean
                     
);

CREATE TYPE promogest.codice_a_barre_articolo_sel_count_type AS (
    count       bigint
);

CREATE OR REPLACE FUNCTION promogest.CodiceABarreArticoloGet(varchar, bigint, bigint) RETURNS SETOF promogest.codice_a_barre_articolo_type AS '
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
        schema_prec:= ARRAY_TO_STRING(CURRENT_SCHEMAS(\'t\'),\',\');
    
        -- Imposta schema corrente
        sql_command:= \'SET SEARCH_PATH TO \' || _schema;
        EXECUTE sql_command;
        
        FOR v_row IN SELECT * FROM codice_a_barre_articolo WHERE id = _id LOOP
            RETURN NEXT v_row;
        END LOOP;

        -- Imposta schema precedente
        sql_command:= \'SET SEARCH_PATH TO \' || schema_prec;
        EXECUTE sql_command;

        RETURN;
    END;
' LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION promogest.CodiceABarreArticoloSel(varchar, bigint, varchar, bigint, varchar, bigint, bigint) RETURNS SETOF promogest.codice_a_barre_articolo_type AS '
    DECLARE
        -- Parametri contesto
        _schema             ALIAS FOR $1;
        _idutente           ALIAS FOR $2;
        
        -- Parametri procedura
        _orderby            ALIAS FOR $3;
        _id_articolo        ALIAS FOR $4;
        _codice             ALIAS FOR $5;
        _offset             ALIAS FOR $6;
        _count              ALIAS FOR $7;
        
        schema_prec         varchar(2000);
        sql_statement       varchar(2000);
        sql_cond            varchar(2000);
        limitstring         varchar(500);
        _add                varchar(500);
        OrderBy             varchar(200);
        v_row               record;
    BEGIN
        -- Memorizza schema precedente
        schema_prec:= ARRAY_TO_STRING(CURRENT_SCHEMAS(\'t\'),\',\');
    
        -- Imposta schema corrente
        sql_statement:= \'SET SEARCH_PATH TO \' || _schema;
        EXECUTE sql_statement;

        sql_statement:= \'SELECT * FROM codice_a_barre_articolo \';
        sql_cond:=\'\';
        
        IF _orderby IS NULL THEN
            OrderBy = \'codice \';
        ELSE
            OrderBy = _orderby;
        END IF;
        
        IF _codice IS NOT NULL THEN
            _add:= \'codice ILIKE \'\'%\' || _codice || \'%\'\'\';
            sql_cond:= promogest.sqlAddCondition(sql_cond,_add);
        END IF;
        
        IF _id_articolo IS NOT NULL THEN
            _add:= \'id_articolo = \' || _id_articolo;
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

CREATE OR REPLACE FUNCTION promogest.CodiceABarreArticoloSelCount(varchar, bigint, varchar, bigint, varchar, bigint, bigint) RETURNS SETOF promogest.codice_a_barre_articolo_sel_count_type AS '
    DECLARE
        -- Parametri contesto
        _schema             ALIAS FOR $1;
        _idutente           ALIAS FOR $2;
        
        -- Parametri procedura
        _orderby            ALIAS FOR $3;
        _id_articolo        ALIAS FOR $4;
        _codice             ALIAS FOR $5;
        _offset             ALIAS FOR $6;
        _count              ALIAS FOR $7;
        
        schema_prec         varchar(2000);
        sql_statement       varchar(2000);
        sql_cond            varchar(2000);
        limitstring         varchar(500);
        _add                varchar(500);
        OrderBy             varchar(200);
        v_row               record;
    BEGIN
        -- Memorizza schema precedente
        schema_prec:= ARRAY_TO_STRING(CURRENT_SCHEMAS(\'t\'),\',\');
    
        -- Imposta schema corrente
        sql_statement:= \'SET SEARCH_PATH TO \' || _schema;
        EXECUTE sql_statement;

        sql_statement:= \'SELECT COUNT(id) FROM codice_a_barre_articolo \';
        sql_cond:=\'\';
        
        IF _orderby IS NULL THEN
            OrderBy = \'codice \';
        ELSE
            OrderBy = _orderby;
        END IF;
        
        IF _codice IS NOT NULL THEN
            _add:= \'codice ILIKE \'\'%\' || _codice || \'%\'\'\';
            sql_cond:= promogest.sqlAddCondition(sql_cond,_add);
        END IF;
        
        IF _id_articolo IS NOT NULL THEN
            _add:= \'id_articolo = \' || _id_articolo;
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
