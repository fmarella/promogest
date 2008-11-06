#!/bin/bash

. ./conf.sh

# Non modificare da qua' in poi
SCRIPT_ROOT=../data

export PGPASSWORD=$DB_PASS

echo "ATTENZIONE !!! Ricordarsi di applicare l'aggiornamento a TUTTE le aziende !"

if [[ $1 = "" ]] 
then
	echo "Uso: ./update_pagamenti.sh [nome_schema]"
	exit
fi

# Lettura revisione db

echo -en "SELECT CASE WHEN s.value IS NULL THEN '' ELSE s.value END FROM $1.setting s WHERE s.key = 'update_db_version';" > $TMP/promo_tmp_query
$CAT $TMP/promo_tmp_query | $PSQL -d $DB_NAME -U $DB_USER -h $DB_HOST -t -A > $TMP/response
read version < $TMP/response
echo -en "------------------------------\n" >> update.log
date >> update.log
echo -en "Actual version= $version\n" >> update.log

# Inizio aggiornamento

# Rimozione viste collegate ai documenti

echo -en "SET SEARCH_PATH TO $1;\n\n" > $TMP/promo_tmp_update_pagamenti
echo -en "DROP VIEW v_informazioni_fatturazione_documento;\n" >> $TMP/promo_tmp_update_pagamenti



if [[ $version < "9.5" ]]; then
        echo -en "\nALTER TABLE testata_documento DROP COLUMN documento_saldato, 
        DROP COLUMN id_primo_riferimento,
        DROP COLUMN id_secondo_riferimento,
        DROP COLUMN totale_pagato,
        DROP COLUMN totale_sospeso;" >> $TMP/promo_tmp_update_pagamenti
        $CAT $TMP/promo_tmp_update_pagamenti | $PSQL -d $DB_NAME -U $DB_USER -h $DB_HOST
        echo "Revisione db n. 9.4 completata" >> update.log
fi


    echo -en "\nModifiche alla struttura del database effettuate. Controllare eventuali errori. Premere Enter quando pronti."
    read $enter_daje_schiaccia

# Aggiornamento viste
echo -en "SET SEARCH_PATH TO $1;\n\n" > $TMP/promo_tmp_create_views
$CAT $SCRIPT_ROOT/view/*.sql >> $TMP/promo_tmp_create_views
$CAT $TMP/promo_tmp_create_views | $PSQL -d $DB_NAME -U $DB_USER -h $DB_HOST >> update.log

echo -en "Views installate. Premere enter quando pronti"
read $enter_daje_schiaccia

# Aggiornamento stored procedure di basso livello 
$CAT $SCRIPT_ROOT/sp/*.sql | $PSQL -d $DB_NAME -U $DB_USER -h $DB_HOST >> update.log

echo -en "Stored Procedure aggiornate. Premere enter quando pronti"
read $enter_daje_schiaccia

# Aggiornamento stored procedure applicative 
$CAT $SCRIPT_ROOT/app/*.sql | $PSQL -d $DB_NAME -U $DB_USER -h $DB_HOST >> update.log
