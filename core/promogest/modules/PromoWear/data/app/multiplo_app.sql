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

Multiplo  - Stored procedure applicativa

*/

DROP FUNCTION promogest.MultiploSet(varchar, bigint, bigint, varchar, varchar, bigint, bigint, decimal(15,6));
CREATE OR REPLACE FUNCTION promogest.MultiploSet(varchar, bigint, bigint, varchar, varchar, bigint, bigint, decimal(15,6)) RETURNS promogest.resultid AS '
    DECLARE
        -- Parametri contesto
        _schema                     ALIAS FOR $1;
        _idutente                   ALIAS FOR $2;
        
        -- Parametri tabella
        _id                         ALIAS FOR $3;
        _denominazione_breve        ALIAS FOR $4;
        _denominazione              ALIAS FOR $5;
        _id_unita_base              ALIAS FOR $6;
        _id_articolo                ALIAS FOR $7;
        _moltiplicatore             ALIAS FOR $8;
        
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
        
        SELECT INTO _ret * FROM promogest.MultiploInsUpd(_schema, _idutente, _id, _denominazione_breve, _denominazione, _id_unita_base, _id_articolo, _moltiplicatore);
        
        -- Imposta schema precedente
        sql_command:= \'SET SEARCH_PATH TO \' || schema_prec;
        EXECUTE sql_command;
        
        RETURN _ret;
    END;
' LANGUAGE plpgsql;


DROP FUNCTION promogest.MultiploDel(varchar, bigint, bigint);
CREATE OR REPLACE FUNCTION promogest.MultiploDel(varchar, bigint, bigint) RETURNS promogest.resultid AS '
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
        schema_prec:= ARRAY_TO_STRING(CURRENT_SCHEMAS(\'t\'),\',\');
        
        -- Imposta schema corrente
        sql_command:= \'SET SEARCH_PATH TO \' || _schema;
        EXECUTE sql_command;
        
        SELECT INTO _ret * FROM promogest.ObjectDel(_schema, _idutente, \'multiplo\', _id, \'id\');
        
        -- Imposta schema precedente
        sql_command:= \'SET SEARCH_PATH TO \' || schema_prec;
        EXECUTE sql_command;
        
        RETURN _ret;
    END;
' LANGUAGE plpgsql;

DROP FUNCTION promogest.MultiploGet(varchar, bigint, bigint);
DROP FUNCTION promogest.MultiploSel(varchar, bigint, varchar, varchar, bigint, bigint, bigint, bigint);
DROP FUNCTION promogest.MultiploSelCount(varchar, bigint, varchar, varchar, bigint, bigint, bigint, bigint);

DROP TYPE promogest.multiplo_type;
DROP TYPE promogest.multiplo_sel_type;
DROP TYPE promogest.multiplo_sel_count_type;

CREATE TYPE promogest.multiplo_type AS (
     id                         bigint
    ,denominazione_breve        varchar
    ,denominazione              varchar
    ,id_unita_base              bigint
    ,id_articolo                bigint
    ,moltiplicatore             decimal(15,6)
);

CREATE TYPE promogest.multiplo_sel_type AS (
     id                                     bigint
    ,denominazione_breve                    varchar
    ,denominazione                          varchar
    ,id_unita_base                          bigint
    ,id_articolo                            bigint
    ,moltiplicatore                         decimal(15,6)
    ,codice_articolo                        varchar
    ,articolo                               varchar
    ,unita_base                             varchar
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

CREATE TYPE promogest.multiplo_sel_count_type AS (
    count       bigint
);

CREATE OR REPLACE FUNCTION promogest.MultiploGet(varchar, bigint, bigint) RETURNS SETOF promogest.multiplo_type AS '
    DECLARE
        -- Parametri contesto
        _schema                 ALIAS FOR $1;
        _idutente               ALIAS FOR $2;
        
        -- Parametri tabella
        _id                     ALIAS FOR $3;
        
        schema_prec             varchar(2000);
        sql_command             varchar(2000);
        v_row record;
    BEGIN
        -- Memorizza schema precedente
        schema_prec:= ARRAY_TO_STRING(CURRENT_SCHEMAS(\'t\'),\',\');

        -- Imposta schema corrente
        sql_command:= \'SET SEARCH_PATH TO \' || _schema;
        EXECUTE sql_command;
        
        FOR v_row IN SELECT * FROM multiplo WHERE id = _id LOOP
            RETURN NEXT v_row;
        END LOOP;
                                                                
        -- Imposta schema precedente
        sql_command:= \'SET SEARCH_PATH TO \' || schema_prec;
        EXECUTE sql_command;

        RETURN;
    END;
' LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION promogest.MultiploSel(varchar, bigint, varchar, varchar, bigint, bigint, bigint, bigint) RETURNS SETOF promogest.multiplo_sel_type AS '
    DECLARE
        -- Parametri contesto
        _schema                 ALIAS FOR $1;
        _idutente               ALIAS FOR $2;
        
        -- Parametri procedura
        _orderby                ALIAS FOR $3;
        _denominazione          ALIAS FOR $4;
        _id_articolo            ALIAS FOR $5;
        _id_unita_base          ALIAS FOR $6;
        _offset                 ALIAS FOR $7;
        _count                  ALIAS FOR $8;
        
        schema_prec             varchar(2000);
        sql_statement           varchar(2000);
        sql_cond                varchar(2000);
        limitstring             varchar(500);
        _add                    varchar(500);
        OrderBy                 varchar(200);
        v_row record;
    
        id_unita_base_articolo  bigint;
    BEGIN
        -- Memorizza schema precedente
        schema_prec:= ARRAY_TO_STRING(CURRENT_SCHEMAS(\'t\'),\',\');

        -- Imposta schema corrente
        sql_statement:= \'SET SEARCH_PATH TO \' || _schema;
        EXECUTE sql_statement;

        -- Ricavo unita base dell'' articolo selezionato
        SELECT INTO id_unita_base_articolo id_unita_base FROM articolo WHERE id = _id_articolo;

        sql_statement:= \'SELECT * FROM v_multiplo_completa \';
        sql_cond:=\'\';
            
        IF _orderby IS NULL THEN
            OrderBy = \'denominazione \';
        ELSE
            OrderBy = _orderby;
        END IF;
            
        IF _denominazione IS NOT NULL THEN
            _add:= \'denominazione ILIKE \'\'%\' || _denominazione || \'%\'\'\';
            sql_cond:= promogest.sqlAddCondition(sql_cond,_add);
        END IF;

        IF  (_id_articolo IS NULL AND _id_unita_base IS NULL) THEN
            _add:= \'id_articolo IS NULL\';
            sql_cond:= promogest.sqlAddCondition(sql_cond,_add);
        ELSE
            IF _id_articolo IS NOT NULL THEN
                _add:= \'id_articolo = \' || _id_articolo;
                sql_cond:= promogest.sqlAddCondition(sql_cond,_add);
            ELSE                    
                _add:= \'id_articolo IS NULL\';
                sql_cond:= promogest.sqlAddCondition(sql_cond,_add);
            END IF;
    
            IF _id_unita_base IS NOT NULL THEN
                _add:= \'id_unita_base = \' || _id_unita_base;
                sql_cond:= promogest.sqlAddCondition(sql_cond,_add);
            ELSE                    
                _add:= \'id_unita_base IS NULL \';
                sql_cond:= promogest.sqlAddCondition(sql_cond,_add);
            END IF;
        END IF; 

        IF id_unita_base_articolo IS NOT NULL THEN
            sql_cond:= sql_cond || \' OR ( id_unita_base = \' || id_unita_base_articolo || \' ) \';
        END IF;

        --  RAISE EXCEPTION \' % \', sql_cond;
        --  RETURN;
    
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

        --  RAISE EXCEPTION \'%\', sql_statement;

        FOR v_row IN EXECUTE sql_statement LOOP
            RETURN NEXT v_row;
        END LOOP;

        -- Imposta schema precedente
        sql_statement:= \'SET SEARCH_PATH TO \' || schema_prec;
        EXECUTE sql_statement;

        RETURN;
    END;
' LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION promogest.MultiploSelCount(varchar, bigint, varchar, varchar, bigint, bigint, bigint, bigint) RETURNS SETOF promogest.multiplo_sel_count_type AS '
    DECLARE
        -- Parametri contesto
        _schema                 ALIAS FOR $1;
        _idutente               ALIAS FOR $2;
        
        -- Parametri procedura
        _orderby                ALIAS FOR $3;
        _denominazione          ALIAS FOR $4;
        _id_articolo            ALIAS FOR $5;
        _id_unita_base          ALIAS FOR $6;
        _offset                 ALIAS FOR $7;
        _count                  ALIAS FOR $8;
        
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

        sql_statement:= \'SELECT COUNT(id) FROM v_multiplo_completa \';
        sql_cond:=\'\';
            
        IF _denominazione IS NOT NULL THEN
            _add:= \'denominazione ILIKE \'\'%\' || _denominazione || \'%\'\'\';
            sql_cond:= promogest.sqlAddCondition(sql_cond,_add);
        END IF;
        
        IF  (_id_articolo IS NULL AND _id_unita_base IS NULL) THEN
            _add:= \'id_articolo IS NULL\';
            sql_cond:= promogest.sqlAddCondition(sql_cond,_add);
        ELSE
            IF _id_articolo IS NOT NULL THEN
                _add:= \'id_articolo = \' || _id_articolo;
                sql_cond:= promogest.sqlAddCondition(sql_cond,_add);
            ELSE                    
                _add:= \'id_articolo IS NULL\';
                sql_cond:= promogest.sqlAddCondition(sql_cond,_add);
            END IF;

            IF _id_unita_base IS NOT NULL THEN
                _add:= \'id_unita_base = \' || _id_unita_base;
                sql_cond:= promogest.sqlAddCondition(sql_cond,_add);
            ELSE                    
                _add:= \'id_unita_base IS NULL \';
                sql_cond:= promogest.sqlAddCondition(sql_cond,_add);
            END IF;
        END IF; 
            
        IF _offset IS NULL THEN
            limitstring:= \'\';
        ELSE
            limitstring:= \' LIMIT \' || _count || \' OFFSET  \' || _offset;
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
