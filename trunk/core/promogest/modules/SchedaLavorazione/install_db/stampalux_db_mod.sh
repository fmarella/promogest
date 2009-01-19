#!/bin/bash

# Questo script va lanciato dalla directory "install_db" dei file della personalizzazione
# PRIMA di lanciare lo script "stampalux.sh" per la copia dei files nella directory di 
# installazione del promogest (/opt/promogest). diversamente è necessario modificare il 
# percorso root dei files sql interessati
# Temporary directory
TMP=/tmp
CAT=/bin/cat
# Postgres createlang command
CREATELANG=/usr/bin/createlang
# Postgres client sql
PSQL=/usr/bin/psql
# Default database user
DB_USER=promoadmin
# Default user password
DB_PASS=admin
# user "postgres" password
ADMIN_PASSWORD=
# Database server address
DB_HOST=localhost
# Database name
DB_NAME=promostampalux_db

# Non modificare da qua' in poi
SCRIPT_ROOT=../data

# Inserire qui la revisione del db
# minima necessaria per eseguire lo script
last_version="9"

export PGPASSWORD=$DB_PASS

echo "ATTENZIONE !!! Questo script contiene esclusivamente le modifiche da apportare alle" 
echo "tabelle esistenti nel database!"
echo "Eseguire solo dopo aver aggiornato il database alla versione "$last_version
echo "Continuare [s/n]?"
read confirm
if [[ $confirm != s ]];
then
    echo "Aborted"
    exit
else

if [[ $1 = "" ]] 
then
	echo "Uso: ./stampalux_db_mod.sh [nome_schema]"
	exit
fi

# Lettura revisione db
echo $TMP

echo -en "SELECT CASE WHEN s.value IS NULL THEN '' ELSE s.value END FROM $1.setting s WHERE s.key = 'update_db_version';" > $TMP/promo_tmp_query

$CAT $TMP/promo_tmp_query | $PSQL -d $DB_NAME -U $DB_USER -h $DB_HOST -t -A > $TMP/response1
read version < $TMP/response1
echo -en "------------------------------\n" >> stampalux_inst.log
date >> stampalux_inst.log
echo -en "Actual version= $version\n" >> stampalux_inst.log

if [[ $version != $last_version ]]
then
    echo "il database non è alla versione cui ci si aspettava"
    echo "expected: "$last_version
    echo "found: "$version
    exit
fi

# Inizio aggiornamento
echo -en "SET SEARCH_PATH TO $1;\n\n" > $TMP/promo_tmp_update_db

# Rimozione viste
#in questo modulo, nessuna vista da rimuovere

#modifica delle tabelle interessate
echo -en "\nDELETE FROM setting WHERE key = 'Scheda Ordinazione.registro';">> $TMP/promo_tmp_update_db
echo -en "\nDELETE FROM setting WHERE key = 'registro_scheda_ordinazione.rotazione';">> $TMP/promo_tmp_update_db
echo -en "\nINSERT INTO setting (key, description, value) VALUES ('Scheda Ordinazione.registro', 'Registro associato alle schede lavorazione del modulo Stampalux', 'registro_scheda_ordinazione'), ('registro_scheda_ordinazione.rotazione','Tipologia di rotazione per le schede lavorazione', 'annuale');">> $TMP/promo_tmp_update_db

$CAT $TMP/promo_tmp_update_db | $PSQL -d $DB_NAME -U $DB_USER -h $DB_HOST
echo "modifica db $last_version per modulo Stampalux completata" >> stampalux_inst.log


    echo -en "\nModifiche alla struttura del database effettuate. Controllare eventuali errori. Premere Enter quando pronti."
    read $enter_daje_schiaccia

# Inserimento tabelle
echo "Creazione nuove tabelle per modulo Stampalux"
echo "Creazione nuove tabelle per modulo Stampalux" >> stampalux_inst.log
echo -en "SET SEARCH_PATH TO $1;" > $TMP/promo_tmp_create_views
$CAT $SCRIPT_ROOT/tab/*.sql >> $TMP/promo_tmp_create_views
$CAT $TMP/promo_tmp_create_views | $PSQL -d $DB_NAME -U $DB_USER -h $DB_HOST >> stampalux_inst.log

echo "Inserimento viste, stored procedure di basso livello e applicative per modulo Stampalux"
echo "Inserimento viste tabelle Stampalux" >> stampalux_inst.log
# Aggiornamento viste
echo -en "SET SEARCH_PATH TO $1;" > $TMP/promo_tmp_create_views
$CAT $SCRIPT_ROOT/views/*.sql >> $TMP/promo_tmp_create_views
$CAT $TMP/promo_tmp_create_views | $PSQL -d $DB_NAME -U $DB_USER -h $DB_HOST >> stampalux_inst.log
echo -en "controllare gli errori e se tutto ok, premere invio"
read $dajeschiaccia


echo "Inserimento Stored Procedure di basso livello tabelle Stampalux" >> stampalux_inst.log
# Aggiornamento stored procedure di basso livello 
$CAT $SCRIPT_ROOT/sp/*.sql | $PSQL -d $DB_NAME -U $DB_USER -h $DB_HOST >> stampalux_inst.log
echo -en "controllare gli errori e se tutto ok, premere invio"
read $dajeschiaccia

echo "Inserimento Stored Procedure applicative tabelle Stampalux" >> stampalux_inst.log
# Aggiornamento stored procedure applicative 
$CAT $SCRIPT_ROOT/app/*.sql | $PSQL -d $DB_NAME -U $DB_USER -h $DB_HOST >> stampalux_inst.log

fi
echo "aggiornamento completato. Enjoy :D"
