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

DROP FUNCTION promogest.ColoreStampaInsUpd (varchar,bigint, bigint, varchar);
CREATE OR REPLACE FUNCTION promogest.ColoreStampaInsUpd (varchar,bigint, bigint, varchar) RETURNS promogest.resultid AS
$$
    DECLARE
        --Parametri contesto
        _schema                         ALIAS FOR $1;
        _idutente                       ALIAS FOR $2;
        
        --Parametri tabella
        _id                             ALIAS FOR $3;
        _denominazione                  ALIAS FOR $4;

        _sql_statement                  varchar(2000);
        _sql_command                    varchar(2000);
        _resultid                       promogest.resultid;
        logid                           bigint;
        _rec                            record;
        
    BEGIN
        IF _id IS NULL THEN
            INSERT INTO colori_stampa (denominazione)
            VALUES (_denominazione);
        ELSE
            UPDATE colori_stampa SET
            denominazione = _denominazione
            WHERE id = _id;
        END IF;

	    IF FOUND THEN
                PERFORM promogest.LogSet(_idutente, _schema, 'I', 'promogest.ColoreStampaInsUpd', 'Modificato Colore stampa',NULL,_id);
                SELECT INTO _resultid _id;
            ELSE
                PERFORM promogest.LogSet(_idutente, _schema,  '', 'promogest.ColoreStampaInsUpd', 'Colore stampa non trovato',NULL,_id);
                RAISE WARNING 'Colore stampa non trovato: %',_id;
                logid := CURRVAL('promogest.application_log_id_seq');
                SELECT INTO _resultid -logid;
            END IF;

        RETURN _resultid;
    END;
$$ LANGUAGE plpgsql;
