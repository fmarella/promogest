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

associazione articoli - Procedure di inserimento/aggiornamento

*/

DROP FUNCTION promogest.AssociazioneArticoloInsUpd(varchar,bigint,bigint,bigint,bigint) CASCADE;
CREATE OR REPLACE FUNCTION promogest.AssociazioneArticoloInsUpd(varchar,bigint,bigint,bigint,bigint,integer) RETURNS promogest.resultid AS 
$$
    DECLARE
        -- Parametri contesto
        _schema                         ALIAS FOR $1;
        _idutente                       ALIAS FOR $2;
        
        --parametri tabella
        _id                             ALIAS FOR $3;
        _id_padre                       ALIAS FOR $4;
        _id_figlio                      ALIAS FOR $5;
        _posizione                      ALIAS FOR $6;
        
        _resultid                       promogest.resultid;
        logid                           bigint;
    BEGIN
    IF _id IS NULL THEN
        INSERT INTO associazioni_articoli(id_padre, id_figlio, posizione)
            VALUES (_id_padre, _id_figlio, _posizione);
    ELSE
        UPDATE associazioni_articoli SET
        id_padre = _id_padre
        ,id_figlio = _id_figlio
        ,posizione = _posizione
        WHERE id = _id;
        IF FOUND THEN
                PERFORM promogest.LogSet(_idutente, _schema, 'I', 'promogest.AssociazioneArticoloInsUpd', 'Modificata associazione articolo',NULL,_id);
        ELSE
                PERFORM promogest.LogSet(_idutente, _schema,  'E', 'promogest.AssociazioneArticoloInsUpd', 'Associazione articolo non trovata',NULL,_id);
                RAISE WARNING 'Associazione articolo non trovata: %',_id;
                logid := CURRVAL('promogest.application_log_id_seq');
                SELECT INTO _resultid logid;
            END IF;
    END IF;
        RETURN _resultid;
    END;
$$   LANGUAGE plpgsql;

