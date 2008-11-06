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

GruppoTaglia<->Taglia  - Stored procedure di inserimento/aggiornamento

*/

DROP FUNCTION promogest.GruppoTagliaTagliaInsUpd(varchar, bigint, bigint, bigint);
DROP FUNCTION promogest.GruppoTagliaTagliaInsUpd(varchar, bigint, bigint, bigint, bigint);
CREATE OR REPLACE FUNCTION promogest.GruppoTagliaTagliaInsUpd(varchar, bigint, bigint, bigint, bigint) RETURNS promogest.resultid AS '
    DECLARE
        -- Parametri contesto
        _schema                 ALIAS FOR $1;
        _idutente               ALIAS FOR $2;

        -- Parametri tabella
        _id_gruppo_taglia       ALIAS FOR $3;
        _id_taglia              ALIAS FOR $4;
        _ordine                 ALIAS FOR $5;
                        
        sql_command             varchar(2000);
        schema_prec             varchar(2000);
        logid                   bigint;
        _resultid               promogest.resultid;
        TempId                  bigint;
        _cnt                    bigint;
    BEGIN
        SELECT INTO _cnt COUNT(*) 
            FROM gruppo_taglia_taglia
            WHERE id_gruppo_taglia = _id_gruppo_taglia AND id_taglia = _id_taglia;
        
        IF _cnt = 0 THEN
            INSERT INTO gruppo_taglia_taglia (id_gruppo_taglia, id_taglia, ordine) 
                VALUES (_id_gruppo_taglia, _id_taglia, _ordine);

            PERFORM promogest.LogSet(_idutente, _schema, \'I\',\'promogest.GruppoTagliaTagliaInsUpd\',\'Inserito GruppoTagliaTaglia\',NULL,NULL);
        ELSE
            UPDATE gruppo_taglia_taglia SET
                 ordine = COALESCE(_ordine,ordine)
            WHERE id_gruppo_taglia = _id_gruppo_taglia AND id_taglia = _id_taglia;
                
            IF FOUND THEN
                PERFORM promogest.LogSet(_idutente, _schema, \'I\',\'promogest.GruppoTagliaTagliaInsUpd\',\'Modificato GruppoTagliaTaglia\',NULL,NULL);
                SELECT INTO _resultid 1;
            ELSE
                PERFORM promogest.LogSet(_idutente, _schema, \'E\',\'promogest.GruppoTagliaTagliaInsUpd\',\'GruppoTagliaTaglia non trovato\',NULL,NULL);
                RAISE WARNING \'GruppoTagliaTaglia non trovato: \';
            END IF;
        END IF;
        RETURN _resultid;
    END;
' LANGUAGE plpgsql;
