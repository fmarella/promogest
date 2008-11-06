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
-- MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.|  See the
-- GNU General Public License for more details.
--
-- You should have received a copy of the GNU General Public License
-- along with this program; if not, write to the Free Software
-- Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA|  02111-1307, USA.

/*

Prima Nota - Stored Procedure applicativa

*/

DROP FUNCTION promogest.TotaleClienteDareGet(varchar, bigint, bigint);
DROP FUNCTION promogest.TotaleAnnualeClienteDareGet(varchar, bigint, bigint);
DROP TYPE promogest.totale_cliente_dare_sel_type;

CREATE TYPE promogest.totale_cliente_dare_sel_type AS (
        totale_dare_fatt_vend          decimal(16,4)
        ,totale_dare_fatt_diff_vend    decimal(16,4)
        ,totale_dare_fatt_acc          decimal(16,4)
        ,totale_dare_vendita_dett      decimal(16,4)
        ,totale_dare_note_cred         decimal(16,4)
);

CREATE OR REPLACE FUNCTION promogest.TotaleClienteDareGet(varchar, bigint, bigint) RETURNS  SETOF promogest.totale_cliente_dare_sel_type AS E'
    DECLARE
        -- Parametri contesto
        _schema                 ALIAS FOR $1;
        _id_utente              ALIAS FOR $2;
        _id_cliente             ALIAS FOR $3;

         schema_prec            varchar(2000);
         sql_command            varchar(2000);
         _tot_fatt_vend         float;
         _tot_fatt_diff_vend    float;
         _tot_fatt_acc          float;
         _tot_vendita_dett      float;
         _tot_note_cred         float;
         _rec                   record;
    BEGIN
        -- Memorizza schema precedente
        schema_prec:= ARRAY_TO_STRING(CURRENT_SCHEMAS(\'t\'),\',\');

        -- Imposta schema corrente
        sql_command:= \'SET SEARCH_PATH TO \' || _schema;
        EXECUTE sql_command;

        SELECT INTO _rec FV.totale_dare_fatt_vend AS tot_fatt_vend, FD.totale_dare_fatt_diff_vend AS tot_fatt_diff_vend, FA.totale_dare_fatt_acc AS tot_fatt_acc, VD.totale_dare_vendita_dett AS tot_vend_dett, NC.totale_dare_note_cred AS tot_note_cred
        FROM 
            (SELECT SUM(TD.totale_sospeso) AS totale_dare_fatt_vend FROM 
                v_informazioni_contabili_documento_completa TD 
                WHERE TD.id_cliente = _id_cliente 
                AND TD.operazione = \'Fattura vendita\') AS FV,
            (SELECT SUM(TD.totale_sospeso) AS totale_dare_fatt_diff_vend FROM 
                v_informazioni_contabili_documento_completa TD 
                WHERE TD.id_cliente = _id_cliente 
                AND TD.operazione = \'Fattura differita vendita\') AS FD, 
            (SELECT SUM(TD.totale_sospeso) AS totale_dare_fatt_acc FROM 
                v_informazioni_contabili_documento_completa TD 
                WHERE TD.id_cliente = _id_cliente 
                AND TD.operazione = \'Fattura accompagnatoria\') AS FA, 
            (SELECT SUM(TD.totale_sospeso) AS totale_dare_vendita_dett FROM 
                v_informazioni_contabili_documento_completa TD 
                WHERE TD.id_cliente = _id_cliente 
                AND TD.operazione = \'Vendita dettaglio\') AS VD,
            (SELECT SUM(TD.totale_pagato) AS totale_dare_note_cred FROM 
                v_informazioni_contabili_documento_completa TD 
                WHERE TD.id_cliente = _id_cliente 
                AND TD.operazione = \'Nota di credito a cliente\') AS NC;

        -- Imposta schema precedente
        sql_command:= \'SET SEARCH_PATH TO \' || schema_prec;
        EXECUTE sql_command;

        RETURN NEXT _rec;
    END;
' LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION promogest.TotaleAnnualeClienteDareGet(varchar, bigint, bigint) RETURNS  SETOF promogest.totale_cliente_dare_sel_type AS E'
    DECLARE
        -- Parametri contesto
        _schema                 ALIAS FOR $1;
        _id_utente              ALIAS FOR $2;
        _id_cliente             ALIAS FOR $3;

         schema_prec            varchar(2000);
         sql_command            varchar(2000);
         _tot_fatt_vend         float;
         _tot_fatt_diff_vend    float;
         _tot_fatt_acc          float;
         _tot_vendita_dett      float;
         _tot_note_cred         float;
         _rec                   record;
    BEGIN
        -- Memorizza schema precedente
        schema_prec:= ARRAY_TO_STRING(CURRENT_SCHEMAS(\'t\'),\',\');

        -- Imposta schema corrente
        sql_command:= \'SET SEARCH_PATH TO \' || _schema;
        EXECUTE sql_command;

        SELECT INTO _rec FV.totale_dare_fatt_vend AS tot_fatt_vend, FD.totale_dare_fatt_diff_vend AS tot_fatt_diff_vend, FA.totale_dare_fatt_acc AS tot_fatt_acc, VD.totale_dare_vendita_dett AS tot_vend_dett, NC.totale_dare_note_cred AS tot_note_cred
        FROM 
            (SELECT SUM(TD.totale_pagato + TD.totale_sospeso) 
                AS totale_dare_fatt_vend FROM 
                v_informazioni_contabili_documento_completa TD 
                WHERE TD.id_cliente = _id_cliente 
                AND TD.operazione = \'Fattura vendita\') AS FV,
            (SELECT SUM(TD.totale_pagato + TD.totale_sospeso)
                AS totale_dare_fatt_diff_vend FROM 
                v_informazioni_contabili_documento_completa TD 
                WHERE TD.id_cliente = _id_cliente 
                AND TD.operazione = \'Fattura differita vendita\') AS FD, 
            (SELECT SUM(TD.totale_pagato + TD.totale_sospeso)
                AS totale_dare_fatt_acc FROM 
                v_informazioni_contabili_documento_completa TD 
                WHERE TD.id_cliente = _id_cliente 
                AND TD.operazione = \'Fattura accompagnatoria\') AS FA, 
            (SELECT SUM(TD.totale_pagato + TD.totale_sospeso)
                AS totale_dare_vendita_dett FROM 
                v_informazioni_contabili_documento_completa TD 
                WHERE TD.id_cliente = _id_cliente 
                AND TD.operazione = \'Vendita dettaglio\') AS VD,
            (SELECT SUM(TD.totale_pagato + TD.totale_sospeso)
                AS totale_dare_note_cred FROM 
                v_informazioni_contabili_documento_completa TD 
                WHERE TD.id_cliente = _id_cliente 
                AND TD.operazione = \'Nota di credito a cliente\') AS NC;

        -- Imposta schema precedente
        sql_command:= \'SET SEARCH_PATH TO \' || schema_prec;
        EXECUTE sql_command;

        RETURN NEXT _rec;
    END;
' LANGUAGE plpgsql;

DROP FUNCTION promogest.TotaleFornitoreAvereGet(varchar, bigint, bigint);
DROP FUNCTION promogest.TotaleAnnualeFornitoreAvereGet(varchar, bigint, bigint);
DROP TYPE promogest.totale_fornitore_avere_sel_type;

CREATE TYPE promogest.totale_fornitore_avere_sel_type AS (
        totale_dare_fatt_acq          decimal(16,4)
        ,totale_dare_fatt_diff_acq    decimal(16,4)
        ,totale_dare_note_cred        decimal(16,4)
);

CREATE OR REPLACE FUNCTION promogest.TotaleFornitoreAvereGet(varchar, bigint, bigint) RETURNS SETOF promogest.totale_fornitore_avere_sel_type AS E'
    DECLARE
        -- Parametri contesto
        _schema                 ALIAS FOR $1;
        _id_utente              ALIAS FOR $2;
        _id_fornitore           ALIAS FOR $3;

        schema_prec            varchar(2000);
        sql_command            varchar(2000);
        _tot_fatt_acq          float;
        _tot_fatt_diff_acq     float;
        _tot_note_cred         float;
        _rec                   record;
    BEGIN
        -- Memorizza schema precedente
        schema_prec:= ARRAY_TO_STRING(CURRENT_SCHEMAS(\'t\'),\',\');

        -- Imposta schema corrente
        sql_command:= \'SET SEARCH_PATH TO \' || _schema;
        EXECUTE sql_command;

        SELECT INTO _rec FV.totale_avere_fatt_acq AS tot_fatt_acq, FD.totale_avere_fatt_diff_acq AS tot_fatt_diff_acq, NC.totale_avere_note_cred AS tot_note_cred 
        FROM 
            (SELECT SUM(TD.totale_sospeso) AS totale_avere_fatt_acq FROM 
                v_informazioni_contabili_documento_completa TD 
                WHERE TD.id_fornitore = _id_fornitore 
                AND TD.operazione = \'Fattura acquisto\') AS FV,
            (SELECT SUM(TD.totale_sospeso) AS totale_avere_fatt_diff_acq FROM 
                v_informazioni_contabili_documento_completa TD 
                WHERE TD.id_fornitore = _id_fornitore 
                AND TD.operazione = \'Fattura differita acquisto\') AS FD, 
            (SELECT SUM(TD.totale_pagato) AS totale_avere_note_cred FROM 
                v_informazioni_contabili_documento_completa TD 
                WHERE TD.id_fornitore = _id_fornitore 
                AND TD.operazione = \'Nota di credito da fornitore\') AS NC;
       
        -- Imposta schema precedente
        sql_command:= \'SET SEARCH_PATH TO \' || schema_prec;
        EXECUTE sql_command;

        RETURN NEXT _rec;
    END;
' LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION promogest.TotaleAnnualeFornitoreAvereGet(varchar, bigint, bigint) RETURNS SETOF promogest.totale_fornitore_avere_sel_type AS E'
    DECLARE
        -- Parametri contesto
        _schema                 ALIAS FOR $1;
        _id_utente              ALIAS FOR $2;
        _id_fornitore           ALIAS FOR $3;

        schema_prec            varchar(2000);
        sql_command            varchar(2000);
        _tot_fatt_acq          float;
        _tot_fatt_diff_acq     float;
        _tot_note_cred         float;
        _rec                   record;
    BEGIN
        -- Memorizza schema precedente
        schema_prec:= ARRAY_TO_STRING(CURRENT_SCHEMAS(\'t\'),\',\');

        -- Imposta schema corrente
        sql_command:= \'SET SEARCH_PATH TO \' || _schema;
        EXECUTE sql_command;

        SELECT INTO _rec FV.totale_avere_fatt_acq AS tot_fatt_acq, FD.totale_avere_fatt_diff_acq AS tot_fatt_diff_acq, NC.totale_avere_note_cred AS tot_note_cred 
        FROM 
            (SELECT SUM(TD.totale_pagato + TD.totale_sospeso)
                AS totale_avere_fatt_acq FROM 
                v_informazioni_contabili_documento_completa TD 
                WHERE TD.id_fornitore = _id_fornitore 
                AND TD.operazione = \'Fattura acquisto\') AS FV,
            (SELECT SUM(TD.totale_pagato + TD.totale_sospeso)
                AS totale_avere_fatt_diff_acq FROM 
                v_informazioni_contabili_documento_completa TD 
                WHERE TD.id_fornitore = _id_fornitore 
                AND TD.operazione = \'Fattura differita acquisto\') AS FD, 
            (SELECT SUM(TD.totale_pagato + TD.totale_sospeso)
                AS totale_avere_note_cred FROM 
                v_informazioni_contabili_documento_completa TD 
                WHERE TD.id_fornitore = _id_fornitore 
                AND TD.operazione = \'Nota di credito da fornitore\') AS NC;
       
        -- Imposta schema precedente
        sql_command:= \'SET SEARCH_PATH TO \' || schema_prec;
        EXECUTE sql_command;

        RETURN NEXT _rec;
    END;
' LANGUAGE plpgsql;


