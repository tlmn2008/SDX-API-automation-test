# -*- coding: utf-8 -*-

from configurations import config
from send_check.req_send import send_file_m_req
from send_check.req_send import send_user_m_req
from test_cases import base
from utilities import logger
from utilities.clean_env import delete_files
from utilities.common_method import get_uuid_from_token
from utilities.common_method import check_files_folders_exist
from utilities.sshConnection import SSHConnection
import time

class TestFileDelete(base.Base):
    @classmethod
    def setup_class(cls):
        super(TestFileDelete, cls).setup_class(logger_name='file_delete')
        cls.token = send_user_m_req.get_token_simple()
        # delete_files(cls.token)

    def test_skte_t1006_delete_file(self):
        filename = config.file_name
        file = '{}{}'.format(config.file_url, filename)
        target = config.ceph_path
        paths = []
        paths.append('{}{}'.format(target, filename))
        # 上传文件用于删除操作
        send_file_m_req.upload_file(self.token, file, target)
        # 删除文件
        send_file_m_req.delete_files_and_folders(self.token, paths)

    def test_skte_t1007_delete_folder(self):
        # Title: 删除文件夹
        # Owner：qingzhen
        # PreCondition：创建测试目录T1007，上传iris.csv文件到该目录成功,并检查宿主机上对应user volumn下文件夹存在
        target = config.ceph_path
        file = '{}{}'.format(config.file_url, config.file_name)
        send_file_m_req.create_folder(self.token, target, 'T1007')
        send_file_m_req.upload_file(self.token, file, target + 'T1007')
        user_uuid = get_uuid_from_token(self.token)
        volume_id = send_file_m_req.get_volume_id_by_user_uuid(user_uuid)

        # 1. 删除文件夹
        send_file_m_req.delete_files_and_folders(self.token, paths= [target + 'T1007'])
        time.sleep(2)

        # 2. 在对应user volume下检查文件夹删除成功
        foler_check = '/SkyDiscovery/cephfs/data/user/volume_{}/T1007'.format(volume_id)
        assert check_files_folders_exist(input_path_list=[foler_check], isExistCheck=False)


    def test_skte_t1008_delete_multi_files_folders(self):
        # Title: 删除多个文件或文件夹
        # Owner：qingzhen
        # PreCondition：创建测试目录T1008，上传iris_folder文件夹到该目录成功
        target = config.ceph_path
        # iris_folder文件结构：
        # iris_folder
        #   iris0(iris0_1.csv+iris0_2.csv+iris0_3.csv)
        #   iris1(iris1.csv)
        #   iris2(iris2_1.csv+iris2_2.csv)
        #   iris3.csv
        #   iris4.csv
        #   iris5.csv
        folder = '{}{}'.format(config.file_url, config.folder_name)
        send_file_m_req.create_folder(self.token, target, 'T1008')
        send_file_m_req.upload_file(self.token, folder + '/iris3.csv', target + 'T1008/' + config.folder_name)
        send_file_m_req.upload_file(self.token, folder + '/iris4.csv', target + 'T1008/' + config.folder_name)
        send_file_m_req.upload_file(self.token, folder + '/iris5.csv', target + 'T1008/' + config.folder_name)
        send_file_m_req.upload_file(self.token, folder + '/iris0/iris0_1.csv', target + 'T1008/' + config.folder_name + '/iris0')
        send_file_m_req.upload_file(self.token, folder + '/iris0/iris0_2.csv', target + 'T1008/' + config.folder_name + '/iris0')
        send_file_m_req.upload_file(self.token, folder + '/iris0/iris0_3.csv', target + 'T1008/' + config.folder_name + '/iris0')
        send_file_m_req.upload_file(self.token, folder + '/iris1/iris1.csv', target + 'T1008/' + config.folder_name + '/iris1')
        send_file_m_req.upload_file(self.token, folder + '/iris2/iris2_1.csv', target + 'T1008/' + config.folder_name + '/iris2')
        send_file_m_req.upload_file(self.token, folder + '/iris2/iris2_2.csv', target + 'T1008/' + config.folder_name + '/iris2')

        user_uuid = get_uuid_from_token(self.token)
        volume_id = send_file_m_req.get_volume_id_by_user_uuid(user_uuid)

        # 1. 删除文件夹和文件夹
        delete_paths = [target + 'T1008/'+config.folder_name+'/iris0',
                                            target + 'T1008/'+config.folder_name+'/iris2',target + 'T1008/'+config.folder_name+'/iris3.csv',
                                            target + 'T1008/'+config.folder_name+'/iris5.csv']
        send_file_m_req.delete_files_and_folders(self.token, paths=delete_paths)
        time.sleep(2)

        # 2.在对应user volume下检查文件夹和文件夹删除成功
        user_volume_path = '/SkyDiscovery/cephfs/data/user/volume_{}/'.format(volume_id)
        delete_paths_check = [user_volume_path + 'T1008/' + config.folder_name + '/iris0',
                        user_volume_path + 'T1008/' + config.folder_name + '/iris2',
                        user_volume_path + 'T1008/' + config.folder_name + '/iris3.csv',
                        user_volume_path + 'T1008/' + config.folder_name + '/iris5.csv']

        assert check_files_folders_exist(input_path_list=delete_paths_check,isExistCheck=False)

        # Reset: 删除目录 T1008
        send_file_m_req.delete_files_and_folders(self.token, paths=[target + 'T1008'])

    @classmethod
    def teardown(cls):
        pass