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

Fornitura  - Stored procedure applicativa

*/

DROP FUNCTION promogest.FornituraSet(varchar, bigint, bigint, varchar, decimal(16,4), decimal(16,4), varchar, integer, integer, boolean, decimal(8,4), date, date, bigint, bigint, bigint);
CREATE OR REPLACE FUNCTION promogest.FornituraSet(varchar, bigint, bigint, varchar, decimal(16,4), decimal(16,4), varchar, integer, integer, boolean, decimal(8,4), date, date, bigint, bigint, bigint) RETURNS promogest.resultid AS '
    DECLARE
        -- Parametri contesto
        _schema                         ALIAS FOR $1;
        _idutente                       ALIAS FOR $2;
        
        -- Parametri tabella
        _id                             ALIAS FOR $3;
        _codice_articolo_fornitore      ALIAS FOR $4;
        _prezzo_lordo                   ALIAS FOR $5;
        _prezzo_netto                   ALIAS FOR $6;
        _applicazione_sconti            ALIAS FOR $7;
        _scorta_minima                  ALIAS FOR $8;
        _tempo_arrivo_merce             ALIAS FOR $9;
        _fornitore_preferenziale        ALIAS FOR $10;
        _percentuale_iva                ALIAS FOR $11;
        _data_fornitura                 ALIAS FOR $12;
        _data_prezzo                    ALIAS FOR $13;
        _id_fornitore                   ALIAS FOR $14;
        _id_articolo                    ALIAS FOR $15;
        _id_multiplo                    ALIAS FOR $16;

        schema_prec                     varchar(2000);
        sql_command                     varchar(2000);
        _ret                            promogest.resultid;
        _rec                            record;
        __id                            bigint;
        _oldcountpreferenziale          bigint;
    BEGIN
        -- Memorizza schema precedente
        schema_prec:= ARRAY_TO_STRING(CURRENT_SCHEMAS(\'t\'),\',\');
    
        -- Imposta schema corrente
        sql_command:= \'SET SEARCH_PATH TO \' || _schema;
        EXECUTE sql_command;
        
        -- Controllo chiave naturale
        SELECT INTO __id id FROM fornitura WHERE id_articolo = _id_articolo AND id_fornitore = _id_fornitore AND data_prezzo = _data_prezzo;

        -- Check fornitore preferenziale
        IF _fornitore_preferenziale = \'t\' THEN
            SELECT COUNT(*) INTO _oldcountpreferenziale FROM fornitura WHERE id_articolo = _id_articolo AND fornitore_preferenziale;
            IF _oldcountpreferenziale > 0 THEN
                -- Disattivo vecchi preferenziali
                UPDATE fornitura SET fornitore_preferenziale = \'f\' WHERE id_articolo = _id_articolo AND fornitore_preferenziale;
            END IF;
        END IF;

        SELECT INTO _ret * FROM promogest.FornituraInsUpd(_schema, _idutente, __id, _codice_articolo_fornitore, _prezzo_lordo, _prezzo_netto,
                                                          _applicazione_sconti, _scorta_minima, _tempo_arrivo_merce, _fornitore_preferenziale, 
                                                          _percentuale_iva, _data_fornitura, _data_prezzo, _id_fornitore, _id_articolo, _id_multiplo); 
        
        -- Imposta schema precedente
        sql_command:= \'SET SEARCH_PATH TO \' || schema_prec;
        EXECUTE sql_command;
        
        RETURN _ret;
    END;
' LANGUAGE plpgsql;


DROP FUNCTION promogest.FornituraDel(varchar, bigint, bigint);
CREATE OR REPLACE FUNCTION promogest.FornituraDel(varchar, bigint, bigint) RETURNS promogest.resultid AS '
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
        
        SELECT INTO _ret * FROM promogest.ObjectDel(_schema, _idutente, \'fornitura\', _id, \'id\');
        
        -- Imposta schema precedente
        sql_command:= \'SET SEARCH_PATH TO \' || schema_prec;
        EXECUTE sql_command;
        
        RETURN _ret;
    END;
' LANGUAGE plpgsql;


DROP FUNCTION promogest.FornituraGet(varchar, bigint, bigint);
DROP FUNCTION promogest.FornituraSel(varchar, bigint, varchar, bigint, bigint, date, date, date, date, varchar, bigint, bigint);
DROP FUNCTION promogest.FornituraSelCount(varchar, bigint, varchar, bigint, bigint, date, date, date, date, varchar, bigint, bigint);

DROP TYPE promogest.fornitura_type;
DROP TYPE promogest.fornitura_sel_type;
DROP TYPE promogest.fornitura_sel_count_type;

CREATE TYPE promogest.fornitura_type AS (
     id                             bigint
    ,codice_articolo_fornitore      varchar(100)
    ,prezzo_lordo                   decimal(16,4)
    ,prezzo_netto                   decimal(16,4)
    ,applicazione_sconti            varchar(20)
    ,scorta_minima                  integer
    ,tempo_arrivo_merce             integer
    ,fornitore_preferenziale        boolean
    ,percentuale_iva                decimal(8,4)
    ,data_fornitura                 date
    ,data_prezzo                    date
    ,id_fornitore                   bigint 
    ,id_articolo                    bigint
    ,id_multiplo                    bigint
);

CREATE TYPE promogest.fornitura_sel_type AS (
     id                                     bigint
    ,codice_articolo_fornitore              varchar(100)
    ,prezzo_lordo                           decimal(16,4)
    ,prezzo_netto                           decimal(16,4)
    ,applicazione_sconti                    varchar(20)
    ,scorta_minima                          integer
    ,tempo_arrivo_merce                     integer
    ,fornitore_preferenziale                boolean
    ,percentuale_iva                        decimal(8,4)
    ,data_fornitura                         date
    ,data_prezzo                            date
    ,id_fornitore                           bigint
    ,id_articolo                            bigint
    ,id_multiplo                            bigint
    ,codice_fornitore                       varchar
    ,fornitore                              varchar
    ,codice_articolo                        varchar
    ,articolo                               varchar
    ,multiplo                               varchar
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

CREATE TYPE promogest.fornitura_sel_count_type AS (
    count       bigint
);

CREATE OR REPLACE FUNCTION promogest.FornituraGet(varchar, bigint, bigint) RETURNS SETOF promogest.fornitura_type AS '
    DECLARE
        -- Parametri contesto
        _schema                 ALIAS FOR $1;
        _idutente               ALIAS FOR $2;
        
        -- Parametri tabella
        _id                     ALIAS FOR $3;
        
        schema_prec             varchar(2000);
        sql_command             varchar(2000);
        v_row                   record;
        id_tipo_fornitura       bigint;
    BEGIN
        -- Memorizza schema precedente
        schema_prec:= ARRAY_TO_STRING(CURRENT_SCHEMAS(\'t\'),\',\');
    
        -- Imposta schema corrente
        sql_command:= \'SET SEARCH_PATH TO \' || _schema;
        EXECUTE sql_command;
        
        FOR v_row IN SELECT * FROM fornitura WHERE id = _id LOOP
            RETURN NEXT v_row;
        END LOOP;
                                    
        -- Imposta schema precedente
        sql_command:= \'SET SEARCH_PATH TO \' || schema_prec;
        EXECUTE sql_command;

        RETURN;
    END;
' LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION promogest.FornituraSel(varchar, bigint, varchar, bigint, bigint, date, date, date, date, varchar, bigint, bigint) RETURNS SETOF promogest.fornitura_sel_type AS '
    DECLARE
        -- Parametri contesto
        _schema                         ALIAS FOR $1;
        _idutente                       ALIAS FOR $2;
        
        -- Parametri procedura
        _orderby                        ALIAS FOR $3;
        _id_articolo                    ALIAS FOR $4;
        _id_fornitore                   ALIAS FOR $5;
        _da_data_fornitura              ALIAS FOR $6;
        _a_data_fornitura               ALIAS FOR $7;
        _da_data_prezzo                 ALIAS FOR $8;
        _a_data_prezzo                  ALIAS FOR $9;
        _codice_articolo_fornitore      ALIAS FOR $10;
        _offset                         ALIAS FOR $11;
        _count                          ALIAS FOR $12;
        
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

        sql_statement:= \'SELECT F.* FROM v_fornitura_completa F \';
        sql_cond:=\'\';
        
        IF _orderby IS NULL THEN
            OrderBy = \'F.fornitore \';
        ELSE
            OrderBy = _orderby;
        END IF;
        
        IF _codice_articolo_fornitore IS NOT NULL THEN
            _add:= \'F.codice_articolo_fornitore ILIKE \'\'%\' || _codice_articolo_fornitore  || \'%\'\'\';
            sql_cond:= promogest.sqlAddCondition(sql_cond,_add);
        END IF;
        
        IF _id_articolo IS NOT NULL THEN
            _add:= \'F.id_articolo = \' || _id_articolo;
            sql_cond:= promogest.sqlAddCondition(sql_cond,_add);
        ELSE
            SELECT INTO _tablename * FROM promogest.ArticoloFilteredExists(_schema, _idutente);
            IF _tablename <> \'\' THEN
                sql_statement:= sql_statement || \' INNER JOIN \' || _tablename || \' AF ON F.id_articolo = AF.id\';
            END IF;
        END IF;
        
        IF _id_fornitore IS NOT NULL THEN
            _add:= \'F.id_fornitore = \' || _id_fornitore;
            sql_cond:= promogest.sqlAddCondition(sql_cond,_add);
        ELSE
            SELECT INTO _tablename * FROM promogest.FornitoreFilteredExists(_schema, _idutente);
            IF _tablename <> \'\' THEN
                sql_statement:= sql_statement || \' INNER JOIN \' || _tablename || \' FF ON F.id_fornitore = FF.id\';
            END IF;
        END IF;

        IF _da_data_fornitura IS NOT NULL THEN
            _add:= \'F.data_fornitura >= \' || QUOTE_LITERAL(_da_data_fornitura);
            sql_cond:= promogest.sqlAddCondition(sql_cond,_add);
        END IF;

        IF _a_data_fornitura IS NOT NULL THEN
            _add:= \'F.data_fornitura <= \' || QUOTE_LITERAL(_a_data_fornitura);
            sql_cond:= promogest.sqlAddCondition(sql_cond,_add);
        END IF;
        
        IF _da_data_prezzo IS NOT NULL THEN
            _add:= \'F.data_prezzo >= \' || QUOTE_LITERAL(_da_data_prezzo);
            sql_cond:= promogest.sqlAddCondition(sql_cond,_add);
        END IF;

        IF _a_data_prezzo IS NOT NULL THEN
            _add:= \'F.data_prezzo <= \' || QUOTE_LITERAL(_a_data_prezzo);
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

CREATE OR REPLACE FUNCTION promogest.FornituraSelCount(varchar, bigint, varchar, bigint, bigint, date, date, date, date, varchar, bigint, bigint) RETURNS SETOF promogest.fornitura_sel_count_type AS '
    DECLARE
        -- Parametri contesto
        _schema                         ALIAS FOR $1;
        _idutente                       ALIAS FOR $2;
        
        -- Parametri procedura
        _orderby                        ALIAS FOR $3;
        _id_articolo                    ALIAS FOR $4;
        _id_fornitore                   ALIAS FOR $5;
        _da_data_fornitura              ALIAS FOR $6;
        _a_data_fornitura               ALIAS FOR $7;
        _da_data_prezzo                 ALIAS FOR $8;
        _a_data_prezzo                  ALIAS FOR $9;
        _codice_articolo_fornitore      ALIAS FOR $10;
        _offset                         ALIAS FOR $11;
        _count                          ALIAS FOR $12;
        
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

        sql_statement:= \'SELECT COUNT(F.id) FROM v_fornitura_completa F \';
        sql_cond:=\'\';

        IF _codice_articolo_fornitore IS NOT NULL THEN
            _add:= \'F.codice_articolo_fornitore ILIKE \'\'%\' || _codice_articolo_fornitore  || \'%\'\'\';
            sql_cond:= promogest.sqlAddCondition(sql_cond,_add);
        END IF;
        
        IF _id_articolo IS NOT NULL THEN
            _add:= \'F.id_articolo = \' || _id_articolo;
            sql_cond:= promogest.sqlAddCondition(sql_cond,_add);
        ELSE
            SELECT INTO _tablename * FROM promogest.ArticoloFilteredExists(_schema, _idutente);
            IF _tablename <> \'\' THEN
                sql_statement:= sql_statement || \' INNER JOIN \' || _tablename || \' AF ON F.id_articolo = AF.id\';
            END IF;
        END IF;
        
        IF _id_fornitore IS NOT NULL THEN
            _add:= \'F.id_fornitore = \' || _id_fornitore;
            sql_cond:= promogest.sqlAddCondition(sql_cond,_add);
        ELSE
            SELECT INTO _tablename * FROM promogest.FornitoreFilteredExists(_schema, _idutente);
            IF _tablename <> \'\' THEN
                sql_statement:= sql_statement || \' INNER JOIN \' || _tablename || \' FF ON F.id_fornitore = FF.id\';
            END IF;
        END IF;

        IF _da_data_fornitura IS NOT NULL THEN
            _add:= \'F.data_fornitura >= \' || QUOTE_LITERAL(_da_data_fornitura);
            sql_cond:= promogest.sqlAddCondition(sql_cond,_add);
        END IF;

        IF _a_data_fornitura IS NOT NULL THEN
            _add:= \'F.data_fornitura <= \' || QUOTE_LITERAL(_a_data_fornitura);
            sql_cond:= promogest.sqlAddCondition(sql_cond,_add);
        END IF;
        
        IF _da_data_prezzo IS NOT NULL THEN
            _add:= \'F.data_prezzo >= \' || QUOTE_LITERAL(_da_data_prezzo);
            sql_cond:= promogest.sqlAddCondition(sql_cond,_add);
        END IF;

        IF _a_data_prezzo IS NOT NULL THEN
            _add:= \'F.data_prezzo <= \' || QUOTE_LITERAL(_a_data_prezzo);
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
