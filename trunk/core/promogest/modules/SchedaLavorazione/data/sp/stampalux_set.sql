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
 * Schede ordinazione  - Stored procedure di inserimento/aggiornamento
 * 
 *
 */ 

DROP FUNCTION promogest.schedaordinazioneinsupd("varchar", int8, int8, int8, text, "varchar", "varchar", "varchar", "varchar", "varchar", bool, int8, int8, bool, "varchar", "varchar", "varchar", "varchar", "varchar", "varchar", "varchar", "varchar", "varchar", "varchar", "varchar", "varchar", "varchar", "varchar", "varchar", "varchar", "varchar", "varchar", date, date, date, date, date, date, date, bool, bool, "varchar", "numeric", "varchar", "varchar", "varchar", "varchar", int8, int8);

CREATE OR REPLACE FUNCTION promogest.schedaordinazioneinsupd("varchar", int8, int8, int8, text, "varchar", "varchar", "varchar", "varchar", "varchar", bool, int8, int8, bool, "varchar", "varchar", "varchar", "varchar", "varchar", "varchar", "varchar", "varchar", "varchar", "varchar", "varchar", "varchar", "varchar", "varchar", "varchar", "varchar", "varchar", "varchar", date, date, date, date, date, date, date, bool, bool, "varchar", "numeric", "varchar", "varchar", "varchar", "varchar", int8, int8)
  RETURNS promogest.resultid AS
$$
    DECLARE
        -- Parametri contesto
        _schema                          ALIAS FOR $1;
        _idutente                        ALIAS FOR $2;
        
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
	    _documento_saldato               ALIAS FOR $40;
	    _fattura                         ALIAS FOR $41;
	    _ricevuta_associata              ALIAS FOR $42;
	    _totale_lordo                    ALIAS FOR $43;
	    _applicazione_sconti             ALIAS FOR $44;
	    _userid_cliente                  ALIAS FOR $45;
	    _passwd_cliente                  ALIAS FOR $46;
	    _lui_e_lei                       ALIAS FOR $47;
	    _id_cliente                      ALIAS FOR $48;
	    _id_magazzino		             ALIAS FOR $49;

	    schema_prec                      varchar(2000);
        sql_command                      varchar(2000);
        _resultid                        promogest.resultid;
        logid                            bigint;
        TempId                           bigint;
        _rec                             record;
    BEGIN

	IF _id IS NULL THEN
	    TempId := NEXTVAL('schede_ordinazioni_id_seq');

	    INSERT INTO schede_ordinazioni (id, numero, mezzo_ordinazione, mezzo_spedizione, disp_materiale, id_colore_stampa, id_carattere_stampa, bomba_in_cliche, codice_spedizione, operatore, nomi_sposi, provenienza, documento_saldato, fattura, ricevuta_associata, totale_lordo, applicazione_sconti, userid_cliente, passwd_cliente, lui_e_lei, id_cliente, id_magazzino)
	    VALUES (TempId, _numero, _mezzo_ordinazione, _mezzo_spedizione, _materiale_disponibile, _id_colore_stampa, _id_carattere_stampa, _bomba_in_cliche, _codice_spedizione, _operatore, _nomi_sposi, _provenienza, _documento_saldato, _fattura, _ricevuta_associata, _totale_lordo, _applicazione_sconti, _userid_cliente, _passwd_cliente, _lui_e_lei, _id_cliente, _id_magazzino);

	    INSERT INTO contatti_schede (referente, prima_email, seconda_email, telefono, cellulare, skype, id_scheda)
	    VALUES (_nome_contatto, _prima_email, _seconda_email, _telefono, _cellulare, _skype, TempId);

	    INSERT INTO datari(matrimonio, presa_in_carico, ordine_al_fornitore, consegna_bozza, spedizione, consegna, ricevuta, id_scheda)
	    VALUES (_data_matrimonio, _data_presa_in_carico, _data_ordine_al_fornitore, _data_consegna_bozza, _data_spedizione, _data_consegna, _data_ricevuta, TempId);

	    INSERT INTO note_schede(note_text, note_fornitore, note_final, note_spedizione, id_scheda)
	    VALUES (_note_text, _note_fornitore, _note_final, _note_spedizione, TempId);
	    
	    INSERT INTO recapiti_spedizioni (referente, presso, via_piazza, num_civ, zip, localita, provincia, stato, id_scheda)
	    VALUES (_referente, _presso, _via_piazza, _num_civ, _zip, _localita, _provincia, _stato, TempId);

	    SELECT INTO _resultid TempId;

	ELSE
		
	    UPDATE schede_ordinazioni SET
	    numero = _numero
	    , mezzo_ordinazione = _mezzo_ordinazione
	    , mezzo_spedizione = _mezzo_spedizione
	    , disp_materiale = _materiale_disponibile
	    , id_colore_stampa = _id_colore_stampa
	    , id_carattere_stampa = _id_carattere_stampa
	    , bomba_in_cliche = _bomba_in_cliche
	    , codice_spedizione = _codice_spedizione
	    , operatore = _operatore
	    , nomi_sposi = _nomi_sposi
	    , provenienza = _provenienza
	    , documento_saldato = _documento_saldato
	    , fattura = _fattura
	    , ricevuta_associata = _ricevuta_associata
	    , totale_lordo = _totale_lordo
	    , applicazione_sconti = _applicazione_sconti
	    , userid_cliente = _userid_cliente
	    , passwd_cliente = _passwd_cliente
	    , lui_e_lei = _lui_e_lei
	    , id_cliente = _id_cliente
	    , id_magazzino = _id_magazzino
	    WHERE id = _id;
	    

	    IF FOUND THEN
		PERFORM promogest.LogSet(_idutente, _schema, 'I', 'promogest.SchedeOrdinazioneInsUpd', 'Modificata scheda ordinazione',NULL,_id);
		SELECT INTO _resultid _id;

		UPDATE datari SET
		matrimonio = _data_matrimonio
		,presa_in_carico = _data_presa_in_carico
		,ordine_al_fornitore = _data_ordine_al_fornitore
		,consegna_bozza = _data_consegna_bozza
		,spedizione = _data_spedizione
		,consegna = _data_consegna
		,ricevuta = _data_ricevuta
		WHERE id_scheda = _id;

		IF FOUND THEN
		    UPDATE datari SET
		     matrimonio = _data_matrimonio
		    ,presa_in_carico = _data_presa_in_carico
		    ,ordine_al_fornitore = _data_consegna_bozza
		    ,consegna_bozza = _data_consegna_bozza
		    ,spedizione = _data_spedizione
		    ,consegna = _data_consegna
		    ,ricevuta = _data_ricevuta
		     WHERE id_scheda = _id;
			
		    IF FOUND THEN
			PERFORM promogest.LogSet(_idutente, _schema, 'I', 'promogest.SchedeOrdinazioneInsUpd', 'Modificata scheda ordinazione - datario',NULL,_id);
			SELECT INTO _resultid _id;

			 UPDATE recapiti_spedizioni SET
			 referente = _referente
			,presso = _presso
			,via_piazza = _via_piazza
			,num_civ = num_civ
			,zip = _zip
			,localita = _localita
			,provincia = _provincia
			,stato = _stato
			 WHERE id_scheda = _id;

			IF FOUND THEN
			    PERFORM promogest.LogSet(_idutente, _schema, 'I', 'promogest.SchedeOrdinazioneInsUpd', 'Modificata scheda ordinazione recapiti spedizioni',NULL,_id);
			    SELECT INTO _resultid _id;

			    UPDATE note_schede SET
			    note_text = _note_text
			   ,note_fornitore = _note_fornitore
		   	   ,note_final = _note_final
			   ,note_spedizione = _note_spedizione
			    WHERE id_scheda = _id;

			    IF FOUND THEN
				 PERFORM promogest.LogSet(_idutente, _schema, 'I', 'promogest.SchedeOrdinazioneInsUpd', 'Modificata scheda ordinazione note schede',NULL,_id);
				 SELECT INTO _resultid _id;

				 UPDATE contatti_schede SET
				 referente = _nome_contatto
				,prima_email = _prima_email
				,seconda_email = _seconda_email
				,telefono = _telefono
				,cellulare = _cellulare
				,skype = _skype
				 WHERE id_scheda = _id;

				IF FOUND THEN
				    PERFORM promogest.LogSet(_idutente, _schema, 'I', 'promogest.SchedeOrdinazioneInsUpd', 'Modificata scheda ordinazione - contatti sched',NULL,_id);
				    SELECT INTO _resultid _id;
				ELSE
				    PERFORM promogest.LogSet(_idutente, _schema,  'E', 'promogest.SchedeOrdinazioneInsUpd', 'Scheda ordinazione - set di contatti non trovato',NULL,_id);
				    RAISE WARNING 'Scheda ordinazione - set di contatti non trovato: %',_id;
				    logid := CURRVAL('promogest.application_log_id_seq');
				    SELECT INTO _resultid logid;
				END IF;
			    ELSE
				PERFORM promogest.LogSet(_idutente, _schema,  'E', 'promogest.SchedeOrdinazioneInsUpd', 'Scheda ordinazione - set note non trovato',NULL,_id);
				RAISE WARNING 'Scheda ordinazione - set note non trovato: %',_id;
				logid := CURRVAL('promogest.application_log_id_seq');
				SELECT INTO _resultid logid;
			    END IF;	
			ELSE
			    PERFORM promogest.LogSet(_idutente, _schema,  'E', 'promogest.SchedeOrdinazioneInsUpd', 'Scheda ordinazione - set indirizzo non trovato',NULL,_id);
			    RAISE WARNING 'Scheda ordinazione - set indirizzo non trovato: %',_id;
			    logid := CURRVAL('promogest.application_log_id_seq');
			    SELECT INTO _resultid logid;
			END IF;
		    ELSE
			PERFORM promogest.LogSet(_idutente, _schema,  'E', 'promogest.SchedeOrdinazioneInsUpd', 'Set di date non trovat',NULL,_id);
			RAISE WARNING 'Scheda ordinazione - Set di date non trovate: %',_id;
			logid := CURRVAL('promogest.application_log_id_seq');
			SELECT INTO _resultid logid;
		    END IF;
		ELSE
   		    PERFORM promogest.LogSet(_idutente, _schema,  'E', 'promogest.SchedeOrdinazioneInsUpd', 'Scheda ordinazione non trovata',NULL,_id);
		    RAISE WARNING 'Scheda ordinazione non trovata: %',_id;
		    logid := CURRVAL('promogest.application_log_id_seq');
		    SELECT INTO _resultid logid;
		END IF;
        END IF;
    END IF;
        RETURN _resultid;
    END;
$$ LANGUAGE plpgsql;

