#!/bin/sh
printf '%s' "$SERVICE_ACCOUNT_KEY" > $GOOGLE_APPLICATION_CREDENTIALS
uwsgi --ini uwsgi.ini
