--
-- Copyright (C) 2005 by Promotux Informatica - http://www.promotux.it/
-- Author: Enrico Pintus <enrico@promotux.it>
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
 * Promemoria schede ordinazioni. funzioni applicative tabella promemoria_schede_ordinazioni
 *
 */

DROP TYPE promogest.promemoria_scheda_type CASCADE;

CREATE TYPE promogest.promemoria_scheda_type AS (
     id                         bigint
    ,data_inserimento           timestamp
    ,data_scadenza              timestamp
    ,oggetto                    varchar
    ,incaricato                 varchar
    ,autore                     varchar
    ,descrizione                text
    ,annotazione                text
    ,riferimento                varchar
    ,giorni_preavviso           integer
    ,in_scadenza                boolean
    ,scaduto                    boolean
    ,completato                 boolean
    ,id_scheda                  bigint
);


CREATE OR REPLACE FUNCTION promogest.PromemoriaSchedaSet(varchar, bigint, bigint, timestamp, timestamp, varchar, varchar, varchar, text, text, varchar, integer, boolean, boolean, boolean, bigint) RETURNS promogest.resultid AS 
$$
    DECLARE
        -- Dati contesto
        _schema                     ALIAS FOR $1;
        _idutente                  ALIAS FOR $2;
        
        -- Dati tabella
        _id                         ALIAS FOR $3;
        _data_inserimento           ALIAS FOR $4;
        _data_scadenza              ALIAS FOR $5;
        _oggetto                    ALIAS FOR $6;
        _incaricato                 ALIAS FOR $7;
        _autore                     ALIAS FOR $8;
        _descrizione                ALIAS FOR $9;
        _annotazione                ALIAS FOR $10;
        _riferimento                ALIAS FOR $11;
        _giorni_preavviso           ALIAS FOR $12;
        _in_scadenza                ALIAS FOR $13;
        _scaduto                    ALIAS FOR $14;
        _completato                 ALIAS FOR $15;
        _id_scheda                  ALIAS FOR $16;
        
        schema_prec             varchar(2000);
        sql_command             varchar(2000);
        TempId                  bigint;
        _ret                            promogest.resultid;
        _rec                            record;
        
    BEGIN
        -- Memorizza schema precedente
        schema_prec:= ARRAY_TO_STRING(CURRENT_SCHEMAS('t'),',');

        -- Imposta schema corrente
        sql_command:= 'SET SEARCH_PATH TO ' || _schema;
        EXECUTE sql_command;
        
        IF _id IS NULL THEN
            --this is a first insertion of a promemoria_scheda_record (does not exist, yet)
            SELECT INTO _ret * FROM promogest.PromemoriaInsUpd(_schema, _idutente, _id, _data_inserimento, _data_scadenza, _oggetto, _incaricato, _autore, _descrizione, _annotazione, _riferimento, _giorni_preavviso, _in_scadenza, _scaduto, _completato);
            
            if _ret IS NOT NULL THEN
                select into TempId _ret.id;
                INSERT INTO promemoria_schede_ordinazioni (id, id_scheda)
                VALUES
                    (TempId, _id_scheda);
            END IF;
        ELSE
            SELECT INTO _ret * FROM promogest.PromemoriaInsUpd(_schema, _idutente, _id, _data_inserimento, _data_scadenza, _oggetto, _incaricato, _autore, _descrizione, _annotazione, _riferimento, _giorni_preavviso, _in_scadenza, _scaduto, _completato);
        END IF;
    
        RETURN _ret;
    END;
$$
LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION promogest.PromemoriaSchedaGet(varchar, bigint, bigint) RETURNS SETOF promogest.promemoria_scheda_type AS
$$
    DECLARE
        -- dati contesto
        _schema                     ALIAS FOR $1;
        _idutente                   ALIAS FOR $2;
        
        --dati tabella
        _id_scheda                  ALIAS FOR $3;
        
        schema_prec             varchar(2000);
        sql_command             varchar(2000);
        v_row                   record;
        
    BEGIN
        -- Memorizza schema precedente
        schema_prec:= ARRAY_TO_STRING(CURRENT_SCHEMAS('t'),',');

        -- Imposta schema corrente
        sql_command:= 'SET SEARCH_PATH TO ' || _schema;
        EXECUTE sql_command;

        FOR v_row IN SELECT * FROM v_promemoria_scheda WHERE id_scheda = _id_scheda LOOP
            RETURN NEXT v_row;
        END LOOP;

        -- Imposta schema precedente
        sql_command:= 'SET SEARCH_PATH TO ' || schema_prec;
        EXECUTE sql_command;

        RETURN;
    END;
$$
LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION promogest.PromemoriaSchedaDel(varchar, bigint, bigint) RETURNS promogest.resultid AS
$$
    DECLARE
        -- Dati contesto
        _schema                     ALIAS FOR $1;
        _idutente                   ALIAS FOR $2;
        
        --Dati tabella
        _id_promemoria              ALIAS FOR $3;
        
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
        
        SELECT INTO _ret * FROM promogest.ObjectDel(_schema, _idutente, 'promemoria', _id_promemoria, 'id');
        
        -- Imposta schema precedente
        sql_command:= 'SET SEARCH_PATH TO ' || schema_prec;
        EXECUTE sql_command;
        
        RETURN _ret;
    END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION promogest.PromemoriaSchedaDeleteAll(varchar, bigint, bigint) RETURNS promogest.resultid AS
$$
    DECLARE
        -- Dati contesto
        _schema                     ALIAS FOR $1;
        _idutente                   ALIAS FOR $2;
        
        --Dati tabella
        _id_scheda                  ALIAS FOR $3;
        
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
        
        DELETE FROM promemoria P WHERE P.id IN (SELECT PS.id from promemoria_schede_ordinazioni PS WHERE PS.id_scheda = _id_scheda);
        DELETE FROM promemoria_schede_ordinazioni PS WHERE PS.id_scheda = _id_scheda;
        
        -- Imposta schema precedente
        sql_command:= 'SET SEARCH_PATH TO ' || schema_prec;
        EXECUTE sql_command;
        
        RETURN _ret;
    END;
$$ LANGUAGE plpgsql;

DROP FUNCTION promogest.PromemoriaSchedaSel(varchar, bigint, varchar, timestamp, timestamp, timestamp, timestamp, varchar, varchar, varchar, text, text, varchar, integer,boolean, boolean, boolean, bigint, bigint, bigint);


CREATE OR REPLACE FUNCTION promogest.promemoriaschedasel("varchar", int8, "varchar", "timestamp", "timestamp", "timestamp", "timestamp", "varchar", "varchar", "varchar", text, text, "varchar", int4, bool, bool, bool, int8, int8, int8)
  RETURNS SETOF promogest.promemoria_scheda_type AS
$BODY$
    DECLARE
        -- Parametri contesto
	    _schema                 ALIAS FOR $1;
        _idutente               ALIAS FOR $2;

        --Parametri tabella
        _orderby                ALIAS FOR $3;
        _da_data_inserimento    ALIAS FOR $4;
        _a_data_inserimento     ALIAS FOR $5;
        _da_data_scadenza       ALIAS FOR $6;
        _a_data_scadenza        ALIAS FOR $7;
        _oggetto                ALIAS FOR $8;
        _incaricato             ALIAS FOR $9;
        _autore                 ALIAS FOR $10;
        _descrizione            ALIAS FOR $11;
        _annotazione            ALIAS FOR $12;
        _riferimento            ALIAS FOR $13;
        _giorni_preavviso       ALIAS FOR $14;
        _in_scadenza            ALIAS FOR $15;
        _scaduto                ALIAS FOR $16;
        _completato             ALIAS FOR $17;
        _id_scheda              ALIAS FOR $18;
        _offset                 ALIAS FOR $19;
        _count                  ALIAS FOR $20;
        
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

        sql_statement:= 'SELECT * FROM v_promemoria_scheda ';
        sql_cond:='';

        IF _orderby IS NULL THEN
            OrderBy = 'data_scadenza ';
        ELSE
            OrderBy = _orderby;
        END IF;

        IF _da_data_scadenza IS NOT NULL THEN
            _add := 'data_scadenza >= '  || QUOTE_LITERAL(_da_data_scadenza);
            sql_cond:= promogest.sqlAddCondition(sql_cond,_add);
        END IF;

        IF _a_data_scadenza IS NOT NULL THEN
            _add := 'data_scadenza <= ' || QUOTE_LITERAL(_a_data_scadenza);
            sql_cond:= promogest.sqlAddCondition(sql_cond,_add);
        END IF;

        IF _da_data_inserimento IS NOT NULL THEN
            _add:= 'data_inserimento >= ' || QUOTE_LITERAL(_da_data_inserimento);
            sql_cond:= promogest.sqlAddCondition(sql_cond,_add);
        END IF;

        IF _a_data_inserimento IS NOT NULL THEN
            _add:= 'data_inserimento <= ' || QUOTE_LITERAL(_a_data_inserimento);
            sql_cond:= promogest.sqlAddCondition(sql_cond,_add);
        END IF;

        IF _oggetto IS NOT NULL THEN
            _add:= E'oggetto ILIKE \'' || _oggetto || E'\' ';
            sql_cond:= promogest.sqlAddCondition(sql_cond,_add);
        END IF;

        IF _incaricato IS NOT NULL THEN
            _add:= E'incaricato ILIKE \'' || _incaricato  || E'\' ';
            sql_cond:= promogest.sqlAddCondition(sql_cond,_add);
        END IF;

        IF _autore IS NOT NULL THEN
            _add:= E'autore ILIKE \'' || _autore || E'\' ';
            sql_cond:= promogest.sqlAddCondition(sql_cond,_add);
        END IF;

        IF _descrizione IS NOT NULL THEN
            _add:= E'descrizione ILIKE \'' || _descrizione || E'\' ';
            sql_cond:= promogest.sqlAddCondition(sql_cond,_add);
        END IF;

        IF _annotazione IS NOT NULL THEN
            _add:= E'annotazione ILIKE \'' || _annotazione || E'\' ';
            sql_cond:= promogest.sqlAddCondition(sql_cond,_add);
        END IF;
        
        IF _id_scheda IS NOT NULL THEN
            _add := 'id_scheda = ' || _id_scheda;
            sql_cond:= promogest.sqlAddCondition(sql_cond,_add);
        END IF;

        IF _riferimento IS NOT NULL THEN
            _add:= E'riferimento ILIKE \'' || _riferimento || E'\' ';
            sql_cond:= promogest.sqlAddCondition(sql_cond,_add);
        END IF;

        IF _giorni_preavviso IS NOT NULL THEN
            _add:= 'giorni_preavviso = ' || _giorni_preavviso;
            sql_cond:= promogest.sqlAddCondition(sql_cond,_add);
        END IF;
	
	IF _in_scadenza IS NOT NULL THEN
		IF _in_scadenza = True THEN
			_add:= E'in_scadenza = \'t\'';
			sql_cond:= promogest.sqlAddCondition(sql_cond,_add);
		ELSE
			_add:= E'in_scadenza = \'f\'';
			sql_cond:= promogest.sqlAddCondition(sql_cond,_add);
		END IF;
	END IF;


	IF _scaduto IS NOT NULL THEN
		IF _scaduto = True THEN
			_add:= E'scaduto = \'t\'';
			sql_cond:= promogest.sqlAddCondition(sql_cond,_add);
		ELSE
			_add:= E'scaduto = \'f\'';
			sql_cond:= promogest.sqlAddCondition(sql_cond,_add);
		END IF;
	END IF;

	IF _completato IS NOT NULL THEN
		IF _completato = True THEN
			_add:= E'completato = \'t\'';
			sql_cond:= promogest.sqlAddCondition(sql_cond,_add);
		ELSE
			_add:= E'completato = \'f\'';
			sql_cond:= promogest.sqlAddCondition(sql_cond,_add);
		END IF;
	END IF;

        IF _offset IS NULL THEN
            limitstring:= '';
        ELSE
            limitstring:= ' LIMIT ' || _count || ' OFFSET  ' || _offset;
        END IF;


        IF sql_cond != '' THEN
            sql_statement:= sql_statement || ' WHERE ' || sql_cond || ' ORDER BY ' || OrderBy || limitstring;
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
$BODY$
  LANGUAGE 'plpgsql' VOLATILE;
ALTER FUNCTION promogest.promemoriaschedasel("varchar", int8, "varchar", "timestamp", "timestamp", "timestamp", "timestamp", "varchar", "varchar", "varchar", text, text, "varchar", int4, bool, bool, bool, int8, int8, int8) OWNER TO promoadmin;

