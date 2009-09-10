--
-- Copyright (C) 2005 by Promotux Informatica - http://www.promotux.it/
-- Author: JJDaNiMoTh <jjdanimoth@gmail.com>
--          Dr astico <marco@promotux.it>
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

riga_documento  - Stored procedure applicativa

*/

DROP FUNCTION promogest.RigheDocumentoDel(varchar, bigint, bigint);
CREATE OR REPLACE FUNCTION promogest.RigheDocumentoDel(varchar, bigint, bigint) RETURNS promogest.resultid AS E'
    DECLARE
        -- Parametri contesto
        _schema                     ALIAS FOR $1;
        _idutente                   ALIAS FOR $2;

        -- Parametri tabella
        _id_testata_documento       ALIAS FOR $3;

        schema_prec                 varchar(2000);
        sql_command                 varchar(2000);
        _ret                        promogest.resultid;
        _rec                        record;
        _id_testata_movimento       bigint;
    BEGIN
        -- Memorizza schema precedente
        schema_prec:= ARRAY_TO_STRING(CURRENT_SCHEMAS(\'t\'),\',\');

        -- Imposta schema corrente
        sql_command:= \'SET SEARCH_PATH TO \' || _schema;
        EXECUTE sql_command;

        -- Cerco eventuale movimento associato
        SELECT INTO _id_testata_movimento id FROM testata_movimento WHERE id_testata_documento = _id_testata_documento;

        -- Cancello righe e misure del documento
        DELETE FROM riga WHERE id IN (SELECT id FROM riga_documento WHERE id_testata_documento = _id_testata_documento);

        -- Cancello righe del movimento
        DELETE FROM misura_pezzo WHERE id_riga IN (SELECT id FROM riga_movimento WHERE id_testata_movimento = _id_testata_movimento);
        DELETE FROM riga WHERE id IN (SELECT id FROM riga_movimento WHERE id_testata_movimento = _id_testata_movimento);

        -- Imposta schema precedente
        sql_command:= \'SET SEARCH_PATH TO \' || schema_prec;
        EXECUTE sql_command;

        RETURN _ret;
    END;
' LANGUAGE plpgsql;
