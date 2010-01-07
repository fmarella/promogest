# -*- coding: utf-8 -*-



tablesMain = [
            #"azienda",
            ("operazione","denominazione"),
#            ("tipo_aliquota_iva","id"),
#            ("stato_articolo","id"),
#            ("unita_base","id"),
            #"role",
            #"language",
            ("tipo_recapito","denominazione"),
            #"user",
            #"app_log",
            #"action",
            #"roleaction"
]
tablesSchemeArticolo = [
            ("magazzino","id"),
            #("setting","key"),
            ("aliquota_iva","id"),
            ("categoria_articolo","id"),
            ("famiglia_articolo","id"),#########
            ("image","id"),
            ("imballaggio","id"),
            ("articolo","id"),
            ("multiplo","id"),
            ("pagamento","id"),
            ("persona_giuridica","id"),
            ("fornitore","id"),
#
            ("sconto" ,"id"),
            ("categoria_cliente","id"),
            ("codice_a_barre_articolo","id"),

            #("cart","id"),
            ("articolo_associato","id"),
            #("access","id"),
            ("listino","id"),
            ("listino_magazzino","id_listino"),
            ("listino_categoria_cliente","id_listino"),
#
            ("listino_articolo","id_listino"),
#            ("listino_articolo","data_listino_articolo"),
            #("feed","id"),
            ("fornitura","id"),
            ("sconto_fornitura","id"),
            #("inventario","id"),
            ("listino_complesso_listino","id_listino"),
            ("listino_complesso_articolo_prevalente","id_articolo"),
            ("sconti_vendita_dettaglio","id"),
            ("sconti_vendita_ingrosso","id"),
            #("spesa","id"),
            ("stoccaggio","id")
]
tablesSchemeAnagrafiche = [
            ("persona_giuridica","id"),
            ("banca","id"),
            ("cliente","id"),
            ("categoria_fornitore","id"),
            ("destinazione_merce","id"),
            ("vettore","id"),
            ("agente","id"),
            ("cliente_categoria_cliente","id_cliente"),
            ("contatto","id"),
            ("contatto_cliente","id"),
            ("recapito","id"),
            ("categoria_contatto","id"),
            ("contatto_categoria_contatto","id_contatto"),
            ("contatto_fornitore","id"),
            ("contatto_magazzino","id"),
            ("contatto_azienda","id"),
]
tablesSchemePromemoria = [
            ("promemoria","id"),

]
tablesSchemeDocumenti = [
            ("testata_documento","id"),
            ("testata_movimento","id"),
            ("riga","id"),
            ("riga_movimento","id"),
            ("sconto_riga_movimento","id"),
            #("inventario","id"),
            ("riga_documento","id"),
            ("sconto_riga_documento","id"),
            ("sconto_testata_documento","id"),
            ("testata_documento_scadenza","id"),
            ("informazioni_contabili_documento","id"),
]

tablesMainSchemePromoWear = [
            ("anno_abbigliamento","id"),
            ("genere_abbigliamento","id"),
            ("stagione_abbigliamento","id"),
            ]

tablesSchemePromoWear = [
            ("colore","id"),
            ("gruppo_taglia","id"),
            ("taglia","id"),
            ("gruppo_taglia_taglia","id"),
            ("modello","id"),
            ("articolo_taglia_colore","id")
            ]
