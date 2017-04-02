from rest_framework.response import Response
from rest_framework import status

import uuid, socket, requests, json

from . import models

def verify_uuid4(uuid, uuid_string):
    return uuid.hex == uuid_string.replace('-', '')

def verify_ip(ip_address):
    try:
        socket.inet_aton(ip_address)
    except socket.error:
        return False
    return True

def verify_port(port):
    try:
        int(port)
    except ValueError:
        return False
    return True

def get_peer_entry(ip_address, port, token):
    json_ret = {}

    # if verify_ip(ip_address) is False and check_ip is True:
    #     json_ret["status"] = "fail"
    #     json_ret["reason"] = "IP invalid."
    #     return (None, Response(json_ret, status=status.HTTP_400_BAD_REQUEST))

    if verify_port(port) is False:
        json_ret["status"] = "fail"
        json_ret["reason"] = "Port invalid."
        return (None, Response(json_ret, status=status.HTTP_400_BAD_REQUEST))

    try:
        peer_obj = models.peer.objects.get(ip_address=ip_address, port=port)
    except models.peer.DoesNotExist:
        json_ret["status"] = "fail"
        json_ret["reason"] = "Combination not found, please register."
        return (None, Response(json_ret, status=status.HTTP_400_BAD_REQUEST))

    if verify_uuid4(peer_obj.token_update, token):
        json_ret["status"] = "success"
        return (peer_obj, Response(json_ret, status=status.HTTP_200_OK))
    else:
        json_ret["status"] = "fail"
        json_ret["reason"] = "Wrong update token."
        return (None, Response(json_ret, status=status.HTTP_401_UNAUTHORIZED))

def get_local_ip():
    # http://stackoverflow.com/questions/166506/finding-local-ip-addresses-using-pythons-stdlib?page=1&tab=votes#tab-top
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ret = s.getsockname()[0]
    s.close()
    return ret

def get_external_ip():
    r = requests.get('https://api.ipify.org?format=json')
    ip = json.loads(r.text)
    return ip["ip"]
