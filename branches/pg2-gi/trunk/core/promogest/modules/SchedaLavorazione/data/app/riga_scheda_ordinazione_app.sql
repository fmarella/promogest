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
-- MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.� See the
-- GNU General Public License for more details.
--
-- You should have received a copy of the GNU General Public License
-- along with this program; if not, write to the Free Software
-- Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA� 02111-1307, USA.

/*

riga_scheda  - Stored procedure applicativa

*/

DROP FUNCTION promogest.RigaSchedaSet(varchar, bigint, bigint, decimal(16,4), decimal(16,4), decimal(16,4), decimal(15,6), varchar, decimal(8,4), varchar, bigint, bigint, bigint, bigint, varchar, bigint, text);
CREATE OR REPLACE FUNCTION promogest.RigaSchedaSet(varchar, bigint, bigint, decimal(16,4), decimal(16,4), decimal(16,4), decimal(15,6), varchar, decimal(8,4), varchar, bigint, bigint, bigint, bigint, varchar, bigint, text) RETURNS promogest.resultid AS
$$
    DECLARE
        -- Parametri contesto
        _schema                         ALIAS FOR $1;
        _idutente                       ALIAS FOR $2;
        
        -- Parametri tabella
        _id                             ALIAS FOR $3;
        _valore_unitario_netto          ALIAS FOR $4;
        _valore_unitario_lordo          ALIAS FOR $5;
        _quantita                       ALIAS FOR $6;
        _moltiplicatore                 ALIAS FOR $7;
        _applicazione_sconti            ALIAS FOR $8;
        _percentuale_iva                ALIAS FOR $9;
        _descrizione                    ALIAS FOR $10;
        _id_listino                     ALIAS FOR $11;
        _id_magazzino                   ALIAS FOR $12;
        _id_articolo                    ALIAS FOR $13;
        _id_multiplo                    ALIAS FOR $14;
        _codice_articolo                ALIAS FOR $15;
        _id_scheda                      ALIAS FOR $16;
        _dummy                          ALIAS FOR $17;

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

        SELECT INTO _ret * FROM promogest.RigaSchedaInsUpd(_schema, _idutente, _id, _valore_unitario_netto, _valore_unitario_lordo, _quantita, _moltiplicatore, _applicazione_sconti, _percentuale_iva, _descrizione, _id_listino, _id_magazzino, _id_articolo, _id_multiplo, _id_scheda, _dummy);           
        -- Imposta schema precedente
        sql_command:= 'SET SEARCH_PATH TO ' || schema_prec;
        EXECUTE sql_command;
        
        RETURN _ret;
    END;
$$ LANGUAGE plpgsql;


DROP FUNCTION promogest.RigaSchedaDel(varchar, bigint, bigint);
CREATE OR REPLACE FUNCTION promogest.RigaSchedaDel(varchar, bigint, bigint) RETURNS promogest.resultid AS 
$$
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
        schema_prec:= ARRAY_TO_STRING(CURRENT_SCHEMAS('t'),',');

        -- Imposta schema corrente
        sql_command:= 'SET SEARCH_PATH TO ' || _schema;
        EXECUTE sql_command;
        
        SELECT INTO _ret * FROM promogest.ObjectDel(_schema, _idutente, 'riga', _id, 'id');
        
        -- Imposta schema precedente
        sql_command:= 'SET SEARCH_PATH TO ' || schema_prec;
        EXECUTE sql_command;
        
        RETURN _ret;
    END;
$$ LANGUAGE plpgsql;

DROP FUNCTION promogest.RigheSchedaDel(varchar, bigint, bigint);
CREATE OR REPLACE FUNCTION promogest.RigheSchedaDel(varchar, bigint, bigint) RETURNS promogest.resultid AS 
$$
    DECLARE
        -- Parametri contesto
        _schema                     ALIAS FOR $1;
        _idutente                   ALIAS FOR $2;
        
        -- Parametri tabella
        _id_scheda                  ALIAS FOR $3;
        
        schema_prec                 varchar(2000);
        sql_command                 varchar(2000);
        _ret                        promogest.resultid;
        _rec                        record;
        _id_testata_movimento       bigint;
    BEGIN
        -- Memorizza schema precedente
        schema_prec:= ARRAY_TO_STRING(CURRENT_SCHEMAS('t'),',');

        -- Imposta schema corrente
        sql_command:= 'SET SEARCH_PATH TO ' || _schema;
        EXECUTE sql_command;

        -- Cancello righe dalla scheda ordinazione
        DELETE FROM riga WHERE id IN (SELECT id FROM righe_schede_ordinazioni WHERE id_scheda = _id_scheda);
        DELETE FROM righe_schede_ordinazioni WHERE id_scheda = _id_scheda;
                    
        -- Imposta schema precedente
        sql_command:= 'SET SEARCH_PATH TO ' || schema_prec;
        EXECUTE sql_command;
        
        RETURN _ret;
    END;
$$ LANGUAGE plpgsql;

DROP FUNCTION promogest.RigaSchedaGet(varchar, bigint, bigint);
DROP FUNCTION promogest.RigaSchedaSel(varchar, bigint, varchar, bigint, bigint, bigint);
DROP FUNCTION promogest.RigaSchedaSelCount(varchar, bigint, varchar, bigint, bigint, bigint);

DROP TYPE promogest.riga_scheda_type;
DROP TYPE promogest.riga_scheda_sel_type;
DROP TYPE promogest.riga_scheda_sel_count_type;

CREATE TYPE promogest.riga_scheda_type AS (
     id                         bigint
    ,valore_unitario_netto      decimal(16,4)
    ,valore_unitario_lordo      decimal(16,4)
    ,quantita                   decimal(16,4)
    ,moltiplicatore             decimal(15,6)
    ,applicazione_sconti        varchar(20)
    ,percentuale_iva            decimal(8,4)
    ,descrizione                varchar(100)
    ,id_listino                 bigint
    ,id_magazzino               bigint
    ,id_articolo                bigint
    ,id_multiplo                bigint
    ,codice_articolo            varchar
    ,id_scheda                  bigint 
    ,tipo_riga                  text
);

CREATE TYPE promogest.riga_scheda_sel_type AS (
     id                                     bigint
    ,valore_unitario_netto                  decimal
    ,valore_unitario_lordo                  decimal
    ,quantita                               decimal
    ,moltiplicatore                         decimal
    ,applicazione_sconti                    varchar
    ,percentuale_iva                        decimal
    ,descrizione                            varchar
    ,id_listino                             bigint
    ,id_magazzino                           bigint
    ,id_articolo                            bigint
    ,id_multiplo                            bigint
    ,id_scheda                              bigint 
    ,listino                                varchar
    ,magazzino                              varchar
    ,multiplo                               varchar
    ,codice_articolo                        varchar
    ,unita_base                             varchar
    ,tipo_riga                              text
);


CREATE TYPE promogest.riga_scheda_sel_count_type AS (
    count       bigint
);

CREATE OR REPLACE FUNCTION promogest.RigaSchedaGet(varchar, bigint, bigint) RETURNS SETOF promogest.riga_scheda_type AS 
$$
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
        schema_prec:= ARRAY_TO_STRING(CURRENT_SCHEMAS('t'),',');

        -- Imposta schema corrente
        sql_command:= 'SET SEARCH_PATH TO ' || _schema;
        EXECUTE sql_command;

        FOR v_row IN SELECT * FROM v_riga_scheda WHERE id = _id LOOP
            RETURN NEXT v_row;
        END LOOP;
                                                                
        -- Imposta schema precedente
        sql_command:= 'SET SEARCH_PATH TO ' || schema_prec;
        EXECUTE sql_command;

        RETURN;
    END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION promogest.RigaSchedaSel(varchar, bigint, varchar, bigint, bigint, bigint) RETURNS SETOF promogest.riga_scheda_type AS 
$$
    DECLARE
        -- Parametri contesto
        _schema                     ALIAS FOR $1;
        _idutente                   ALIAS FOR $2;
        
        -- Parametri procedura
        _orderby                    ALIAS FOR $3;
        _id_scheda                  ALIAS FOR $4;
        _offset                     ALIAS FOR $5;
        _count                      ALIAS FOR $6;
        
        schema_prec                 varchar(2000);
        sql_statement               varchar(2000);
        sql_cond                    varchar(2000);
        limitstring                 varchar(500);
        _add                        varchar(500);
        OrderBy                     varchar(200);
        v_row                       record;
    BEGIN
        -- Memorizza schema precedente
        schema_prec:= ARRAY_TO_STRING(CURRENT_SCHEMAS('t'),',');

        -- Imposta schema corrente
        sql_statement:= 'SET SEARCH_PATH TO ' || _schema;
        EXECUTE sql_statement;

        sql_statement:= 'SELECT * FROM v_riga_scheda ';
        sql_cond:='';
        
        IF _orderby IS NULL THEN
            OrderBy = ' id  ';
        ELSE
            OrderBy = _orderby;
        END IF;
        
        IF _id_scheda IS NOT NULL THEN
            _add:= 'id_scheda = ' || _id_scheda;
            sql_cond:= promogest.sqlAddCondition(sql_cond,_add);
        ELSE                    
            _add:= 'id_scheda IS NULL ';
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

--      RAISE EXCEPTION '%', sql_statement;
--      RETURN;

        FOR v_row IN EXECUTE sql_statement LOOP
            RETURN NEXT v_row;
        END LOOP;

        -- Imposta schema precedente
        sql_statement:= 'SET SEARCH_PATH TO ' || schema_prec;
        EXECUTE sql_statement;

        RETURN;
    END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION promogest.RigaSchedaSelCount(varchar, bigint, varchar, bigint, bigint, bigint) RETURNS SETOF promogest.riga_scheda_sel_count_type AS 
$$
    DECLARE
        -- Parametri contesto
        _schema                     ALIAS FOR $1;
        _idutente                   ALIAS FOR $2;
        
        -- Parametri procedura
        _orderby                    ALIAS FOR $3;
        _id_scheda                  ALIAS FOR $4;
        _offset                     ALIAS FOR $5;
        _count                      ALIAS FOR $6;
        
        schema_prec                 varchar(2000);
        sql_statement               varchar(2000);
        sql_cond                    varchar(2000);
        limitstring                 varchar(500);
        _add                        varchar(500);
        OrderBy                     varchar(200);
        v_row                       record;
    BEGIN
        -- Memorizza schema precedente
        schema_prec:= ARRAY_TO_STRING(CURRENT_SCHEMAS('t'),',');

        -- Imposta schema corrente
        sql_statement:= 'SET SEARCH_PATH TO ' || _schema;
        EXECUTE sql_statement;

        sql_statement:= 'SELECT COUNT(id) FROM v_riga_scheda ';
        sql_cond:='';

        IF _id_scheda IS NOT NULL THEN
            _add:= 'id_scheda = ' || _id_scheda;
            sql_cond:= promogest.sqlAddCondition(sql_cond,_add);
        ELSE                    
            _add:= 'id_scheda IS NULL ';
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
