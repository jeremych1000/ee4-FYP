#!/bin/bash

python3 manage.py runcrons 'client.cron.register.Register' --force
python3 manage.py runcrons 'client.cron.get_peer_list.Get_Peer_List' --force
python3 manage.py runcrons 'client.cron.keep_alive.Keep_Alive' --force
python3 manage.py runcrons 'client.cron.keep_alive.peer.Keep_Alive.Peer' --force