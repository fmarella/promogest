--
-- Copyright (C) 2007 by Promotux Informatica - http://www.promotux.it/
-- Author: JJDaNiMoTh <jjdanimoth@gmail.com>
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

testata_documento_scadenza  - Stored procedure applicativa

*/

DROP FUNCTION promogest.TestataDocumentoScadenzaSet(varchar, bigint, bigint, bigint, decimal(16,4), decimal(16,4), date, decimal(16,4), date, decimal(16,4), varchar, date, date, decimal(16,4), varchar, date, date, decimal(16,4), varchar, date, date, decimal(16,4), varchar, date, boolean);

CREATE OR REPLACE FUNCTION promogest.TestataDocumentoScadenzaSet(varchar, bigint, bigint, bigint, date, decimal(16,4), varchar, date, bigint) RETURNS promogest.resultid AS E'
    DECLARE
        -- Parametri contesto
        _schema                         ALIAS FOR $1;
        _idutente                       ALIAS FOR $2;
        
        -- Parametri tabella
        _id                             ALIAS FOR $3;
        _id_testata_documento           ALIAS FOR $4;
        _data                           ALIAS FOR $5;
        _importo                        ALIAS FOR $6;
        _pagamento                      ALIAS FOR $7;
        _data_pagamento                 ALIAS FOR $8;
        _numero_scadenza                ALIAS FOR $9;
        
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

        SELECT INTO _ret * FROM promogest.TestataDocumentoScadenzaInsUpd(_schema, _idutente, _id, _id_testata_documento, _data, _importo, _pagamento, _data_pagamento, _numero_scadenza);
        
        -- Imposta schema precedente
        sql_command:= \'SET SEARCH_PATH TO \' || schema_prec;
        EXECUTE sql_command;
        
        RETURN _ret;
    END;
' LANGUAGE plpgsql;


DROP FUNCTION promogest.TestataDocumentoScadenzaDel(varchar, bigint, bigint);
CREATE OR REPLACE FUNCTION promogest.TestataDocumentoScadenzaDel(varchar, bigint, bigint) RETURNS promogest.resultid AS E'
    DECLARE
        -- Parametri contesto
        _schema                 ALIAS FOR $1;
        _idutente               ALIAS FOR $2;
        
        -- Parametri tabella
        _id_testata_documento   ALIAS FOR $3;
        
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
        
       DELETE FROM testata_documento_scadenza WHERE id_testata_documento = _id_testata_documento;

        -- Imposta schema precedente
        sql_command:= \'SET SEARCH_PATH TO \' || schema_prec;
        EXECUTE sql_command;
        
        RETURN _ret;
    END;
' LANGUAGE plpgsql;

DROP FUNCTION promogest.TestataDocumentoScadenzaGet(varchar, bigint, bigint);
DROP FUNCTION promogest.TestataDocumentoScadenzaSel(varchar, bigint, varchar, bigint, bigint, bigint);
DROP FUNCTION promogest.TestataDocumentoScadenzaSelCount(varchar, bigint, varchar, bigint, bigint, bigint);

DROP TYPE promogest.testata_documento_scadenza_type;
DROP TYPE promogest.testata_documento_scadenza_sel_type;
DROP TYPE promogest.testata_documento_scadenza_sel_count_type;

CREATE TYPE promogest.testata_documento_scadenza_type AS (
     id                             bigint
     ,id_testata_documento          bigint
     ,data                          date
     ,importo                       decimal(16,4)
     ,pagamento                     varchar
     ,data_pagamento                date
     ,numero_scadenza               bigint
);

CREATE TYPE promogest.testata_documento_scadenza_sel_type AS (
     id                             bigint
     ,id_testata_documento          bigint
     ,data                          date
     ,importo                       decimal(16,4)
     ,pagamento                     varchar
     ,data_pagamento                date
     ,numero_scadenza               bigint
);

CREATE TYPE promogest.testata_documento_scadenza_sel_count_type AS (
    count       bigint
);

CREATE OR REPLACE FUNCTION promogest.TestataDocumentoScadenzaGet(varchar, bigint, bigint) RETURNS SETOF promogest.testata_documento_scadenza_type AS E'
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

        FOR v_row IN SELECT * FROM v_testata_documento_scadenza WHERE id = _id LOOP
            RETURN NEXT v_row;
        END LOOP;
                                                                
        -- Imposta schema precedente
        sql_command:= \'SET SEARCH_PATH TO \' || schema_prec;
        EXECUTE sql_command;

        RETURN;
    END;
' LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION promogest.TestataDocumentoScadenzaSel(varchar, bigint, varchar, bigint, bigint, bigint) RETURNS SETOF promogest.testata_documento_scadenza_sel_type AS E'
    DECLARE
        -- Parametri contesto
        _schema                     ALIAS FOR $1;
        _idutente                   ALIAS FOR $2;
        
        -- Parametri procedura
        _orderby                    ALIAS FOR $3;
        _id_testata_documento       ALIAS FOR $4;
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
        schema_prec:= ARRAY_TO_STRING(CURRENT_SCHEMAS(\'t\'),\',\');

        -- Imposta schema corrente
        sql_statement:= \'SET SEARCH_PATH TO \' || _schema;
        EXECUTE sql_statement;

        sql_statement:= \'SELECT * FROM v_testata_documento_scadenza \';
        sql_cond:=\'\';
        
        IF _orderby IS NULL THEN
            OrderBy = \'id \';
        ELSE
            OrderBy = _orderby;
        END IF;
        
        IF _id_testata_documento IS NOT NULL THEN
            _add:= \'id_testata_documento = \' || _id_testata_documento;
            sql_cond:= promogest.sqlAddCondition(sql_cond,_add);
        ELSE                    
            _add:= \'id_testata_documento IS NULL \';
            sql_cond:= promogest.sqlAddCondition(sql_cond,_add);
        END IF;
                
        IF _offset IS NULL THEN
            limitstring:= \'\';
        ELSE
            limitstring:= \' LIMIT \' || _count || \' OFFSET  \' || _offset;
        END IF;
        
        IF sql_cond != \'\' THEN
            sql_statement:= sql_statement || \' WHERE \' || sql_cond || \' ORDER BY \' || OrderBy || limitstring;
        ELSE
            sql_statement:= sql_statement || \' ORDER BY \' || OrderBy || limitstring;
        END IF;

--        RAISE EXCEPTION \'%\', sql_statement;
--       RETURN;

        FOR v_row IN EXECUTE sql_statement LOOP
            RETURN NEXT v_row;
        END LOOP;

        -- Imposta schema precedente
        sql_statement:= \'SET SEARCH_PATH TO \' || schema_prec;
        EXECUTE sql_statement;

        RETURN;
    END;
' LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION promogest.TestataDocumentoScadenzaSelCount(varchar, bigint, varchar, bigint, bigint, bigint) RETURNS SETOF promogest.testata_documento_scadenza_sel_count_type AS E'
    DECLARE
        -- Parametri contesto
        _schema                     ALIAS FOR $1;
        _idutente                   ALIAS FOR $2;
        
        -- Parametri procedura
        _orderby                    ALIAS FOR $3;
        _id_testata_documento       ALIAS FOR $4;
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
        schema_prec:= ARRAY_TO_STRING(CURRENT_SCHEMAS(\'t\'),\',\');

        -- Imposta schema corrente
        sql_statement:= \'SET SEARCH_PATH TO \' || _schema;
        EXECUTE sql_statement;

        sql_statement:= \'SELECT COUNT(id) FROM v_testata_documento_scadenza \';
        sql_cond:=\'\';

        IF _id_testata_documento IS NOT NULL THEN
            _add:= \'id_testata_documento = \' || _id_testata_documento;
            sql_cond:= promogest.sqlAddCondition(sql_cond,_add);
        ELSE                    
            _add:= \'id_testata_documento IS NULL \';
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
