from django.utils import timezone
from django.db.models import Q, Avg

import datetime

from client import models


def live_data(request):
    try:
        bootstrap_obj = models.bootstrap.objects.all()
        peer_obj = models.peer_list.objects.all()
        plates_obj = models.plates.objects.all()
        violations_obj = models.violations.objects.all()

        no_peers_in_network = len(peer_obj)

        time_connected_to_bootstrap = (timezone.now() - bootstrap_obj.first().time_accepted).total_seconds()
        time_connected_to_bootstrap = int(time_connected_to_bootstrap / 60)  # in minutes

        peer_self = peer_obj.filter(is_self=True)
        plates_others = plates_obj.filter(~Q(source=peer_self))

        no_plates_from_peers = len(plates_others)

        ret = {
            "no_peers_in_network": {
                "current": no_peers_in_network,
                "min": 0,
                "max": 5,
                "width": int(100 * no_peers_in_network / 5)
            },
            "time_connected_to_bootstrap": {
                "current": time_connected_to_bootstrap,
                "min": 0,
                "max": 10000,
                "width": int(100 * time_connected_to_bootstrap / 10000)
            },
            "no_plates_from_peers": {
                "current": no_plates_from_peers,
                "min": 0,
                "max": 20,
                "width": int(100 * no_plates_from_peers / 20)
            },
        }

    except AttributeError:
        return {"registered": (len(bootstrap_obj) > 0), "peers_exist": (len(peer_obj) > 0)}

    try:
        avg_confidence = plates_obj.aggregate(Avg('confidence'))["confidence__avg"]
        avg_speed_violations = violations_obj.aggregate(Avg('average_speed'))["average_speed__avg"]

        ret["avg_confidence"] = {
                "current": avg_confidence,
                "min": 0,
                "max": 100,
                "width": int(100 * avg_confidence / 100)
            }
        ret["avg_speed_violations"] = {
                "current": avg_speed_violations,
                "min": 0,
                "max": 50,
                "width": int(100 * avg_speed_violations / 50)
        }
    except TypeError:
        pass

    ret["registered"] = len(bootstrap_obj) > 0
    ret["peers_exist"] = len(peer_obj) > 0
    return ret
