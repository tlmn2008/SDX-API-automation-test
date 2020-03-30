#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# @Time    : 2/13/2020 1:54 PM
# @Author  : Xin He
# @File    : test_user_manager.py
# @Desc    :

import pytest

from test_cases import base
from configurations import config
from send_check.req_send import send_user_m_req
from send_check.req_send import send_project_m_req
from utilities import date_time


class TestUserManager(base.Base):
    @classmethod
    def setup_class(cls):
        super(TestUserManager, cls).setup_class(logger_name='user_manager')
        cls.token = send_user_m_req.get_token_simple(
            username=config.user_sysadmin,
            userpwd=config.user_passwd_sysadmin)

    @pytest.mark.smoke
    def test_skte_t1066_create_edit_delete_user(self):
        """
        该用例包含T1066，T1065, T1078，T1079.
        测试步骤：
        1. 创建用户
        2. 查找新建用户
        3. 编辑用户
        4. 使用新用户创建多种任务
        5. 删除用户
        6. 检查共享任务是否存在

        """
        # 1.创建新用户
        uuid = send_user_m_req.create_user(self.token,
                                           username=config.user_name_tmp,
                                           fullname=config.user_full_name_tmp,
                                           password=config.user_passwd_tmp)

        # 2. 查找新建用户
        user_uuid = send_user_m_req.get_uuid_by_username(
            self.token, username=config.user_name_tmp)
        assert user_uuid == uuid

        # 3.编辑用户
        user_update = send_user_m_req.edit_user(self.token, uuid,
                                                fullname='更新用户全名')
        assert user_update['fullName'] == '更新用户全名'

        # 4. 新用户登录创建多种任务
        # TODO: 补充创建共享image，文件等项目
        tmp_token = send_user_m_req.get_token_simple(config.user_name_tmp,
                                                     config.user_passwd_tmp)
        users = send_user_m_req.get_uuid_list_by_users(
            token=tmp_token, users=[config.user_name_a])
        send_project_m_req.create_project(tmp_token, project_name='T1079',
                                          users=users)

        # 5.删除新用户
        send_user_m_req.delete_user(self.token, uuid=uuid)
        uuid = send_user_m_req.get_uuid_by_username(
            self.token, username=config.user_name_tmp)

        assert uuid == ''

        # 6. 使用被共享用户登录, 查看被删除用户共享任务是否存在
        # TODO: 等待SDX功能完善, 修改判断条件
        token = send_user_m_req.get_token_simple(config.user_name_a,
                                                 config.user_passwd_a)
        project_list = send_project_m_req.get_project_list(token)
        if project_list['total'] > 0:
            items = project_list['data']['items']
            for item in items:
                if item['owner'].get('username') == config.user_name_tmp:
                    assert False
        assert True

    def test_skte_t1074_active_user(self):
        """
        该用例包含T1074, T1075.
        测试步骤：
        1. 创建用户
        2. 激活用户
        3. 新用户登录
        4. 取消激活用户
        5. 用户再次登录
        6. 删除用户

        """
        # 1.创建未激活用户
        uuid = send_user_m_req.create_user(self.token,
                                           username=config.user_name_tmp,
                                           fullname=config.user_full_name_tmp,
                                           password=config.user_passwd_tmp,
                                           active=False)

        # 2.激活用户
        user_update = send_user_m_req.edit_user(self.token, uuid,
                                                active=True)
        assert user_update['isActive'] is True

        # 3. 新用户登录, 并查看用户详细
        tmp_token = send_user_m_req.get_token_simple(config.user_name_tmp,
                                                     config.user_passwd_tmp)
        user_detail = send_user_m_req.get_user_detail(tmp_token, uuid)
        assert user_detail

        # 4. 取消激活用户
        user_update = send_user_m_req.edit_user(self.token, uuid,
                                                active=False)
        assert user_update['isActive'] is False

        # 5. 用户再次登录
        message = send_user_m_req.get_token_simple(config.user_name_tmp,
                                                   config.user_passwd_tmp,
                                                   return_code='403')
        assert message == 'user disabled'

        # 6. 删除用户
        send_user_m_req.delete_user(self.token, uuid=uuid)

    @pytest.mark.parametrize("test_data",
                             [{'days': 1}, {'weeks': 1}, {'months': 1},
                              {'months': 3}, {'months': 6}, {'years': 1},
                              {'years': 99}])
    def test_skte_t1072_create_user_with_diff_expire(self, test_data):
        """
        创建用户, 设置不同的有效期.
        测试步骤：
        1. 创建用户, 有效期为1天, 1周, 1月, 3月, 6月, 1年, 99年
        2. 新用户登录, 查看有效期设置
        3. 删除用户

        """

        expires = date_time.get_delta_datetime(**test_data)

        # 1.创建用户
        uuid = send_user_m_req.create_user(self.token,
                                           username=config.user_name_tmp,
                                           fullname=config.user_full_name_tmp,
                                           password=config.user_passwd_tmp,
                                           expires=expires)

        # 2. 新用户登录, 并查看用户详细
        tmp_token = send_user_m_req.get_token_simple(config.user_name_tmp,
                                                     config.user_passwd_tmp)
        user_detail = send_user_m_req.get_user_detail(tmp_token, uuid)
        assert user_detail['expiresAt'] == expires

        # 3. 删除用户
        send_user_m_req.delete_user(self.token, uuid=uuid)

    def test_skte_t4342_reset_password(self):
        """
        重置用户密码
        测试步骤：
        1. 创建用户
        2. 重置密码
        3. 使用新密码登录
        4. 删除用户

        """
        # 1.创建用户
        uuid = send_user_m_req.create_user(self.token,
                                           username=config.user_name_tmp)

        # 2. 重置密码
        resp = send_user_m_req.reset_password(self.token, user_uuid=uuid)

        # 3. 新用户登录, 并查看用户详细
        tmp_token = send_user_m_req.get_token_simple(config.user_name_tmp,
                                                     userpwd=resp['password'])
        user_detail = send_user_m_req.get_user_detail(tmp_token, uuid)
        assert user_detail['uuid'] == uuid

        # 4. 删除用户
        send_user_m_req.delete_user(self.token, uuid=uuid)

    def test_skte_t4343_change_password(self):
        """
        修改用户密码
        测试步骤：
        1. 创建用户
        2. 登录后修改密码
        3. 使用新密码登录
        4. 删除用户

        """
        new_password = '123456'

        # 1.创建用户
        uuid = send_user_m_req.create_user(self.token,
                                           username=config.user_name_tmp,
                                           password=config.user_passwd_tmp)

        # 2. 登录修改密码
        token = send_user_m_req.get_token_simple(username=config.user_name_tmp,
                                                 userpwd=config.user_passwd_tmp)
        resp = send_user_m_req.change_password(
            token, user_uuid=uuid, old_password=config.user_passwd_tmp,
            password=new_password)
        assert resp['uuid'] == uuid

        # 3. 使用新密码登录, 并查看用户详细
        token = send_user_m_req.get_token_simple(config.user_name_tmp,
                                                 userpwd=new_password)
        user_detail = send_user_m_req.get_user_detail(token, uuid)
        assert user_detail['uuid'] == uuid

        # 4. 删除用户
        send_user_m_req.delete_user(self.token, uuid=uuid)

    @classmethod
    def teardown_class(cls):
        pass
