from django.conf import settings
from django_cron import CronJobBase, Schedule

import requests, json, datetime

from client import models, serializers


class Share_Plates(CronJobBase):
    RUN_EVERY_MINS = 1
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'peer.share_plates'

    def do(self):
        if models.plates.objects.filter(sent=False).count() >= settings.NO_PLATES_BATCH_BEFORE_SEND:
            plate_payload = []
            distinct_sources = models.plates.objects.values('source').distinct()
            print("1")
            for source in distinct_sources:
                s = models.peer_list.objects.get(id=source["source"])
                plate_payload_tmp = {}
                plate_payload_tmp["source"] = {
                    "ip_address": s.ip_address,
                    "port": s.port
                }
                se = models.plates.objects.filter(source=s, sent=False)
                ser = serializers.get_plates(list(se), many=True)
                plate_payload_tmp["plates"] = json.dumps(ser.data)
                plate_payload.append(plate_payload_tmp)

            #now get list of peers and send payload to each of them
            active_peers = models.peer_list.objects.filter(active=True,
                                                           is_self=False)  # , trust__gte=settings.TRUST_THRESHOLD)

            for i in active_peers:
                if i.trust > settings.MIN_TRUST_FOR_SHARE_PLATES or i.trust == 0:  # if 0 assumes the peer is new, so broadcast anyway
                    base_url = 'http://' + i.ip_address + ':' + str(i.port) + '/client/plates/'
                    token = str(i.token)
                    print(base_url, token)
                    headers = {
                        'Content-Type': 'application/json',
                        'Authorization': token,
                    }

                    payload = {
                        "ip_address": settings.PEER_HOSTNAME,
                        "port": settings.PEER_PORT,
                        "plate_list": plate_payload
                    }
                    print("\n\npayload is ", payload)
                    try:
                        r = requests.post(base_url, data=json.dumps(payload), headers=headers)
                        r.raise_for_status()
                    except requests.RequestException as e:
                        print(r.status_code, r.json(), str(e))
                    print(r.status_code)
                    if r.status_code == 200:
                        at_least_one_peer_received = True
                        print("Setting plates to 'sent'")
                        for p in range(0): #plates_to_be_sent:
                            p.sent = True
                            try:
                                p.save()
                            except Exception as e:
                                print("Exception occured while saving - ", str(e))
        else:
            print("Not enough plates yet.")
