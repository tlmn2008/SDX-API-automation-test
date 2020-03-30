# -*- coding: utf-8 -*-

import pytest

from configurations import config
from utilities import logger
from send_check.req_send import send_user_m_req
from test_cases import base


class TestUserGroup(base.Base):
    @classmethod
    def setup_class(cls):
        super(TestUserGroup, cls).setup_class(logger_name='user_group')
        cls.token = send_user_m_req.get_token_simple(config.user_sysadmin, config.user_passwd_sysadmin)

    def test_SKTE_T1081_create_user_group(self):
        # 创建用户组并且删除. 同时实现了用例SKTE-T1085, SKTE-T1083, SKTE-T1080

        # 获取user_role角色的uuid
        user_role_uuid = send_user_m_req.fetch_user_role_uuid_by_role_name(self.token, config.user_role_name)
        group_name = 'group_T1081'
        # 创建用户组
        if user_role_uuid:
            group_uuid = send_user_m_req.create_user_group(self.token, group_name, [user_role_uuid])
        else:
            # 找不到角色的uuid
            assert False
        # 修改用户组
        new_group_name = group_name + '_new'
        # 获取admin_role角色的uuid
        admin_role_uuid = send_user_m_req.fetch_user_role_uuid_by_role_name(self.token, config.admin_role_name)
        new_role = [user_role_uuid, admin_role_uuid]
        send_user_m_req.modify_user_group(self.token, group_uuid, new_group_name, new_role)

        # 检查修改结果
        user_group_details = send_user_m_req.get_user_group_detail(self.token, group_uuid)
        if user_group_details['name'] != new_group_name:
            logger.log_error('The group name is wrong, it should be {}, but it is {}'.format(
                new_group_name, user_group_details['name']))
            assert False
        if user_group_details['roles'] != new_role:
            logger.log_error('The group role is wrong, it should be {}, but it is {}'.format(
                new_role, user_group_details['roles']))
            assert False

        # 删除刚刚创建的用户组
        send_user_m_req.delete_user_group(self.token, group_uuid)
        # 确认用户组已被删除
        if send_user_m_req.fetch_user_group_uuid_by_group_name(self.token, group_name):
            logger.log_error('The user group should be deleted, but it is still existed.')
            assert False

    @pytest.mark.smoke
    def test_skte_t1076_add_user_to_group(self):
        """
        该用例包含T1076, T1077.
        测试步骤：
        1. 创建用户组, 用户组角色包含user_role, admin_role
        2. 创建用户，角色为user_role
        3. 将新建用户添加到用户组
        4. 用户登录, 有admin权限
        5. 删除用户组

        """

        username = config.user_name_tmp + '_t1076'
        user_group = 'user_group_t1076'
        admin_group = 'admin_group_t1076'

        user_role_uuid = send_user_m_req.fetch_user_role_uuid_by_role_name(
            self.token, config.user_role_name)
        admin_role_uuid = send_user_m_req.fetch_user_role_uuid_by_role_name(
            self.token, config.admin_role_name)

        # 1. 创建用户组
        user_group = send_user_m_req.create_user_group(self.token, user_group,
                                                       role=[user_role_uuid])
        admin_group = send_user_m_req.create_user_group(
            self.token, admin_group, role=[user_role_uuid, admin_role_uuid])

        # 2. 新建用户, 该用户没有删除用户组权限
        user_uuid = send_user_m_req.create_user(
            self.token, username=username, fullname=config.user_full_name_tmp,
            password=config.user_passwd_tmp)

        token = send_user_m_req.get_token_simple(username,
                                                 userpwd=config.user_passwd_tmp)
        send_user_m_req.delete_user_group(token, user_group,
                                          return_code='403')

        # 3. 将用户添加到2个用户组
        resp = send_user_m_req.add_user_to_groups(
            self.token, user_uuid, groups=[user_group, admin_group])
        assert sorted(resp['groups']) == sorted([user_group, admin_group])

        # 4. 新用户有删除用户组权限
        send_user_m_req.delete_user_group(token, user_group)
        send_user_m_req.delete_user_group(self.token, admin_group)

        # 5. 删除创建的用户组和用户
        send_user_m_req.delete_user(self.token, uuid=user_uuid)

    @pytest.mark.smoke
    def test_skte_t1082_add_roles_to_group(self):
        """
        该用例包含T1082, T1084, T1086, T1087
        测试步骤：
        1. 创建用户组, 用户组角色包含user_role, admin_role
        2. 添加多个用户到用户组，用户有admin权限
        3. 查看组内成员列表
        4. 修改用户组，去除admin_role
        5. 用户登录, 只有user_role权限
        6. 删除用户组

        """

        group_name = 'group_t1082'
        new_group_name = 'new_group_t1082'

        user_role_uuid = send_user_m_req.fetch_user_role_uuid_by_role_name(
            self.token, config.user_role_name)
        admin_role_uuid = send_user_m_req.fetch_user_role_uuid_by_role_name(
            self.token, config.admin_role_name)

        # 1. 创建用户组
        user_group = send_user_m_req.create_user_group(self.token, group_name,
                                                       role=[user_role_uuid,
                                                             admin_role_uuid])
        user_a_uuid = send_user_m_req.get_uuid_by_username(self.token,
                                                           config.user_name_a)
        user_b_uuid = send_user_m_req.get_uuid_by_username(self.token,
                                                           config.user_name_b)
        # 2. 将用户添加到用户组
        resp = send_user_m_req.add_user_to_groups(
            self.token, user_a_uuid, groups=[user_group])
        assert resp['groups'] == [user_group]

        resp = send_user_m_req.add_user_to_groups(
            self.token, user_b_uuid, groups=[user_group])
        assert resp['groups'] == [user_group]

        # 3. 查看用户组列表，用户有创建用户组权限
        token = send_user_m_req.get_token_simple(username=config.user_name_a,
                                                 userpwd=config.user_passwd_a)
        group_detail = send_user_m_req.get_user_group_detail(token, user_group)
        assert sorted(group_detail['users']) == sorted([user_a_uuid,
                                                        user_b_uuid])
        tmp_group = send_user_m_req.create_user_group(
            token, group_name=new_group_name, role=[user_role_uuid])

        # 4. 修改用户组, 去除admin角色
        send_user_m_req.modify_user_group(self.token, user_group,
                                          roles=[user_role_uuid])

        # 5. 用户没有创建删除用户组权限
        send_user_m_req.delete_user_group(token, group_uuid=tmp_group,
                                          return_code='403')

        # 6. 使用admin删除创建的用户组
        send_user_m_req.delete_user_group(self.token, tmp_group)
        send_user_m_req.delete_user_group(self.token, user_group)

    @classmethod
    def teardown_class(cls):
        pass
