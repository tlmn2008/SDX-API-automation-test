# -*- coding: utf-8 -*-
import json
import time

from configurations import config
from send_check.req_send.send_storage_m_req import get_user_ceph_path
from utilities import logger
from utilities.db_operation import delete_from_mongodb, insert_to_mongodb, query_from_mongodb
from utilities.sshConnection import SSHConnection


def get_auto_test_user_uuid():
    """
    收集所有自动化测试创建的用户的uuid
    :return:
    """
    uuid_list = []
    users_uuid = query_from_mongodb(db_name='user-manager', collection_name='users',
                                    query_conditions={'username': {"$regex": "^Teng.*"}}, columns={'_id': 1})
    for uuid in users_uuid:
        uuid_list.append(str(uuid['_id']))
    return uuid_list


def clean_volumes_from_disk(conn_info=config.ssh_conn_info):
    """
    删除自动化测试用户的user volume，以及所有的pod,project volume
    :param conn_info:
    :return:
    """

    host = conn_info['host']
    port = conn_info['port']
    user = conn_info['user']
    passwd = conn_info['passwd']
    conn = SSHConnection(host, port, user, passwd)

    conn.exec_command('rm -rf /SkyDiscovery/cephfs/data/pod/volume-*')
    conn.exec_command('rm -rf /SkyDiscovery/cephfs/data/project/volume-*')
    # 目前不会重建测试账户，不要清理此账户的volume
    # # 查出所有自动化测试用启的uuid
    # user_uuids = get_auto_test_user_uuid()
    # # 根据用户uuid查询volume _id
    # volume_uuid = query_from_mongodb(db_name='storage-manager', collection_name='volumes',
    #                                  query_conditions={'owner_id': {"$in": user_uuids}}, columns={'_id': 1})
    # # 从磁盘上删除volume
    # for uuid in volume_uuid:
    #     conn.exec_command('rm -rf /SkyDiscovery/cephfs/data/user/volume-{}'.format(str(uuid['_id'])))

    time.sleep(5)
    conn.close()
    print('success')


def clean_db_data_manager():
    data_source = {'data_source': {"name": {"$regex": "^autoT.*"}}}
    data_set = {'data_set': {"name": {"$regex": "^autoT.*"}}}
    data_set_tag = {'data_set_tag': {"label": {"$regex": "^autoT.*"}}}  # 需要关联表
    delete_from_mongodb('data-manager', [data_source, data_set, data_set_tag])


def clean_db_file_manager():
    user_uuids = get_auto_test_user_uuid()
    file_shares = {'file_shares': {"owner_id": {"$in": user_uuids}}}
    delete_from_mongodb('file-manager', [file_shares])


def clean_db_image_manager():
    base_image = {'baseImage': {"build_type": {"$nin": ['BASIC']}}}
    image_builder = {'imageBuilder': {}}
    # 暂未清理
    image_package_op = {}
    delete_from_mongodb('image-manager', [base_image, image_builder])


def clean_db_model_manager():
    labels = {'labels': {}}
    models = {'models': {}}
    versions = {'versions': {}}
    # 暂未清理
    edge_nodes = {'versions': {}}
    delete_from_mongodb('model-manager', [labels, models, versions])


def clean_db_project_manager():
    project = {'project': {}}
    tasks = {'tasks': {}}
    delete_from_mongodb('project-manager', [project, tasks])


def clean_db_resource_manager():
    resource_configs = {'resource_configs': {}}
    # 无法区分新添加的内容，暂时不清理
    resource_templates = {'resource_templates': {}}
    delete_from_mongodb('resource-manager', [resource_configs])

    default_config = """{
        "_id" : "efc3afdc-8570-4d32-9b4c-ba3674116ffb",
        "created_at" : "2019-09-11T04:34:14.956Z",
        "updated_at" : "2019-09-11T04:34:14.956Z",
        "user_id" : null,
        "max_concurrent_tasks" : 10,
        "max_concurrent_heavy_tasks" : 3,
        "max_cpu_time" : 259200,
        "max_gpu_time" : 5184000,
        "max_gpus" : 3,
        "heavy_task_threshold" : {
            "cpu" : 16000,
            "memory" : 34359738368
        },
        "parameter_type" : "GLOBAL",
        "_cls" : "apis.v1.config.models.ResourceConfig"
    } """
    default_config = json.loads(default_config)
    resource_configs_recover = {'resource_configs': default_config}
    insert_to_mongodb('resource-manager', resource_configs_recover)


def clean_db_skyflow_manager():
    skyflow = {'skyflow': {}}
    skyflow_component = {'skyflow_component': {'is_custom': True}}
    skyflow_execute = {'skyflow_execute': {}}
    delete_from_mongodb('skyflow-manager', [skyflow, skyflow_component, skyflow_execute])


def clean_db_storage_manager():
    pass
    # user_uuids = get_auto_test_user_uuid()
    # volumes = {'volumes': {'owner_id': {"$in": user_uuids}}}
    # delete_from_mongodb('storage-manager', [volumes])


def clean_db_workflow_engine():
    workflow_engine = {'workflow-engine': {}}
    delete_from_mongodb('workflow-engine', [workflow_engine])


def clean_db_user_manager():
    # 用户清理需放在数据库清理的最后一步调用
    user = {'users': {"username": {"$regex": "^autoT.*"}}}
    group = {'groups': {"name": {"$regex": "^autoT.*"}}}
    delete_from_mongodb('user-manager', [user, group])


def clean_db():
    clean_db_data_manager()
    clean_db_file_manager()
    clean_db_image_manager()
    clean_db_model_manager()
    clean_db_project_manager()
    clean_db_resource_manager()
    # 目前不重建用户，不要清理storage表
    clean_db_storage_manager()
    clean_db_skyflow_manager()
    clean_db_workflow_engine()
    # 目前不重建用户，不要清理用户表
    # clean_db_user_manager()


def clean_pod_service(conn_info=config.ssh_conn_info):
    host = conn_info['host']
    port = conn_info['port']
    user = conn_info['user']
    passwd = conn_info['passwd']
    conn = SSHConnection(host, port, user, passwd)
    # 清理swf
    conn.exec_command('kubectl delete swf --all --force --grace-period=0  -n skydiscovery-app')
    # 清理service
    conn.exec_command('kubectl delete service --all --force --grace-period=0  -n skydiscovery-app')
    # 清理pod
    conn.exec_command('kubectl delete pod --all --force --grace-period=0  -n skydiscovery-app')

    time.sleep(10)
    conn.close()
    print('clean pod service success')


def delete_files(token, conn_info=config.ssh_conn_info):
    host = conn_info['host']
    port = conn_info['port']
    user = conn_info['user']
    passwd = conn_info['passwd']
    conn = SSHConnection(host, port, user, passwd)
    # 清理ceph下用户目录
    path = get_user_ceph_path(token)
    conn.exec_command('rm -rf {}/*'.format(path))
    time.sleep(3)
    conn.close()
    print('delete files success')


def clean_all():
    return True
    # import datetime
    # print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    logger.log_debug('Start to clean ENV')
    clean_volumes_from_disk()
    clean_db()
    clean_pod_service()
    logger.log_debug('Finished clean ENV')
    # print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
