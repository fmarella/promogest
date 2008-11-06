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

riga_documento  - Stored procedure di inserimento/aggiornamento

*/

DROP FUNCTION promogest.RigaDocumentoInsUpd(varchar, bigint, bigint, decimal(16,4), decimal(16,4), decimal(16,4), decimal(15,6), varchar, decimal(8,4), varchar, bigint, bigint, bigint, bigint, bigint, text);
CREATE OR REPLACE FUNCTION promogest.RigaDocumentoInsUpd(varchar, bigint, bigint, decimal(16,4), decimal(16,4), decimal(16,4), decimal(15,6), varchar, decimal(8,4), varchar, bigint, bigint, bigint, bigint, bigint, text) RETURNS promogest.resultid AS '

    DECLARE
        -- Parametri contesto
        _schema                     ALIAS FOR $1;
        _idutente                   ALIAS FOR $2;
        
        -- Parametri tabella
        _id                         ALIAS FOR $3;
        _valore_unitario_netto      ALIAS FOR $4;
        _valore_unitario_lordo      ALIAS FOR $5;
        _quantita                   ALIAS FOR $6;
        _moltiplicatore             ALIAS FOR $7;
        _applicazione_sconti        ALIAS FOR $8;
        _percentuale_iva            ALIAS FOR $9;
        _descrizione                ALIAS FOR $10;
        -- Chiavi esterne
        _id_listino                 ALIAS FOR $11;
        _id_magazzino               ALIAS FOR $12;
        _id_articolo                ALIAS FOR $13;
        _id_multiplo                ALIAS FOR $14;
        _id_testata_documento       ALIAS FOR $15;
        _dummy                      ALIAS FOR $16;

        schema_prec                 varchar(2000);
        logid                       bigint;
        _resultid                   promogest.resultid;
        TempId                      bigint;
    BEGIN
        IF _id IS NULL THEN
            INSERT INTO riga (valore_unitario_netto, valore_unitario_lordo, quantita, moltiplicatore, applicazione_sconti, percentuale_iva, descrizione, id_listino, id_magazzino, id_articolo, id_multiplo) 
                VALUES (_valore_unitario_netto, _valore_unitario_lordo, _quantita, _moltiplicatore, _applicazione_sconti, _percentuale_iva, _descrizione, _id_listino, _id_magazzino, _id_articolo, _id_multiplo);
                
            TempId := CURRVAL(\'riga_documento_id_seq\');

            INSERT INTO riga_documento (id, id_testata_documento) 
                VALUES (TempId, _id_testata_documento);
            
            PERFORM promogest.LogSet(_idutente, _schema, \'I\',\'promogest.RigaDocumentoInsUpd\',\'Inserita riga documento\',NULL,TempId);
            SELECT INTO _resultid TempId;
        ELSE
            UPDATE riga SET
                 valore_unitario_netto = _valore_unitario_netto
                ,valore_unitario_lordo = _valore_unitario_lordo
                ,quantita = COALESCE(_quantita,quantita)
                ,moltiplicatore = COALESCE(_moltiplicatore,moltiplicatore)
                ,applicazione_sconti = COALESCE(_applicazione_sconti,applicazione_sconti) 
                ,percentuale_iva = COALESCE(_percentuale_iva,percentuale_iva)
                ,descrizione = _descrizione
                ,id_listino = _id_listino
                ,id_magazzino = COALESCE(_id_magazzino,id_magazzino)
                ,id_articolo = COALESCE(_id_articolo,id_articolo)
                ,id_multiplo = _id_multiplo
            WHERE id = _id;

            UPDATE riga_documento SET
                id_testata_documento = COALESCE(_id_testata_documento,id_testata_documento)
            WHERE id = _id;

            IF FOUND THEN
                PERFORM promogest.LogSet(_idutente, _schema, \'I\',\'promogest.RigaDocumentoInsUpd\',\'Modificata riga documento\',NULL,_id);
                SELECT INTO _resultid _id;
            ELSE
                PERFORM promogest.LogSet(_idutente, _schema,  \'E\',\'promogest.RigaDocumentoInsUpd\',\'Riga documento non trovata\',NULL,_id);
                RAISE WARNING \'Riga documento non trovata: %\',_id;
                logid := CURRVAL(\'promogest.application_log_id_seq\');
                SELECT INTO _resultid -logid;
            END IF;
        END IF; 
        RETURN _resultid;
    END;
' LANGUAGE plpgsql;
