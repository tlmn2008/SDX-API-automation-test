# -*- coding: utf-8 -*-
import time

from send_check.apis import api_project_m
from send_check.apis import api_compose
from send_check.req_send import send_req
from utilities.db_operation import query_from_mongodb
from utilities.sshConnection import SSHConnection
from utilities import logger
from configurations import config


def create_project(token, project_name='auto test project', description='automation test', is_template=False, users=None, groups=None, model_id=''):
    '''
    自动创建项目
    :param token:
    :param project_name:
    :param description:
    :param is_template: 是否创建为模板
    :param users: 协作用户
    :param groups: 协作用户组
    :param model_id: 基于模板创建项目时，源模板项目uuid
    :return:
    '''
    req = api_project_m.get_create_new_project_req(token=token, project_name=project_name, description=description,
                                                   is_template=is_template, users=users, groups=groups, model_id=model_id)
    res = send_req.send_request(req, '201')
    return res['uuid']


def delete_project_by_uuid(token, uuid, result_code='204'):
    """
    按uuid删除项目
    :param token:
    :param uuid:
    :return:
    """
    req = api_project_m.get_delete_project_req(token=token, uuid=uuid)
    res = send_req.send_request(req, result_code)
    return res


def entry_project_by_uuid(token, uuid):
    '''
    进入项目页面
    :param token:
    :param uuid:
    :return:
    '''
    req = api_project_m.get_entry_project_req(token=token, uuid=uuid)
    res = send_req.send_request(req)
    return res


def create_project_task(token, task_name, project_id, task_type, image_id, resource_config,
                        description='automation test task'):
    """
    自动创建新任务
    :param token:
    :param task_name:
    :param project_id:
    :param task_type:
    :param image_id:
    :param resource_config:
    :param description:
    :return: 新任务的uuid
    """
    req = api_project_m.get_create_task_req(token=token, task_name=task_name, task_type=task_type, project_id=project_id,
                                            image_id=image_id, resource_config=resource_config, description=description)
    res = send_req.send_request(req, '201')
    return res['uuid']


def start_project_task(token, task_uuid):
    """
    启动任务
    :param token:
    :param task_uuid:
    :return: uuid
    """
    req = api_project_m.get_start_task_req(token=token, task_id=task_uuid)
    res = send_req.send_request(req, '202')
    return res['uuid']


def stop_project_task(token, task_uuid):
    """
    停止任务
    :param token:
    :param task_uuid:
    :return:
    """
    req = api_project_m.get_stop_task_req(token=token, task_id=task_uuid)
    res = send_req.send_request(req, '202')
    return res['uuid']


def get_project_task_info_by_uuid(token, task_uuid):
    """
    根据uuid获取任务信息
    :param token:
    :param task_uuid:
    :return:
    """
    req = api_project_m.get_task_info_req(token=token, task_id=task_uuid)
    res = send_req.send_request(req, '200')
    return res


def get_project_task_status_by_uuid(token, task_uuid):
    """
    根据uuid获取任务的运行状态
    :param token:
    :param task_uuid:
    :return:
    """
    info = get_project_task_info_by_uuid(token, task_uuid)
    if not info:
        logger.log_warning('Got None task info.')
        return False
    return info['state']


def check_project_task_status(token, task_uuid, expected_status, timeout):
    """
    根据task uuid查询状态. 在timeout时间内检查任务是否达到期望状态
    :param token:
    :param task_uuid:
    :param expected_status:
    :param timeout:
    :return:
    """
    pass


def delete_project_task_by_uuid(token, task_uuid):
    """
    根据uuid删除任务
    :param token:
    :param task_uuid:
    :return:
    """
    req = api_project_m.get_delete_task_req(token=token, task_id=task_uuid)
    send_req.send_request(req, '204')



def query_pod_ids_by_task_id(task_uuid):

    pod_ids = query_from_mongodb(db_name='project-manager', collection_name='tasks',
                                 query_conditions={'1_id': task_uuid}, columns={'pods': 1, '_id': 0})
    if len(pod_ids) != 0:
        return pod_ids
    else:
        logger.log_debug('Got empty result.')
        return False


def check_pod_status(pod_ids, expected_status='Running', timeout=30):
    """
    根据pod id检查pod的状态 (此方法暂时不使用）
    :param pod_ids: str或list
    :param expected_status:
    :param timeout: 检查的次数，每隔一秒检查一次（kubectl命令需要时间，因此总时间大于timeout*1秒），如果所有pod达到期望状态，则提前返回
    :return: bool
    """

    if not isinstance(pod_ids, (list, str)):
        logger.log_error('The pod_id type is wrong, expect list or string, but got {}'.format(type(pod_ids)))
        return False
    if isinstance(pod_ids, str):
        pod_ids = list(pod_ids)

    match_status_pod_list = []
    host = config.ssh_conn_info['host']
    port = config.ssh_conn_info['port']
    user = config.ssh_conn_info['user']
    passwd = config.ssh_conn_info['passwd']
    conn = SSHConnection(host, port, user, passwd)
    command = "kubectl get pod {} -n skydiscovery-app|awk '{print $3}'|grep -v STATUS"

    while timeout > 0:
        timeout = timeout - 1
        for pod_id in pod_ids:
            pod_status = conn.exec_command(command.format(pod_id))

            if pod_status == expected_status:
                logger.log_debug("Pod {}'s status is {}, = {}.".format(pod_id, pod_status, expected_status))
                if pod_id not in match_status_pod_list:
                    match_status_pod_list.append(pod_id)
            else:
                logger.log_debug("Pod {}'s status is {}, != {}.".format(pod_id, pod_status, expected_status))
                if pod_id in match_status_pod_list:
                    match_status_pod_list.remove(pod_id)

        if len(match_status_pod_list) == len(pod_ids):
            logger.log_debug('The pod(s) status match to the expectation.')
            conn.close()
            return True
        time.sleep(1)

    logger.log_error('The pod(s) status do not match to the expectation.')
    conn.close()
    return False


def get_project_list(token, name=None, project_type=None, start=1,
                     count=1000, order='desc', order_by='createdAt'):
    """
    获取project列表
    Args:
        token: 用户token
        name: project名称
        project_type: project类型,如public
        start: 起始数
        count: 截至数
        order: 排序方式, 例如desc
        order_by: 排序依据

    Returns:
        project_list: project列表

    """
    req = api_compose.get_compose_project_list_req(
        token, name=name, project_type=project_type, start=start,
        count=count, order=order, order_by=order_by)

    project_list = send_req.send_request(req)

    return project_list
