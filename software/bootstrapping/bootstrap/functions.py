import uuid, socket


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
