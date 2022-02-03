#!/bin/sh

# force the startup script to fail if one of the comamnds fails
set -e

# download the Django static content and clear eventual leftover files
python manage.py collectstatic --noinput --clear

# run a TCP socket
uwsgi --socket :8000 --master --enable-threads --module delfitlm.wsgi
