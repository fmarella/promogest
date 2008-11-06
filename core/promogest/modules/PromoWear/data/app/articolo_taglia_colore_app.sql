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

articolo_taglia_colore app  - Stored procedure applicativa

*/

DROP FUNCTION promogest.ArticoloTagliaColoreSet(varchar, bigint, bigint, bigint, bigint, bigint, bigint);
DROP FUNCTION promogest.ArticoloTagliaColoreSet(varchar, bigint, bigint, bigint, bigint, bigint, bigint, bigint, bigint, bigint);
CREATE OR REPLACE FUNCTION promogest.ArticoloTagliaColoreSet(varchar, bigint, bigint, bigint, bigint, bigint, bigint, bigint, bigint, bigint) RETURNS promogest.resultid AS '
    DECLARE
        -- Parametri contesto
        _schema                     ALIAS FOR $1;
        _idutente                   ALIAS FOR $2;
        
        -- Parametri tabella
        _id_articolo                ALIAS FOR $3;
        _id_articolo_padre          ALIAS FOR $4;
        _id_gruppo_taglia           ALIAS FOR $5;
        _id_taglia                  ALIAS FOR $6;
        _id_colore                  ALIAS FOR $7;
        _id_anno                    ALIAS FOR $8;
        _id_stagione                ALIAS FOR $9;
        _id_genere                  ALIAS FOR $10;

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
        
        SELECT INTO _ret * FROM promogest.ArticoloTagliaColoreInsUpd(_schema, _idutente, _id_articolo, _id_articolo_padre, _id_gruppo_taglia, _id_taglia, _id_colore, _id_anno, _id_stagione, _id_genere); 
        
        -- Imposta schema precedente
        sql_command:= \'SET SEARCH_PATH TO \' || schema_prec;
        EXECUTE sql_command;
        
        RETURN _ret;
    END;
' LANGUAGE plpgsql;


DROP FUNCTION promogest.ArticoloTagliaColoreDel(varchar, bigint, bigint);
CREATE OR REPLACE FUNCTION promogest.ArticoloTagliaColoreDel(varchar, bigint, bigint) RETURNS promogest.resultid AS '
    DECLARE
        -- Parametri contesto
        _schema                 ALIAS FOR $1;
        _idutente               ALIAS FOR $2;
        
        -- Parametri tabella
        _id_articolo            ALIAS FOR $3;
        
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
        
        SELECT INTO _ret * FROM promogest.ObjectDel(_schema, _idutente, \'articolo_taglia_colore\', _id_articolo, \'id_articolo\');
        
        -- Imposta schema precedente
        sql_command:= \'SET SEARCH_PATH TO \' || schema_prec;
        EXECUTE sql_command;
        
        RETURN _ret;
    END;
' LANGUAGE plpgsql;

DROP FUNCTION promogest.ArticoloTagliaColoreGet(varchar, bigint, bigint);
DROP FUNCTION promogest.ArticoloTagliaColoreSel(varchar, bigint, varchar, bigint, bigint, bigint, bigint, bigint, bigint);
DROP FUNCTION promogest.ArticoloTagliaColoreSel(varchar, bigint, varchar, bigint, bigint, bigint, bigint, bigint, bigint, bigint, bigint, bigint, bigint);
DROP FUNCTION promogest.ArticoloTagliaColoreSelCount(varchar, bigint, varchar, bigint, bigint, bigint);
DROP FUNCTION promogest.ArticoloTagliaColoreSelCount(varchar, bigint, varchar, bigint, bigint, bigint, bigint, bigint, bigint, bigint, bigint, bigint, bigint);

DROP TYPE promogest.articolo_taglia_colore_type;
DROP TYPE promogest.articolo_taglia_colore_sel_type;
DROP TYPE promogest.articolo_taglia_colore_sel_count_type;

CREATE TYPE promogest.articolo_taglia_colore_type AS (
     id_articolo                    bigint
    ,id_articolo_padre              bigint
    ,id_gruppo_taglia               bigint
    ,id_taglia                      bigint
    ,id_colore                      bigint
    ,id_anno                        bigint
    ,id_stagione                    bigint
    ,id_genere                      bigint
);

CREATE TYPE promogest.articolo_taglia_colore_sel_type AS (
     id_articolo                            bigint
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

CREATE TYPE promogest.articolo_taglia_colore_sel_count_type AS (
    count       bigint
);

CREATE OR REPLACE FUNCTION promogest.ArticoloTagliaColoreGet(varchar, bigint, bigint) RETURNS SETOF promogest.articolo_taglia_colore_type AS '
    DECLARE
        -- Parametri contesto
        _schema                 ALIAS FOR $1;
        _idutente               ALIAS FOR $2;
        
        -- Parametri tabella
        _id_articolo            ALIAS FOR $3;
        
        schema_prec             varchar(2000);
        sql_command             varchar(2000);
        v_row                   record;
    BEGIN
        -- Memorizza schema precedente
        schema_prec:= ARRAY_TO_STRING(CURRENT_SCHEMAS(\'t\'),\',\');

        -- Imposta schema corrente
        sql_command:= \'SET SEARCH_PATH TO \' || _schema;
        EXECUTE sql_command;
        
        FOR v_row IN SELECT * FROM articolo_taglia_colore WHERE id_articolo = _id_articolo LOOP
            RETURN NEXT v_row;
        END LOOP;

        -- Imposta schema precedente
        sql_command:= \'SET SEARCH_PATH TO \' || schema_prec;
        EXECUTE sql_command;

        RETURN;
    END;
' LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION promogest.ArticoloTagliaColoreSel(varchar, bigint, varchar, bigint, bigint, bigint, bigint, bigint, bigint, bigint, bigint, bigint, bigint) RETURNS SETOF promogest.articolo_taglia_colore_sel_type AS '
    DECLARE
        -- Parametri contesto
        _schema                     ALIAS FOR $1;
        _idutente                   ALIAS FOR $2;
        
        -- Parametri procedura
        _orderby                    ALIAS FOR $3;
        _id_articolo                ALIAS FOR $4;
        _id_articolo_padre          ALIAS FOR $5;
        _id_gruppo_taglia           ALIAS FOR $6;
        _id_taglia                  ALIAS FOR $7;
        _id_colore                  ALIAS FOR $8;
        _id_anno                    ALIAS FOR $9;
        _id_stagione                ALIAS FOR $10;
        _id_genere                  ALIAS FOR $11;
        _offset                     ALIAS FOR $12;
        _count                      ALIAS FOR $13;
        
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

        sql_statement:= \'SELECT * FROM v_articolo_taglia_colore_completa \';
        sql_cond:=\'\';
        
        IF _orderby IS NULL THEN
            OrderBy = \'id \';
        ELSE
            OrderBy = _orderby;
        END IF;
        
        IF _id_articolo IS NOT NULL THEN
            _add:= \'id_articolo = \' || _id_articolo;
            sql_cond:= promogest.sqlAddCondition(sql_cond,_add);
        END IF;
        
        IF _id_articolo_padre IS NOT NULL THEN
            _add:= \'id_articolo_padre = \' || _id_articolo_padre;
            sql_cond:= promogest.sqlAddCondition(sql_cond,_add);
        END IF;
        
        IF _id_gruppo_taglia IS NOT NULL THEN
            _add:= \'id_gruppo_taglia = \' || _id_gruppo_taglia;
            sql_cond:= promogest.sqlAddCondition(sql_cond,_add);
        END IF;
        
        IF _id_taglia IS NOT NULL THEN
            _add:= \'id_taglia = \' || _id_taglia;
            sql_cond:= promogest.sqlAddCondition(sql_cond,_add);
        END IF;
        
        IF _id_colore IS NOT NULL THEN
            _add:= \'id_colore = \' || _id_colore;
            sql_cond:= promogest.sqlAddCondition(sql_cond,_add);
        END IF;

        IF _id_anno IS NOT NULL THEN
            _add:= \'id_anno = \' || _id_anno;
            sql_cond:= promogest.sqlAddCondition(sql_cond,_add);
        END IF;

        IF _id_stagione IS NOT NULL THEN
            _add:= \'id_stagione = \' || _id_stagione;
            sql_cond:= promogest.sqlAddCondition(sql_cond,_add);
        END IF;

        IF _id_genere IS NOT NULL THEN
            _add:= \'id_genere = \' || _id_genere;
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

CREATE OR REPLACE FUNCTION promogest.ArticoloTagliaColoreSelCount(varchar, bigint, varchar, bigint, bigint, bigint, bigint, bigint, bigint, bigint, bigint, bigint, bigint) RETURNS SETOF promogest.articolo_taglia_colore_sel_count_type AS '
    DECLARE
        -- Parametri contesto
        _schema                     ALIAS FOR $1;
        _idutente                   ALIAS FOR $2;
        
        -- Parametri procedura
        _orderby                    ALIAS FOR $3;
        _id_articolo                ALIAS FOR $4;
        _id_articolo_padre          ALIAS FOR $5;
        _id_gruppo_taglia           ALIAS FOR $6;
        _id_taglia                  ALIAS FOR $7;
        _id_colore                  ALIAS FOR $8;
        _id_anno                    ALIAS FOR $9;
        _id_stagione                ALIAS FOR $10;
        _id_genere                  ALIAS FOR $11;
        _offset                     ALIAS FOR $12;
        _count                      ALIAS FOR $13;
        
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

        sql_statement:= \'SELECT COUNT(id) FROM v_articolo_taglia_colore \';
        sql_cond:=\'\';
        
        IF _orderby IS NULL THEN
            OrderBy = \'id \';
        ELSE
            OrderBy = _orderby;
        END IF;
        
        IF _id_articolo IS NOT NULL THEN
            _add:= \'id_articolo = \' || _id_articolo;
            sql_cond:= promogest.sqlAddCondition(sql_cond,_add);
        END IF;
        
        IF _id_articolo_padre IS NOT NULL THEN
            _add:= \'id_articolo_padre = \' || _id_articolo_padre;
            sql_cond:= promogest.sqlAddCondition(sql_cond,_add);
        END IF;
        
        IF _id_gruppo_taglia IS NOT NULL THEN
            _add:= \'id_gruppo_taglia = \' || _id_gruppo_taglia;
            sql_cond:= promogest.sqlAddCondition(sql_cond,_add);
        END IF;
        
        IF _id_taglia IS NOT NULL THEN
            _add:= \'id_taglia = \' || _id_taglia;
            sql_cond:= promogest.sqlAddCondition(sql_cond,_add);
        END IF;
        
        IF _id_colore IS NOT NULL THEN
            _add:= \'id_colore = \' || _id_colore;
            sql_cond:= promogest.sqlAddCondition(sql_cond,_add);
        END IF;

        IF _id_anno IS NOT NULL THEN
            _add:= \'id_anno = \' || _id_anno;
            sql_cond:= promogest.sqlAddCondition(sql_cond,_add);
        END IF;

        IF _id_stagione IS NOT NULL THEN
            _add:= \'id_stagione = \' || _id_stagione;
            sql_cond:= promogest.sqlAddCondition(sql_cond,_add);
        END IF;

        IF _id_genere IS NOT NULL THEN
            _add:= \'id_genere = \' || _id_genere;
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
