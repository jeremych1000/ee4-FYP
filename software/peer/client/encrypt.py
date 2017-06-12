from cryptography.fernet import Fernet
import base64, json


def encrypt(payload, key=b'a0SThzUK3EFVlxbZ5_3ru1ou2vWShkGR6Ca_RV7kvWQ='):
    f = Fernet(key)
    payload = json.dumps(payload)
    payload_b64 = base64.b64encode(payload.encode('utf-8'))
    token = f.encrypt(payload_b64)
    return token


def decrypt(payload, key=b'a0SThzUK3EFVlxbZ5_3ru1ou2vWShkGR6Ca_RV7kvWQ='):
    f = Fernet(key)
    ret = f.decrypt(payload)
    ret_payload = base64.b64decode(ret)
    ret_json = ret_payload.decode('utf-8')
    ret_dict = json.loads(ret_json)
    return ret_dict

    # payload = {"a": 1, "b": 2}
    # a = encypt(payload)
    # print(a)
    # b = decrypt(a)
    # print(b, type(b))
