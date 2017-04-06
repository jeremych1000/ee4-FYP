#!/bin/bash

printf "Registering with bootstrap server"
python3 manage.py runcrons 'client.cron.register.Register' --force