#!/bin/bash

printf "Registering with bootstrap server\n"
python3 manage.py runcrons 'client.cron.register.Register' --force