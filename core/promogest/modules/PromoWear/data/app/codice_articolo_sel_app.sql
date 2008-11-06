DROP FUNCTION promogest.CodiceArticoloGet(varchar, bigint, integer, bigint, integer, integer);
CREATE OR REPLACE FUNCTION promogest.CodiceArticoloGet(varchar, bigint, integer, bigint, integer, integer) RETURNS VARCHAR AS $$
    DECLARE
        -- Parametri contesto
        _schema                         ALIAS FOR $1;
        _idutente                       ALIAS FOR $2;

        -- Parametri operativi
        _lunghezza_progressivo          ALIAS FOR $3;
        _id_famiglia                    ALIAS FOR $4;
        _lunghezza_codice_famiglia      ALIAS FOR $5;
        _numero_famiglie                ALIAS FOR $6;

        -- Campi appoggio
        schema_prec                     varchar(2000);
        sql_command                     varchar(2000);
        code                            varchar(100);
        progressivo                     bigint;
        prefisso                        varchar;
        lunghezza_codice                integer;
    BEGIN
        -- Memorizza schema precedente
        schema_prec:= ARRAY_TO_STRING(CURRENT_SCHEMAS('t'),',');

        -- Imposta schema corrente
        sql_command:= 'SET SEARCH_PATH TO ' || _schema;
        EXECUTE sql_command;

        code:= '';
        BEGIN
            IF _id_famiglia IS NULL THEN
                --prendo la lunghezza dell'ultimo codice
                SELECT INTO lunghezza_codice CHAR_LENGTH(MAX(a.codice)) FROM articolo a
                        INNER JOIN articolo_taglia_colore atc ON a.id = atc.id_articolo AND atc.id_articolo_padre IS NULL;

                --ottengo il progressivo prelevando gli ultimi _lunghezza_progressivo caratteri del codice
                SELECT INTO progressivo CAST((SUBSTRING(MAX(articolo.codice) 
                                                FROM (lunghezza_codice - _lunghezza_progressivo + 1) 
                                                FOR (_lunghezza_progressivo))) AS INTEGER) 
                    FROM articolo;

                IF progressivo IS NULL THEN
                    progressivo:= 0;
                END IF;

                progressivo:= progressivo + 1;

                SELECT CAST(progressivo AS varchar) INTO code;
                SELECT INTO code LPAD(code, _lunghezza_progressivo, '0');
            ELSE
                --prendo la lunghezza dell'ultimo codice inserito per quella famiglia
                SELECT INTO lunghezza_codice CHAR_LENGTH(MAX(a.codice)) 
                    FROM articolo a INNER JOIN famiglia_articolo fa ON a.id_famiglia_articolo = fa.id
                        INNER JOIN articolo_taglia_colore atc ON a.id = atc.id_articolo AND atc.id_articolo_padre IS NULL
                    WHERE fa.id = _id_famiglia;

                --ottengo il progressivo prelevando gli ultimi _lunghezza_progressivo caratteri del codice
                SELECT INTO progressivo CAST((SUBSTRING(MAX(a.codice) 
                                                FROM (lunghezza_codice - _lunghezza_progressivo + 1) 
                                                FOR (_lunghezza_progressivo))) AS bigint) 
                    FROM articolo a INNER JOIN famiglia_articolo fa ON a.id_famiglia_articolo = fa.id
                        INNER JOIN articolo_taglia_colore atc ON a.id = atc.id_articolo AND atc.id_articolo_padre IS NULL
                    WHERE fa.id = _id_famiglia;

                IF progressivo IS NULL THEN
                    progressivo:= 0;
                END IF;

                progressivo:= progressivo + 1;

                SELECT CAST(progressivo AS varchar) INTO code;
                SELECT INTO code LPAD(code, _lunghezza_progressivo, '0');
                SELECT INTO prefisso promogest.FamigliaArticoloHierarchyGet(_schema, _idutente, _id_famiglia, _lunghezza_codice_famiglia, _numero_famiglie);
                SELECT INTO code prefisso || code;
            END IF;
        EXCEPTION
            WHEN data_exception THEN
                RAISE WARNING 'Errore nella generazione del progressivo';
        END;

        -- Imposta schema precedente
        sql_command:= 'SET SEARCH_PATH TO ' || schema_prec;
        EXECUTE sql_command;

        RETURN code;
    END;
$$ LANGUAGE plpgsql;


DROP FUNCTION promogest.FamigliaArticoloHierarchyGet(varchar, bigint, bigint, integer, integer);
CREATE OR REPLACE FUNCTION promogest.FamigliaArticoloHierarchyGet(varchar, bigint, bigint, integer, integer) RETURNS VARCHAR AS $$
    DECLARE
        -- Parametri contesto
        _schema                         ALIAS FOR $1;
        _idutente                       ALIAS FOR $2;

        -- Parametri operativi
        _id_famiglia                    ALIAS FOR $3;
        _lunghezza_codice_famiglia      ALIAS FOR $4;
        _numero_famiglie                ALIAS FOR $5;

        -- Campi appoggio
        i                               integer;
        prefisso                        varchar;
        corrente                        bigint;
        padre                           bigint;
        codice_famiglia                 varchar;
        schema_prec                     varchar;
        sql_command                     varchar;
    BEGIN
        -- Memorizza schema precedente
        schema_prec:= ARRAY_TO_STRING(CURRENT_SCHEMAS('t'),',');

        -- Imposta schema corrente
        sql_command:= 'SET SEARCH_PATH TO ' || _schema;
        EXECUTE sql_command;

        prefisso:= '';
        codice_famiglia:= '';
        i := 0;

        SELECT INTO corrente _id_famiglia;

        FOR i IN 1.._numero_famiglie LOOP
            IF corrente IS NOT NULL THEN
                SELECT INTO codice_famiglia,padre codice,id_padre
                    FROM famiglia_articolo
                    WHERE id = corrente;
                    
                SELECT INTO prefisso RTRIM(SUBSTRING(codice_famiglia FROM 1 FOR _lunghezza_codice_famiglia)) || prefisso;
                
                corrente:= padre;
            ELSE
                --exit from the loop
                EXIT;
            END IF;
        END LOOP;

        -- Imposta schema precedente
        sql_command:= 'SET SEARCH_PATH TO ' || schema_prec;
        EXECUTE sql_command;

        RETURN prefisso;
    END;
$$ LANGUAGE plpgsql;
