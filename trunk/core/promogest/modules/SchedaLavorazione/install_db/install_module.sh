#!/bin/bash

install_module () {
    local _root_path = $1
    local _schema_db = $2
    local nome_modulo = $3
    
    if [ $1 = ""] || [ $2 = ""] || [ $3 = ""]
    then
        echo "function install_module \nusage: install_module rootpath schema_db module_name"
        exit
    fi
    
    $CAT $_root_path/data/*.sql | $PSQL -d $DB_NAME -U $DB_USER -h $DB_HOST >> update.log
    cp -f $_root_path/ui/* /opt/promogest/python/promogest/ui     
    cp -f $_root_path/gui/* /opt/promogest/python/gui
    cp -f $_root_path/lib/* /opt/promogest/python/promogest/lib
    cp -f $_root_path/dao/* /opt/promogest/python/promogest/dao
    cp -f $_root_path/report-templates/* /opt/promogest/python/report-templates
    cp -f $_root_path/templates/* /opt/promogest/python/templates
    cp -f $_root_path/kid/* /opt/promogest/python/kid
    cp -f $_root_path/elementtree/* /opt/promogest/python/elementtree
    cp -f $_root_path/report-templates/* /opt/promogest/python/report-templates
    cp -f $_root_path/data/* /opt/promogest/python/install_db/$nome_modulo
}
