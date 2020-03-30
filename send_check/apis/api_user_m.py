# -*- coding: utf-8 -*-
from urllib.parse import urljoin

from configurations import config
from send_check.apis.api_template import ApiTemplate


def get_create_user_req():
    req = ApiTemplate()
    sub_path = "user-manager/api/v1/users_manager"
    req.url = "{}{}".format(config.base_url, sub_path)
    req.headers = {"Content-Type: application/json"}
    return req


def get_user_login_req(username=config.user_name_a, userpwd=config.user_passwd_a):
    req = ApiTemplate()
    sub_path = "/user-manager/api/v1/tokens/"
    req.url = urljoin(config.base_url, sub_path)
    req.method = 'post'
    req.body = {
        "grantType": "password",
        "username": username,
        "password": userpwd
    }
    return req


def get_create_user_group_req(token, group_name, roles, permissions=None):
    req = ApiTemplate()
    sub_path = "/user-manager/api/v1/groups/"
    req.url = urljoin(config.base_url, sub_path)
    req.method = 'post'
    req.headers = {'Authorization': token}
    req.body = {
        "name": group_name,
        "roles": roles,
        "permissions": [] if permissions is None else permissions
    }
    return req


def modify_user_group_req(token, group_uuid, new_group_name=None, roles=None, permissions=None):
    req = ApiTemplate()
    sub_path = "/user-manager/api/v1/groups/{}".format(group_uuid)
    req.url = urljoin(config.base_url, sub_path)
    req.method = 'patch'
    req.headers = {'Authorization': token}
    req.body = {
        "name": new_group_name,
        "roles": roles,
        "permissions": permissions
    }
    # 如果值是None说明不修改这个值，从Body中剔除
    if new_group_name is None:
        req.body.pop('name')
    if roles is None:
        req.body.pop('roles')
    if permissions is None:
        req.body.pop('permissions')

    return req


def get_delete_user_group_req(token, group_uuid):
    path = '/user-manager/api/v1/groups/{}'.format(group_uuid)
    req = ApiTemplate()
    req.url = urljoin(config.base_url, path)
    req.method = 'delete'
    req.headers = {'Authorization': token}
    return req


def get_query_user_roles_req(token):
    path = '/user-manager/api/v1/roles/'
    req = ApiTemplate()
    req.url = urljoin(config.base_url, path)
    req.method = 'get'
    req.headers = {'Authorization': token}
    return req


def get_user_group_list_req(token):
    path = '/user-manager/api/v1/groups/'
    req = ApiTemplate()
    req.url = urljoin(config.base_url, path)
    req.method = 'get'
    req.headers = {'Authorization': token}
    return req


def get_user_group_detail_req(token, group_uuid):
    path = '/user-manager/api/v1/groups/{}'.format(group_uuid)
    req = ApiTemplate()
    req.url = urljoin(config.base_url, path)
    req.method = 'get'
    req.headers = {'Authorization': token}
    return req


def create_user_req(token, username="new_tester",
                    fullname="new_tester@iluvarta.ai",
                    password="testSDX@001", permissions=None,
                    active=True, roles=None, groups=None,
                    expires="2050-12-31T00:00:00.000Z"):

    req = ApiTemplate()
    sub_path = "user-manager/api/v1/users"
    req.url = "{}{}".format(config.base_url, sub_path)
    req.headers = {'Authorization': token}
    req.method = 'post'
    req.body = {
        "username": username,
        "fullName": fullname,
        "permissions": permissions if permissions else [],
        "isActive": active,
        "roles": roles if roles else [],
        "groups": groups if groups else [],
        "password": password,
        "expiresAt": expires
    }

    return req


def delete_user_req(token, uuid):
    req = ApiTemplate()
    sub_path = "user-manager/api/v1/users/{}".format(uuid)
    req.url = "{}{}".format(config.base_url, sub_path)
    req.headers = {'Authorization': token}
    req.method = 'delete'

    return req


def get_user_detail_req(token, uuid):
    req = ApiTemplate()
    sub_path = "user-manager/api/v1/users/{}".format(uuid)
    req.url = "{}{}".format(config.base_url, sub_path)
    req.headers = {'Authorization': token, "Content-Type": "application/json"}
    req.method = 'get'

    return req


def edit_user_req(token, uuid, fullname, active,
                  roles, groups, expires):

    req = ApiTemplate()
    sub_path = "user-manager/api/v1/users/{}".format(uuid)
    req.url = "{}{}".format(config.base_url, sub_path)
    req.headers = {'Authorization': token}
    req.method = 'patch'
    req.body = {
        "fullName": fullname,
        "groups": groups,
        "roles": roles,
        "permissions": [],
        "isActive": active,
        "uuid": uuid,
        "expiresAt": expires
    }

    return req


def add_user_to_groups_req(token, uuid, groups):
    req = ApiTemplate()
    sub_path = "user-manager/api/v1/users/{}".format(uuid)
    req.url = "{}{}".format(config.base_url, sub_path)
    req.headers = {'Authorization': token, "Content-Type": "application/json"}
    req.method = 'patch'
    req.body = {"groups": groups}

    return req


def reset_password_req(token, uuid):
    req = ApiTemplate()
    sub_path = "user-manager/api/v1/users/{}/password/reset".format(uuid)
    req.url = "{}{}".format(config.base_url, sub_path)
    req.headers = {'Authorization': token, "Content-Type": "application/json"}
    req.method = 'post'

    return req


def change_password_req(token, uuid, old_password, password):
    req = ApiTemplate()
    sub_path = "user-manager/api/v1/users/{}".format(uuid)
    req.url = "{}{}".format(config.base_url, sub_path)
    req.headers = {'Authorization': token, "Content-Type": "application/json"}
    req.method = 'patch'
    req.body = {
        "oldPassword": old_password,
        "password": password
    }

    return req
