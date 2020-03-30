# -*- coding: utf-8 -*-

import pytest

from configurations import config
from send_check.req_send import send_user_m_req, send_model_m_req, send_resource_m_req, send_image_m_req
from test_cases import base
from utilities import logger
import time


class TestCreateModel(base.Base):
    @classmethod
    def setup_class(cls):
        super(TestCreateModel, cls).setup_class(logger_name='model_creation')
        cls.token = send_user_m_req.get_token_simple()

    @pytest.mark.smoke
    # @pytest.mark.skip(reason="This is a skip example")
    def test_SKTE_T3597_create_and_delete_model(self):
        uuid = send_model_m_req.create_model(self.token, model_name='T3597')
        send_model_m_req.delete_model(self.token, uuid)

    def test_SKTE_T3606_modify_model(self):
        # 创建模型
        uuid = send_model_m_req.create_model(self.token, model_name='T3606')
        # 修改模型
        model_name = 'T3606_modified'
        description = 'modified test'
        labels = ['lmodified']
        model_type = 'mmodified'
        send_model_m_req.modify_model(token=self.token, uuid=uuid, model_name=model_name,
                                      description=description, labels=labels, model_type=model_type,
                                      share_type='PRIVATE')
        # 获取模型信息并检查修改结果
        result = send_model_m_req.get_model_info(self.token, uuid)
        if result['name'] != model_name:
            logger.log_error('Model name is wrong, it should be {} but actually it is {}'.format
                             (model_name, result['name']))
            assert False
        if result['description'].strip() != description:
            logger.log_error('Model description is wrong, it should be {} but actually it is {}'.format
                             (description, result['description'].strip()))
            assert False
        if result['labels'] != labels:
            logger.log_error('Model labels is wrong, it should be {} but actually it is {}'.format
                             (labels, result['labels']))
            assert False
        if result['modelType'] != model_type:
            logger.log_error('Model type is wrong, it should be {} but actually it is {}'.format
                             (model_type, result['modelType']))
            assert False

        # 删除模型
        send_model_m_req.delete_model(self.token, uuid)

    @pytest.mark.smoke
    def test_SKTE_T3609_model_version_import(self):
        # 创建模型
        model_uuid = send_model_m_req.create_model(self.token, model_name='T3609')
        user_uuid = send_user_m_req.get_uuid_by_username(self.token, config.user_name_a)
        model_location = '{}:{}'.format(user_uuid, config.tf_model_location)
        # 添加模型版本
        description = 'T3609 description'
        version_uuid = send_model_m_req.create_model_version(self.token, model_uuid, model_location, description)[
            'uuid']
        # 获取模型版本信息并检查
        result = send_model_m_req.get_model_version_info(self.token, model_uuid, version_uuid)
        if result['name'].lower() != 'v1':
            logger.log_error('Model version number is wrong, it should be "v1" but actually it is {}'.format
                             (result['name']))
            assert False
        if result['description'].strip() != description:
            logger.log_error('Model version description is wrong, it should be {} but actually it is {}'.format
                             (description, result['description'].strip()))
            assert False
        if result['modelPath'].strip() != model_location:
            logger.log_error('Model version modelPath is wrong, it should be {} but actually it is {}'.format
                             (model_location, result['modelPath'].strip()))
            assert False

        # 删除模型版本
        send_model_m_req.delete_model_version(self.token, model_uuid, version_uuid)
        # 删除模型
        send_model_m_req.delete_model(self.token, model_uuid)

    def test_SKTE_T3622_modity_model_version(self):
        # 创建模型
        model_uuid = send_model_m_req.create_model(self.token, model_name='T3622')
        user_uuid = send_user_m_req.get_uuid_by_username(self.token, config.user_name_a)
        model_location = '{}:{}'.format(user_uuid, config.tf_model_location)
        # 添加模型版本
        description = 'T3622 description'
        version_uuid = send_model_m_req.create_model_version(self.token, model_uuid, model_location, description)[
            'uuid']
        # 修改模型版本
        modelPath_mdf = '{}:{}'.format(user_uuid, config.spark_model_location)
        description_mdf = 'T3609 description modified'
        send_model_m_req.modity_model_version(self.token, model_uuid, version_uuid, modelPath_mdf, description_mdf)
        # 获取模型版本信息并检查
        result = send_model_m_req.get_model_version_info(self.token, model_uuid, version_uuid)
        if result['description'].strip() != description:
            logger.log_error('Model version description is wrong, it should be {} but actually it is {}'.format
                             (description_mdf, result['description'].strip()))
            assert False
        if result['modelPath'].strip() != model_location:
            logger.log_error('Model version modelPath is wrong, it should be {} but actually it is {}'.format
                             (modelPath_mdf, result['modelPath'].strip()))
            assert False

        # 删除模型版本
        send_model_m_req.delete_model_version(self.token, model_uuid, version_uuid)
        # 删除模型
        send_model_m_req.delete_model(self.token, model_uuid)

    def test_SKTE_T3623_delete_model_version_then_add_new_version(self):
        # Title: 删除模型版本后添加版本
        # Owner: qingzhen
        # PreCondition：新建模型，添加模型版本v1和v2
        model_uuid = send_model_m_req.create_model(self.token, model_name='T3623')
        time.sleep(1)
        user_uuid = send_user_m_req.get_uuid_by_username(self.token, config.user_name_a)
        time.sleep(1)
        model_location = '{}:{}'.format(user_uuid, config.tf_model_location)
        description = 'T3623 description'
        version_uuid_v1 = send_model_m_req.create_model_version(self.token, model_uuid, model_location, description)[
            'uuid']
        time.sleep(1)
        result = send_model_m_req.get_model_version_info(self.token, model_uuid, version_uuid_v1)
        if result['name'].lower() != 'v1':
            logger.log_error('Model version number is wrong, it should be "v1" but actually it is {}'.format
                             (result['name']))
            assert False
        version_uuid_v2 = send_model_m_req.create_model_version(self.token, model_uuid, model_location, description)[
            'uuid']
        time.sleep(1)
        result = send_model_m_req.get_model_version_info(self.token, model_uuid, version_uuid_v2)
        if result['name'].lower() != 'v2':
            logger.log_error('Model version number is wrong, it should be "v2" but actually it is {}'.format
                             (result['name']))
            assert False
        time.sleep(1)
        # 1.删除模型版本 v1
        send_model_m_req.delete_model_version(self.token, model_uuid, version_uuid_v1)
        # 2. 删除版本 v1后检查模型版本
        time.sleep(1)
        send_model_m_req.get_model_version_info(self.token, model_uuid, version_uuid_v1, resultcode='404')
        time.sleep(1)
        send_model_m_req.get_model_version_info(self.token, model_uuid, version_uuid_v2)
        if result['name'].lower() != 'v2':
            logger.log_error('Model version number is wrong, it should be "v2" but actually it is {}'.format
                             (result['name']))
            assert False
        # 3. 添加模型版本 v3
        time.sleep(1)
        version_uuid_v3 = send_model_m_req.create_model_version(self.token, model_uuid, model_location, description)[
            'uuid']
        time.sleep(1)
        result = send_model_m_req.get_model_version_info(self.token, model_uuid, version_uuid_v3)
        if result['name'].lower() != 'v3':
            logger.log_error('Model version number is wrong, it should be "v3" but actually it is {}'.format
                             (result['name']))
            assert False
        # 4.删除模型版本 v3
        send_model_m_req.delete_model_version(self.token, model_uuid, version_uuid_v3)
        time.sleep(1)
        send_model_m_req.get_model_version_info(self.token, model_uuid, version_uuid_v3, resultcode='404')
        time.sleep(1)
        # 5.添加模型版本 v4，并检查剩下模型版本v2,v4信息。
        version_uuid_v4 = send_model_m_req.create_model_version(self.token, model_uuid, model_location, description)[
            'uuid']
        time.sleep(1)
        result = send_model_m_req.get_model_version_info(self.token, model_uuid, version_uuid_v4)
        if result['name'].lower() != 'v4':
            logger.log_error('Model version number is wrong, it should be "v4" but actually it is {}'.format
                             (result['name']))
            assert False
        time.sleep(1)
        result = send_model_m_req.get_model_version_info(self.token, model_uuid, version_uuid_v2)
        if result['name'].lower() != 'v2':
            logger.log_error('Model version number is wrong, it should be "v2" but actually it is {}'.format
                             (result['name']))
            assert False
        time.sleep(1)
        # Reset：删除模型
        send_model_m_req.delete_model(self.token, model_uuid)

    def test_SKTE_T3624_create_tf_model_service_onlyby_CPU(self):
        # 创建模型
        model_uuid = send_model_m_req.create_model(self.token, model_name='T3624 model')
        user_uuid = send_user_m_req.get_uuid_by_username(self.token, config.user_name_a)
        model_location = '{}:{}'.format(user_uuid, config.tf_model_location)
        # 添加模型版本
        description = 'T3624 description'
        version_uuid = send_model_m_req.create_model_version(self.token, model_uuid, model_location, description)[
            'uuid']
        # 添加模型服务
        resources = send_resource_m_req.get_select_resource_template_info(self.token, 0)
        image_uuid = send_image_m_req.get_image_uuid_by_image_name(self.token,
                                                                   config.tf_model_service_image_name_only_cpu)
        service_uuid = send_model_m_req.create_model_service(token=self.token, name='T3624 service', modelId=model_uuid,
                                                             runtimeImage=image_uuid, cpu=resources['cpu'],
                                                             memory=resources['memory'],
                                                             description='T3624 service description',
                                                             versionName='v1', instances=1)
        # 删除模型服务
        send_model_m_req.delete_model_service(self.token, service_uuid)
        # 删除模型版本
        send_model_m_req.delete_model_version(self.token, model_uuid, version_uuid)
        # 删除模型
        send_model_m_req.delete_model(self.token, model_uuid)

    def test_SKTE_T3720_share_model_and_cancel(self):
        # 创建模型
        model_uuid = send_model_m_req.create_model(self.token, model_name='T3720 model')
        user_uuid = send_user_m_req.get_uuid_by_username(self.token, config.user_name_a)
        model_location = '{}:{}'.format(user_uuid, config.tf_model_location)
        # 添加模型版本
        description = 'T3720 description'
        version_uuid = send_model_m_req.create_model_version(self.token, model_uuid, model_location, description)[
            'uuid']
        # 共享模型
        send_model_m_req.share_model_and_cancel(token=self.token, uuid=model_uuid, share_type="PUBLIC", is_public=True)
        shareuser_token = send_user_m_req.get_token_simple(config.user_name_b, config.user_passwd_b)
        # 验证模型已共享，1）可查看该模型；2）可查看该模型版本
        send_model_m_req.get_model_info(shareuser_token, model_uuid)
        send_model_m_req.get_model_version_info(shareuser_token, model_uuid, version_uuid)
        # 取消共享模型
        send_model_m_req.share_model_and_cancel(token=self.token, uuid=model_uuid, share_type="PRIVATE", is_public=False)
        # 验证模型已取消共享，无权进入该模型
        send_model_m_req.get_model_info(shareuser_token, model_uuid, '401')
        # 删除模型版本
        send_model_m_req.delete_model_version(self.token, model_uuid, version_uuid)
        # 删除模型
        send_model_m_req.delete_model(self.token, model_uuid)

    def test_SKTE_T3616_create_duplicated_model(self):
        # Title: 新建重名模型
        # Owner: qingzhen
        model_uuid = send_model_m_req.create_model(self.token, model_name='T3616')
        send_model_m_req.create_model(self.token, model_name='T3616',resultcode='400')

        # Reset：删除模型
        send_model_m_req.delete_model(self.token, model_uuid)

    @classmethod
    def teardown_class(cls):
        pass
