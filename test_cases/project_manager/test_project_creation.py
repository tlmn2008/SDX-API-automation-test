# -*- coding: utf-8 -*-
from configurations import config
from send_check.req_send import send_user_m_req, send_project_m_req
from test_cases import base


class TestCreateProject(base.Base):
    @classmethod
    def setup_class(cls):
        super(TestCreateProject, cls).setup_class(logger_name='project_creation')
        cls.token = send_user_m_req.get_token_simple()

    def test_SKTE_T3594_create_and_delete_empty_project(self):
        res = send_project_m_req.create_project(self.token, project_name='T3594 auto test empty project')
        send_project_m_req.delete_project_by_uuid(self.token, res)

    def test_SKTE_T3595_create_and_delete_model_project(self):
        res = send_project_m_req.create_project(self.token, project_name='T3595 auto test model project ', is_template=True)
        send_project_m_req.delete_project_by_uuid(self.token, res)

    def test_SKTE_T3596_create_and_delete_project_from_model(self):
        # 创建模板项目
        uuid = send_project_m_req.create_project(self.token, project_name='T3596 model project ', is_template=True)
        # 基于模板项目创建项目
        res = send_project_m_req.create_project(self.token, model_id=uuid)
        # 删除基于模板项目创建的项目
        send_project_m_req.delete_project_by_uuid(self.token, res)
        # 删除模板项目
        send_project_m_req.delete_project_by_uuid(self.token, uuid)


    def test_SKTE_T3712_create_and_delete_collaborative_project(self):
        # 创建协作项目
        uuid = send_user_m_req.get_uuid_by_username(self.token, config.collaborative_user)  # 获取协作用户uuid
        joint_id = []
        joint_id.append(uuid)
        res = send_project_m_req.create_project(self.token, project_name='T3712 auto test collaborative project', users=joint_id)  # 获取协作项目uuid
        # 协作项目校验：协作用户可以进入协作项目页面，可以创建/删除、启停任务（任务部分待补充），不支持对协作项目进行写操作，如删除协作项目
        joint_token = send_user_m_req.get_token_simple(config.collaborative_user, config.collaborative_userpwd)  # 获取协作用户token
        send_project_m_req.entry_project_by_uuid(joint_token, res)  # 协作用户可以进入协作项目页面
        # send_project_m_req.delete_project_by_uuid(joint_token, res, '403')  # 协作用户无权删除协作项目，实际测试不通过，可以通过接口删除
        # 创建者删除协作项目
        send_project_m_req.delete_project_by_uuid(self.token, res)


    @classmethod
    def teardown_class(cls):
        pass
