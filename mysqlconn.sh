#!/usr/bin/env bash

# 5 minutes between alerts
SECONDS_BETWEEN_ALERTS=300

# Track when we sent the last alert
LAST_ALERT=0

while true; do
    NUMBER_CONNECTIONS=$(mysql --defaults-extra-file=/data/.prod.cnf -sNe "select count(*) as connection_count from INFORMATION_SCHEMA.PROCESSLIST;")

    RIGHTNOW=$(date +"%s")

    if [ "$NUMBER_CONNECTIONS" -ge "750" ] && [ "`expr $RIGHTNOW - $LAST_ALERT`" -ge "$SECONDS_BETWEEN_ALERTS" ]; then
        CONNECTIONS_PER_USER=$(mysql --defaults-extra-file=/data/.prod.cnf -e "select USER, HOST, count(*) as connection_count from INFORMATION_SCHEMA.PROCESSLIST group by USER order by connection_count desc;")

        curl -X POST https://hooks.slack.com/services/xxx/xxx/xxx --data-urlencode "payload={\"username\": \"RDS Police\", \"text\": \"\nTOTAL CONNECTIONS: $NUMBER_CONNECTIONS\n$CONNECTIONS_PER_USER\n\", \"icon_emoji\": \":alert:\"}"

        LAST_ALERT="$RIGHTNOW"
    fi

    sleep 5
done
