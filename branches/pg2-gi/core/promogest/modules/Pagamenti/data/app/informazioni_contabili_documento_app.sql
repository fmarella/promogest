--
-- Copyright (C) 2005 by Promotux Informatica - http://www.promotux.it/
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

Informazioni Contabili Documento  - Stored procedure applicativa

*/

DROP FUNCTION promogest.InformazioniContabiliDocumentoSet(varchar, bigint, boolean, bigint, bigint, bigint, decimal(16,4), decimal(16,4));

CREATE OR REPLACE FUNCTION promogest.InformazioniContabiliDocumentoSet(varchar, bigint, bigint, boolean, bigint, bigint, bigint, decimal(16,4), decimal(16,4)) RETURNS promogest.resultid AS E'
    DECLARE
        -- Parametri contesto
        _schema                         ALIAS FOR $1;
        _idutente                       ALIAS FOR $2;
        
        -- Parametri tabella
        _id                             ALIAS FOR $3;
        _documento_saldato              ALIAS FOR $4;
        _id_documento                   ALIAS FOR $5;
        _id_primo_riferimento           ALIAS FOR $6;
        _id_secondo_riferimento         ALIAS FOR $7;
        _totale_pagato                  ALIAS FOR $8;
        _totale_sospeso                 ALIAS FOR $9;


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

        SELECT INTO _ret * FROM promogest.InformazioniContabiliDocumentoInsUpd(_schema, _idutente, _id, _documento_saldato, _id_documento, _id_primo_riferimento, _id_secondo_riferimento, _totale_pagato, _totale_sospeso);

        -- Imposta schema precedente
        sql_command:= \'SET SEARCH_PATH TO \' || schema_prec;
        EXECUTE sql_command;
                        
    RETURN _ret;
END;
' LANGUAGE plpgsql;

DROP FUNCTION promogest.InformazioniContabiliDocumentoDel(varchar, bigint, bigint);
CREATE OR REPLACE FUNCTION promogest.InformazioniContabiliDocumentoDel(varchar, bigint, bigint) RETURNS promogest.resultid AS E'
    DECLARE
        -- Parametri contesto
        _schema                 ALIAS FOR $1;
        _idutente               ALIAS FOR $2;
        
        -- Parametri tabella
        _id_documento                ALIAS FOR $3;
        
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
        
       DELETE FROM informazioni_contabili_documento WHERE id_documento = _id_documento ;

        -- Imposta schema precedente
        sql_command:= \'SET SEARCH_PATH TO \' || schema_prec;
        EXECUTE sql_command;
        
        RETURN _ret;
    END;
' LANGUAGE plpgsql;

DROP FUNCTION promogest.InformazioniContabiliDocumentoGet(varchar, bigint, bigint);
DROP FUNCTION promogest.InformazioniContabiliDocumentoSel(varchar, bigint, varchar, bigint, bigint, bigint);

DROP TYPE promogest.informazioni_contabili_documento_type CASCADE;

CREATE TYPE promogest.informazioni_contabili_documento_type AS (
     id                         bigint
    ,documento_saldato          boolean
    ,id_documento               bigint
    ,id_primo_riferimento       bigint
    ,id_secondo_riferimento     bigint
    ,totale_pagato              decimal(16,4)
    ,totale_sospeso             decimal(16,4)
);


CREATE OR REPLACE FUNCTION promogest.InformazioniContabiliDocumentoGet(varchar, bigint, bigint) RETURNS SETOF promogest.informazioni_contabili_documento_type AS E'
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

        FOR v_row IN SELECT * FROM v_informazioni_contabili_documento WHERE id_documento = _id LOOP
            RETURN NEXT v_row;
        END LOOP;

        -- Imposta schema precedente
        sql_command:= \'SET SEARCH_PATH TO \' || schema_prec;
        EXECUTE sql_command;

        RETURN;
    END;
' LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION promogest.InformazioniContabiliDocumentoSel(varchar, bigint, varchar, bigint, bigint, bigint) RETURNS SETOF promogest.informazioni_contabili_documento_type AS E'
    DECLARE
        -- Parametri contesto
        _schema                     ALIAS FOR $1;
        _idutente                   ALIAS FOR $2;
        
        -- Parametri procedura
        _orderby                ALIAS FOR $3;
        _id_documento           ALIAS FOR $4;
        _offset                 ALIAS FOR $5;
        _count                  ALIAS FOR $6;

        
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

        sql_statement:= \'SELECT * FROM v_informazioni_contabili_documento \';
        sql_cond:=\'\';
        
        IF _id_documento IS NOT NULL THEN
            _add:= \'id_documento = \' || _id_documento;
            sql_cond:= promogest.sqlAddCondition(sql_cond,_add);
        ELSE                    
            _add:= \'id_documento IS NULL \';
            sql_cond:= promogest.sqlAddCondition(sql_cond,_add);
        END IF;

        IF _orderby IS NULL THEN
            OrderBy = \' id_documento \';
        ELSE
            OrderBy = _orderby;
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

        FOR v_row IN EXECUTE sql_statement LOOP
            RETURN NEXT v_row;
        END LOOP;

        -- Imposta schema precedente
        sql_statement:= \'SET SEARCH_PATH TO \' || schema_prec;
        EXECUTE sql_statement;

        RETURN;
    END;
' LANGUAGE plpgsql;

