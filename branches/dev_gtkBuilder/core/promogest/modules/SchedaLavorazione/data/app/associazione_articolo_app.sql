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

associazione articolo  - Stored procedure applicativa

*/
DROP TYPE promogest.associazione_articoli_sel_type CASCADE;
DROP TYPE promogest.associazione_articoli_sel_count_type CASCADE;

CREATE TYPE promogest.associazione_articoli_sel_type AS (
    id                                      bigint
    ,id_associato                           bigint
    ,id_articolo                            bigint
    ,posizione                              integer
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
);

CREATE TYPE promogest.associazione_articoli_sel_count_type AS (
    count       bigint
);

DROP FUNCTION promogest.AssociazioneArticoloSet(varchar, bigint, bigint, bigint, bigint, integer) CASCADE;
CREATE OR REPLACE FUNCTION promogest.AssociazioneArticoloSet(varchar,bigint, bigint, bigint, bigint,integer) RETURNS promogest.resultid AS 
$$
    DECLARE
        -- Parametri contesto
        _schema                         ALIAS FOR $1;
        _idutente                       ALIAS FOR $2;
        
        -- Parametri tabella
        _id                             ALIAS FOR $3;
        _id_padre                       ALIAS FOR $4;
        _id_figlio                      ALIAS FOR $5;
        _posizione                      ALIAS FOR $6;
        
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
        
        SELECT INTO _ret * FROM promogest.AssociazioneArticoloInsUpd(_schema, _idutente, _id, _id_padre, _id_figlio, _posizione);
        
        -- reimposta lo schema precedente
        sql_command:= 'SET SEARCH_PATH TO ' || schema_prec;
        EXECUTE sql_command;
        
        RETURN _ret;
    END;
$$ LANGUAGE plpgsql;

DROP FUNCTION promogest.AssociazioneArticoloGet(varchar, bigint, bigint) CASCADE;

CREATE OR REPLACE FUNCTION promogest.AssociazioneArticoloGet(varchar, bigint, bigint) RETURNS SETOF promogest.associazione_articoli_sel_type AS
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
            
        FOR v_row IN SELECT * FROM v_nodo_associazione_articoli AA WHERE AA.id = _id LOOP
            RETURN NEXT v_row;
        END LOOP;
                                                                    
        -- Imposta schema precedente
        sql_command:= 'SET SEARCH_PATH TO ' || schema_prec;
        EXECUTE sql_command;

        RETURN;
    END;
$$ LANGUAGE plpgsql;

DROP FUNCTION promogest.AssociazioneArticoloDel(varchar, bigint, bigint) CASCADE;

CREATE OR REPLACE FUNCTION promogest.AssociazioneArticoloDel(varchar, bigint, bigint) RETURNS promogest.resultid AS
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
        
        SELECT INTO _ret * FROM promogest.ObjectDel(_schema, _idutente, 'associazioni_articoli', _id, 'id');
        
        -- Imposta schema precedente
        sql_command:= 'SET SEARCH_PATH TO ' || schema_prec;
        EXECUTE sql_command;
        RETURN _ret;
    END;
$$ LANGUAGE plpgsql;

DROP FUNCTION promogest.AssociazioneArticoloSel(varchar, bigint, boolean, bigint, varchar, varchar, varchar, varchar, varchar, varchar, bigint, bigint, bigint, boolean, bigint, bigint) CASCADE;

CREATE OR REPLACE FUNCTION promogest.AssociazioneArticoloSel(varchar, bigint, boolean, bigint, varchar, varchar, varchar, varchar, varchar, varchar, bigint, bigint, bigint, boolean, bigint, bigint) RETURNS SETOF promogest.associazione_articoli_sel_type AS 
$$
    DECLARE
        -- Parametri contesto
        _schema                         ALIAS FOR $1;
        _idutente                       ALIAS FOR $2;
        
        -- Parametri procedura
        _nodo                           ALIAS FOR $3;
        _id_associato                   ALIAS FOR $4;
        _orderby                        ALIAS FOR $5;
        _denominazione                  ALIAS FOR $6;
        _codice                         ALIAS FOR $7;
        _codice_a_barre                 ALIAS FOR $8;
        _codice_articolo_fornitore      ALIAS FOR $9;
        _produttore                     ALIAS FOR $10;
        _id_famiglia                    ALIAS FOR $11;
        _id_categoria                   ALIAS FOR $12;
        _id_stato                       ALIAS FOR $13;
        _cancellato                     ALIAS FOR $14;
        _offset                         ALIAS FOR $15;
        _count                          ALIAS FOR $16;
        
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
        schema_prec:= ARRAY_TO_STRING(CURRENT_SCHEMAS('t'),',');

        -- Imposta schema corrente
        sql_statement:= 'SET SEARCH_PATH TO ' || _schema;
        EXECUTE sql_statement;
        
        IF _nodo IS NOT NULL THEN
            IF _nodo = 't' THEN
                sql_statement:= 'SELECT * FROM v_nodo_associazione_articoli ';
            ELSE
                sql_statement:= 'SELECT * FROM v_elemento_associazione_articoli ';
            END IF;
        ELSE
            sql_statement:= 'SELECT * FROM v_elemento_associazione_articoli ';
        END IF;
        
        sql_cond:='';

        IF _orderby IS NULL THEN
            OrderBy = 'denominazione ';
        ELSE
            OrderBy = _orderby;
        END IF;

        IF _id_associato IS NOT NULL THEN
            _add:= 'id_associato = ' || _id_associato ;
            sql_cond:= promogest.sqlAddCondition(sql_cond,_add);
        END IF;
    
        IF _denominazione IS NOT NULL THEN
            _add:= 'denominazione ILIKE \'' || _denominazione || '\' ';
            sql_cond:= promogest.sqlAddCondition(sql_cond,_add);
        END IF;

        IF _produttore IS NOT NULL THEN
            _add:= 'produttore ILIKE \'' || _produttore || '\' ';
            sql_cond:= promogest.sqlAddCondition(sql_cond,_add);
        END IF;

        IF _codice IS NOT NULL THEN
            _add:= 'codice ILIKE \'' || _codice || '\' ';
            sql_cond:= promogest.sqlAddCondition(sql_cond,_add);
        END IF;

        IF _codice_a_barre IS NOT NULL THEN
            _add:= 'id IN (SELECT id_articolo FROM codice_a_barre_articolo WHERE codice ILIKE \'' || _codice_a_barre || '\')';
            sql_cond:= promogest.sqlAddCondition(sql_cond,_add);
        END IF;

        IF _codice_articolo_fornitore IS NOT NULL THEN
            _add:= 'id IN (SELECT id_articolo FROM fornitura WHERE codice_articolo_fornitore ILIKE \'' || _codice_articolo_fornitore || '\')';
            sql_cond:= promogest.sqlAddCondition(sql_cond,_add);
        END IF;

        IF _id_famiglia IS NOT NULL THEN
            _add:= 'id_famiglia_articolo =' || _id_famiglia;
            sql_cond:= promogest.sqlAddCondition(sql_cond,_add);
        END IF;

        IF _id_categoria IS NOT NULL THEN
            _add:= 'id_categoria_articolo =' || _id_categoria;
            sql_cond:= promogest.sqlAddCondition(sql_cond,_add);
        END IF;

        IF _id_stato IS NOT NULL THEN
            _add:= 'id_stato_articolo = ' || _id_stato;
            sql_cond:= promogest.sqlAddCondition(sql_cond,_add);
        END IF;

        IF _cancellato IS NOT NULL THEN
            IF _cancellato = True THEN
                _add:= 'cancellato = \'t\' ';
                sql_cond:= promogest.sqlAddCondition(sql_cond,_add);
            ELSE
                _add:= 'cancellato = \'f\' ';
                sql_cond:= promogest.sqlAddCondition(sql_cond,_add);
            END IF;
        END IF;

        IF _offset IS NULL AND _count IS NULL THEN
            limitstring:= '';
        ELSIF _offset IS NULL THEN
            limitstring:= ' limit ' || _count;
        ELSIF _count IS NULL THEN
            limitstring:= ' offset ' || _offset;
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
$$ LANGUAGE plpgsql;


DROP FUNCTION promogest.AssociazioneArticoloSelCount(varchar, bigint, boolean, bigint, varchar, varchar, varchar, varchar, varchar, bigint, bigint, bigint, boolean) CASCADE;

CREATE OR REPLACE FUNCTION promogest.AssociazioneArticoloSelCount(varchar, bigint, boolean, bigint, varchar, varchar, varchar, varchar, varchar, varchar, bigint, bigint, bigint, boolean, bigint, bigint) RETURNS SETOF promogest.associazione_articoli_sel_count_type AS 
$$
    DECLARE
        -- Parametri contesto
        _schema                         ALIAS FOR $1;
        _idutente                       ALIAS FOR $2;
        
        -- Parametri procedura
        _nodo                           ALIAS FOR $3;
        _id_associato                   ALIAS FOR $4;
        _orderby                        ALIAS FOR $5;
        _denominazione                  ALIAS FOR $6;
        _codice                         ALIAS FOR $7;
        _codice_a_barre                 ALIAS FOR $8;
        _codice_articolo_fornitore      ALIAS FOR $9;
        _produttore                     ALIAS FOR $10;
        _id_famiglia                    ALIAS FOR $11;
        _id_categoria                   ALIAS FOR $12;
        _id_stato                       ALIAS FOR $13;
        _cancellato                     ALIAS FOR $14;
        _offset                         ALIAS FOR $15;
        _count                          ALIAS FOR $16;
        
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
        schema_prec:= ARRAY_TO_STRING(CURRENT_SCHEMAS('t'),',');

        -- Imposta schema corrente
        sql_statement:= 'SET SEARCH_PATH TO ' || _schema;
        EXECUTE sql_statement;
        
        sql_cond:='';

        IF _nodo IS NOT NULL THEN
            IF _nodo = 't' THEN
                sql_statement:= 'SELECT COUNT(id) FROM v_nodo_associazione_articoli ';
            ELSE
                sql_statement:= 'SELECT COUNT(id) FROM v_elemento_associazione_articoli ';
            END IF;
        ELSE
            sql_statement:= 'SELECT * FROM v_nodo_associazione_articoli ';
        END IF;
        

        IF _orderby IS NULL THEN
            OrderBy = 'denominazione ';
        ELSE
            OrderBy = _orderby;
        END IF;
        
        IF _id_associato IS NOT NULL THEN
            _add:= 'id_associato = ' || _id_associato ;
            sql_cond:= promogest.sqlAddCondition(sql_cond,_add);
        END IF;
    
        IF _denominazione IS NOT NULL THEN
            _add:= 'denominazione ILIKE \'' || _denominazione || '\' ';
            sql_cond:= promogest.sqlAddCondition(sql_cond,_add);
        END IF;

        IF _produttore IS NOT NULL THEN
            _add:= 'produttore ILIKE \'' || _produttore || '\' ';
            sql_cond:= promogest.sqlAddCondition(sql_cond,_add);
        END IF;

        IF _codice IS NOT NULL THEN
            _add:= 'codice ILIKE \'' || _codice || '\' ';
            sql_cond:= promogest.sqlAddCondition(sql_cond,_add);
        END IF;

        IF _codice_a_barre IS NOT NULL THEN
            _add:= 'id IN (SELECT id_articolo FROM codice_a_barre_articolo WHERE codice ILIKE \'' || _codice_a_barre || '\')';
            sql_cond:= promogest.sqlAddCondition(sql_cond,_add);
        END IF;

        IF _codice_articolo_fornitore IS NOT NULL THEN
            _add:= 'id IN (SELECT id_articolo FROM fornitura WHERE codice_articolo_fornitore ILIKE \'' || _codice_articolo_fornitore || '\')';
            sql_cond:= promogest.sqlAddCondition(sql_cond,_add);
        END IF;

        IF _id_famiglia IS NOT NULL THEN
            _add:= 'id_famiglia_articolo =' || _id_famiglia;
            sql_cond:= promogest.sqlAddCondition(sql_cond,_add);
        END IF;

        IF _id_categoria IS NOT NULL THEN
            _add:= 'id_categoria_articolo =' || _id_categoria;
            sql_cond:= promogest.sqlAddCondition(sql_cond,_add);
        END IF;

        IF _id_stato IS NOT NULL THEN
            _add:= 'id_stato_articolo = ' || _id_stato;
            sql_cond:= promogest.sqlAddCondition(sql_cond,_add);
        END IF;

        IF _cancellato IS NOT NULL THEN
            IF _cancellato = True THEN
                _add:= 'cancellato = \'t\' ';
                sql_cond:= promogest.sqlAddCondition(sql_cond,_add);
            ELSE
                _add:= 'cancellato = \'f\' ';
                sql_cond:= promogest.sqlAddCondition(sql_cond,_add);
            END IF;
        END IF;

        IF _offset IS NULL AND _count IS NULL THEN
            limitstring:= '';
        ELSIF _offset IS NULL THEN
            limitstring:= ' limit ' || _count;
        ELSIF _count IS NULL THEN
            limitstring:= ' offset ' || _offset;
        ELSE
            limitstring:= ' LIMIT ' || _count || ' OFFSET  ' || _offset;
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

