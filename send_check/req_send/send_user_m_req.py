# -*- coding: utf-8 -*-

from configurations import config
from send_check.apis import api_user_m, api_compose
from send_check.req_send import send_req
from utilities import logger
from utilities import date_time


def get_token_simple(username=config.user_name_a, userpwd=config.user_passwd_a,
                     return_code='200'):
    req = api_user_m.get_user_login_req(username, userpwd)
    resp = send_req.send_request(req, result_code=return_code)
    if return_code == '200':
        token = f"Bearer {resp.get('accessToken')}"
        return token
    else:
        return resp.get("message", '')


def get_uuid_by_username(token, username):
    req = api_compose.get_compose_user_list_req(token=token, username=username)
    res = send_req.send_request(req)
    if res['total'] == 0:
        logger.log_debug("Can not find user {}".format(username))
    else:
        for user in res['users']:
            if user['username'] == username:
                return user['uuid']

    return ''


def get_user_role_list(token):
    """
    获取所有角色列表
    :param token:
    :return:
    """
    req = api_user_m.get_query_user_roles_req(token=token)
    res = send_req.send_request(req)
    if res['total'] == 0:
        logger.log_debug("Notice, the user role list is Empty!")
        return None
    else:
        return res['roles']


def fetch_user_role_uuid_by_role_name(token, role_name):
    """
    查询指定角色的uuid
    :param token:
    :param role_name:
    :return:
    """
    user_role_list = get_user_role_list(token)
    if user_role_list:
        for role in user_role_list:
            if role['name'] == role_name:
                return role['uuid']
        logger.log_error('Can not find user role uuid for {}'.format(role_name))
        return False
    else:
        return False


def create_user_group(token, group_name, role, permission=None, result_code='201'):
    """
    创建用户组
    :param token:
    :param group_name:
    :param role: list
    :param permission: list
    :param result_code:
    :return:
    """
    req = api_user_m.get_create_user_group_req(token, group_name, role, permission)
    res = send_req.send_request(req, result_code)
    return res['uuid']


def modify_user_group(token, group_uuid, new_group_name=None, roles=None, permissions=None):
    """
    修改用户组
    :param token:
    :param group_uuid:
    :param new_group_name:
    :param roles:
    :param permissions:
    :return:
    """
    req = api_user_m.modify_user_group_req(token, group_uuid, new_group_name, roles, permissions)
    res = send_req.send_request(req)


def delete_user_group(token, group_uuid, return_code='204'):
    """
    删除用户组
    :param token:
    :param group_uuid:
    :param return_code:
    :return:
    """
    req = api_user_m.get_delete_user_group_req(token, group_uuid)
    res = send_req.send_request(req, return_code)


def get_user_group_list(token):
    """
    查询所有用户组
    :param token:
    :return:
    """
    req = api_user_m.get_user_group_list_req(token)
    res = send_req.send_request(req)
    if res['total'] == 0:
        logger.log_debug("Notice, the user group list is Empty!")
        return None
    else:
        return res['groups']


def fetch_user_group_uuid_by_group_name(token, group_name):
    """
    查询指定用户组的uuid
    :param token:
    :param group_name:
    :return:
    """
    user_group_list = get_user_group_list(token)
    if user_group_list:
        for group in user_group_list:
            if group['name'] == group_name:
                return group['uuid']
        logger.log_error('Can not find user role uuid for {}'.format(group_name))
        return False


def get_user_group_detail(token, group_uuid):
    """
    获取指定用户组详细信息
    :param token:
    :param group_uuid:
    :return:
    """
    req = api_user_m.get_user_group_detail_req(token, group_uuid)
    res = send_req.send_request(req)
    return res


def create_user(token, username='new_tester', fullname='new_tester@iluvatar.ai',
                password='testSDX@001', permissions=None, active=True,
                roles=None, groups=None, expires="2050-12-31T00:00:00.000Z"):
    """
    创建新用户
    Args:
        token: 管理员用户token
        username: 新用户名称
        fullname: 新用户全名
        password: 新用户密码
        permissions: 新用户权限列表，默认[]
        active: 是否激活，默认True
        roles: 拥有角色列表，默认[]
        groups: 所属组列表, 默认[]
        expires: 过期时间，默认[]

    Returns: uuid

    """
    if not roles:
        role_uuid = fetch_user_role_uuid_by_role_name(
            token, role_name=config.user_role_name)
        roles = [role_uuid]

    req = api_user_m.create_user_req(token, username, fullname,
                                     password, permissions, active,
                                     roles, groups, expires)
    resp = send_req.send_request(req, result_code='201')
    uuid = resp.get('uuid', '')

    logger.log_info(f"uuid is: {uuid}.")

    if len(uuid) == 0:
        logger.log_error(f"uuid is error.")
        assert False

    return uuid


def delete_user(token, uuid, result_code='204'):
    """
    删除用户
    Args:
        token: 管理员用户token
        uuid: 用户uuid
        result_code: 期待返回码
    Returns:

    """

    req = api_user_m.delete_user_req(token, uuid)
    resp = send_req.send_request(req, result_code=result_code)
    logger.log_info(f"resp is: {resp}.")


def edit_user(token, uuid, **kwargs):
    """
    编辑用户
    Args:
        token: 管理员用户token
        uuid: 用户uuid
        **kwargs: 包含可选参数fullname,
                  active, roles, groups, expires
    Returns:
        resp: updated user info

    """

    res = get_user_detail(token, uuid)

    fullname = kwargs['fullname'] if kwargs.get('fullname') else res['fullName']
    if kwargs.get('active') is not None:
        active = kwargs['active']
    else:
        active = res['isActive']
    roles = kwargs['roles'] if kwargs.get('roles') else res['roles']
    groups = kwargs['groups'] if kwargs.get('groups') else res['groups']

    if kwargs.get('expires'):
        expires = kwargs.get('expires')
    else:
        # 默认有效期一年
        expires = date_time.get_delta_datetime(years=1)

    req = api_user_m.edit_user_req(token, uuid, fullname,
                                   active, roles, groups, expires)
    resp = send_req.send_request(req)

    return resp


def get_user_detail(token, uuid):
    req = api_user_m.get_user_detail_req(token=token, uuid=uuid)
    resp = send_req.send_request(req)

    logger.log_info(f'user detail is: {resp}.')

    return resp


def get_uuid_list_by_users(token, users=None):
    """
    根据用户列表返回uuid列表
    Args:
        token: 用户token
        users: 用户列表, 例如['userA', 'userB']

    Returns:
        users_uuid: 用户uuid列表

    """
    users_uuid = []
    if users:
        for user in users:
            users_uuid.append(get_uuid_by_username(token, username=user))

    return users_uuid


def get_uuid_list_by_groups(token, groups=None):
    """
    根据用户列表返回uuid列表
    Args:
        token: 用户token
        groups: 用户组列表, 例如['groupA', 'groupB']

    Returns:
        groups_uuid: 用户组uuid列表

    """
    groups_uuid = []
    if groups:
        for group in groups:
            groups_uuid.append(fetch_user_group_uuid_by_group_name(token,
                                                                   group))

    return groups_uuid


def add_user_to_groups(token, user_uuid, groups):
    """
    add user to groups
    Args:
        token: user token
        user_uuid: user uuid
        groups: group uuid list

    Returns:
        resp

    """
    req = api_user_m.add_user_to_groups_req(token, user_uuid, groups)
    resp = send_req.send_request(req)

    return resp


def reset_password(token, user_uuid):
    """
    Reset user password
    Args:
        token: admin user token
        user_uuid: user uuid

    Returns:
        resp

    """

    req = api_user_m.reset_password_req(token, user_uuid)
    resp = send_req.send_request(req)

    return resp


def change_password(token, user_uuid, old_password, password):
    """
    Reset user password
    Args:
        token: admin user token
        user_uuid: user uuid
        old_password: old password
        password: new password

    Returns:
        resp

    """

    req = api_user_m.change_password_req(token, user_uuid,
                                         old_password, password)
    resp = send_req.send_request(req)

    return resp
