#!/bin/bash

printf "Get Peer List\n"
python3 manage.py runcrons 'client.cron.get_peer_list.Get_Peer_List' --force

printf "Keep Alive\n"
python3 manage.py runcrons 'client.cron.keep_alive.Keep_Alive' --force

printf "Keep Alive Peer\n"
python3 manage.py runcrons 'client.cron.keep_alive.Keep_Alive_Peer' --force