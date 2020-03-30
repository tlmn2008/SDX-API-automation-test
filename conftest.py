# -*- coding: utf-8 -*-
import pytest
import requests
import sys
from configurations import config
from utilities import logger
from urllib.parse import urljoin

# from os import path
# sys.path.append('./')
# sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
# @pytest.fixture(scope='session')
# def token_admin():
#     url = urljoin(config.base_url, "/user-manager/api/v1/tokens/")
#     data = {
#         "grantType": "password",
#         "username": "Teng_Liang",
#         "password": "testSDX@001"
#     }
#     resp = requests.post(url=url,  json=data)
#     print(resp.json())
#
#     token = f"Bearer {resp.json()['accessToken']}"
#     return token