# -*- coding: utf-8 -*-
from test_cases import base
from utilities import logger
from configurations import config
from send_check.req_send import send_user_m_req, send_resource_m_req


class TestResourceTemplate(base.Base):
    @classmethod
    def setup_class(cls):
        super(TestResourceTemplate, cls).setup_class(logger_name='resource_template')
        cls.token = send_user_m_req.get_token_simple(config.user_sysadmin, config.user_passwd_sysadmin)

    def test_create_and_delete_resource_template_cpu(self):
        uuid = send_resource_m_req.create_resource_template_cpu(self.token, cpu=8000, memory=17179869184)
        send_resource_m_req.delete_resource_template(self.token, uuid)

    # 测试环境中没有GPU则不能执行
    def not_test_create_and_delete_resource_template_gpu(self):
        uuid = send_resource_m_req.create_resource_template_gpu(self.token, label='gpu-1660', count=10)
        send_resource_m_req.delete_resource_template(self.token, uuid)

    @classmethod
    def teardown_class(cls):
        pass
