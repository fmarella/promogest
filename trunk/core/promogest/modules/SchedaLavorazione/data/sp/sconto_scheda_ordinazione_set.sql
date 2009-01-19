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
-- MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
-- GNU General Public License for more details.
--
-- You should have received a copy of the GNU General Public License
-- along with this program; if not, write to the Free Software
-- Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.

/*

sconto_scheda_ordinazione  - Stored procedure di inserimento/aggiornamento

*/

DROP FUNCTION promogest.scontoschedaordinazioneinsupd("varchar", int8, int8, "numeric", "varchar", int8);

CREATE OR REPLACE FUNCTION promogest.scontoschedaordinazioneinsupd("varchar", int8, int8, "numeric", "varchar", int8)
  RETURNS promogest.resultid AS
$$
    DECLARE
        -- Parametri contesto
        _schema                 ALIAS FOR $1;
        _idutente               ALIAS FOR $2;
        
        -- Parametri tabella
        _id                     ALIAS FOR $3;
        _valore                 ALIAS FOR $4;
        _tipo_sconto            ALIAS FOR $5;
        _id_scheda_ordinazione   ALIAS FOR $6;
        
        sql_command             varchar(2000);
        schema_prec             varchar(2000);
	TempIdScheda		bigint;
        logid                   bigint;
        _resultid               promogest.resultid;
        TempId                  bigint;
    BEGIN

        -- Memorizza schema precedente
        schema_prec:= ARRAY_TO_STRING(CURRENT_SCHEMAS('t'),',');

        -- Imposta schema corrente
        sql_command:= 'SET SEARCH_PATH TO ' || _schema;
        EXECUTE sql_command;

        IF _id IS NULL THEN
            INSERT INTO sconto (valore,tipo_sconto) 
                VALUES (_valore,_tipo_sconto);

            TempId := CURRVAL('sconto_id_seq');
	    IF _id_scheda_ordinazione IS NULL THEN
		TempIdScheda := CURRVAL('schede_ordinazione_id_seq');
		INSERT INTO sconti_schede_ordinazioni (id, id_scheda_ordinazione) 
			VALUES (TempId, TempIdScheda);
	    ELSE

            INSERT INTO sconti_schede_ordinazioni (id, id_scheda_ordinazione) 
                VALUES (TempId, _id_scheda_ordinazione);
	    END IF;
                
            PERFORM promogest.LogSet(_idutente, _schema, 'I', 'promogest.ScontoSchedaOrdinazioneInsUpd', 'Inserito sconto',NULL,TempId);
            SELECT INTO _resultid TempId;
        ELSE
            UPDATE sconto SET
                 valore = COALESCE(_valore,valore)
                ,tipo_sconto = COALESCE(_tipo_sconto,tipo_sconto)
            WHERE id = _id;

            UPDATE sconti_schede_ordinazioni SET
                 id_scheda_ordinazione = _id_scheda_ordinazione
            WHERE id = _id;

            IF FOUND THEN
                PERFORM promogest.LogSet(_idutente, _schema, 'I', 'promogest.ScontoSchedaOrdinazioneInsUpd', 'Modificato sconto',NULL,_id);
                SELECT INTO _resultid _id;
            ELSE
                PERFORM promogest.LogSet(_idutente, _schema,  '', 'promogest.ScontoSchedaOrdinazioneInsUpd', 'Sconto non trovato',NULL,_id);
                RAISE WARNING 'Sconto non trovato: %', _id;
                logid := CURRVAL('promogest.application_log_id_seq');
                SELECT INTO _resultid -logid;
            END IF;
        END IF; 
        RETURN _resultid;
    END;
$$ LANGUAGE plpgsql;
