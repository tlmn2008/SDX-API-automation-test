# -*- coding: utf-8 -*-
from utilities import logger
from send_check.req_send import send_req
from send_check.apis import api_compose


def get_image_uuid_by_image_name(token, image_name):
    req = api_compose.get_compose_image_list_req(token=token, name=image_name)
    res = send_req.send_request(req)
    if len(res['data']) == 0:
        logger.log_error('Did not find such image: {}'.format(image_name))
        return False
    else:
        return res['data'][0]['uuid']
