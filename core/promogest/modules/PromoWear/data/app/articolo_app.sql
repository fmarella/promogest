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
-- MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
-- GNU General Public License for more details.
--
-- You should have received a copy of the GNU General Public License
-- along with this program; if not, write to the Free Software
-- Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.

/*

articolo  - Stored procedure applicativa

*/

DROP FUNCTION promogest.ArticoloSet(varchar, bigint, bigint, varchar, varchar, bigint, bigint, bigint, bigint, varchar, varchar, real, real, real, varchar, real, varchar, real, bigint, decimal(8,4), boolean, varchar, varchar, boolean, varchar, boolean, timestamp, text, boolean, boolean, bigint);
CREATE OR REPLACE FUNCTION promogest.ArticoloSet(varchar, bigint, bigint, varchar, varchar, bigint, bigint, bigint, bigint, varchar, varchar, real, real, real, varchar, real, varchar, real, bigint, decimal(8,4), boolean, varchar, varchar, boolean, varchar, boolean, timestamp, text, boolean, boolean, bigint) RETURNS promogest.resultid AS '
    DECLARE
        -- Parametri contesto
        _schema                         ALIAS FOR $1;
        _idutente                       ALIAS FOR $2;
        
        -- Parametri tabella
        _id                             ALIAS FOR $3;
        _codice                         ALIAS FOR $4;
        _denominazione                  ALIAS FOR $5;
        _id_aliquota_iva                ALIAS FOR $6;
        _id_famiglia_articolo           ALIAS FOR $7;
        _id_categoria_articolo          ALIAS FOR $8;
        _id_unita_base                  ALIAS FOR $9;
        _produttore                     ALIAS FOR $10;
        _unita_dimensioni               ALIAS FOR $11;
        _lunghezza                      ALIAS FOR $12;
        _larghezza                      ALIAS FOR $13;
        _altezza                        ALIAS FOR $14;
        _unita_volume                   ALIAS FOR $15;
        _volume                         ALIAS FOR $16;
        _unita_peso                     ALIAS FOR $17;
        _peso_lordo                     ALIAS FOR $18;
        _id_imballaggio                 ALIAS FOR $19;
        _peso_imballaggio               ALIAS FOR $20;
        _stampa_etichetta               ALIAS FOR $21;
        _codice_etichetta               ALIAS FOR $22;
        _descrizione_etichetta          ALIAS FOR $23;
        _stampa_listino                 ALIAS FOR $24;
        _descrizione_listino            ALIAS FOR $25;
        _aggiornamento_listino_auto     ALIAS FOR $26;
        _timestamp_variazione           ALIAS FOR $27;
        _note                           ALIAS FOR $28;
        _cancellato                     ALIAS FOR $29;
        _sospeso                        ALIAS FOR $30;
        _id_stato_articolo              ALIAS FOR $31;
        
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
        
        SELECT INTO _ret * FROM promogest.ArticoloInsUpd(_schema, _idutente, _id, _codice, _denominazione, _id_aliquota_iva, _id_famiglia_articolo, _id_categoria_articolo, _id_unita_base, _produttore, _unita_dimensioni, _lunghezza, _larghezza, _altezza, _unita_volume, _volume,  _unita_peso, _peso_lordo, _id_imballaggio, _peso_imballaggio, _stampa_etichetta, _codice_etichetta, _descrizione_etichetta, _stampa_listino, _descrizione_listino, _aggiornamento_listino_auto, _timestamp_variazione, _note, _cancellato, _sospeso, _id_stato_articolo);
        sql_command:= \'SET SEARCH_PATH TO \' || schema_prec;
        EXECUTE sql_command;
        
        RETURN _ret;
    END;
' LANGUAGE plpgsql;


DROP FUNCTION promogest.ArticoloDel(varchar, bigint, bigint);
CREATE OR REPLACE FUNCTION promogest.ArticoloDel(varchar, bigint, bigint) RETURNS promogest.resultid AS '
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
        
        SELECT INTO _ret * FROM promogest.ObjectDel(_schema, _idutente, \'articolo\', _id, \'id\');
        
        -- Imposta schema precedente
        sql_command:= \'SET SEARCH_PATH TO \' || schema_prec;
        EXECUTE sql_command;
        
        RETURN _ret;
    END;
' LANGUAGE plpgsql;

DROP FUNCTION promogest.ArticoloGet(varchar, bigint, bigint);
DROP FUNCTION promogest.ArticoloSel(varchar, bigint, varchar, varchar, varchar, varchar, varchar, varchar, bigint, bigint, bigint, boolean, bigint, bigint);
DROP FUNCTION promogest.ArticoloSel(varchar, bigint, varchar, varchar, varchar, varchar, varchar, varchar, bigint, bigint, bigint, boolean, bigint, bigint, bigint, boolean, boolean, bigint, bigint);
DROP FUNCTION promogest.ArticoloSel(varchar, bigint, varchar, varchar, varchar, varchar, varchar, varchar, bigint, bigint, bigint, boolean, bigint, bigint, bigint, bigint, bigint, bigint, boolean, boolean, bigint, bigint);
DROP FUNCTION promogest.ArticoloSelCount(varchar, bigint, varchar, varchar, varchar, varchar, varchar, varchar, bigint, bigint, bigint, boolean, bigint, bigint);
DROP FUNCTION promogest.ArticoloSelCount(varchar, bigint, varchar, varchar, varchar, varchar, varchar, varchar, bigint, bigint, bigint, boolean, bigint, bigint, bigint, boolean, boolean, bigint, bigint);
DROP FUNCTION promogest.ArticoloSelCount(varchar, bigint, varchar, varchar, varchar, varchar, varchar, varchar, bigint, bigint, bigint, boolean, bigint, bigint, bigint, bigint, bigint, bigint, boolean, boolean, bigint, bigint);

DROP TYPE promogest.articolo_type;

CREATE TYPE promogest.articolo_type AS (
     id                                 bigint
    ,codice                             varchar
    ,denominazione                      varchar
    ,id_aliquota_iva                    bigint
    ,id_famiglia_articolo               bigint
    ,id_categoria_articolo              bigint
    ,id_unita_base                      bigint
    ,produttore                         varchar
    ,unita_dimensioni                   varchar
    ,lunghezza                          real
    ,larghezza                          real
    ,altezza                            real
    ,unita_volume                       varchar
    ,volume                             real
    ,unita_peso                         varchar
    ,peso_lordo                         real
    ,id_imballaggio                     bigint
    ,peso_imballaggio                   numeric
    ,stampa_etichetta                   boolean
    ,codice_etichetta                   varchar
    ,descrizione_etichetta              varchar
    ,stampa_listino                     boolean
    ,descrizione_listino                varchar
    ,aggiornamento_listino_auto         boolean
    ,timestamp_variazione               timestamp
    ,note                               text
    ,cancellato                         boolean
    ,sospeso                            boolean
    ,id_stato_articolo                  bigint
);

DROP TYPE promogest.articolo_sel_type;
DROP TYPE promogest.articolo_sel_count_type;

CREATE TYPE promogest.articolo_sel_type AS (
     id                                     bigint
    ,codice                                 varchar
    ,denominazione                          varchar
    ,id_aliquota_iva                        bigint
    ,id_famiglia_articolo                   bigint
    ,id_categoria_articolo                  bigint
    ,id_unita_base                          bigint
    ,produttore                             varchar
    ,unita_dimensioni                       varchar
    ,lunghezza                              real
    ,larghezza                              real
    ,altezza                                real
    ,unita_volume                           varchar
    ,volume                                 real
    ,unita_peso                             varchar
    ,peso_lordo                             real
    ,id_imballaggio                         bigint
    ,peso_imballaggio                       numeric
    ,stampa_etichetta                       boolean
    ,codice_etichetta                       varchar
    ,descrizione_etichetta                  varchar
    ,stampa_listino                         boolean
    ,descrizione_listino                    varchar
    ,aggiornamento_listino_auto             boolean
    ,timestamp_variazione                   timestamp
    ,note                                   text
    ,cancellato                             boolean
    ,sospeso                                boolean
    ,id_stato_articolo                      bigint 
    ,denominazione_breve_aliquota_iva       varchar
    ,denominazione_aliquota_iva             varchar
    ,percentuale_aliquota_iva               decimal
    ,denominazione_breve_famiglia           varchar
    ,denominazione_famiglia                 varchar
    ,denominazione_breve_categoria          varchar
    ,denominazione_categoria                varchar
    ,denominazione_breve_unita_base         varchar
    ,denominazione_unita_base               varchar
    ,imballaggio                            varchar
    ,stato_articolo                         varchar
    ,codice_a_barre                         varchar
    ,codice_articolo_fornitore              varchar
    ,id_articolo_padre_taglia_colore        bigint
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

CREATE TYPE promogest.articolo_sel_count_type AS (
    count       bigint
);

CREATE OR REPLACE FUNCTION promogest.ArticoloGet(varchar, bigint, bigint) RETURNS SETOF promogest.articolo_type AS '
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
            
        FOR v_row IN SELECT * FROM articolo WHERE id = _id LOOP
            RETURN NEXT v_row;
        END LOOP;
                                                                    
        -- Imposta schema precedente
        sql_command:= \'SET SEARCH_PATH TO \' || schema_prec;
        EXECUTE sql_command;

        RETURN;
    END;
' LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION promogest.ArticoloSel(varchar, bigint, varchar, varchar, varchar, varchar, varchar, varchar, bigint, bigint, bigint, boolean, bigint, bigint, bigint, bigint, bigint, bigint, boolean, boolean, bigint, bigint) RETURNS SETOF promogest.articolo_sel_type AS '
    DECLARE
        -- Parametri contesto
        _schema                         ALIAS FOR $1;
        _idutente                       ALIAS FOR $2;
        
        -- Parametri procedura
        _orderby                        ALIAS FOR $3;
        _denominazione                  ALIAS FOR $4;
        _codice                         ALIAS FOR $5;
        _codice_a_barre                 ALIAS FOR $6;
        _codice_articolo_fornitore      ALIAS FOR $7;
        _produttore                     ALIAS FOR $8;
        _id_famiglia                    ALIAS FOR $9;
        _id_categoria                   ALIAS FOR $10;
        _id_stato                       ALIAS FOR $11;
        _cancellato                     ALIAS FOR $12;
        _id_gruppo_taglia               ALIAS FOR $13;
        _id_taglia                      ALIAS FOR $14;
        _id_colore                      ALIAS FOR $15;
        _id_anno                        ALIAS FOR $16;
        _id_stagione                    ALIAS FOR $17;
        _id_genere                      ALIAS FOR $18;
        _padri_taglia_colore            ALIAS FOR $19;
        _figli_taglia_colore            ALIAS FOR $20;
        _offset                         ALIAS FOR $21;
        _count                          ALIAS FOR $22;
        
        schema_prec                     varchar(2000);
        sql_statement                   varchar(2000);
        sql_cond                        varchar(2000);
        limitstring                     varchar(500);
        _add                            varchar(500);
        OrderBy                         varchar(200);
        v_row                           record;
        _tablename                      varchar;
    BEGIN
        -- Memorizza schema precedente
        schema_prec:= ARRAY_TO_STRING(CURRENT_SCHEMAS(\'t\'),\',\');

        -- Imposta schema corrente
        sql_statement:= \'SET SEARCH_PATH TO \' || _schema;
        EXECUTE sql_statement;

        sql_statement:= \'SELECT * FROM v_articolo_completa \';
        sql_cond:=\'\';

        IF _orderby IS NULL THEN
            OrderBy = \'denominazione \';
        ELSE
            OrderBy = _orderby;
        END IF;

        IF (_denominazione IS NULL AND _codice IS NULL AND 
            _codice_a_barre IS NULL AND _codice_articolo_fornitore IS NULL AND 
            _produttore IS NULL AND _id_famiglia IS NULL AND _id_categoria IS NULL AND 
            _id_stato IS NULL AND _cancellato IS NULL AND
            _id_gruppo_taglia IS NULL AND _id_taglia IS NULL AND _id_colore IS NULL AND 
            _id_anno IS NULL AND _id_stagione IS NULL AND _id_genere IS NULL AND 
            _padri_taglia_colore IS NULL AND _figli_taglia_colore IS NULL) THEN
            SELECT INTO _tablename * FROM promogest.ArticoloFilteredExists(_schema, _idutente);
            IF _tablename <> \'\' THEN
                sql_statement:= sql_statement || \' NATURAL JOIN \' || _tablename || \' \';
            END IF;
        ELSE
            IF _denominazione IS NOT NULL THEN
                _add:= \'denominazione ILIKE \'\'%\' || _denominazione || \'%\'\'\';
                sql_cond:= promogest.sqlAddCondition(sql_cond,_add);
            END IF;

            IF _produttore IS NOT NULL THEN
                _add:= \'produttore ILIKE \'\'%\' || _produttore || \'%\'\'\';
                sql_cond:= promogest.sqlAddCondition(sql_cond,_add);
            END IF;

            IF _codice IS NOT NULL THEN
                _add:= \'codice ILIKE \'\'%\' || _codice || \'%\'\'\';
                sql_cond:= promogest.sqlAddCondition(sql_cond,_add);
            END IF;

            IF _codice_a_barre IS NOT NULL THEN
                _add:= \'id IN (SELECT id_articolo FROM codice_a_barre_articolo WHERE codice ILIKE \'\'%\' || _codice_a_barre || \'%\'\')\';
                sql_cond:= promogest.sqlAddCondition(sql_cond,_add);
            END IF;

            IF _codice_articolo_fornitore IS NOT NULL THEN
                _add:= \'id IN (SELECT id_articolo FROM fornitura WHERE codice_articolo_fornitore ILIKE \'\'%\' || _codice_articolo_fornitore || \'%\'\')\';
                sql_cond:= promogest.sqlAddCondition(sql_cond,_add);
            END IF;

            IF _id_famiglia IS NOT NULL THEN
                _add:= \'id_famiglia_articolo =\' || _id_famiglia;
                sql_cond:= promogest.sqlAddCondition(sql_cond,_add);
            END IF;

            IF _id_categoria IS NOT NULL THEN
                _add:= \'id_categoria_articolo =\' || _id_categoria;
                sql_cond:= promogest.sqlAddCondition(sql_cond,_add);
            END IF;

            IF _id_stato IS NOT NULL THEN
                _add:= \'id_stato_articolo = \' || _id_stato;
                sql_cond:= promogest.sqlAddCondition(sql_cond,_add);
            END IF;

            IF _cancellato IS NOT NULL THEN
                IF _cancellato = True THEN
                    _add:= \'cancellato = \'\'t\'\'\';
                    sql_cond:= promogest.sqlAddCondition(sql_cond,_add);
                ELSE
                    _add:= \'cancellato = \'\'f\'\'\';
                    sql_cond:= promogest.sqlAddCondition(sql_cond,_add);
                END IF;
            END IF;

            IF NOT(_padri_taglia_colore IS NULL AND _figli_taglia_colore IS NULL) THEN
                IF NOT(_padri_taglia_colore = True AND _figli_taglia_colore = True) THEN
                    IF _padri_taglia_colore = True THEN
                        _add:= \'id_articolo_padre_taglia_colore IS NULL\';
                        sql_cond:= promogest.sqlAddCondition(sql_cond,_add);
                    ELSE
                        IF _figli_taglia_colore = True THEN
                            _add:= \'id_articolo_padre_taglia_colore IS NOT NULL\';
                            sql_cond:= promogest.sqlAddCondition(sql_cond,_add);
                        END IF;
                    END IF;
                END IF;

                IF _id_gruppo_taglia IS NOT NULL THEN
                    _add:= \'id_gruppo_taglia =\' || _id_gruppo_taglia;
                    sql_cond:= promogest.sqlAddCondition(sql_cond,_add);
                END IF;

                IF _id_taglia IS NOT NULL THEN
                    _add:= \'id_taglia =\' || _id_taglia;
                    sql_cond:= promogest.sqlAddCondition(sql_cond,_add);
                END IF;

                IF _id_colore IS NOT NULL THEN
                    _add:= \'id_colore =\' || _id_colore;
                    sql_cond:= promogest.sqlAddCondition(sql_cond,_add);
                END IF;

                IF _id_anno IS NOT NULL THEN
                    _add:= \'id_anno =\' || _id_anno;
                    sql_cond:= promogest.sqlAddCondition(sql_cond,_add);
                END IF;

                IF _id_stagione IS NOT NULL THEN
                    _add:= \'id_stagione =\' || _id_stagione;
                    sql_cond:= promogest.sqlAddCondition(sql_cond,_add);
                END IF;

                IF _id_genere IS NOT NULL THEN
                    _add:= \'id_genere =\' || _id_genere;
                    sql_cond:= promogest.sqlAddCondition(sql_cond,_add);
                END IF;
            END IF;
        END IF;

        IF _offset IS NULL AND _count IS NULL THEN
            limitstring:= \'\';
        ELSIF _offset IS NULL THEN
            limitstring:= \' limit \' || _count;
        ELSIF _count IS NULL THEN
            limitstring:= \' offset \' || _offset;
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

CREATE OR REPLACE FUNCTION promogest.ArticoloSelCount(varchar, bigint, varchar, varchar, varchar, varchar, varchar, varchar, bigint, bigint, bigint, boolean, bigint, bigint, bigint, bigint, bigint, bigint, boolean, boolean, bigint, bigint) RETURNS SETOF promogest.articolo_sel_count_type AS '
    DECLARE
        -- Parametri contesto
        _schema                         ALIAS FOR $1;
        _idutente                       ALIAS FOR $2;

        -- Parametri procedura
        _orderby                        ALIAS FOR $3;
        _denominazione                  ALIAS FOR $4;
        _codice                         ALIAS FOR $5;
        _codice_a_barre                 ALIAS FOR $6;
        _codice_articolo_fornitore      ALIAS FOR $7;
        _produttore                     ALIAS FOR $8;
        _id_famiglia                    ALIAS FOR $9;
        _id_categoria                   ALIAS FOR $10;
        _id_stato                       ALIAS FOR $11;
        _cancellato                     ALIAS FOR $12;
        _id_gruppo_taglia               ALIAS FOR $13;
        _id_taglia                      ALIAS FOR $14;
        _id_colore                      ALIAS FOR $15;
        _id_anno                        ALIAS FOR $16;
        _id_stagione                    ALIAS FOR $17;
        _id_genere                      ALIAS FOR $18;
        _padri_taglia_colore            ALIAS FOR $19;
        _figli_taglia_colore            ALIAS FOR $20;
        _offset                         ALIAS FOR $21;
        _count                          ALIAS FOR $22;
        
        schema_prec                     varchar(2000);
        sql_statement                   varchar(2000);
        sql_cond                        varchar(2000);
        limitstring                     varchar(500);
        _add                            varchar(500);
        OrderBy                         varchar(200);
        v_row                           record;
        _tablename                      varchar;
    BEGIN
        -- Memorizza schema precedente
        schema_prec:= ARRAY_TO_STRING(CURRENT_SCHEMAS(\'t\'),\',\');

        -- Imposta schema corrente
        sql_statement:= \'SET SEARCH_PATH TO \' || _schema;
        EXECUTE sql_statement;

        IF (_denominazione IS NULL) AND  (_produttore IS NULL) AND 
           (_codice IS NULL) AND (_codice_a_barre IS NULL) AND 
           (_codice_articolo_fornitore IS NULL) AND (_id_famiglia IS NULL) AND 
           (_id_categoria IS NULL) AND (_id_stato IS NULL) AND
           (_padri_taglia_colore IS NULL) AND (_figli_taglia_colore IS NULL) AND
           (_id_gruppo_taglia IS NULL) AND (_id_taglia IS NULL) AND (_id_colore IS NULL) AND
           (_id_anno IS NULL) AND (_id_stagione IS NULL) AND (_id_genere IS NULL) THEN
            sql_statement:= \'SELECT COUNT(id) AS count FROM articolo \';
        ELSE
            sql_statement:= \'SELECT COUNT(id) AS count FROM v_articolo_completa \';
        END IF;

        sql_cond:=\'\';

        IF (_denominazione IS NULL AND _codice IS NULL AND 
            _codice_a_barre IS NULL AND _codice_articolo_fornitore IS NULL AND 
            _produttore IS NULL AND _id_famiglia IS NULL AND _id_categoria IS NULL AND 
            _id_stato IS NULL AND _cancellato IS NULL AND
            _id_gruppo_taglia IS NULL AND _id_taglia IS NULL AND _id_colore IS NULL AND 
            _id_anno IS NULL AND _id_stagione IS NULL AND _id_genere IS NULL AND 
            _padri_taglia_colore IS NULL AND _figli_taglia_colore IS NULL) THEN
            SELECT INTO _tablename * FROM promogest.ArticoloFilteredExists(_schema, _idutente);
            IF _tablename <> \'\' THEN
                sql_statement:= sql_statement || \' NATURAL JOIN \' || _tablename || \' \';
            END IF;
        ELSE
            IF _denominazione IS NOT NULL THEN
                _add:= \'denominazione ILIKE \'\'%\' || _denominazione || \'%\'\'\';
                sql_cond:= promogest.sqlAddCondition(sql_cond,_add);
            END IF;

            IF _produttore IS NOT NULL THEN
                _add:= \'produttore ILIKE \'\'%\' || _produttore || \'%\'\'\';
                sql_cond:= promogest.sqlAddCondition(sql_cond,_add);
            END IF;

            IF _codice IS NOT NULL THEN
                _add:= \'codice ILIKE \'\'%\' || _codice || \'%\'\'\';
                sql_cond:= promogest.sqlAddCondition(sql_cond,_add);
            END IF;

            IF _codice_a_barre IS NOT NULL THEN
                _add:= \'id IN (SELECT id_articolo FROM codice_a_barre_articolo WHERE codice ILIKE \'\'%\' || _codice_a_barre || \'%\'\')\';
                sql_cond:= promogest.sqlAddCondition(sql_cond,_add);
            END IF;

            IF _codice_articolo_fornitore IS NOT NULL THEN
                _add:= \'id IN (SELECT id_articolo FROM fornitura WHERE codice_articolo_fornitore ILIKE \'\'%\' || _codice_articolo_fornitore || \'%\'\')\';
                sql_cond:= promogest.sqlAddCondition(sql_cond,_add);
            END IF;

            IF _id_famiglia IS NOT NULL THEN
                _add:= \'id_famiglia_articolo =\' || _id_famiglia;
                sql_cond:= promogest.sqlAddCondition(sql_cond,_add);
            END IF;

            IF _id_categoria IS NOT NULL THEN
                _add:= \'id_categoria_articolo =\' || _id_categoria;
                sql_cond:= promogest.sqlAddCondition(sql_cond,_add);
            END IF;

            IF _id_stato IS NOT NULL THEN
                _add:= \'id_stato_articolo = \' || _id_stato;
                sql_cond:= promogest.sqlAddCondition(sql_cond,_add);
            END IF;

            IF _cancellato IS NOT NULL THEN
                IF _cancellato = True THEN
                    _add:= \'cancellato = \'\'t\'\'\';
                    sql_cond:= promogest.sqlAddCondition(sql_cond,_add);
                ELSE
                    _add:= \'cancellato = \'\'f\'\'\';
                    sql_cond:= promogest.sqlAddCondition(sql_cond,_add);
                END IF;
            END IF;

            IF NOT(_padri_taglia_colore IS NULL AND _figli_taglia_colore IS NULL) THEN
                IF NOT(_padri_taglia_colore = True AND _figli_taglia_colore = True) THEN
                    IF _padri_taglia_colore = True THEN
                        _add:= \'id_articolo_padre_taglia_colore IS NULL\';
                        sql_cond:= promogest.sqlAddCondition(sql_cond,_add);
                    ELSE
                        IF _figli_taglia_colore = True THEN
                            _add:= \'id_articolo_padre_taglia_colore IS NOT NULL\';
                            sql_cond:= promogest.sqlAddCondition(sql_cond,_add);
                        END IF;
                    END IF;
                END IF;

                IF _id_gruppo_taglia IS NOT NULL THEN
                    _add:= \'id_gruppo_taglia =\' || _id_gruppo_taglia;
                    sql_cond:= promogest.sqlAddCondition(sql_cond,_add);
                END IF;

                IF _id_taglia IS NOT NULL THEN
                    _add:= \'id_taglia =\' || _id_taglia;
                    sql_cond:= promogest.sqlAddCondition(sql_cond,_add);
                END IF;

                IF _id_colore IS NOT NULL THEN
                    _add:= \'id_colore =\' || _id_colore;
                    sql_cond:= promogest.sqlAddCondition(sql_cond,_add);
                END IF;

                IF _id_anno IS NOT NULL THEN
                    _add:= \'id_anno =\' || _id_anno;
                    sql_cond:= promogest.sqlAddCondition(sql_cond,_add);
                END IF;

                IF _id_stagione IS NOT NULL THEN
                    _add:= \'id_stagione =\' || _id_stagione;
                    sql_cond:= promogest.sqlAddCondition(sql_cond,_add);
                END IF;

                IF _id_genere IS NOT NULL THEN
                    _add:= \'id_genere =\' || _id_genere;
                    sql_cond:= promogest.sqlAddCondition(sql_cond,_add);
                END IF;
            END IF;
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
