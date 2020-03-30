# -*- coding: utf-8 -*-
import pytest
from test_cases import base
from utilities import logger
from send_check.req_send import send_user_m_req, send_project_m_req, send_image_m_req
from configurations import config


class TestCreateProject(base.Base):
    @classmethod
    def setup_class(cls):
        super(TestCreateProject, cls).setup_class(logger_name='container_dev')
        cls.token = send_user_m_req.get_token_simple()

    @pytest.mark.skip(reason="SDX can not run container dev task now.")
    def test_SKTE_T3600_container_dev_task(self):
        # 因环境问题创建任务时报错，不能继续调试

        # 获取image的uuid
        image_id = send_image_m_req.get_image_uuid_by_image_name(self.token, config.container_dev_tf114_py36_cpu_image)
        # 创建项目
        project_id = send_project_m_req.create_project(self.token, project_name='project for SKTE_T3600')
        # 创建任务
        task_uuid = send_project_m_req.create_project_task(self.token, task_name='container dev task', project_id=project_id,
                                                           task_type='CONTAINER_DEV', image_id=image_id, resource_config=None)
        logger.log_debug('new task id is {}'.format(task_uuid))
        # 启动任务
        started_task_uuid = send_project_m_req.start_project_task(self.token, task_uuid)
        assert False if task_uuid != started_task_uuid else True
        # 查询任务状态
        start_status = send_project_m_req.get_project_task_status_by_uuid(self.token, task_uuid)
        logger.log_debug('task status after starting is {}'.format(start_status))
        # 停止任务
        # send_project_m_req.stop_project_task(self.token, task_uuid)
        # # 查询任务状态
        # stop_status = send_project_m_req.get_project_task_status_by_uuid(self.token, task_uuid)
        # logger.log_debug('task status after stopping is {}'.format(stop_status))
        # # 删除任务
        # send_project_m_req.delete_project_task_by_uuid(self.token, task_uuid)
        # # 删除项目
        # send_project_m_req.delete_project_by_uuid(self.token, project_id)

    @classmethod
    def teardown_class(cls):
        pass
