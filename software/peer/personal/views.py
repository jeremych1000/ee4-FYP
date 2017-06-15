from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.http import HttpResponse
from django.utils.safestring import mark_safe
from django.core.management import call_command

from django_tables2 import RequestConfig

import requests, os, subprocess, json

import googlemaps

from client import models, serializers
from alpr import models as models_alpr


def index(request):
    my_name = settings.MY_NAME
    return render(request, "personal/home.html", {"my_name": my_name})


def contact(request):
    details = [
        {'name': 'Jeremy Chan', 'email': 'jc4913@ic.ac.uk'},
    ]
    return render(request, "personal/contact.html", {'details': details})


def about(request):
    return render(request, "personal/about.html")


def download(request):
    return render(request, "personal/download.html")


def privacy(request):
    return render(request, "personal/privacy.html")


def blank(request):
    return render(request, "personal/blank.html")


def peers(request):
    peer_list = models.peer_list.objects.all()
    peer_locations = []

    # ['Bondi Beach', -33.890542, 151.274856, 4],
    # ['Coogee Beach', -33.923036, 151.259052, 5],
    # ['Cronulla Beach', -34.028249, 151.157507, 3],
    # ['Manly Beach', -33.80010128657071, 151.28747820854187, 2],
    # ['Maroubra Beach', -33.950198, 151.259302, 1]
    for i in peer_list:
        peer_locations.append([str(i.ip_address)+":"+str(i.port), str(i.location_lat), str(i.location_long)])

    #print(mark_safe(peer_locations), type(mark_safe(peer_locations)))
    return render(request, "personal/peers.html", {"locations": mark_safe(peer_locations)})



def violations(request):
    violations_obj = models.violations.objects.all()
    violations_list = []

    gmaps = googlemaps.Client(key=settings.GOOGLE_MAPS_API_KEY)
    for v in violations_obj:
        origin = v.plate1.location_lat, v.plate1.location_long
        destination = v.plate2.location_lat, v.plate2.location_long
        ret = gmaps.directions(origin=origin, destination=destination, units="imperial")

        polyline = ret[0]["overview_polyline"]["points"]

        static_maps_url = "https://maps.googleapis.com/maps/api/staticmap?size=400x400&zoom=13" \
                          + "&path=weight:7|color:red|enc:" + polyline \
                        + "&markers=color:blue|" + str(origin[0]) + "," + str(origin[1])\
                          + "|" + str(destination[0]) + "," + str(destination[1])\
                          + "&key=" + settings.GOOGLE_MAPS_API_KEY

        violations_list.append(
            {
                "plate": v.plate1.plate,
                "time1": v.time1,
                "time2": v.time2,
                "distance": v.distance,
                "speed": v.average_speed,
                "unit": v.unit,
                "img_path": v.plate1.img_path,
                "gmaps": static_maps_url
            }
        )
    return render(request, "personal/violations.html", {"violations": violations_list})


def get_alpr_image(request, dir):
    try:
        with open(dir, "rb") as f:
            return HttpResponse(f.read(), content_type="image/jpeg")
    except IOError:
        return render(request, "personal/blank.html", {"data": "Cannot open image."})


def dashboard(request):
    if request.method == 'GET' and 'action' in request.GET:
        action = request.GET.get('action')
        # RESET BUTTONS
        if action == "register":
            path_to_script = settings.BASE_DIR + '/b1.sh'
            try:
                output = subprocess.check_output([path_to_script])
            except Exception as e:
                messages.error(request, str(e))
                raise
            messages.success(request, "Done.")
        elif action == "get_peer_list":
            path_to_script = settings.BASE_DIR + '/b2.sh'
            try:
                output = subprocess.check_output([path_to_script])
            except Exception as e:
                messages.error(request, str(e))
                raise
            messages.success(request, "Done.")
        elif action == "clear_bootstrap":
            b = models.bootstrap.objects.all()
            if len(b) == 0:
                messages.info(request, "Nothing to delete.")
            for i in b:
                try:
                    i.delete()
                except Exception as e:
                    messages.error(request, str(e))
                    raise
            messages.success(request, "Deleted "+str(len(b))+" bootstrap object(s).")
        elif action == "clear_peers":
            b = models.peer_list.objects.all()
            if len(b) == 0:
                messages.info(request, "Nothing to delete.")
            for i in b:
                try:
                    i.delete()
                except Exception as e:
                    messages.error(request, str(e))
                    raise
            messages.success(request, "Deleted "+str(len(b))+" peer_list object(s).")
        elif action == "clear_videos":
            b = models_alpr.videos.objects.all()
            if len(b) == 0:
                messages.info(request, "Nothing to delete.")
            for i in b:
                try:
                    i.delete()
                except Exception as e:
                    messages.error(request, str(e))
                    raise
            messages.success(request, "Deleted "+str(len(b))+" video object(s).")
        elif action == "clear_plates":
            b = models.plates.objects.all()
            if len(b) == 0:
                messages.info(request, "Nothing to delete.")
            for i in b:
                try:
                    i.delete()
                except Exception as e:
                    messages.error(request, str(e))
                    raise
            messages.success(request, "Deleted "+str(len(b))+" plate object(s).")
        elif action == "clear_violations":
            b = models.violations.objects.all()
            if len(b) == 0:
                messages.info(request, "Nothing to delete.")
            for i in b:
                try:
                    i.delete()
                except Exception as e:
                    messages.error(request, str(e))
                    raise
            messages.success(request, "Deleted "+str(len(b))+" violation object(s).")
        elif action == "reset_all":
            messages.error(request, "Are you SURE you want to delete everything? This is permanent!")
            messages.error(request, mark_safe("<a href='/dashboard?action=reset_all_conf'>Click here to delete.</a>"))
            messages.error(request, mark_safe("<a href='/dashboard'>Click here to go back.</a>"))
        elif action == "reset_all_conf":
            list_to_delete = []
            for i in models.bootstrap.objects.all():
                list_to_delete.append(i)
            for i in models.peer_list.objects.all():
                list_to_delete.append(i)
            for i in models.plates.objects.all():
                list_to_delete.append(i)
            for i in models.violations.objects.all():
                list_to_delete.append(i)
            for i in models_alpr.videos.objects.all():
                list_to_delete.append(i)
            for i in list_to_delete:
                try:
                    i.delete()
                except Exception as e:
                    messages.error(request, str(e))
                    raise
            messages.success(request, "Deleted "+len(list_to_delete)+" object(s).")

        # ACTION BUTTONS
        elif action == "keep_alive_bootstrap":
            call_command('runcrons', 'client.cron.keep_alive.Keep_Alive', force=True)
            messages.info(request, "Action run, please check server console for results.")
        elif action == "keep_alive_peer":
            call_command('runcrons', 'client.cron.keep_alive.Keep_Alive_Peer', force=True)
            messages.info(request, "Action run, please check server console for results.")
        elif action == "modify_trust":
            call_command('runcrons', 'client.cron.modify_trust.Modify_Trust', force=True)
            messages.info(request, "Action run, please check server console for results.")
        elif action == "share_plates":
            call_command('runcrons', 'client.cron.share_plates.Share_Plates', force=True)
            messages.info(request, "Action run, please check server console for results.")
        elif action == "detect_videos":
            call_command('runcrons', 'alpr.cron.import_videos.Import_Videos', force=True)
            messages.info(request, "Action run, please check server console for results.")
        elif action == "detect_plates":
            call_command('runcrons', 'alpr.cron.process_videos.Process_Videos', force=True)
            messages.info(request, "Action run, please check server console for results.")
        elif action == "detect_violations":
            call_command('runcrons', 'client.cron.violations.Detect_Violations', force=True)
            messages.info(request, "Action run, please check server console for results.")

        # IF ACTION ELSE ENDS HERE
        else:
            messages.error(request, "Invalid action specified.")

    try:
        bootstrap_obj = models.bootstrap.objects.all()
        peer_obj = models.peer_list.objects.all()
        plates_obj = models.plates.objects.all()
        violations_obj = models.violations.objects.all()

        bootstrap_obj_s = serializers.dashboard_bootstrap(bootstrap_obj, many=True)
        peer_obj_s = serializers.dashboard_peer(peer_obj, many=True)
        plates_obj_s = serializers.dashboard_plates(plates_obj, many=True)
        violations_obj_s = serializers.dashboard_violations(violations_obj, many=True)

        bo = json.loads(json.dumps(bootstrap_obj_s.data))
        pe = json.loads(json.dumps(peer_obj_s.data))
        pl = json.loads(json.dumps(plates_obj_s.data))
        vi = json.loads(json.dumps(violations_obj_s.data))

        bo_table = serializers.table_bootstrap(bo)
        pe_table = serializers.table_peers(pe)
        pl_table = serializers.table_plates(pl)
        vi_table = serializers.table_violations(vi)

        #RequestConfig(request).configure(bo_table)

        data = {
            "bootstrap": bo_table,
            "peer": pe_table,
            "plate": pl_table,
            "violation": vi_table
        }

        length = {
            "bootstrap": len(bootstrap_obj),
            "peer": len(peer_obj),
            "plate": len(plates_obj),
            "violation": len(violations_obj)
        }
    except AttributeError:
        messages.warning(request, "Attribute error, please make sure there is complete data.")
        return render(request, "personal/dashboard.html")
    except TypeError:
        messages.warning(request, "Type error, please make sure there is complete data.")
        return render(request, "personal/dashboard.html")

    # else
    return render(request, "personal/dashboard.html", {"data": data, "length": length})
