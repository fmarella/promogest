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
 *
 * Schede lavorazione  - Stored procedure applicative (get-set-del)
 *
*/

DROP TYPE promogest.scheda_ordinazione_type CASCADE;
DROP TYPE promogest.scheda_ordinazione_sel_count_type CASCADE;
DROP TYPE promogest.scheda_ordinazione_sel_type CASCADE;



CREATE TYPE promogest.scheda_ordinazione_type AS
   (id int8,
    numero int8,
    note_text text,
    note_fornitore varchar,
    note_final varchar,
    note_spedizione varchar,
    mezzo_ordinazione varchar,
    mezzo_spedizione varchar,
    disp_materiale bool,
    id_colore_stampa int8,
    id_carattere_stampa int8,
    bomba_in_cliche bool,
    codice_spedizione varchar,
    operatore varchar,
    nomi_sposi varchar,
    provenienza varchar,
    nome_contatto varchar,
    prima_email varchar,
    seconda_email varchar,
    telefono varchar,
    cellulare varchar,
    skype varchar,
    referente varchar,
    presso varchar,
    via_piazza varchar,
    num_civ varchar,
    zip varchar,
    localita varchar,
    provincia varchar,
    stato varchar,
    data_matrimonio date,
    data_presa_in_carico date,
    data_ordine_al_fornitore date,
    data_consegna_bozza date,
    data_spedizione date,
    data_consegna date,
    data_ricevuta date,
    ricevuta_associata varchar,
    applicazione_sconti varchar,
    documento_saldato bool,
    fattura bool,
    totale_lordo numeric(16,4),
    userid_cliente varchar,
    passwd_cliente varchar,
    lui_e_lei varchar,
    id_cliente int8,
    id_magazzino int8,
    colore_stampa varchar,
    carattere_stampa varchar);


    

CREATE TYPE promogest.scheda_ordinazione_sel_type AS
   (id int8,
    numero int8,
    note_text text,
    note_fornitore varchar,
    note_final varchar,
    note_spedizione varchar,
    mezzo_ordinazione varchar,
    mezzo_spedizione varchar,
    disp_materiale bool,
    id_colore_stampa int8,
    id_carattere_stampa int8,
    bomba_in_cliche bool,
    codice_spedizione varchar,
    operatore varchar,
    nomi_sposi varchar,
    provenienza varchar,
    nome_contatto varchar,
    prima_email varchar,
    seconda_email varchar,
    telefono varchar,
    cellulare varchar,
    skype varchar,
    referente varchar,
    presso varchar,
    via_piazza varchar,
    num_civ varchar,
    zip varchar,
    localita varchar,
    provincia varchar,
    stato varchar,
    data_matrimonio date,
    data_presa_in_carico date,
    data_ordine_al_fornitore date,
    data_consegna_bozza date,
    data_spedizione date,
    data_consegna date,
    data_ricevuta date,
    ricevuta_associata varchar,
    applicazione_sconti varchar,
    documento_saldato bool,
    fattura bool,
    totale_lordo numeric(16,4),
    userid_cliente varchar,
    passwd_cliente varchar,
    lui_e_lei
    id_cliente int8,
    id_magazzino int8,
    colore_stampa varchar,
    carattere_stampa varchar);


CREATE TYPE promogest.scheda_ordinazione_sel_count_type AS (
    count                               bigint
);

DROP FUNCTION promogest.SchedaOrdinazioneSet ("varchar", int8, int8, int8, text, "varchar", "varchar", "varchar", "varchar", "varchar", bool, int8, int8, bool, "varchar", "varchar", "varchar", "varchar", "varchar", "varchar", "varchar", "varchar", "varchar", "varchar", "varchar", "varchar", "varchar", "varchar", "varchar", "varchar", "varchar", "varchar", date, date, date, date, date, date, date, "varchar", "varchar", bool, bool, "numeric", "varchar", "varchar", "varchar", int8, int8, "varchar", "varchar") CASCADE;
CREATE OR REPLACE FUNCTION promogest.schedaordinazioneset("varchar", int8, int8, int8, text, "varchar", "varchar", "varchar", "varchar", "varchar", bool, int8, int8, bool, "varchar", "varchar", "varchar", "varchar", "varchar", "varchar", "varchar", "varchar", "varchar", "varchar", "varchar", "varchar", "varchar", "varchar", "varchar", "varchar", "varchar", "varchar", date, date, date, date, date, date, date, "varchar", "varchar", bool, bool, "numeric", "varchar", "varchar", "varchar", int8, int8, "varchar", "varchar")
  RETURNS promogest.resultid AS
$$
    DECLARE
        -- Parametri contesto
        _schema                    	     ALIAS FOR $1;
        _idutente                	     ALIAS FOR $2;
        
        -- Parametri tabella
            _id                              ALIAS FOR $3;
            _numero                          ALIAS FOR $4;
            _note_text                       ALIAS FOR $5;
            _note_fornitore                  ALIAS FOR $6;
            _note_final                      ALIAS FOR $7;
            _note_spedizione                 ALIAS FOR $8;
            _mezzo_ordinazione               ALIAS FOR $9;
            _mezzo_spedizione                ALIAS FOR $10;
            _materiale_disponibile           ALIAS FOR $11;
            _id_colore_stampa                ALIAS FOR $12;
            _id_carattere_stampa             ALIAS FOR $13;
            _bomba_in_cliche                 ALIAS FOR $14;
            _codice_spedizione               ALIAS FOR $15;
            _operatore                       ALIAS FOR $16;
            _nomi_sposi                      ALIAS FOR $17;
            _provenienza                     ALIAS FOR $18;
            _nome_contatto                   ALIAS FOR $19;
            _prima_email                     ALIAS FOR $20;
            _seconda_email                   ALIAS FOR $21;
            _telefono                        ALIAS FOR $22;
            _cellulare                       ALIAS FOR $23;
            _skype                           ALIAS FOR $24;
            _referente                       ALIAS FOR $25;
            _presso                          ALIAS FOR $26;
            _via_piazza                      ALIAS FOR $27;    
            _num_civ                         ALIAS FOR $28;
            _zip                             ALIAS FOR $29;
            _localita                        ALIAS FOR $30;
            _provincia                       ALIAS FOR $31;
            _stato                           ALIAS FOR $32;
            _data_matrimonio                 ALIAS FOR $33;
	        _data_presa_in_carico            ALIAS FOR $34;
	        _data_ordine_al_fornitore        ALIAS FOR $35;
	        _data_consegna_bozza             ALIAS FOR $36;
	        _data_spedizione                 ALIAS FOR $37;
	        _data_consegna                   ALIAS FOR $38;
	        _data_ricevuta                   ALIAS FOR $39;
	        _ricevuta_associata              ALIAS FOR $40;
	        _applicazione_sconti             ALIAS FOR $41;
	        _documento_saldato               ALIAS FOR $42;
	        _fattura                	     ALIAS FOR $43;
	        _totale_lordo		             ALIAS FOR $44;
	        _userid_cliente                  ALIAS FOR $45;
	        _passwd_cliente                  ALIAS FOR $46;
	        _lui_e_lei                       ALIAS FOR $47;
	        _id_cliente                      ALIAS FOR $48;
	        _id_magazzino		             ALIAS FOR $49;



	        _number                          integer;
            _registro                        varchar(100);
            schema_prec                      varchar(2000);
            sql_command                      varchar(2000);
	        sql_statement		             varchar(2000);
            _ret                             promogest.resultid;
            _rec                             record;
    BEGIN
    
        -- Memorizza schema precedente
        schema_prec:= ARRAY_TO_STRING(CURRENT_SCHEMAS('t'),',');

        -- Imposta schema corrente
        sql_command:= 'SET SEARCH_PATH TO ' || _schema;
        EXECUTE sql_command;
        
        --Se siamo in inserimento ottengo numero e registro scheda
        IF _id IS NULL THEN
            SELECT numero, registro INTO _number, _registro FROM promogest.NumeroRegistroSchedaGet('Scheda Ordinazione', _data_presa_in_carico);
        ELSE
            _number:=_numero;
        END IF;
        
        SELECT * INTO _ret  FROM promogest.SchedaOrdinazioneInsUpd(_schema, _idutente, _id, _number, _note_text, _note_fornitore, _note_final,_note_spedizione, _mezzo_ordinazione, _mezzo_spedizione, _materiale_disponibile,_id_colore_stampa, _id_carattere_stampa, _bomba_in_cliche, _codice_spedizione, _operatore,_nomi_sposi, _provenienza, _nome_contatto, _prima_email,_seconda_email, _telefono, _cellulare, _skype, _referente, _presso,_via_piazza, _num_civ, _zip,  _localita, _provincia, _stato, _data_matrimonio,_data_presa_in_carico, _data_ordine_al_fornitore, _data_consegna_bozza, _data_spedizione, _data_consegna, _data_ricevuta, _documento_saldato, _fattura, _ricevuta_associata, _totale_lordo, _applicazione_sconti, _userid_cliente, _passwd_cliente, _lui_e_lei, _id_cliente, _id_magazzino );        
	-- reimposta lo schema precedente
        sql_command:= 'SET SEARCH_PATH TO ' || schema_prec;

        RETURN  _ret;

    END;
$$ LANGUAGE plpgsql;

DROP FUNCTION promogest.SchedaOrdinazioneGet(varchar,bigint,bigint);
CREATE OR REPLACE FUNCTION promogest.schedaordinazioneget("varchar", int8, int8)
  RETURNS SETOF promogest.scheda_ordinazione_type AS
$$
    DECLARE
        -- Parametri contesto
        _schema                         ALIAS FOR $1;
        _idutente                       ALIAS FOR $2;
        
        -- Parametri Tabella
        _id                             ALIAS FOR $3;
        
        schema_prec                     varchar(2000);
        sql_command                     varchar(2000);
        v_row                           record;
    BEGIN
        -- Memorizza schema precedente
        schema_prec:= ARRAY_TO_STRING(CURRENT_SCHEMAS('t'),',');

        -- Imposta schema corrente
        sql_command:= 'SET SEARCH_PATH TO ' || _schema;
        EXECUTE sql_command;
        
        FOR v_row IN SELECT * FROM v_scheda_ordinazione WHERE id = _id LOOP
            RETURN NEXT v_row;
        END LOOP;
        
        -- Imposta schema precedente
        sql_command:= 'SET SEARCH_PATH TO ' || schema_prec;
        EXECUTE sql_command;

        RETURN;
    END;
$$ LANGUAGE plpgsql;

DROP FUNCTION promogest.SchedaOrdinazioneDel (varchar, bigint, bigint);
CREATE OR REPLACE FUNCTION promogest.schedaordinazionedel("varchar", int8, int8)
  RETURNS SETOF promogest.resultid AS
$$
    DECLARE
        -- Parametri contesto
        _schema                         ALIAS FOR $1;
        _idutente                       ALIAS FOR $2;
        
        -- Parametri tabella
        _id		        		        ALIAS FOR $3;

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
        

        
        DELETE FROM schede_ordinazioni WHERE id = _id;
        DELETE FROM datari WHERE id_scheda = _id;
        DELETE FROM recapiti_spedizioni WHERE id_scheda = _id;
        DELETE FROM note_schede WHERE id_scheda = _id;
	    DELETE FROM contatti_schede WHERE id_scheda = _id;
	
        
        -- Imposta schema precedente
        sql_command:= 'SET SEARCH_PATH TO ' || schema_prec;
        EXECUTE sql_command;
        RETURN;
    END;
$$ LANGUAGE plpgsql;


DROP FUNCTION promogest.SchedaOrdinazioneSel("varchar", int8, "varchar", int8, int8, int8, int8, date, date, date, date, date, date, date, date, "varchar", "varchar", "varchar", "varchar", "varchar", bool, int8, int8, int8);
CREATE OR REPLACE FUNCTION promogest.schedaordinazionesel("varchar", int8, "varchar", int8, int8, int8, int8, date, date, date, date, date, date, date, date, "varchar", "varchar", "varchar", "varchar", "varchar", bool, int8, int8, int8)
  RETURNS SETOF promogest.scheda_ordinazione_type AS
$$
    DECLARE
        -- Parametri contesto
        _schema                 ALIAS FOR $1;
        _idutente               ALIAS FOR $2;
        
        -- Parametri procedura
        _orderby                ALIAS FOR $3;
        _da_numero              ALIAS FOR $4;
        _a_numero               ALIAS FOR $5;
        _colore_stampa          ALIAS FOR $6;
        _carattere_stampa       ALIAS FOR $7;
        _da_data_matrimonio     ALIAS FOR $8;
        _a_data_matrimonio      ALIAS FOR $9;
        _da_data_spedizione     ALIAS FOR $10;
        _a_data_spedizione      ALIAS FOR $11;
        _da_data_consegna       ALIAS FOR $12;
        _a_data_consegna        ALIAS FOR $13;
        _da_data_carico         ALIAS FOR $14;
        _a_data_carico	        ALIAS FOR $15;
        _operatore              ALIAS FOR $16;
        _referente              ALIAS FOR $17;
        _nomi_sposi             ALIAS FOR $18;
        _codice_spedizione      ALIAS FOR $19;
        _ricevuta_associata     ALIAS FOR $20;
        _documento_saldato      ALIAS FOR $21;
        _id_cliente             ALIAS FOR $22;
        _offset                 ALIAS FOR $23;
        _count                  ALIAS FOR $24;

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
        schema_prec:= ARRAY_TO_STRING(CURRENT_SCHEMAS('t'),',');
    
        -- Imposta schema corrente
        sql_statement:= 'SET SEARCH_PATH TO ' || _schema;
        EXECUTE sql_statement;

        sql_statement:= 'SELECT SO.* FROM v_scheda_ordinazione SO ';
        sql_cond:='';

        IF _orderby IS NULL THEN
            OrderBy = ' SO.numero  ';
        ELSE
            OrderBy = _orderby;
        END IF;
        
        IF _da_numero IS NOT NULL THEN
            _add:= ' ( SO.numero >= ' || _da_numero || ')';
            sql_cond:= promogest.sqlAddCondition(sql_cond,_add);
        END IF;
        
        IF _a_numero IS NOT NULL THEN
            _add:= ' ( SO.numero <= ' || _a_numero || ')';
            sql_cond:= promogest.sqlAddCondition(sql_cond,_add);
        END IF;
        
        IF _da_data_matrimonio IS NOT NULL THEN
            _add:= ' ( SO.data_matrimonio >= ' || QUOTE_LITERAL(_da_data_matrimonio) || ')';
            sql_cond:= promogest.sqlAddCondition(sql_cond,_add);
        END IF;
        
        IF _a_data_matrimonio IS NOT NULL THEN
            _add:= ' ( SO.data_matrimonio <= ' || QUOTE_LITERAL(_a_data_matrimonio) || ')';
            sql_cond:= promogest.sqlAddCondition(sql_cond,_add);
        END IF;

        IF _da_data_spedizione IS NOT NULL THEN
            _add:= ' ( SO.data_spedizione >= ' || QUOTE_LITERAL(_da_data_spedizione) || ')';
            sql_cond:= promogest.sqlAddCondition(sql_cond,_add);
        END IF;
        
        IF _a_data_spedizione IS NOT NULL THEN
            _add:= ' ( SO.data_spedizione <= ' || QUOTE_LITERAL(_a_data_spedizione) || ')';
            sql_cond:= promogest.sqlAddCondition(sql_cond,_add);
        END IF;

        IF _da_data_consegna IS NOT NULL THEN
            _add:= ' ( SO.data_consegna >= ' || QUOTE_LITERAL(_da_data_consegna) || ')';
            sql_cond:= promogest.sqlAddCondition(sql_cond,_add);
        END IF;
        
        IF _a_data_consegna IS NOT NULL THEN
            _add:= ' ( SO.data_consegna <= ' || QUOTE_LITERAL(_a_data_consegna) || ')';
            sql_cond:= promogest.sqlAddCondition(sql_cond,_add);
        END IF;
        
        IF _da_data_carico IS NOT NULL THEN
            _add:= ' ( SO.data_presa_in_carico >= ' || QUOTE_LITERAL(_da_data_carico) || ')';
            sql_cond:= promogest.sqlAddCondition(sql_cond,_add);
        END IF;
        
        IF _a_data_carico IS NOT NULL THEN
            _add:= ' ( SO.data_presa_in_carico <= ' || QUOTE_LITERAL(_a_data_carico) || ')';
            sql_cond:= promogest.sqlAddCondition(sql_cond,_add);
        END IF;

        IF _colore_stampa IS NOT NULL THEN
            _add:= ' SO.id_colore_stampa =' || _colore_stampa ;
            sql_cond:= promogest.sqlAddCondition(sql_cond,_add);
        END IF;
        
        IF _carattere_stampa IS NOT NULL THEN
            _add:= ' SO.id_carattere_stampa =' || _carattere_stampa ;
            sql_cond:= promogest.sqlAddCondition(sql_cond,_add);
        END IF;
        
        IF _operatore IS NOT NULL THEN
            _add:= E' SO.operatore ILIKE \'%' || _operatore || '%\' ';
            sql_cond:= promogest.sqlAddCondition(sql_cond,_add);
        END IF;
        
        IF _nomi_sposi IS NOT NULL THEN
            _add:= E' SO.nomi_sposi ILIKE \'%' || _nomi_sposi || '%\'' ';
            sql_cond:= promogest.sqlAddCondition(sql_cond,_add);
        END IF;

        IF _referente IS NOT NULL THEN
            _add:= E' SO.referente ILIKE \'%' || _referente || '%\' ';
            sql_cond:= promogest.sqlAddCondition(sql_cond,_add);
        END IF;

        IF _codice_spedizione IS NOT NULL THEN
            _add:= E' SO.codice_spedizione ILIKE \'%' || _codice_spedizione || '%\' ';
            sql_cond:= promogest.sqlAddCondition(sql_cond,_add);
        END IF;

        IF _ricevuta_associata IS NOT NULL THEN
            _add:= E' SO.ricevuta_associata ILIKE \'%' || _ricevuta_associata || '%\' ';
            sql_cond:= promogest.sqlAddCondition(sql_cond,_add);
        END IF;

        IF _documento_saldato = false THEN
            condition:= 'f';
            _add:= ' ( SO.documento_saldato = ' || QUOTE_LITERAL(condition) || ') ';
            sql_cond:= promogest.sqlAddCondition(sql_cond,_add);
        END IF;
        
        IF _documento_saldato = true THEN
            condition:= 't';
            _add:= ' ( SO.documento_saldato = ' || QUOTE_LITERAL(condition) || ') ';
            sql_cond:= promogest.sqlAddCondition(sql_cond,_add);
        END IF;
        
        IF _id_cliente IS NOT NULL THEN
            _add:= 'SO.id_cliente = ' || _id_cliente ||;
            sql_cond:= promogest.sqlAddCondition(sql_cond,_add);
        END IF;
        
        IF _offset IS NULL THEN
            limitstring:= '';
        ELSE
            limitstring:= ' LIMIT ' || _count || ' OFFSET ' || _offset;
        END IF;

        IF sql_cond != '' THEN
            sql_statement:= sql_statement || ' WHERE ' || sql_cond || ' ORDER BY ' || OrderBy || ' DESC ' || limitstring;
        ELSE
            sql_statement:= sql_statement || ' ORDER BY ' || OrderBy || ' DESC ' || limitstring;
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

DROP FUNCTION promogest.schedaordinazioneselcount("varchar", int8, int8, int8, int8, int8, date, date, date, date, date, date, "varchar", "varchar", "varchar", "varchar", "varchar", bool, int8);

CREATE OR REPLACE FUNCTION promogest.schedaordinazioneselcount("varchar", int8, int8, int8, int8, int8, date, date, date, date, date, date, date, date, "varchar", "varchar", "varchar", "varchar", "varchar", bool, int8)
  RETURNS SETOF promogest.scheda_ordinazione_sel_count_type AS
$$
    DECLARE
        -- Parametri contesto
        _schema                 ALIAS FOR $1;
        _idutente               ALIAS FOR $2;
        
        -- Parametri procedura
        _da_numero              ALIAS FOR $3;
        _a_numero               ALIAS FOR $4;
        _colore_stampa          ALIAS FOR $5;
        _carattere_stampa       ALIAS FOR $6;
        _da_data_matrimonio     ALIAS FOR $7;
        _a_data_matrimonio      ALIAS FOR $8;
        _da_data_spedizione     ALIAS FOR $9;
        _a_data_spedizione      ALIAS FOR $10;
        _da_data_consegna       ALIAS FOR $11;
        _a_data_consegna        ALIAS FOR $12;
        _da_data_carico         ALIAS FOR $13;
        _a_data_carico          ALIAS FOR $14;
        _operatore              ALIAS FOR $15;
        _referente              ALIAS FOR $16;
        _nomi_sposi             ALIAS FOR $17;
        _codice_spedizione      ALIAS FOR $18;
        _ricevuta_associata     ALIAS FOR $19;
        _documento_saldato      ALIAS FOR $20;
        _id_cliente             ALIAS FOR $21;

        schema_prec             varchar(2000);
        sql_statement           varchar(2000);
        sql_cond                varchar(2000);
        _add                    varchar(500);
        v_row                   record;
        _tablename              varchar;
        condition               varchar(10);
        
    BEGIN
        -- Memorizza schema precedente
        schema_prec:= ARRAY_TO_STRING(CURRENT_SCHEMAS('t'),',');
    
        -- Imposta schema corrente
        sql_statement:= 'SET SEARCH_PATH TO ' || _schema;
        EXECUTE sql_statement;

        sql_statement:= 'SELECT COUNT(SO.id) FROM v_scheda_ordinazione SO ';
        sql_cond:='';
        
        IF _da_numero IS NOT NULL THEN
            _add:= ' ( SO.numero >= ' || _da_numero || ')';
            sql_cond:= promogest.sqlAddCondition(sql_cond,_add);
        END IF;
        
        IF _a_numero IS NOT NULL THEN
            _add:= ' ( SO.numero <= ' || _a_numero || ')';
            sql_cond:= promogest.sqlAddCondition(sql_cond,_add);
        END IF;
        
        IF _da_data_matrimonio IS NOT NULL THEN
            _add:= ' ( SO.data_matrimonio >= ' || QUOTE_LITERAL(_da_data_matrimonio) || ')';
            sql_cond:= promogest.sqlAddCondition(sql_cond,_add);
        END IF;
        
        IF _a_data_matrimonio IS NOT NULL THEN
            _add:= ' ( SO.data_matrimonio <= ' || QUOTE_LITERAL(_a_data_matrimonio) || ')';
            sql_cond:= promogest.sqlAddCondition(sql_cond,_add);
        END IF;

        IF _da_data_spedizione IS NOT NULL THEN
            _add:= ' ( SO.data_spedizione >= ' || QUOTE_LITERAL(_da_data_spedizione) || ')';
            sql_cond:= promogest.sqlAddCondition(sql_cond,_add);
        END IF;
        
        IF _a_data_spedizione IS NOT NULL THEN
            _add:= ' ( SO.data_spedizione <= ' || QUOTE_LITERAL(_a_data_spedizione) || ')';
            sql_cond:= promogest.sqlAddCondition(sql_cond,_add);
        END IF;

        IF _da_data_consegna IS NOT NULL THEN
            _add:= ' ( SO.data_consegna >= ' || QUOTE_LITERAL(_da_data_consegna) || ')';
            sql_cond:= promogest.sqlAddCondition(sql_cond,_add);
        END IF;
        
        IF _a_data_consegna IS NOT NULL THEN
            _add:= ' ( SO.data_consegna <= ' || QUOTE_LITERAL(_a_data_consegna) || ')';
            sql_cond:= promogest.sqlAddCondition(sql_cond,_add);
        END IF;

        IF _da_data_carico IS NOT NULL THEN
            _add:= ' ( SO.data_presa_in_carico >= ' || QUOTE_LITERAL(_da_data_carico) || ')';
            sql_cond:= promogest.sqlAddCondition(sql_cond,_add);
        END IF;
        
        IF _a_data_carico IS NOT NULL THEN
            _add:= ' ( SO.data_presa_in_carico <= ' || QUOTE_LITERAL(_a_data_carico) || ')';
            sql_cond:= promogest.sqlAddCondition(sql_cond,_add);
        END IF;

        IF _colore_stampa IS NOT NULL THEN
            _add:= ' SO.id_colore_stampa =' || _id_colore_stampa ;
            sql_cond:= promogest.sqlAddCondition(sql_cond,_add);
        END IF;
        
        IF _carattere_stampa IS NOT NULL THEN
            _add:= ' SO.id_carattere_stampa =' || _id_carattere_stampa ;
            sql_cond:= promogest.sqlAddCondition(sql_cond,_add);
        END IF;
        
        IF _operatore IS NOT NULL THEN
            _add:= E' SO.operatore ILIKE \'%' || _operatore || '%\' ';
            sql_cond:= promogest.sqlAddCondition(sql_cond,_add);
        END IF;
        
        IF _nomi_sposi IS NOT NULL THEN
            _add:= E' SO.nomi_sposi ILIKE \'%' || _nomi_sposi || '%\' ';
            sql_cond:= promogest.sqlAddCondition(sql_cond,_add);
        END IF;

        IF _referente IS NOT NULL THEN
            _add:= E' SO.referente ILIKE \'%' || _referente || '%\' ';
            sql_cond:= promogest.sqlAddCondition(sql_cond,_add);
        END IF;

        IF _codice_spedizione IS NOT NULL THEN
            _add:= E' SO.codice_spedizione ILIKE \'%' || _codice_spedizione || '%\' ';
            sql_cond:= promogest.sqlAddCondition(sql_cond,_add);
        END IF;

        IF _ricevuta_associata IS NOT NULL THEN
            _add:= E' SO.ricevuta_associata ILIKE \'%' || _ricevuta_associata || '%\' ';
            sql_cond:= promogest.sqlAddCondition(sql_cond,_add);
        END IF;

        IF _documento_saldato = false THEN
            condition:= 'f';
            _add:= ' ( SO.documento_saldato = ' || QUOTE_LITERAL(condition) || ')';
            sql_cond:= promogest.sqlAddCondition(sql_cond,_add);
        END IF;
        
        IF _documento_saldato = true THEN
            condition:= 't';
            _add:= ' ( SO.documento_saldato = ' || QUOTE_LITERAL(condition) || ')';
            sql_cond:= promogest.sqlAddCondition(sql_cond,_add);
        END IF;
        
        IF _id_cliente IS NOT NULL THEN
            _add:= 'SO.id_cliente = ' || _id_cliente ||;
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


