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

testata_documento  - Stored procedure di inserimento/aggiornamento

*/

DROP FUNCTION promogest.TestataDocumentoInsUpd(varchar, bigint, bigint, integer, integer, varchar, varchar, date, timestamp, varchar, text, varchar, varchar, varchar, timestamp, timestamp, varchar, integer, varchar, varchar, bigint, bigint, bigint, bigint, bigint, bigint, bigint);
DROP FUNCTION promogest.TestataDocumentoInsUpd(varchar, bigint, bigint, integer, integer, varchar, varchar, date, timestamp, varchar, text, varchar, varchar, varchar, timestamp, timestamp, varchar, integer, varchar, varchar, bigint, bigint, bigint, bigint, bigint, bigint, bigint, bigint);
CREATE OR REPLACE FUNCTION promogest.TestataDocumentoInsUpd(varchar, bigint, bigint, integer, integer, varchar, varchar, date, timestamp, varchar, text, varchar, varchar, varchar, timestamp, timestamp, varchar, integer, varchar, varchar, bigint, bigint, bigint, bigint, bigint, bigint, bigint, bigint) RETURNS promogest.resultid AS '
    DECLARE
        -- Parametri contesto
        _schema                     ALIAS FOR $1;
        _idutente                   ALIAS FOR $2;
        
        -- Parametri tabella
        _id                         ALIAS FOR $3;
        _numero                     ALIAS FOR $4;
        _parte                      ALIAS FOR $5;
        _registro_numerazione       ALIAS FOR $6;
        _operazione                 ALIAS FOR $7;
        _data_documento             ALIAS FOR $8;
        _data_inserimento           ALIAS FOR $9;
        _protocollo                 ALIAS FOR $10;
        _note_interne               ALIAS FOR $11;
        _note_pie_pagina            ALIAS FOR $12;
        _causale_trasporto          ALIAS FOR $13;
        _aspetto_esteriore_beni     ALIAS FOR $14;
        _inizio_trasporto           ALIAS FOR $15;
        _fine_trasporto             ALIAS FOR $16;
        _incaricato_trasporto       ALIAS FOR $17;
        _totale_colli               ALIAS FOR $18;
        _totale_peso                ALIAS FOR $19;
        _applicazione_sconti        ALIAS FOR $20;
        _id_cliente                 ALIAS FOR $21;
        _id_fornitore               ALIAS FOR $22;
        _id_destinazione_merce      ALIAS FOR $23;
        _id_pagamento               ALIAS FOR $24;
        _id_banca                   ALIAS FOR $25;
        _id_aliquota_iva_esenzione  ALIAS FOR $26;
        _id_vettore                 ALIAS FOR $27;
	_id_agente                  ALIAS FOR $28;

        schema_prec                 varchar(2000);
        logid                       bigint;
        _resultid                   promogest.resultid;
        TempId                      bigint;
    BEGIN
        IF _id IS NULL THEN
            INSERT INTO testata_documento (numero,parte,registro_numerazione,operazione,data_documento,data_inserimento,protocollo,note_interne,note_pie_pagina,causale_trasporto,aspetto_esteriore_beni,inizio_trasporto,fine_trasporto,incaricato_trasporto,totale_colli,totale_peso,applicazione_sconti,id_cliente,id_fornitore,id_destinazione_merce,id_pagamento,id_banca,id_aliquota_iva_esenzione,id_vettore,id_agente) 
                VALUES (_numero,_parte,_registro_numerazione,_operazione,_data_documento,CURRENT_TIMESTAMP,_protocollo,_note_interne,_note_pie_pagina,_causale_trasporto,_aspetto_esteriore_beni,_inizio_trasporto,_fine_trasporto,_incaricato_trasporto,_totale_colli,_totale_peso,_applicazione_sconti,_id_cliente,_id_fornitore,_id_destinazione_merce,_id_pagamento,_id_banca,_id_aliquota_iva_esenzione,_id_vettore,_id_agente);
                
            TempId := CURRVAL(\'testata_documento_id_seq\');
            PERFORM promogest.LogSet(_idutente, _schema, \'I\',\'promogest.TestataDocumentoInsUpd\',\'Inserita testata documento\',NULL,TempId);
            SELECT INTO _resultid TempId;
        ELSE
            UPDATE testata_documento SET
                 numero = COALESCE(_numero,numero)
                ,parte = COALESCE(_parte,parte)
                ,registro_numerazione = COALESCE(_registro_numerazione,registro_numerazione)
                ,operazione = COALESCE(_operazione,operazione)
                ,data_documento = COALESCE(_data_documento,data_documento)
                ,protocollo = _protocollo
                ,note_interne = _note_interne
                ,note_pie_pagina = _note_pie_pagina
                ,causale_trasporto = _causale_trasporto
                ,aspetto_esteriore_beni = _aspetto_esteriore_beni
                ,inizio_trasporto = _inizio_trasporto
                ,fine_trasporto = _fine_trasporto
                ,incaricato_trasporto = _incaricato_trasporto
                ,totale_colli = _totale_colli
                ,totale_peso = _totale_peso
                ,applicazione_sconti = _applicazione_sconti
                ,id_cliente = _id_cliente
                ,id_fornitore = _id_fornitore
                ,id_destinazione_merce = _id_destinazione_merce
                ,id_pagamento = _id_pagamento
                ,id_banca = _id_banca
                ,id_aliquota_iva_esenzione = _id_aliquota_iva_esenzione
                ,id_vettore = _id_vettore
                ,id_agente = _id_agente 
            WHERE id = _id;

            IF FOUND THEN
                PERFORM promogest.LogSet(_idutente, _schema, \'I\',\'promogest.TestataDocumentoInsUpd\',\'Modificata testata documento\',NULL,_id);
                SELECT INTO _resultid _id;
            ELSE
                PERFORM promogest.LogSet(_idutente, _schema,  \'E\',\'promogest.TestataDocumentoInsUpd\',\'Testata documento non trovata\',NULL,_id);
                RAISE WARNING \'Testata documento non trovata: %\',_id;
                logid := CURRVAL(\'promogest.application_log_id_seq\');
                SELECT INTO _resultid -logid;
            END IF;
        END IF;
        RETURN _resultid;
    END;
' LANGUAGE plpgsql;
