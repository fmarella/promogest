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

testata_documento  - Stored procedure applicativa

*/
DROP FUNCTION promogest.testatadocumentoset("varchar", int8, int8, int4, int4, "varchar", "varchar", date, "timestamp", "varchar", text, "varchar", "varchar", "varchar", "timestamp", "timestamp", "varchar", int4, "varchar", "varchar", int8, int8, int8, int8, int8, int8, int8, int8, "varchar", "numeric", bool);
DROP FUNCTION promogest.TestataDocumentoSet(varchar, bigint, bigint, integer, integer, varchar, varchar, date, timestamp, varchar, text, varchar, varchar, varchar, timestamp, timestamp, varchar, integer, varchar, varchar, bigint, bigint, bigint, bigint, bigint, bigint, bigint, bigint, varchar, boolean, decimal(16,4), decimal(16,4), bigint, bigint, decimal(16,4), boolean);
CREATE OR REPLACE FUNCTION promogest.TestataDocumentoSet(varchar, bigint, bigint, integer, integer, varchar, varchar, date, timestamp, varchar, text, varchar, varchar, varchar, timestamp, timestamp, varchar, integer, varchar, varchar, bigint, bigint, bigint, bigint, bigint, bigint, bigint, bigint, varchar, boolean, decimal(16,4), decimal(16,4), bigint, bigint, decimal(16,4), boolean) RETURNS promogest.resultid AS E'
    DECLARE
        -- Parametri contesto
        _schema                         ALIAS FOR $1;
        _idutente                       ALIAS FOR $2;

        -- Parametri tabella
        _id                             ALIAS FOR $3;
        _numero                         ALIAS FOR $4;
        _parte                          ALIAS FOR $5;
        _registro_numerazione           ALIAS FOR $6;
        _operazione                     ALIAS FOR $7;
        _data_documento                 ALIAS FOR $8;
        _data_inserimento               ALIAS FOR $9;
        _protocollo                     ALIAS FOR $10;
        _note_interne                   ALIAS FOR $11;
        _note_pie_pagina                ALIAS FOR $12;
        _causale_trasporto              ALIAS FOR $13;
        _aspetto_esteriore_beni         ALIAS FOR $14;
        _inizio_trasporto               ALIAS FOR $15;
        _fine_trasporto                 ALIAS FOR $16;
        _incaricato_trasporto           ALIAS FOR $17;
        _totale_colli                   ALIAS FOR $18;
        _totale_peso                    ALIAS FOR $19;
        _applicazione_sconti            ALIAS FOR $20;
        _id_cliente                     ALIAS FOR $21;
        _id_fornitore                   ALIAS FOR $22;
        _id_destinazione_merce          ALIAS FOR $23;
        _id_pagamento                   ALIAS FOR $24;
        _id_banca                       ALIAS FOR $25;
        _id_aliquota_iva_esenzione      ALIAS FOR $26;
        _id_vettore                     ALIAS FOR $27;
        _id_agente                      ALIAS FOR $28;
    	_porto                          ALIAS FOR $29;
        _documento_saldato              ALIAS FOR $30;
        _totale_pagato                  ALIAS FOR $31;
        _totale_sospeso                 ALIAS FOR $32;
        _id_primo_riferimento           ALIAS FOR $33;
        _id_secondo_riferimento         ALIAS FOR $34;
        _costo_da_ripartire             ALIAS FOR $35;
        _ripartire_importo              ALIAS FOR $36;

        _number                         integer;
        _registro                       varchar(100);
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

        -- Se siamo in inserimento ottengo il registro ed il prossimo numero
        IF _id IS NULL THEN
            SELECT numero, registro INTO _number, _registro FROM promogest.NumeroRegistroGet(_operazione, _data_documento);
        ELSE
            _number:=_numero;
        END IF;

        SELECT INTO _ret * FROM promogest.TestataDocumentoInsUpd(_schema, _idutente, _id, _number, _parte, _registro, _operazione, _data_documento, _data_inserimento, _protocollo, _note_interne, _note_pie_pagina, _causale_trasporto, _aspetto_esteriore_beni, _inizio_trasporto, _fine_trasporto, _incaricato_trasporto, _totale_colli, _totale_peso, _applicazione_sconti,  _id_cliente, _id_fornitore, _id_destinazione_merce, _id_pagamento, _id_banca, _id_aliquota_iva_esenzione, _id_vettore, _id_agente, _porto, _documento_saldato, _totale_pagato, _totale_sospeso, _id_primo_riferimento, _id_secondo_riferimento, _costo_da_ripartire, _ripartire_importo);

        -- Imposta schema precedente
        sql_command:= \'SET SEARCH_PATH TO \' || schema_prec;
        EXECUTE sql_command;

        RETURN _ret;
    END;
' LANGUAGE plpgsql;


DROP FUNCTION promogest.TestataDocumentoDel(varchar, bigint, bigint) CASCADE;
CREATE OR REPLACE FUNCTION promogest.TestataDocumentoDel(varchar, bigint, bigint) RETURNS promogest.resultid AS E'
    DECLARE
        -- Parametri contesto
        _schema             ALIAS FOR $1;
        _idutente           ALIAS FOR $2;

        -- Parametri tabella
        _id                 ALIAS FOR $3;
        schema_prec         varchar(2000);
        sql_command         varchar(2000);
        _ret                promogest.resultid;
        _rec                record;
    BEGIN
        -- Memorizza schema precedente
        schema_prec:= ARRAY_TO_STRING(CURRENT_SCHEMAS(\'t\'),\',\');

        -- Imposta schema corrente
        sql_command:= \'SET SEARCH_PATH TO \' || _schema;
        EXECUTE sql_command;

        SELECT INTO _ret * FROM promogest.ObjectDel(_schema, _idutente, \'informazioni_fatturazione_documento\', _id, \'id_fattura\');
        SELECT INTO _ret * FROM promogest.RigheDocumentoDel(_schema, _idutente, _id);

        SELECT INTO _ret * FROM promogest.ObjectDel(_schema, _idutente, \'informazioni_contabili_documento\', _id, \'id_documento\');

        SELECT INTO _ret * FROM promogest.ObjectDel(_schema, _idutente, \'testata_documento_scadenza\', _id, \'id_testata_documento\');

        SELECT INTO _ret * FROM promogest.ObjectDel(_schema, _idutente, \'testata_documento\', _id, \'id\');

        -- Imposta schema precedente
        sql_command:= \'SET SEARCH_PATH TO \' || schema_prec;
        EXECUTE sql_command;

        RETURN _ret;
    END;
' LANGUAGE plpgsql;


DROP FUNCTION promogest.TestataDocumentoGet(varchar, bigint, bigint) CASCADE;
DROP FUNCTION promogest.testatadocumentosel("varchar", int8, "varchar", int4, int4, int4, int4, date, date, "varchar", "varchar", int8, int8, int8, int8, int8, int8, int8);
DROP FUNCTION promogest.TestataDocumentoSel(varchar, bigint, varchar, integer, integer, integer, integer, date, date, varchar, varchar, bigint, bigint, bigint, bigint, bigint, bigint, bigint, bigint) CASCADE;
DROP FUNCTION promogest.testatadocumentoselcount("varchar", int8, "varchar", int4, int4, int4, int4, date, date, "varchar", "varchar", int8, int8, int8, int8, int8, int8, int8);
DROP FUNCTION promogest.TestataDocumentoSelCount(varchar, bigint, varchar, integer, integer, integer, integer, date, date, varchar, varchar, bigint, bigint, bigint, bigint, bigint, bigint, bigint, bigint) CASCADE;

DROP TYPE promogest.testata_documento_type CASCADE;
DROP TYPE promogest.testata_documento_sel_type CASCADE;
DROP TYPE promogest.testata_documento_sel_count_type CASCADE;


CREATE TYPE promogest.testata_documento_type AS (
      id                            bigint
     ,numero                        integer
     ,parte                         integer
     ,registro_numerazione          varchar
     ,operazione                    varchar
     ,data_documento                date
     ,data_inserimento              timestamp
     ,protocollo                    varchar
     ,note_interne                  text
     ,note_pie_pagina               varchar
     ,causale_trasporto             varchar
     ,aspetto_esteriore_beni        varchar
     ,inizio_trasporto              timestamp
     ,fine_trasporto                timestamp
     ,incaricato_trasporto          varchar
     ,totale_colli                  integer
     ,totale_peso                   varchar
     ,applicazione_sconti           varchar
     ,id_cliente                    bigint
     ,id_fornitore                  bigint
     ,id_destinazione_merce         bigint
     ,id_pagamento                  bigint
     ,id_banca                      bigint
     ,id_aliquota_iva_esenzione     bigint
     ,id_vettore                    bigint
     ,id_agente                     bigint
     ,porto                         varchar
     ,documento_saldato             boolean
     ,totale_pagato                 decimal(16,4)
     ,totale_sospeso                decimal(16,4)
     ,id_primo_riferimento          bigint
     ,id_secondo_riferimento        bigint
     ,costo_da_ripartire	        decimal(16,4)
     ,ripartire_importo             boolean

);

CREATE TYPE promogest.testata_documento_sel_type AS (
      id                            bigint
     ,numero                        integer
     ,parte                         integer
     ,registro_numerazione          varchar
     ,operazione                    varchar
     ,data_documento                date
     ,data_inserimento              timestamp
     ,protocollo                    varchar
     ,note_interne                  text
     ,note_pie_pagina               varchar
     ,causale_trasporto             varchar
     ,aspetto_esteriore_beni        varchar
     ,inizio_trasporto              timestamp
     ,fine_trasporto                timestamp
     ,incaricato_trasporto          varchar
     ,totale_colli                  integer
     ,totale_peso                   varchar
     ,applicazione_sconti           varchar
     ,id_cliente                    bigint
     ,id_fornitore                  bigint
     ,id_destinazione_merce         bigint
     ,id_pagamento                  bigint
     ,id_banca                      bigint
     ,id_aliquota_iva_esenzione     bigint
     ,id_vettore                    bigint
     ,id_agente                     bigint
     ,porto                         varchar
     ,documento_saldato             boolean
     ,totale_pagato                 decimal(16,4)
     ,totale_sospeso                decimal(16,4)
     ,id_primo_riferimento          bigint
     ,id_secondo_riferimento        bigint
     ,costo_da_ripartire	        decimal(16,4)
     ,ripartire_importo             boolean
     ,ragione_sociale_cliente       varchar
     ,cognome_cliente               varchar
     ,nome_cliente                  varchar
     ,indirizzo_cliente             varchar
     ,localita_cliente              varchar
     ,cap_cliente                   char
     ,provincia_cliente             varchar
     ,codice_fiscale_cliente        varchar
     ,partita_iva_cliente           varchar
     ,ragione_sociale_fornitore     varchar
     ,cognome_fornitore             varchar
     ,nome_fornitore                varchar
     ,indirizzo_fornitore           varchar
     ,localita_fornitore            varchar
     ,cap_fornitore                 char
     ,provincia_fornitore           varchar
     ,codice_fiscale_fornitore      varchar
     ,partita_iva_fornitore         varchar
     ,destinazione_merce            varchar
     ,indirizzo_destinazione_merce  varchar
     ,localita_destinazione_merce   varchar
     ,cap_destinazione_merce        char
     ,provincia_destinazione_merce  varchar
     ,pagamento                     varchar
     ,banca                         varchar
     ,agenzia                       varchar
     ,iban                          varchar
     ,aliquota_iva_esenzione        varchar
     ,ragione_sociale_vettore       varchar
     ,ragione_sociale_agente        varchar
);

CREATE TYPE promogest.testata_documento_sel_count_type AS (
    count       bigint
);

CREATE OR REPLACE FUNCTION promogest.TestataDocumentoGet(varchar, bigint, bigint) RETURNS SETOF promogest.testata_documento_type AS E'
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
        
        FOR v_row IN SELECT * FROM v_testata_documento WHERE id = _id LOOP
            RETURN NEXT v_row;
        END LOOP;
                                    
        -- Imposta schema precedente
        sql_command:= \'SET SEARCH_PATH TO \' || schema_prec;
        EXECUTE sql_command;

        RETURN;
    END;
' LANGUAGE plpgsql;



CREATE OR REPLACE FUNCTION promogest.TestataDocumentoSel(varchar, bigint, varchar, integer, integer, integer, integer, date, date, varchar, varchar, bigint, bigint, bigint, bigint, bigint, bigint, bigint, bigint) RETURNS SETOF promogest.testata_documento_sel_type AS E'
    DECLARE
        -- Parametri contesto
        _schema                 ALIAS FOR $1;
        _idutente               ALIAS FOR $2;
        
        -- Parametri procedura
        _orderby                ALIAS FOR $3;
        _da_numero              ALIAS FOR $4;
        _a_numero               ALIAS FOR $5;
        _da_parte               ALIAS FOR $6;
        _a_parte                ALIAS FOR $7;
        _da_data_documento      ALIAS FOR $8;
        _a_data_documento       ALIAS FOR $9;
        _protocollo             ALIAS FOR $10;
        _operazione             ALIAS FOR $11;
        _id_magazzino           ALIAS FOR $12;
        _id_cliente             ALIAS FOR $13;
        _id_fornitore           ALIAS FOR $14;
        _id_agente              ALIAS FOR $15;
        _documento_saldato      ALIAS FOR $16;
        _id_articolo            ALIAS FOR $17;
        _offset                 ALIAS FOR $18;
        _count                  ALIAS FOR $19;
        
        schema_prec             varchar(2000);
        sql_statement           varchar(2000);
        sql_cond                varchar(2000);
        limitstring             varchar(500);
        _add                    varchar(500);
        OrderBy                 varchar(200);
        v_row                   record;
        _tablename              varchar;
        condition               varchar(10);
    BEGIN
        -- Memorizza schema precedente
        schema_prec:= ARRAY_TO_STRING(CURRENT_SCHEMAS(\'t\'),\',\');
    
        -- Imposta schema corrente
        sql_statement:= \'SET SEARCH_PATH TO \' || _schema;
        EXECUTE sql_statement;

        sql_statement:= \'SELECT TD.* FROM v_testata_documento_completa TD \';
        sql_cond:=\'\';
        
        IF _orderby IS NULL THEN
            OrderBy = \' TD.numero  \';
        ELSE
            OrderBy = _orderby;
        END IF;
        
        IF _da_numero IS NOT NULL THEN
            _add:= \' ( TD.numero >= \' || _da_numero || \') \';
            sql_cond:= promogest.sqlAddCondition(sql_cond,_add);
        END IF;
        
        IF _a_numero IS NOT NULL THEN
            _add:= \' ( TD.numero <= \' || _a_numero || \') \';
            sql_cond:= promogest.sqlAddCondition(sql_cond,_add);
        END IF;
        
        IF _da_parte IS NOT NULL THEN
            _add:= \' ( TD.parte >= \' || _da_parte || \') \';
            sql_cond:= promogest.sqlAddCondition(sql_cond,_add);
        END IF;
        
        IF _a_parte IS NOT NULL THEN
            _add:= \' ( TD.parte <= \' || _a_parte || \') \';
            sql_cond:= promogest.sqlAddCondition(sql_cond,_add);
        END IF;
        
        IF _da_data_documento IS NOT NULL THEN
            _add:= \' ( TD.data_documento >= \' || QUOTE_LITERAL(_da_data_documento) || \') \';
            sql_cond:= promogest.sqlAddCondition(sql_cond,_add);
        END IF;
        
        IF _a_data_documento IS NOT NULL THEN
            _add:= \' ( TD.data_documento <= \' || QUOTE_LITERAL(_a_data_documento) || \') \';
            sql_cond:= promogest.sqlAddCondition(sql_cond,_add);
        END IF;
        
        IF _protocollo IS NOT NULL THEN
            _add:= \' TD.protocollo ILIKE \'\'%\' || _protocollo || \'%\'\'\';
            sql_cond:= promogest.sqlAddCondition(sql_cond,_add);
        END IF;
        
        IF _operazione IS NOT NULL THEN
            _add:= \' TD.operazione = \' || QUOTE_LITERAL(_operazione);
            sql_cond:= promogest.sqlAddCondition(sql_cond,_add);
        END IF;

        IF _id_magazzino IS NOT NULL THEN
            _add:= \' TD.id IN (SELECT id_testata_documento FROM v_riga_documento WHERE id_magazzino = \' || _id_magazzino || \') \';
            sql_cond:= promogest.sqlAddCondition(sql_cond,_add);
        END IF;
        

        IF _id_cliente IS NOT NULL THEN
            _add:= \' TD.id_cliente = \' || _id_cliente;
            sql_cond:= promogest.sqlAddCondition(sql_cond,_add);
        ELSE
            SELECT INTO _tablename * FROM promogest.ClienteFilteredExists(_schema, _idutente);
            IF _tablename <> \'\' THEN
                sql_statement:= sql_statement || \' INNER JOIN \' || _tablename || \' CF ON TD.id_cliente = CF.id\';
            END IF;
        END IF;

        IF _id_fornitore IS NOT NULL THEN
            _add:= \' TD.id_fornitore = \' || _id_fornitore;
            sql_cond:= promogest.sqlAddCondition(sql_cond,_add);
        ELSE
            SELECT INTO _tablename * FROM promogest.FornitoreFilteredExists(_schema, _idutente);
            IF _tablename <> \'\' THEN
                sql_statement:= sql_statement || \' INNER JOIN \' || _tablename || \' FF ON TD.id_fornitore = FF.id\';
            END IF;
        END IF;

        IF _id_agente IS NOT NULL THEN
            _add:= \' TD.id_agente = \' || _id_agente;
            sql_cond:= promogest.sqlAddCondition(sql_cond,_add);
        END IF;

        IF _documento_saldato = 1 THEN
            condition:= \'f\';
            _add:= \' ( TD.documento_saldato = \' || QUOTE_LITERAL(condition) || \') \';
            sql_cond:= promogest.sqlAddCondition(sql_cond,_add);
        END IF;

        IF _documento_saldato = 2 THEN
            condition:= \'t\';
            _add:= \' ( TD.documento_saldato = \' || QUOTE_LITERAL(condition) || \') \';
            sql_cond:= promogest.sqlAddCondition(sql_cond,_add);
        END IF;

        if _id_articolo IS NOT NULL THEN
            _add:= \' TD.id in (select  RD.id_testata_documento from v_riga_documento RD where RD.id in (select R.id from riga R Where id_articolo = \' || _id_articolo || \' ))\'; 
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

CREATE OR REPLACE FUNCTION promogest.TestataDocumentoSelCount(varchar, bigint, varchar, integer, integer, integer, integer, date, date, varchar, varchar, bigint, bigint, bigint, bigint, bigint, bigint, bigint, bigint) RETURNS SETOF promogest.testata_documento_sel_count_type AS E'
    DECLARE
        -- Parametri contesto
        _schema                 ALIAS FOR $1;
        _idutente               ALIAS FOR $2;
        
        -- Parametri procedura
        _orderby                ALIAS FOR $3;
        _da_numero              ALIAS FOR $4;
        _a_numero               ALIAS FOR $5;
        _da_parte               ALIAS FOR $6;
        _a_parte                ALIAS FOR $7;
        _da_data_documento      ALIAS FOR $8;
        _a_data_documento       ALIAS FOR $9;
        _protocollo             ALIAS FOR $10;
        _operazione             ALIAS FOR $11;
        _id_magazzino           ALIAS FOR $12;
        _id_cliente             ALIAS FOR $13;
        _id_fornitore           ALIAS FOR $14;
        _id_agente              ALIAS FOR $15;
        _documento_saldato      ALIAS FOR $16;
        _id_articolo            ALIAS FOR $17;
        _offset                 ALIAS FOR $18;
        _count                  ALIAS FOR $19;
        
        schema_prec             varchar(2000);
        sql_statement           varchar(2000);
        sql_cond                varchar(2000);
        limitstring             varchar(500);
        _add                    varchar(500);
        OrderBy                 varchar(200);
        v_row                   record;
        _tablename              varchar;
        condition            varchar(10);
    BEGIN
        -- Memorizza schema precedente
        schema_prec:= ARRAY_TO_STRING(CURRENT_SCHEMAS(\'t\'),\',\');
    
        -- Imposta schema corrente
        sql_statement:= \'SET SEARCH_PATH TO \' || _schema;
        EXECUTE sql_statement;

        sql_statement:= \'SELECT COUNT(TD.id) FROM v_testata_documento_completa TD \';
        sql_cond:=\'\';

        IF _da_numero IS NOT NULL THEN
            _add:= \' ( TD.numero >= \' || _da_numero || \') \';
            sql_cond:= promogest.sqlAddCondition(sql_cond,_add);
        END IF;
        
        IF _a_numero IS NOT NULL THEN
            _add:= \' ( TD.numero <= \' || _a_numero || \') \';
            sql_cond:= promogest.sqlAddCondition(sql_cond,_add);
        END IF;
        
        IF _da_parte IS NOT NULL THEN
            _add:= \' ( TD.parte >= \' || _da_parte || \') \';
            sql_cond:= promogest.sqlAddCondition(sql_cond,_add);
        END IF;
        
        IF _a_parte IS NOT NULL THEN
            _add:= \' (TD.parte <= \' || _a_parte || \') \';
            sql_cond:= promogest.sqlAddCondition(sql_cond,_add);
        END IF;
        
        IF _da_data_documento IS NOT NULL THEN
            _add:= \' ( TD.data_documento >= \' || QUOTE_LITERAL(_da_data_documento) || \') \';
            sql_cond:= promogest.sqlAddCondition(sql_cond,_add);
        END IF;
        
        IF _a_data_documento IS NOT NULL THEN
            _add:= \' ( TD.data_documento <= \' || QUOTE_LITERAL(_a_data_documento) || \') \';
            sql_cond:= promogest.sqlAddCondition(sql_cond,_add);
        END IF;
        
        IF _protocollo IS NOT NULL THEN
            _add:= \' TD.protocollo ILIKE \'\'%\' || _protocollo || \'%\'\'\';
            sql_cond:= promogest.sqlAddCondition(sql_cond,_add);
        END IF;
        
        IF _operazione IS NOT NULL THEN
            _add:= \' TD.operazione = \' || QUOTE_LITERAL(_operazione);
            sql_cond:= promogest.sqlAddCondition(sql_cond,_add);
        END IF;

        IF _id_magazzino IS NOT NULL THEN
            _add:= \' TD.id IN (SELECT id_testata_documento FROM v_riga_documento WHERE id_magazzino = \' || _id_magazzino || \') \';
            sql_cond:= promogest.sqlAddCondition(sql_cond,_add);
        END IF;
        

        IF _id_cliente IS NOT NULL THEN
            _add:= \' TD.id_cliente = \' || _id_cliente;
            sql_cond:= promogest.sqlAddCondition(sql_cond,_add);
        ELSE
            SELECT INTO _tablename * FROM promogest.ClienteFilteredExists(_schema, _idutente);
            IF _tablename <> \'\' THEN
                sql_statement:= sql_statement || \' INNER JOIN \' || _tablename || \' CF ON TD.id_cliente = CF.id\';
            END IF;
        END IF;

        IF _id_fornitore IS NOT NULL THEN
            _add:= \' TD.id_fornitore = \' || _id_fornitore;
            sql_cond:= promogest.sqlAddCondition(sql_cond,_add);
        ELSE
            SELECT INTO _tablename * FROM promogest.FornitoreFilteredExists(_schema, _idutente);
            IF _tablename <> \'\' THEN
                sql_statement:= sql_statement || \' INNER JOIN \' || _tablename || \' FF ON TD.id_fornitore = FF.id\';
            END IF;
        END IF;

        IF _id_agente IS NOT NULL THEN
            _add:= \' TD.id_agente = \' || _id_agente ;
            sql_cond:= promogest.sqlAddCondition(sql_cond,_add);
        END IF;
        
        IF _documento_saldato = 1 THEN
            condition:= \'f\';
            _add:= \' ( TD.documento_saldato = \' || QUOTE_LITERAL(condition) || \') \';
            sql_cond:= promogest.sqlAddCondition(sql_cond,_add);
        END IF;

        IF _documento_saldato = 2 THEN
            condition:= \'t\';
            _add:= \' ( TD.documento_saldato = \' || QUOTE_LITERAL(condition) || \') \';
            sql_cond:= promogest.sqlAddCondition(sql_cond,_add);
        END IF;

        IF _id_articolo IS NOT NULL THEN
            _add:= \' TD.id in (select  RD.id_testata_documento from riga_documento RD where RD.id in (select R.id from riga R Where id_articolo = \' || _id_articolo || \' ))\'; 
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
