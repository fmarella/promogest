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
-- MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
-- GNU General Public License for more details.
--
-- You should have received a copy of the GNU General Public License
-- along with this program; if not, write to the Free Software
-- Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.

/*

articolo_tagla_colore  - Stored procedure di inserimento/aggiornamento

*/

DROP FUNCTION promogest.ArticoloTagliaColoreInsUpd(varchar, bigint, bigint, bigint, bigint, bigint, bigint);
DROP FUNCTION promogest.ArticoloTagliaColoreInsUpd(varchar, bigint, bigint, bigint, bigint, bigint, bigint, bigint, bigint, bigint);
CREATE OR REPLACE FUNCTION promogest.ArticoloTagliaColoreInsUpd(varchar, bigint, bigint, bigint, bigint, bigint, bigint, bigint, bigint, bigint) RETURNS promogest.resultid AS '
    DECLARE
        -- Parametri contesto
        _schema                     ALIAS FOR $1;
        _idutente                   ALIAS FOR $2;
                
        -- Parametri tabella
        _id_articolo                ALIAS FOR $3;
        _id_articolo_padre          ALIAS FOR $4;
        _id_gruppo_taglia           ALIAS FOR $5;
        _id_taglia                  ALIAS FOR $6;
        _id_colore                  ALIAS FOR $7;
        _id_anno                    ALIAS FOR $8;
        _id_stagione                ALIAS FOR $9;
        _id_genere                  ALIAS FOR $10;

        sql_command                 varchar(2000);
        schema_prec                 varchar(2000);
        logid                       bigint;
        _resultid                   promogest.resultid;
        TempId                      bigint;
        _cnt                        bigint;
    BEGIN
        SELECT INTO _cnt COUNT(*) 
            FROM articolo_taglia_colore
            WHERE id_articolo = _id_articolo;
        
        IF NOT _cnt > 0 THEN
            INSERT INTO articolo_taglia_colore (id_articolo, id_articolo_padre, id_gruppo_taglia, id_taglia, id_colore, id_anno, id_stagione, id_genere)
                VALUES (_id_articolo, _id_articolo_padre, _id_gruppo_taglia, _id_taglia, _id_colore, _id_anno, _id_stagione, _id_genere);
                        
            PERFORM promogest.LogSet(_idutente, _schema, \'I\',\'promogest.ArticoloTagliaColoreInsUpd\',\'Inserito articolo taglia colore\',NULL,TempId);
            SELECT INTO _resultid _id_articolo;
        ELSE
            UPDATE articolo_taglia_colore SET
                 id_articolo_padre = _id_articolo_padre
                ,id_gruppo_taglia = _id_gruppo_taglia
                ,id_taglia = _id_taglia
                ,id_colore = _id_colore
                ,id_anno = _id_anno
                ,id_stagione = _id_stagione
                ,id_genere = _id_genere
            WHERE id_articolo = _id_articolo;

            IF FOUND THEN
                PERFORM promogest.LogSet(_idutente, _schema, \'I\',\'promogest.ArticoloTagliaColoreInsUpd\',\'Modificato articolo taglia colore\',NULL,_id_articolo);
                SELECT INTO _resultid _id_articolo;
            ELSE
                PERFORM promogest.LogSet(_idutente, _schema,  \'E\',\'promogest.ArticoloTagliaColoreInsUpd\',\'articolo taglia colore non trovato\',NULL,_id_articolo);
                RAISE WARNING \'articolo taglia colore non trovato: %\',_id_articolo;
                logid := CURRVAL(\'promogest.application_log_id_seq\');
                SELECT INTO _resultid -logid;
            END IF;
        END IF; 
        RETURN _resultid;
    END;
' LANGUAGE plpgsql;
