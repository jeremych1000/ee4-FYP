import uuid, socket
from rest_framework.response import Response
from rest_framework import status

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

    if verify_ip(ip_address) is False:
        json_ret["status"] = "fail"
        json_ret["reason"] = "IP invalid."
        return (None, Response(json_ret, status=status.HTTP_400_BAD_REQUEST))

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
