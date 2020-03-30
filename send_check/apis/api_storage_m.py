# -*- coding: utf-8 -*-
from urllib.parse import urljoin

from configurations import config
from send_check.apis.api_template import ApiTemplate
from utilities.common_method import get_uuid_from_token


def get_user_volume_id_req(token):
    uuid = get_uuid_from_token(token)
    req = ApiTemplate()
    sub_path = "storage-manager/api/v1/volumes"
    req.url = urljoin(config.base_url, sub_path)
    req.method = 'get'
    req.headers = {
        "Authorization": token,
        "Content-Type": ""
    }
    req.param ={
        'type': 'user',
        'ownerId': uuid
    }
    return req
