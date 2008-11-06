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

colore  - Stored procedure di inserimento/aggiornamento

*/

DROP FUNCTION promogest.ColoreInsUpd(varchar, bigint, bigint, varchar, varchar);
CREATE OR REPLACE FUNCTION promogest.ColoreInsUpd(varchar, bigint, bigint, varchar, varchar) RETURNS promogest.resultid AS '
    DECLARE
        -- Parametri contesto
        _schema                     ALIAS FOR $1;
        _idutente                   ALIAS FOR $2;

        -- Parametri tabella
        _id                         ALIAS FOR $3;
        _denominazione_breve        ALIAS FOR $4;
        _denominazione              ALIAS FOR $5;

        sql_command                 varchar(2000);
        schema_prec                 varchar(2000);
        logid                       bigint;
        _resultid                   promogest.resultid;
        TempId                      bigint;
    BEGIN
        IF _id IS NULL THEN
            INSERT INTO colore (denominazione_breve, denominazione)
                VALUES (_denominazione_breve, _denominazione);

            TempId := CURRVAL(\'colore_id_seq\');
            PERFORM promogest.LogSet(_idutente, _schema, \'I\',\'promogest.ColoreInsUpd\',\'Inserito colore\',NULL,TempId);
            SELECT INTO _resultid TempId;
        ELSE
            UPDATE colore SET
                 denominazione_breve = COALESCE(_denominazione_breve,denominazione_breve)
                ,denominazione = COALESCE(_denominazione,denominazione)
            WHERE id = _id;

            IF FOUND THEN
                PERFORM promogest.LogSet(_idutente, _schema, \'I\',\'promogest.ColoreInsUpd\',\'Modificato colore\',NULL,_id);
                SELECT INTO _resultid _id;
            ELSE
                PERFORM promogest.LogSet(_idutente, _schema, \'E\',\'promogest.ColoreInsUpd\',\'Colore non trovato\',NULL,_id);
                RAISE WARNING \'Colore non trovata: %\',_id;
                logid := CURRVAL(\'promogest.application_log_id_seq\');
                SELECT INTO _resultid -logid;
            END IF;
        END IF;
        RETURN _resultid;
    END;
' LANGUAGE plpgsql;
