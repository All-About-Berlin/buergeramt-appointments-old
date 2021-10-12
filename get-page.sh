#!/usr/bin/env bash
rm cookies.txt

NOW=$(TZ="Europe/Berlin" date +"%Y-%m-%d,%H.%M")

# First month of appointments
/usr/bin/curl 'https://allaboutberlin.com/out/appointment-anmeldung' \
-L -c cookies.txt --compressed -X 'GET' \
-H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8' \
-H 'Upgrade-Insecure-Requests: 1' \
-H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.2 Safari/605.1.15' \
-H 'Accept-Language: en-gb' \
-H 'Accept-Encoding: gzip, deflate' \
-H 'Connection: keep-alive' \
-o "/var/appointments/output/${NOW}.html"

sleep 5

# Move 1 month
NEXT_MONTH=$(TZ="Europe/Berlin" date --date="`date --date="next month" +%Y-%m-01`" +"%s")
/usr/bin/curl "https://service.berlin.de/terminvereinbarung/termin/day/${NEXT_MONTH}/" \
-L -b cookies.txt --compressed -X 'GET' \
-H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8' \
-H 'Upgrade-Insecure-Requests: 1' \
-H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.2 Safari/605.1.15' \
-H 'Accept-Language: en-gb' \
-H 'Accept-Encoding: gzip, deflate' \
-H 'Connection: keep-alive' \
-o "/var/appointments/output/${NOW}+1M.html"
