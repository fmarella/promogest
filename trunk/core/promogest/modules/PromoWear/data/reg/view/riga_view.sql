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

Riga Movimento  - Vista

*/


DROP VIEW v_riga_movimento;

CREATE OR REPLACE VIEW v_riga_movimento AS
    SELECT 
         R.id
        ,R.valore_unitario_netto 
        ,R.valore_unitario_lordo
        ,R.quantita
        ,R.moltiplicatore
        ,R.applicazione_sconti
        ,R.percentuale_iva
        ,R.descrizione
        ,R.id_listino
        ,R.id_magazzino
        ,R.id_articolo
        ,R.id_multiplo
        ,RM.id_testata_movimento
    FROM riga R
    INNER JOIN riga_movimento RM ON RM.id = R.id;


DROP VIEW v_riga_movimento_completa;

CREATE OR REPLACE VIEW v_riga_movimento_completa AS
    SELECT 
         R.id
        ,R.valore_unitario_netto 
        ,R.valore_unitario_lordo
        ,R.quantita
        ,R.moltiplicatore
        ,R.applicazione_sconti
        ,R.percentuale_iva
        ,R.descrizione
        ,R.id_listino
        ,R.id_magazzino
        ,R.id_articolo
        ,R.id_multiplo
        ,RM.id_testata_movimento
        ,L.denominazione AS listino
        ,M.denominazione AS magazzino
        ,MU.denominazione_breve AS multiplo
        ,A.codice AS codice_articolo
        ,U.denominazione_breve AS unita_base
        ,ATC.id_articolo_padre
        ,ATC.id_gruppo_taglia
        ,ATC.id_taglia
        ,ATC.id_colore
        ,ATC.id_anno
        ,ATC.id_stagione
        ,ATC.id_genere
        ,GT.denominazione_breve AS denominazione_breve_gruppo_taglia
        ,GT.denominazione AS denominazione_gruppo_taglia
        ,T.denominazione_breve AS denominazione_breve_taglia
        ,T.denominazione AS denominazione_taglia
        ,C.denominazione_breve AS denominazione_breve_colore
        ,C.denominazione AS denominazione_colore
        ,AAB.denominazione AS anno
        ,SAB.denominazione AS stagione
        ,GAB.denominazione AS genere
    FROM riga R
    INNER JOIN riga_movimento RM ON RM.id = R.id
    LEFT OUTER JOIN listino L ON R.id_listino = L.id
    LEFT OUTER JOIN magazzino M ON R.id_magazzino = M.id
    LEFT OUTER JOIN multiplo MU ON R.id_multiplo = MU.id
    LEFT OUTER JOIN articolo A ON R.id_articolo = A.id
    LEFT OUTER JOIN promogest.unita_base U ON A.id_unita_base = U.id
    LEFT OUTER JOIN articolo_taglia_colore ATC ON A.id = ATC.id_articolo
    LEFT OUTER JOIN gruppo_taglia GT ON ATC.id_gruppo_taglia = GT.id
    LEFT OUTER JOIN taglia T ON ATC.id_taglia = T.id
    LEFT OUTER JOIN colore C ON ATC.id_colore = C.id
    LEFT OUTER JOIN promogest.anno_abbigliamento AAB ON ATC.id_anno = AAB.id
    LEFT OUTER JOIN promogest.stagione_abbigliamento SAB ON ATC.id_stagione = SAB.id
    LEFT OUTER JOIN promogest.genere_abbigliamento GAB ON ATC.id_genere = GAB.id;


/*

Riga Documento  - Vista

*/


DROP VIEW v_riga_documento;

CREATE OR REPLACE VIEW v_riga_documento AS
    SELECT 
         R.id
        ,R.valore_unitario_netto 
        ,R.valore_unitario_lordo
        ,R.quantita
        ,R.moltiplicatore
        ,R.applicazione_sconti
        ,R.percentuale_iva
        ,R.descrizione
        ,R.id_listino
        ,R.id_magazzino
        ,R.id_articolo
        ,R.id_multiplo
        ,RD.id_testata_documento
        ,'movimento' AS tipo_riga
    FROM riga R
    INNER JOIN riga_documento RD ON RD.id = R.id

    UNION

    SELECT 
         R.id
        ,R.valore_unitario_netto 
        ,R.valore_unitario_lordo
        ,R.quantita
        ,R.moltiplicatore
        ,R.applicazione_sconti
        ,R.percentuale_iva
        ,R.descrizione
        ,R.id_listino
        ,R.id_magazzino
        ,R.id_articolo
        ,R.id_multiplo
        ,TM.id_testata_documento
        ,'documento' AS tipo_riga
    FROM riga R
    INNER JOIN riga_movimento RM ON RM.id = R.id
    INNER JOIN testata_movimento TM ON RM.id_testata_movimento = TM.id
    WHERE TM.id_testata_documento IS NOT NULL;


DROP VIEW v_riga_documento_completa;

CREATE OR REPLACE VIEW v_riga_documento_completa AS
    SELECT 
         R.id
        ,R.valore_unitario_netto 
        ,R.valore_unitario_lordo
        ,R.quantita
        ,R.moltiplicatore
        ,R.applicazione_sconti
        ,R.percentuale_iva
        ,R.descrizione
        ,R.id_listino
        ,R.id_magazzino
        ,R.id_articolo
        ,R.id_multiplo
        ,RD.id_testata_documento
        ,L.denominazione AS listino
        ,M.denominazione AS magazzino
        ,MU.denominazione_breve AS multiplo
        ,A.codice AS codice_articolo
        ,U.denominazione_breve AS unita_base
        ,ATC.id_articolo_padre
        ,ATC.id_gruppo_taglia
        ,ATC.id_taglia
        ,ATC.id_colore
        ,ATC.id_anno
        ,ATC.id_stagione
        ,ATC.id_genere
        ,GT.denominazione_breve AS denominazione_breve_gruppo_taglia
        ,GT.denominazione AS denominazione_gruppo_taglia
        ,T.denominazione_breve AS denominazione_breve_taglia
        ,T.denominazione AS denominazione_taglia
        ,C.denominazione_breve AS denominazione_breve_colore
        ,C.denominazione AS denominazione_colore
        ,AAB.denominazione AS anno
        ,SAB.denominazione AS stagione
        ,GAB.denominazione AS genere
        ,'documento' AS tipo_riga
    FROM riga R
    INNER JOIN riga_documento RD ON RD.id = R.id
    LEFT OUTER JOIN listino L ON R.id_listino = L.id
    LEFT OUTER JOIN magazzino M ON R.id_magazzino = M.id
    LEFT OUTER JOIN multiplo MU ON R.id_multiplo = MU.id
    LEFT OUTER JOIN articolo A ON R.id_articolo = A.id
    LEFT OUTER JOIN promogest.unita_base U ON A.id_unita_base = U.id
    LEFT OUTER JOIN articolo_taglia_colore ATC ON A.id = ATC.id_articolo
    LEFT OUTER JOIN gruppo_taglia GT ON ATC.id_gruppo_taglia = GT.id
    LEFT OUTER JOIN taglia T ON ATC.id_taglia = T.id
    LEFT OUTER JOIN colore C ON ATC.id_colore = C.id
    LEFT OUTER JOIN promogest.anno_abbigliamento AAB ON ATC.id_anno = AAB.id
    LEFT OUTER JOIN promogest.stagione_abbigliamento SAB ON ATC.id_stagione = SAB.id
    LEFT OUTER JOIN promogest.genere_abbigliamento GAB ON ATC.id_genere = GAB.id

    UNION ALL

    SELECT 
         R.id
        ,R.valore_unitario_netto 
        ,R.valore_unitario_lordo
        ,R.quantita
        ,R.moltiplicatore
        ,R.applicazione_sconti
        ,R.percentuale_iva
        ,R.descrizione
        ,R.id_listino
        ,R.id_magazzino
        ,R.id_articolo
        ,R.id_multiplo
        ,TM.id_testata_documento
        ,L.denominazione AS listino
        ,M.denominazione AS magazzino
        ,MU.denominazione_breve AS multiplo
        ,A.codice AS codice_articolo
        ,U.denominazione_breve AS unita_base
        ,ATC.id_articolo_padre
        ,ATC.id_gruppo_taglia
        ,ATC.id_taglia
        ,ATC.id_colore
        ,ATC.id_anno
        ,ATC.id_stagione
        ,ATC.id_genere
        ,GT.denominazione_breve AS denominazione_breve_gruppo_taglia
        ,GT.denominazione AS denominazione_gruppo_taglia
        ,T.denominazione_breve AS denominazione_breve_taglia
        ,T.denominazione AS denominazione_taglia
        ,C.denominazione_breve AS denominazione_breve_colore
        ,C.denominazione AS denominazione_colore
        ,AAB.denominazione AS anno
        ,SAB.denominazione AS stagione
        ,GAB.denominazione AS genere
        ,'movimento' AS tipo_riga
    FROM riga R
    INNER JOIN riga_movimento RM ON RM.id = R.id
    INNER JOIN testata_movimento TM ON RM.id_testata_movimento = TM.id
    LEFT OUTER JOIN listino L ON R.id_listino = L.id
    LEFT OUTER JOIN magazzino M ON R.id_magazzino = M.id
    LEFT OUTER JOIN multiplo MU ON R.id_multiplo = MU.id
    LEFT OUTER JOIN articolo A ON R.id_articolo = A.id
    LEFT OUTER JOIN promogest.unita_base U ON A.id_unita_base = U.id
    LEFT OUTER JOIN articolo_taglia_colore ATC ON A.id = ATC.id_articolo
    LEFT OUTER JOIN gruppo_taglia GT ON ATC.id_gruppo_taglia = GT.id
    LEFT OUTER JOIN taglia T ON ATC.id_taglia = T.id
    LEFT OUTER JOIN colore C ON ATC.id_colore = C.id
    LEFT OUTER JOIN promogest.anno_abbigliamento AAB ON ATC.id_anno = AAB.id
    LEFT OUTER JOIN promogest.stagione_abbigliamento SAB ON ATC.id_stagione = SAB.id
    LEFT OUTER JOIN promogest.genere_abbigliamento GAB ON ATC.id_genere = GAB.id
    WHERE TM.id_testata_documento IS NOT NULL;
