--
-- Copyright (C) 2005 by Promotux Informatica - http://www.promotux.it/
-- Author: JJDaNiMoTh <jjdanimoth@gmail.com>
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

misura_pezzo  - Stored procedure di inserimento/aggiornamento

*/

DROP FUNCTION promogest.MisuraPezzoInsUpd(varchar, bigint, bigint, decimal(16,4), decimal(16,4), bigint);
DROP FUNCTION promogest.MisuraPezzoInsUpd(varchar, bigint, bigint, decimal(16,4), decimal(16,4), decimal(16,4), bigint);
CREATE OR REPLACE FUNCTION promogest.MisuraPezzoInsUpd(varchar, bigint, bigint, decimal(16,4), decimal(16,4), decimal(16,4), bigint) RETURNS promogest.resultid AS E'

    DECLARE
        -- Parametri contesto
        _schema                     ALIAS FOR $1;
        _idutente                   ALIAS FOR $2;
        
        -- Parametri tabella
        _id                         ALIAS FOR $3;
        _altezza                    ALIAS FOR $4;
        _larghezza                  ALIAS FOR $5;
        _moltiplicatore             ALIAS FOR $6;
        -- Chiavi esterne
        _id_riga                    ALIAS FOR $7;

        schema_prec                 varchar(2000);
        logid                       bigint;
        _resultid                   promogest.resultid;
        TempId                      bigint;
    BEGIN
        IF _id IS NULL THEN
            INSERT INTO misura_pezzo (altezza, larghezza, moltiplicatore, id_riga) 
                VALUES (_altezza, _larghezza, _moltiplicatore, _id_riga);
                
            TempId := CURRVAL(\'misura_pezzo_id_seq\');

            PERFORM promogest.LogSet(_idutente, _schema, \'I\',\'promogest.MisuraPezzoInsUpd\',\'Inserito misura pezzi\',NULL,TempId);
            SELECT INTO _resultid TempId;
        ELSE
            UPDATE misura_pezzo SET
            altezza = _altezza
            ,larghezza = _larghezza
            ,moltiplicatore = _moltiplicatore
            ,id_riga = _id_riga
            WHERE id = _id;

            IF FOUND THEN
                PERFORM promogest.LogSet(_idutente, _schema, \'I\',\'promogest.MisuraPezzoInsUpd\',\'Modificata misura pezzi\',NULL,_id);
                SELECT INTO _resultid _id;
            ELSE
                PERFORM promogest.LogSet(_idutente, _schema,  \'E\',\'promogest.MisuraPezzoInsUpd\',\'riga documento non trovata\',NULL,_id);
                RAISE WARNING \'Riga documento non trovata: %\',_id;
                logid := CURRVAL(\'promogest.application_log_id_seq\');
                SELECT INTO _resultid -logid;
            END IF;
        END IF; 
        RETURN _resultid;
    END;
' LANGUAGE plpgsql;
