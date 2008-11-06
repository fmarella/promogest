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
-- MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
-- GNU General Public License for more details.
--
-- You should have received a copy of the GNU General Public License
-- along with this program; if not, write to the Free Software
-- Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.

/*
 * CREAZIONE TYPES CARATTERI STAMPA
 */
DROP TYPE promogest.carattere_stampa_type CASCADE;
CREATE TYPE promogest.carattere_stampa_type AS(
    id                      BIGINT
    ,denominazione           VARCHAR
);

DROP TYPE promogest.carattere_stampa_count_type CASCADE;
CREATE TYPE promogest.carattere_stampa_count_type AS (
    count                   BIGINT
);

/*
 * CREAZIONE APPLICAZIONI TABELLA caratteri_stampa (Get - Set - Del - Sel)
 */
 
DROP FUNCTION promogest.CarattereStampaSet(varchar,bigint,bigint,varchar) CASCADE;

CREATE OR REPLACE FUNCTION promogest.CarattereStampaSet(varchar,bigint,bigint,varchar) RETURNS promogest.resultid AS 
$$
    DECLARE
        -- Parametri contesto
        _schema                         ALIAS FOR $1;
        _idutente                       ALIAS FOR $2;
        
        -- Parametri Tabella
        _id                             ALIAS FOR $3;
        _denominazione                  ALIAS FOR $4;
        
        schema_prec                     varchar(2000);
        sql_command                     varchar(2000);
        _ret                            promogest.resultid;
        _rec                            record;

    BEGIN
        -- Memorizza schema precedente
        schema_prec:= ARRAY_TO_STRING(CURRENT_SCHEMAS('t'),',');

        -- Imposta schema corrente
        sql_command:= 'SET SEARCH_PATH TO ' || _schema;
        EXECUTE sql_command;
        
        SELECT INTO _ret * FROM promogest.CarattereStampaInsUpd(_schema, _idutente, _id, _denominazione);
        
        -- reimposta lo schema precedente
        sql_command:= 'SET SEARCH_PATH TO ' || schema_prec;
        EXECUTE sql_command;
        
        RETURN _ret;
    END;
$$ LANGUAGE plpgsql;

DROP FUNCTION promogest.CarattereStampaGet(varchar,bigint,bigint) CASCADE;
CREATE OR REPLACE FUNCTION promogest.CarattereStampaGet(varchar,bigint,bigint) RETURNS SETOF promogest.carattere_stampa_type AS 
$$
    DECLARE
        -- Parametri contesto
        _schema                         ALIAS FOR $1;
        _idutente                       ALIAS FOR $2;
        
        -- Parametri Tabella
        _id                             ALIAS FOR $3;
    
        schema_prec                     varchar(2000);
        sql_command                     varchar(2000);
        v_row                           record;
    BEGIN
        -- Memorizza schema precedente
        schema_prec:= ARRAY_TO_STRING(CURRENT_SCHEMAS('t'),',');

        -- Imposta schema corrente
        sql_command:= 'SET SEARCH_PATH TO ' || _schema;
        EXECUTE sql_command;
        
        FOR v_row IN SELECT CS.* FROM caratteri_stampa CS WHERE id = _id LOOP
            RETURN NEXT v_row;
        END LOOP;

        -- Imposta schema precedente
        sql_command:= 'SET SEARCH_PATH TO ' || schema_prec;
        EXECUTE sql_command;

        RETURN;
    END;
$$ LANGUAGE plpgsql;

DROP FUNCTION promogest.CarattereStampaDel(varchar,bigint,bigint) CASCADE;
CREATE OR REPLACE FUNCTION promogest.CarattereStampaDel(varchar,bigint,bigint) RETURNS promogest.resultid AS 
$$
    DECLARE
        -- Parametri contesto
        _schema                         ALIAS FOR $1;
        _idutente                       ALIAS FOR $2;
        
        -- Parametri Tabella
        _id                             ALIAS FOR $3;
        
        schema_prec                     varchar(2000);
        sql_command                     varchar(2000);
        _ret                            promogest.resultid;
        v_row                           record;
    BEGIN
        -- Memorizza schema precedente
        schema_prec:= ARRAY_TO_STRING(CURRENT_SCHEMAS('t'),',');

        -- Imposta schema corrente
        sql_command:= 'SET SEARCH_PATH TO ' || _schema;
        EXECUTE sql_command;
        
        SELECT INTO _ret * FROM promogest.ObjectDel(_schema, _idutente, 'caratteri_stampa', _id, 'id');
        
        -- Imposta schema precedente
        sql_command:= 'SET SEARCH_PATH TO ' || schema_prec;
        EXECUTE sql_command;

        RETURN _ret;
    END;
$$ LANGUAGE plpgsql;

DROP FUNCTION promogest.CarattereStampaSel (varchar,bigint,varchar,varchar,bigint,bigint)CASCADE;
CREATE OR REPLACE FUNCTION promogest.CarattereStampaSel (varchar, bigint, varchar, varchar, bigint, bigint) RETURNS SETOF promogest.carattere_stampa_type AS 
$$
    DECLARE
        -- Parametri contesto
        _schema                         ALIAS FOR $1;
        _idutente                       ALIAS FOR $2;
        
        -- Parametri Tabella
        _orderby                        ALIAS FOR $3;
        _denominazione                  ALIAS FOR $4;
        _offset                         ALIAS FOR $5;
        _count                          ALIAS FOR $6;
        
        schema_prec             varchar(2000);
        sql_statement           varchar(2000);
        sql_cond                varchar(2000);
        sql_command             varchar(2000);
        _add                    varchar(500);
        limitstring             varchar(2000);
        OrderBy                 varchar(500);
        v_row                   record;
        _tablename              varchar;
        condition               varchar(10);
    BEGIN
    
        -- Memorizza schema precedente
        schema_prec:= ARRAY_TO_STRING(CURRENT_SCHEMAS('t'),',');

        -- Imposta schema corrente
        sql_command:= 'SET SEARCH_PATH TO ' || _schema;
        EXECUTE sql_command;
        
        sql_statement:= 'SELECT CS.* FROM caratteri_stampa CS ';
        sql_cond:= '';
        
        IF _orderby IS NULL THEN
            OrderBy = ' CS.denominazione  ';
        ELSE
            OrderBy = _orderby;
        END IF;
        
        IF _denominazione IS NOT NULL THEN
            _add:= ' CS.denominazione ILIKE \'' || _denominazione || '\' ';
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
        
DROP FUNCTION promogest.CarattereStampaSelCount (varchar,bigint,varchar) CASCADE;
CREATE OR REPLACE FUNCTION promogest.CarattereStampaSelCount (varchar,bigint,varchar) RETURNS SETOF promogest.carattere_stampa_count_type AS 
$$
    DECLARE
        -- Parametri contesto
        _schema                         ALIAS FOR $1;
        _idutente                       ALIAS FOR $2;
        
        -- Parametri Tabella
        _denominazione                  ALIAS FOR $3;

        
        schema_prec             varchar(2000);
        sql_statement           varchar(2000);
        sql_command             varchar(2000);
        sql_cond                varchar(2000);
        _add                    varchar(500);
        v_row                   record;
        _tablename              varchar;
        condition               varchar(10);
    BEGIN
    
        -- Memorizza schema precedente
        schema_prec:= ARRAY_TO_STRING(CURRENT_SCHEMAS('t'),',');

        -- Imposta schema corrente
        sql_command:= 'SET SEARCH_PATH TO ' || _schema;
        EXECUTE sql_command;
        
        sql_statement:= 'SELECT COUNT (CS.id) FROM caratteri_stampa CS ';
        sql_cond:= '';
        
        IF _denominazione IS NOT NULL THEN
            _add:= ' CS.denominazione ILIKE \'' || _denominazione || '\' ';
            sql_cond:= promogest.sqlAddCondition(sql_cond,_add);
        END IF;

        IF sql_cond != '' THEN
            sql_statement:= sql_statement || ' WHERE ' || sql_cond ;
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

