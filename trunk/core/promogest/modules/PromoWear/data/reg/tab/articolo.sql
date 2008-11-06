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

articolo - Tabella articoli

*/


DROP TABLE articolo CASCADE;

DROP SEQUENCE articolo_id_seq;
CREATE SEQUENCE articolo_id_seq;
    
CREATE TABLE articolo (
     id                             bigint              DEFAULT NEXTVAL('articolo_id_seq') PRIMARY KEY NOT NULL
    ,codice                         varchar(50)         NOT NULL
    ,denominazione                  varchar(300)        NOT NULL
    ,id_aliquota_iva                bigint              NOT NULL REFERENCES aliquota_iva ( id ) ON UPDATE CASCADE ON DELETE RESTRICT
    ,id_famiglia_articolo           bigint              NOT NULL REFERENCES famiglia_articolo ( id ) ON UPDATE CASCADE ON DELETE RESTRICT
    ,id_categoria_articolo          bigint              NOT NULL REFERENCES categoria_articolo ( id ) ON UPDATE CASCADE ON DELETE RESTRICT
    ,id_unita_base                  bigint              NOT NULL REFERENCES promogest.unita_base ON UPDATE CASCADE ON DELETE RESTRICT
    ,produttore                     varchar(150)        NULL
    ,unita_dimensioni               varchar(10)         NULL
    ,lunghezza                      real                NULL
    ,larghezza                      real                NULL
    ,altezza                        real                NULL
    ,unita_volume                   varchar(10)         NULL
    ,volume                         real                NULL
    ,unita_peso                     varchar(10)         NULL
    ,peso_lordo                     real                NULL
    ,id_imballaggio                 bigint              NULL REFERENCES imballaggio ( id ) ON UPDATE CASCADE ON DELETE RESTRICT
    ,peso_imballaggio               numeric             NULL
    ,stampa_etichetta               boolean             NULL
    ,codice_etichetta               varchar(50)         NULL
    ,descrizione_etichetta          varchar(200)        NULL
    ,stampa_listino                 boolean             NULL
    ,descrizione_listino            varchar(200)        NULL
    ,aggiornamento_listino_auto     boolean             NULL
    ,timestamp_variazione           timestamp           NULL
    ,note                           text
    ,cancellato                     boolean             NOT NULL DEFAULT false
    ,sospeso                        boolean             NOT NULL DEFAULT false
    ,id_stato_articolo              bigint              NULL REFERENCES promogest.stato_articolo ( id ) ON UPDATE CASCADE ON DELETE RESTRICT

    ,UNIQUE ( codice )
);
