#!/bin/bash

. ./conf.sh

# Non modificare da qua' in poi
SCRIPT_ROOT=../data

export PGPASSWORD=$DB_PASS

if [[ $1 = "" ]] 
then
	echo "Uso: ./install_pagamenti [nome_schema]"
	exit
fi

# Creazione tabelle
echo -en "SET search_path TO $1;\n\n" > $TMP/promo_tmp_create_table
$CAT $SCRIPT_ROOT/tab/*.sql >> $TMP/promo_tmp_create_table
$CAT $TMP/promo_tmp_create_table | $PSQL -d $DB_NAME -U $DB_USER -h $DB_HOST 

# Creazione view
echo -en "SET search_path TO $1;\n\n" > $TMP/promo_tmp_create_view
$CAT $SCRIPT_ROOT/view/*.sql >> $TMP/promo_tmp_create_view
$CAT $TMP/promo_tmp_create_view | $PSQL -d $DB_NAME -U $DB_USER -h $DB_HOST 

# Creazione stored procedure
echo -en "SET search_path TO $1;\n\n" > $TMP/promo_tmp_create_app
$CAT $SCRIPT_ROOT/sp/*.sql >> $TMP/promo_tmp_create_app
$CAT $SCRIPT_ROOT/app/*.sql >> $TMP/promo_tmp_create_app
$CAT $TMP/promo_tmp_create_app | $PSQL -d $DB_NAME -U $DB_USER -h $DB_HOST

echo "done"
