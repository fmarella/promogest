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

Procedura di ottenimento prossimo numero 

*/

DROP FUNCTION promogest.NumeroRegistroSchedaGet(varchar);
DROP FUNCTION promogest.NumeroRegistroSchedaGet(varchar, date);

DROP TYPE promogest.numero_scheda_type;

CREATE TYPE promogest.numero_scheda_type AS (
     numero     bigint
    ,registro   varchar(100)
);
                                 
-- Function: promogest.numeroregistroschedaget("varchar", date)

-- DROP FUNCTION promogest.numeroregistroschedaget("varchar", date);

CREATE OR REPLACE FUNCTION promogest.NumeroRegistroSchedaGet("varchar", date)
  RETURNS SETOF promogest.numero_scheda_type AS
$BODY$

    DECLARE
        _type           ALIAS FOR $1;
        _date           ALIAS FOR $2;
        
        sql_command     varchar(2000);
        registro        varchar(100);
        rotazione       varchar(100);
        numero          integer;
        _key            varchar(1000);
        _currentyear    char(4);
        _rotation       varchar(100);
        v_row record;
    BEGIN
        _key := _type || '.registro';
        
        SELECT INTO registro value FROM setting WHERE key = _key;

        IF registro IS NULL THEN
            RAISE EXCEPTION 'Registro numerazione schede ordinazioni non trovato';
        END IF;
        
        _key := registro || '.rotazione';

        SELECT INTO rotazione value FROM setting WHERE key = _key;
        
        IF rotazione IS NULL THEN
            RAISE EXCEPTION 'Tipologia rotazione schede ordinazioni non trovata';
        END IF;

        SELECT INTO _rotation CASE rotazione WHEN 'annuale' THEN 'year' WHEN 'mensile' THEN 'month' WHEN 'giornaliera' THEN 'day' END;

        IF _type = 'movimento' THEN
            sql_command:= 'SELECT COALESCE(MAX(SO.numero),0) + 1  AS numero, CAST(' || QUOTE_LITERAL(registro) || ' AS varchar(100)) AS registro FROM datari DT, schede_ordinazioni SO WHERE DATE_PART(' || QUOTE_LITERAL(_rotation) || ', DT.presa_in_carico) = DATE_PART(' || QUOTE_LITERAL(_rotation) || ',CAST(' || QUOTE_LITERAL(_date) || 'AS DATE))';
        ELSE
            sql_command:= 'SELECT COALESCE(MAX(SO.numero),0) + 1  AS numero, CAST(' || QUOTE_LITERAL(registro) || ' AS varchar(100)) AS registro FROM datari DT, schede_ordinazioni SO WHERE DATE_PART(''year'', DT.presa_in_carico) = DATE_PART(' || QUOTE_LITERAL(_rotation) || ',CAST(' || QUOTE_LITERAL(_date) || 'AS DATE))' ;
        END IF;
        
        FOR v_row IN EXECUTE sql_command LOOP
            RETURN NEXT v_row;
        END LOOP;
        RETURN;
    END;
$BODY$
  LANGUAGE plpgsql;

