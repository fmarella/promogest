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

sconto_riga_scheda  - Stored procedure di inserimento/aggiornamento

*/

DROP FUNCTION promogest.ScontoRigaSchedaInsUpd(varchar, bigint, bigint, decimal(16,4), varchar, bigint);
CREATE OR REPLACE FUNCTION promogest.ScontoRigaSchedaInsUpd(varchar, bigint, bigint, decimal(16,4), varchar, bigint) RETURNS promogest.resultid AS 
$$
    DECLARE
        -- Parametri contesto
        _schema                 ALIAS FOR $1;
        _idutente               ALIAS FOR $2;
        
        -- Parametri tabella
        _id                     ALIAS FOR $3;
        _valore                 ALIAS FOR $4;
        _tipo_sconto            ALIAS FOR $5;
        _id_riga_scheda         ALIAS FOR $6;
        
        sql_command             varchar(2000);
        schema_prec             varchar(2000);
        logid                   bigint;
        _resultid               promogest.resultid;
        TempId                  bigint;
    BEGIN
        IF _id IS NULL THEN
            INSERT INTO sconto (valore,tipo_sconto) 
                VALUES (_valore,_tipo_sconto);

            TempId := CURRVAL('sconto_id_seq');

            INSERT INTO sconti_righe_schede (id, id_riga_scheda) 
                VALUES (TempId, _id_riga_scheda);
                
            PERFORM promogest.LogSet(_idutente, _schema, 'I','promogest.ScontoRigaSchedaInsUpd','Inserito sconto',NULL,TempId);
            SELECT INTO _resultid TempId;
        ELSE
            UPDATE sconto SET
                 valore = COALESCE(_valore,valore)
                ,tipo_sconto = COALESCE(_tipo_sconto,tipo_sconto)
            WHERE id = _id;

            UPDATE sconti_righe_schede SET
                 id_riga_scheda = _id_riga_scheda
            WHERE id = _id;

            IF FOUND THEN
                PERFORM promogest.LogSet(_idutente, _schema, 'I','promogest.ScontoRigaSchedaInsUpd','Modificato sconto',NULL,_id);
                SELECT INTO _resultid _id;
            ELSE
                PERFORM promogest.LogSet(_idutente, _schema,  'E','promogest.ScontoRigaSchedaInsUpd','Sconto non trovato',NULL,_id);
                RAISE WARNING 'Sconto non trovato: %', _id;
                logid := CURRVAL('promogest.application_log_id_seq');
                SELECT INTO _resultid -logid;
            END IF;
        END IF; 
        RETURN _resultid;
    END;
$$ LANGUAGE plpgsql;
