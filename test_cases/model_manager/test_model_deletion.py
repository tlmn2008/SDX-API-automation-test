# -*- coding: utf-8 -*-

import pytest

from configurations import config
from send_check.req_send import send_user_m_req, send_model_m_req, send_resource_m_req, send_image_m_req
from test_cases import base
from utilities import logger

class TestDeleteModel(base.Base):
    @classmethod
    def setup_class(cls):
        super(TestDeleteModel, cls).setup_class(logger_name='model_deletion')
        cls.token = send_user_m_req.get_token_simple()

    def test_SKTE_T3801_delete_model_with_running_service(self):
        # Title: 删除模型服务正在运行中的模型
        # Owner：qingzhen
        # PreCondition：新建模型，并添加模型版本v1的tensorflow服务。
        model_uuid = send_model_m_req.create_model(self.token, model_name='T3801')
        user_uuid = send_user_m_req.get_uuid_by_username(self.token, config.user_name_a)
        model_location = '{}:{}'.format(user_uuid, config.tf_model_location)
        description = 'T3801 description'
        version_uuid = send_model_m_req.create_model_version(self.token, model_uuid, model_location, description)[
            'uuid']
        resources = send_resource_m_req.get_select_resource_template_info(self.token, 0)
        image_uuid = send_image_m_req.get_image_uuid_by_image_name(self.token,config.tf_model_service_image_name_only_cpu)
        service_uuid = send_model_m_req.create_model_service(token=self.token, name='T3801 service', modelId=model_uuid,
                                                             runtimeImage=image_uuid, cpu=resources['cpu'],
                                                             memory=resources['memory'],
                                                             description="T3801 service description",
                                                             versionName="v1", instances=1)
        #1. 删除模型失败，提示服务正在运行。
        send_model_m_req.delete_model(self.token, model_uuid, resultcode='403')
        #2. 删除模型服务。
        send_model_m_req.delete_model_service(self.token, service_uuid)
        #3. 删除模型成功。
        result = send_model_m_req.delete_model(self.token, model_uuid)

    def test_SKTE_T3802_delete_sharing_model(self):
        # Title: 删除共享模型
        # PreCondition： 创建共享模型,并在共享用户查看该模型。
        model_uuid = send_model_m_req.create_model(self.token, model_name='T3802', users=[config.user_name_b],
                                                   share_type="PUBLIC", is_public=True)
        user_uuid_a = send_user_m_req.get_uuid_by_username(self.token, config.user_name_a)
        token_user_b = send_user_m_req.get_token_simple(config.user_name_b, config.user_passwd_b)
        user_uuid_b = send_user_m_req.get_uuid_by_username(token_user_b, config.user_name_b)

        send_model_m_req.get_model_info(self.token, model_uuid)
        send_model_m_req.get_model_info(token_user_b, model_uuid)

        # 1. 删除共享模型
        send_model_m_req.delete_model(self.token, model_uuid)
        send_model_m_req.get_model_info(self.token, model_uuid, resultcode='404')

        # 2. 切换用户查看共享模型
        send_model_m_req.get_model_info(token_user_b, model_uuid, resultcode='404')


    def test_SKTE_T3803_delete_running_model_version(self):
        # Title: 删除运行中的模型版本
        # Owner：qingzhen
        # PreCondition：新建模型，并添加模型版本v1的tensorflow模型服务启动成功，添加模型版本v2成功。
        model_uuid = send_model_m_req.create_model(self.token, model_name='T3803')
        user_uuid_a = send_user_m_req.get_uuid_by_username(self.token, config.user_name_a)
        model_location = '{}:{}'.format(user_uuid_a, config.tf_model_location)
        description = 'T3803 description'
        version_uuid_v1 = send_model_m_req.create_model_version(self.token, model_uuid, model_location, description)['uuid']
        send_model_m_req.get_model_version_info(self.token, model_uuid, version_uuid_v1)
        version_uuid_v2 = send_model_m_req.create_model_version(self.token, model_uuid, model_location, description)['uuid']
        send_model_m_req.get_model_version_info(self.token, model_uuid, version_uuid_v2)

        resources = send_resource_m_req.get_select_resource_template_info(self.token, 0)
        image_uuid = send_image_m_req.get_image_uuid_by_image_name(self.token,
                                                                   config.tf_model_service_image_name_only_cpu)
        service_uuid = send_model_m_req.create_model_service(token=self.token, name='T3803 service', modelId=model_uuid,
                                                             runtimeImage=image_uuid, cpu=resources['cpu'],
                                                             memory=resources['memory'],
                                                             description="T3803 service description",
                                                             versionName="v1", instances=1)

        send_model_m_req.start_model_service(token=self.token,uuid=service_uuid)
        # 1.删除模型版本v1失败
        result = send_model_m_req.delete_model_version(self.token, model_uuid, version_uuid_v1, resultcode='403')
        # 2.停止模型版本v1服务
        send_model_m_req.stop_model_service(token=self.token, uuid=service_uuid)
        # 3.删除模型版本v1失败
        result = send_model_m_req.delete_model_version(self.token, model_uuid, version_uuid_v1, resultcode='403')
        # 4.删除模型版本v1服务
        send_model_m_req.delete_model_service(token=self.token, uuid=service_uuid)
        # 5.删除模型版本v1成功
        result = send_model_m_req.delete_model_version(self.token, model_uuid, version_uuid_v1)

        #Reset：删除模型
        result = send_model_m_req.delete_model(self.token, model_uuid)

    @classmethod
    def teardown_class(cls):
        pass
