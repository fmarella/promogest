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

stoccaggio  - Stored procedure applicativa

*/

DROP FUNCTION promogest.StoccaggioSet(varchar, bigint, bigint, integer, integer, date, date, bigint, bigint);
CREATE OR REPLACE FUNCTION promogest.StoccaggioSet(varchar, bigint, bigint, integer, integer, date, date, bigint, bigint) RETURNS promogest.resultid AS '
    DECLARE
        -- Parametri contesto
        _schema                         ALIAS FOR $1;
        _idutente                       ALIAS FOR $2;
        
        -- Parametri tabella
        _id                             ALIAS FOR $3;
        _scorta_minima                  ALIAS FOR $4;
        _livello_riordino               ALIAS FOR $5;
        _data_fine_scorte               ALIAS FOR $6;
        _data_prossimo_ordine           ALIAS FOR $7;
        _id_articolo                    ALIAS FOR $8;
        _id_magazzino                   ALIAS FOR $9;

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
        
        SELECT INTO _ret * FROM promogest.StoccaggioInsUpd(_schema, _idutente, _id, _scorta_minima, _livello_riordino, _data_fine_scorte, _data_prossimo_ordine, _id_articolo, _id_magazzino); 
        
        -- Imposta schema precedente
        sql_command:= \'SET SEARCH_PATH TO \' || schema_prec;
        EXECUTE sql_command;
        
        RETURN _ret;
    END;
' LANGUAGE plpgsql;


DROP FUNCTION promogest.StoccaggioDel(varchar, bigint, bigint);
CREATE OR REPLACE FUNCTION promogest.StoccaggioDel(varchar, bigint, bigint) RETURNS promogest.resultid AS '
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
        
        SELECT INTO _ret * FROM promogest.ObjectDel(_schema, _idutente, \'stoccaggio\', _id, \'id\');
        
        -- Imposta schema precedente
        sql_command:= \'SET SEARCH_PATH TO \' || schema_prec;
        EXECUTE sql_command;
        
        RETURN _ret;
    END;
' LANGUAGE plpgsql;

DROP FUNCTION promogest.StoccaggioGet(varchar, bigint, bigint);
DROP FUNCTION promogest.StoccaggioSel(varchar, bigint, varchar, bigint, bigint, bigint, bigint, bigint, bigint, bigint);
DROP FUNCTION promogest.StoccaggioSel(varchar, bigint, varchar, bigint, bigint, bigint, bigint);
DROP FUNCTION promogest.StoccaggioSelCount(varchar, bigint, varchar, bigint, bigint, bigint, bigint, bigint, bigint, bigint);
DROP FUNCTION promogest.StoccaggioSelCount(varchar, bigint, varchar, bigint, bigint, bigint, bigint);

DROP TYPE promogest.stoccaggio_type;
DROP TYPE promogest.stoccaggio_sel_count_type;

CREATE TYPE promogest.stoccaggio_type AS (
     id                         bigint
    ,scorta_minima              integer
    ,livello_riordino           integer
    ,data_fine_scorte           date
    ,data_prossimo_ordine       date
    ,id_articolo                bigint
    ,id_magazzino               bigint
);

DROP TYPE promogest.stoccaggio_sel_type;

CREATE TYPE promogest.stoccaggio_sel_type AS (
     id                                     bigint
    ,scorta_minima                          integer
    ,livello_riordino                       integer
    ,data_fine_scorte                       date
    ,data_prossimo_ordine                   date
    ,id_articolo                            bigint
    ,id_magazzino                           bigint
    ,codice_articolo                        varchar
    ,articolo                               varchar
    ,magazzino                              varchar
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
                                                         
CREATE TYPE promogest.stoccaggio_sel_count_type AS (
    count       bigint
);

CREATE OR REPLACE FUNCTION promogest.StoccaggioGet(varchar, bigint, bigint) RETURNS SETOF promogest.stoccaggio_type AS '
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

        FOR v_row IN SELECT * FROM stoccaggio WHERE id = _id LOOP
            RETURN NEXT v_row;
        END LOOP;

        -- Imposta schema precedente
        sql_command:= \'SET SEARCH_PATH TO \' || schema_prec;
        EXECUTE sql_command;

        RETURN;
    END;
' LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION promogest.StoccaggioSel(varchar, bigint, varchar, bigint, bigint, bigint, bigint) RETURNS SETOF promogest.stoccaggio_sel_type AS '
    DECLARE
        -- Parametri contesto
        _schema                 ALIAS FOR $1;
        _idutente               ALIAS FOR $2;
        
        -- Parametri procedura
        _orderby                ALIAS FOR $3;
        _id_articolo            ALIAS FOR $4;
        _id_magazzino           ALIAS FOR $5;
        _offset                 ALIAS FOR $6;
        _count                  ALIAS FOR $7;
        
        schema_prec             varchar(2000);
        sql_statement           varchar(2000);
        sql_cond                varchar(2000);
        limitstring             varchar(500);
        _add                    varchar(500);
        OrderBy                 varchar(200);
        v_row                   record;
        _tablename              varchar;
    BEGIN
        -- Memorizza schema precedente
        schema_prec:= ARRAY_TO_STRING(CURRENT_SCHEMAS(\'t\'),\',\');

        -- Imposta schema corrente
        sql_statement:= \'SET SEARCH_PATH TO \' || _schema;
        EXECUTE sql_statement;

        sql_statement:= \'SELECT S.* FROM v_stoccaggio_completa S \';
        sql_cond:=\'\';
        
        IF _orderby IS NULL THEN
            OrderBy = \' S.id_articolo, S.id_magazzino  \';
        ELSE
            OrderBy = _orderby;
        END IF;
        
        IF _id_articolo IS NOT NULL THEN
            _add:= \'S.id_articolo = \' || _id_articolo;
             sql_cond:= promogest.sqlAddCondition(sql_cond,_add);
        ELSE
            SELECT INTO _tablename * FROM promogest.ArticoloFilteredExists(_schema, _idutente);
            IF _tablename <> \'\' THEN
                sql_statement:= sql_statement || \' INNER JOIN \' || _tablename || \' AF ON S.id_articolo = AF.id\';
            END IF;
        END IF;
        
        IF _id_magazzino IS NOT NULL THEN
            _add:= \'S.id_magazzino = \' || _id_magazzino;
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

CREATE OR REPLACE FUNCTION promogest.StoccaggioSelCount(varchar, bigint, varchar, bigint, bigint, bigint, bigint) RETURNS SETOF promogest.stoccaggio_sel_count_type AS '
    DECLARE
        -- Parametri contesto
        _schema                 ALIAS FOR $1;
        _idutente               ALIAS FOR $2;
        
        -- Parametri procedura
        _orderby                ALIAS FOR $3;
        _id_articolo            ALIAS FOR $4;
        _id_magazzino           ALIAS FOR $5;
        _offset                 ALIAS FOR $6;
        _count                  ALIAS FOR $7;
        
        schema_prec             varchar(2000);
        sql_statement           varchar(2000);
        sql_cond                varchar(2000);
        limitstring             varchar(500);
        _add                    varchar(500);
        OrderBy                 varchar(200);
        v_row                   record;
        _tablename              varchar;
    BEGIN
        -- Memorizza schema precedente
        schema_prec:= ARRAY_TO_STRING(CURRENT_SCHEMAS(\'t\'),\',\');

        -- Imposta schema corrente
        sql_statement:= \'SET SEARCH_PATH TO \' || _schema;
        EXECUTE sql_statement;

        sql_statement:= \'SELECT COUNT(S.id) FROM v_stoccaggio_completa S \';
        sql_cond:=\'\';
        
        IF _id_articolo IS NOT NULL THEN
            _add:= \'S.id_articolo = \' || _id_articolo;
            sql_cond:= promogest.sqlAddCondition(sql_cond,_add);
        ELSE
            SELECT INTO _tablename * FROM promogest.ArticoloFilteredExists(_schema, _idutente);
            IF _tablename <> \'\' THEN
                sql_statement:= sql_statement || \' INNER JOIN \' || _tablename || \' AF ON S.id_articolo = AF.id\';
            END IF;
        END IF;
        
        IF _id_magazzino IS NOT NULL THEN
            _add:= \'S.id_magazzino = \' || _id_magazzino;
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
