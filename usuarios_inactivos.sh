#!/bin/bash

# Fecha límite (hace 365 días)
LIMIT_DATE=$(date -d "365 days ago" +%s)

printf "%-20s %-25s %-10s\n" "USUARIO" "ULTIMA_CONEXION" "HOME_SIZE"
printf "%-20s %-25s %-10s\n" "-------" "-----------------" "---------"

# Obtener usuarios con UID >= 1000
awk -F: '$3 >= 1000 {print $1}' /etc/passwd | while read USER; do

    # Obtener última conexión
    LASTLOG_LINE=$(lastlog -u "$USER" | tail -n 1)

    # Si nunca ha ingresado
    if echo "$LASTLOG_LINE" | grep -q "Never logged in"; then
        LAST_CONN="Never"
        LAST_CONN_EPOCH=0
    else
        # Extraer fecha (desde columna 4 en adelante)
        LAST_CONN=$(echo "$LASTLOG_LINE" | awk '{for(i=4;i<=NF;i++) printf $i " "; print ""}')
        LAST_CONN_EPOCH=$(date -d "$LAST_CONN" +%s 2>/dev/null)
    fi

    # Validar si es más antiguo que el límite
    if [[ "$LAST_CONN_EPOCH" -lt "$LIMIT_DATE" ]]; then

        # Tamaño del home
        HOME_DIR="/repositorio/$USER"
        if [ -d "$HOME_DIR" ]; then
            SIZE=$(du -sh "$HOME_DIR" 2>/dev/null | awk '{print $1}')
        else
            SIZE="N/A"
        fi

        printf "%-20s %-25s %-10s\n" "$USER" "$LAST_CONN" "$SIZE"
    fi

done
