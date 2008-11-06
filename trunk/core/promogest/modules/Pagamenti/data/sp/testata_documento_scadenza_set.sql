--
-- Copyright (C) 2007 by Promotux Informatica - http://www.promotux.it/
-- Author: JJDaNiMoTh <jjdanimoth@gmail.com>
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

testata_documento_scadenza  - Stored procedure di inserimento/aggiornamento

*/

DROP FUNCTION promogest.TestataDocumentoScadenzaInsUpd(varchar, bigint, bigint, bigint, decimal(16,4), decimal(16,4), date, decimal(16,4), date, decimal(16,4), varchar, date, date, decimal(16,4), varchar, date, date, decimal(16,4), varchar, date, date, decimal(16,4), varchar, date, boolean);
DROP FUNCTION promogest.TestataDocumentoScadenzaInsUpd(varchar, bigint, bigint, bigint, date, decimal(16,4), varchar, date);

CREATE OR REPLACE FUNCTION promogest.TestataDocumentoScadenzaInsUpd(varchar, bigint, bigint, bigint, date, decimal(16,4), varchar, date, bigint) RETURNS promogest.resultid AS E'
    DECLARE
        -- Parametri contesto
        _schema                     ALIAS FOR $1;
        _idutente                   ALIAS FOR $2;
        
        -- Parametri tabella
        _id                             ALIAS FOR $3;
        _id_testata_documento           ALIAS FOR $4;
        _data                           ALIAS FOR $5;
        _importo                        ALIAS FOR $6;
        _pagamento                      ALIAS FOR $7;
        _data_pagamento                 ALIAS FOR $8;
        _numero_scadenza                ALIAS FOR $9;

        schema_prec                 varchar(2000);
        logid                       bigint;
        _resultid                   promogest.resultid;
        TempId                      bigint;
    BEGIN
        IF _id IS NULL THEN
            INSERT INTO testata_documento_scadenza (id_testata_documento, data, importo, pagamento, data_pagamento, numero_scadenza) 
                VALUES (_id_testata_documento, _data, _importo, _pagamento, _data_pagamento, _numero_scadenza);
                
            TempId := CURRVAL(\'testata_documento_scadenza_id_seq\');
            PERFORM promogest.LogSet(_idutente, _schema, \'I\',\'promogest.TestataDocumentoScadenzaInsUpd\',\'Inserita scadenza testata documento\',NULL,TempId);
            SELECT INTO _resultid TempId;
        ELSE
            UPDATE testata_documento_scadenza SET
                id_testata_documento = _id_testata_documento
                ,data_acconto = _data
                ,importo_acconto = _importo
                ,pagamento = _pagamento
                ,data_pagamento = _data_pagamento
                ,numero_scadenza = _numero_scadenza
            WHERE id = _id;

            IF FOUND THEN
                PERFORM promogest.LogSet(_idutente, _schema, \'I\',\'promogest.TestataDocumentoScadenzaInsUpd\',\'Modificata scadenza testata documento\',NULL,_id);
                SELECT INTO _resultid _id;
            ELSE
                PERFORM promogest.LogSet(_idutente, _schema,  \'E\',\'promogest.TestataDocumentoScadenzaInsUpd\',\'Testata documento non trovata\',NULL,_id);
                RAISE WARNING \'Testata documento non trovata: %\',_id;
                logid := CURRVAL(\'promogest.application_log_id_seq\');
                SELECT INTO _resultid -logid;
            END IF;
        END IF;
        RETURN _resultid;
    END;
' LANGUAGE plpgsql;
