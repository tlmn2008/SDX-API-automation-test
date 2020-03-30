# -*- coding: utf-8 -*-
from configurations import config
from send_check.apis.api_template import ApiTemplate
from urllib.parse import urljoin


def get_all_image_list_req(token):
    # 获取所有镜像列表请求
    path = '/image-manager/api/v1/images/'
    req = ApiTemplate()
    req.url = urljoin(config.base_url, path)
    req.method = 'get'
    req.headers = {'Authorization': token}

    return req

