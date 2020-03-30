# -*- coding: utf-8 -*-
from test_cases import base
from utilities import logger
from send_check.req_send import send_user_m_req, send_skyflow_m_req
from configurations import config


class TestSkyFlow(base.Base):
    @classmethod
    def setup_class(cls):
        super(TestSkyFlow, cls).setup_class(logger_name='skyflow')
        cls.token = send_user_m_req.get_token_simple()

    def test_create_and_delete_skyflow_batch(self):
        uuid = send_skyflow_m_req.create_skyflow_batch(self.token, name='autotest_skyflow_batch')
        send_skyflow_m_req.delete_skyflow(self.token, uuid)

    def test_create_and_delete_skyflow_stream(self):
        uuid = send_skyflow_m_req.create_skyflow_stream(self.token, name='autotest_skyflow_stream')
        send_skyflow_m_req.delete_skyflow(self.token, uuid)

    @classmethod
    def teardown_class(cls):
        pass
