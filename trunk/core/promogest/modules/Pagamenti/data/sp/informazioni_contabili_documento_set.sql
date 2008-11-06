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

Informazioni Contabili Documento  - Stored procedure di inserimento/aggiornamento

*/


DROP FUNCTION promogest.InformazioniContabiliDocumentoInsUpd(varchar, bigint, bigint, boolean, bigint, bigint, bigint, decimal(16,4), decimal(16,4));
CREATE OR REPLACE FUNCTION promogest.InformazioniContabiliDocumentoInsUpd(varchar, bigint, bigint, boolean, bigint, bigint, bigint, decimal(16,4), decimal(16,4)) RETURNS promogest.resultid AS E'

    DECLARE
        -- Parametri contesto
        _schema                     ALIAS FOR $1;
        _idutente                   ALIAS FOR $2;
        
        -- Parametri tabella
        _id                             ALIAS FOR $3;
        _documento_saldato              ALIAS FOR $4;
        _id_documento                   ALIAS FOR $5;
        _id_primo_riferimento           ALIAS FOR $6;
        _id_secondo_riferimento         ALIAS FOR $7;
        _totale_pagato                  ALIAS FOR $8;
        _totale_sospeso                 ALIAS FOR $9;

        schema_prec                 varchar(2000);
        logid                       bigint;
        _resultid                   promogest.resultid;
        TempId                      bigint;
    BEGIN
            IF _id_documento IS NULL THEN
                INSERT INTO informazioni_contabili_documento ( documento_saldato, id_documento, id_primo_riferimento, id_secondo_riferimento, totale_pagato, totale_sospeso)
                VALUES (_documento_saldato, _id, _id_primo_riferimento, _id_secondo_riferimento, _totale_pagato, _totale_sospeso);
            ELSE
                UPDATE informazioni_contabili_documento SET
                    documento_saldato = _documento_saldato
                    ,id_primo_riferimento = _id_primo_riferimento
                    ,id_secondo_riferimento = _id_secondo_riferimento
                    ,totale_pagato = _totale_pagato
                    ,totale_sospeso = totale_sospeso
                WHERE id_documento = _id_documento;
            END IF;

            IF FOUND THEN
                PERFORM promogest.LogSet(_idutente, _schema, \'I\',\'promogest.InformazioniContabiliDocumentoInsUpd\',\'Modificati inf contabili doc\',NULL,_id);
                SELECT INTO _resultid _id;
            ELSE
                PERFORM promogest.LogSet(_idutente, _schema,  \'E\',\'promogest.InformazioniContabiliDocumentoInsUpd\',\'info doc non trovati\',NULL,_id);
                RAISE WARNING \'info doc non trovata: %\',_id;
                logid := CURRVAL(\'promogest.application_log_id_seq\');
                SELECT INTO _resultid -logid;
            END IF;
        RETURN _resultid;
    END;
' LANGUAGE plpgsql;
