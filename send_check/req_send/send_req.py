# -*- coding: utf-8 -*-
import requests
import json
from send_check.apis.api_template import ApiTemplate
from utilities import logger


def send_request(request_data: ApiTemplate, result_code='200'):
    """
    将request_data的内容组成http请求并发送，检查result code并返回response body。
    :param request_data: 接口请求内容，包括请求方法、请求URL、URL参数、请求头、请求体
    :param result_code: 期望的response code
    :return: http response
    """

    if len(request_data.url) == 0 or len(request_data.method) == 0:
        logger.log_error("request_data's url or/and method is not presented.")
        return False
    else:
        # 拼接HTTP请求
        url = request_data.url+'?' if len(request_data.param) > 0 else request_data.url
        for i, j in request_data.param.items():
            if url.endswith('?'):
                url = '{}{}={}'.format(url, i, j)
            else:
                url = '{}&{}={}'.format(url, i, j)
        method = request_data.method.upper()
        headers = request_data.headers
        data = request_data.body
        files = request_data.files

        # 发送请求
        if method == 'POST':
            if len(request_data.files) == 0:
                result = requests.post(url=url, headers=headers, json=data)
            else:
                result = requests.post(url=url, headers=headers, data=data, files=files)
        elif method == 'GET':
            result = requests.get(url=url, headers=headers)
        elif method == 'DELETE':
            result = requests.delete(url=url, headers=headers)
        elif method == 'PATCH':
            result = requests.patch(url=url, headers=headers, json=data)
        elif method == 'OPTIONS':
            result = requests.options(url=url, headers=headers)
        elif method == 'HEAD':
            result = requests.head(url=url, headers=headers)
        else:
            logger.log_error("The HTTP method of {} in request_data is not supported!".format(request_data.url))
            return False

        logger.log_debug("url: {}".format(url))
        logger.log_debug("method: {}".format(method))
        logger.log_debug("headers: {}".format(headers))
        logger.log_debug("data: {}".format(data))
        logger.log_debug(">>>>>>>> The HTTP request is sent.")
        # 部分请求返回结果不是json格式，如下载文件，返回为文件内容
        if result.text.startswith("{"):
            # 部分请求如DELETE成功执行后result.content为空
            if len(result.content) != 0:
                content = json.loads(str(result.content, 'utf-8'))
            else:
                content = ''
        else:
            content = result.text
        logger.log_debug("status code: {}".format(result.status_code))
        logger.log_debug("headers: {}".format(result.headers))
        logger.log_debug("body: {}".format(content))
        logger.log_debug("<<<<<<<< Got HTTP response.")

        # 检查return code
        if str(result.status_code) != result_code:
            logger.log_error("The result code of response is {}, not the expected value: {}".format(result.status_code,
                                                                                                    result_code))
            assert False

        return content
