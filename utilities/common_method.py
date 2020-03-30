# -*- coding: utf-8 -*-
import base64
import json
from utilities.sshConnection import SSHConnection
from configurations import config
from utilities import logger

def get_uuid_from_token(token):
    '''
    从token中获取uuid信息
    :param token:
    :return:
    '''
    payload = token.split('.')[1].encode('utf-8')
    rem = len(payload) % 4
    if rem > 0:
        payload += b'=' * (4 - rem)
    data = base64.urlsafe_b64decode(payload)
    s = json.loads(data.decode('utf-8'))['identity']
    uuid = s['uuid']
    return uuid


def remove_None_value_elements(input_dict):
    """
    去除字典中值为None的元素
    :param input_dict:
    :return: new dict
    """
    if type(input_dict) is not dict:
        return None
    result = {}
    for key in input_dict:
        tmp = {}
        if input_dict[key] is not None:
            if type(input_dict[key]).__name__ == 'dict':
                tmp.update({key: remove_None_value_elements(input_dict[key])})
            else:
                tmp.update({key: input_dict[key]})
        result.update(tmp)
    return result

def check_files_folders_exist(conn_info=config.ssh_conn_info, input_path_list=None, isExistCheck=True):
    """
    检查文件和文件夹是否存在
    :param ssh_conn_info {ip,port,user,passwrd}:
    :param input_path_list（绝对路径）:
    :param isExistCheck（绝对路径）: True(存在检查)/False(不存在检查)
    :return: False/True
    """
    path_list = [] if input_path_list is None else input_path_list
    conn = SSHConnection(conn_info['host'], conn_info['port'], conn_info['user'], conn_info['passwd'])
    for path_item in path_list:
        command_foler_check = 'ls {}'
        isExist = conn.exec_command(command_foler_check.format(path_item)).decode('utf-8')

        if isExistCheck is True:
            if 'No such file or directory' in isExist:
                logger.log_error('Folder {} is not exist'.format(path_item))
                conn.close()
                return False
        elif isExistCheck is False:
            if 'No such file or directory' not in isExist:
                logger.log_error('Folder {} is not exist'.format(path_item))
                conn.close()
                return False
    conn.close()
    return True