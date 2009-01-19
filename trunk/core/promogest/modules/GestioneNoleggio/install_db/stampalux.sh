#!/bin/bash
#
# Attenzione per installare questa personalizzazione 
# è necessario impostare il conf.sh con i seguenti parametri:
#
#
#

# Inserire qui la descrizione del modulo che si sta installando
module_name="Personalizzazione Stampalux by Dr astico"

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
INSTALL_PATH=/opt/promogest

# questa è la funzione che verrà chiamata per eseguire l'installazione
# del modulo (si occupa di copiare tutti i files necessari all'installazione,
# anche i ".py", templates ecc.) le sotto directory devono avere
# lo stesso nome della dir di destinazione dei files che contengono.
install_module () {
    
    echo $1
    echo $2
    echo $3
    
    if [[ $1 = "" ]] || [[ $2 = "" ]] || [[ $3 = "" ]]
    then
        echo "function install_module"
        echo "usage: install_module <rootpath> <schema_db> <module_name>"
        exit
    fi
    # root_path è la directory principale che contiene i files del modulo
    local _root_path=$1
    # lo schema dell'azienda da modificare
    local _schema_db=$2
    # il nome del modulo che si sta installando (una singola parola)
    local nome_modulo=$3
    #ìl path su cui eseguire l'installazione
    local _install_path=$4
#
    chmod -R a+r $_root_path
    cp -f  $_root_path/ui/* $_install_path/python/promogest/ui
    cp -f  $_root_path/gui/* $_install_path/python/gui
    cp -f  $_root_path/lib/* $_install_path/python/promogest/lib
    cp -f  $_root_path/dao/* $_install_path/python/promogest/dao
    cp -f  $_root_path/elementtree/* _install_path/python/elementtree
    mkdir  $_install_path/install_db/$nome_modulo
    cp -r  $_root_path/data $_install_path/install_db/$nome_modulo/
}

# Non modificare da qua' in poi
SCRIPT_ROOT=../data

export PGPASSWORD=$DB_PASS

if [[ $1 = "" ]] || [[ $2 = "" ]]
then
	echo "Uso: ./stampalux.sh <nome_azienda> <path_modulo> [overwrite]"
	exit
fi

echo -en "SELECT CASE WHEN s.value IS NULL THEN '' ELSE s.value END FROM $1.SETTING s WHERE s.key = 'modulo_stampalux';" > $TMP/promo_tmp_query
$CAT $TMP/promo_tmp_query | $PSQL -d $DB_NAME -U $DB_USER -h $DB_HOST -t -A > $TMP/response
read status < $TMP/response

echo $status

if [[ $status = "" ]]
then
    echo -en "INSERT INTO $1.setting (key, description, value) VALUES ('modulo_stampalux', '$module_name', 'non installato');" > $TMP/promo_tmp_query
    $CAT $TMP/promo_tmp_query | $PSQL -d $DB_NAME -U $DB_USER -h $DB_HOST -t -A
    echo "First time running this script. Preparing installation of the module named 'Stampalux'..."
    echo -en "-------------------------------------------------" >> update.log
    echo -en "first installation module 'stampalux'" >> update.log
    #installazione della modifica
    install_module $2 $1 Stampalux $INSTALL_PATH
elif [[ $status = "installato" ]] && [[ $3 = "" ]]
then
    echo "il modulo è già stato installato."
    echo "per forzare la re-installazione, effettuare un backup dei dati presenti nelle tabelle"
    echo "e rilanciare il comando con l'opzione 'overwrite'."
    exit
elif [[ $status = 'installato' ]] && [[ $3 = "overwrite" ]]
then
    echo "ATTENZIONE! Confermare la sovrascrittura dei files della modifica."
    echo "L'operazione non comprende alcuna operazione sul database." 
    echo "Continuare? [s/n]"
    read choice
    while [ $choice != "S" ] || [ $choice != "s" ]; do
        case $choice in
            s|S)            echo "Re-installazione del modulo 'Stampalux' in corso"
                            echo "attendere."
                            install_module $2 $1 Stampalux $INSTALL_PATH
                            echo "Re-installazione terminata."
                            echo "Fitter, Happier and More productive."
                            echo "A pig, in a cage, on antibiotics"
                            echo ":-D"
                            break ;;
            n|N)            exit ;;
            *)              echo "Premere S o N e poi Invio"
                            read choice ;;
        esac
    done
fi
echo -en "UPDATE $1.setting SET value = 'installato' WHERE key = 'modulo_stampalux';" > $TMP/promo_tmp_query
    $CAT $TMP/promo_tmp_query | $PSQL -d $DB_NAME -U $DB_USER -h $DB_HOST -t -A

# Questi vanno decommentati solo se l'installazione è sicura :D
#echo "[Stampalux]" >> ~/promogest/configure
#echo "mod_enable = yes" >> ~/promogest/configure
#echo "target1 = data_consegna_bozza" >> ~/promogest/configure
#echo "target2 = data_spedizione" >> ~/promogest/configure
#echo "target3 = data_ordine_al_fornitore" >> ~/promogest/configure
#echo "soglia_consegna_bozza = 2" >> ~/promogest/configure
#echo "soglia_ordine_fornitore = 2" >> ~/promogest/configure
#echo "soglia_spedizione = 2" >> ~/promogest/configure
#
# questa è la sezione di configurazione pronta per l'uso.
#
#[Stampalux]
#mod_enable = yes
#target1 = data_consegna_bozza
#target2 = data_spedizione
#target3 = data_ordine_al_fornitore
#soglia_consegna_bozza = 2
#soglia_ordine_fornitore = 2
#soglia_spedizione = 2
echo "Installazione eseguita."

