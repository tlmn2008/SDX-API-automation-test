# -*- coding: utf-8 -*-
from configurations import config
from send_check.req_send import send_file_m_req
from send_check.req_send import send_user_m_req
from test_cases import base
from utilities.clean_env import delete_files

class TestFileFolderRename(base.Base):
    @classmethod
    def setup_class(cls):
        super(TestFileFolderRename, cls).setup_class(logger_name='file_folder_rename')
        cls.token = send_user_m_req.get_token_simple()
        # delete_files(cls.token)

    def test_SKTE_T1016_rename(self):
        # Title: 重命名文件
        # Owner：qingzhen
        # PreCondition：创造测试文件夹T1016，上传测试文件iris.csv
        target = config.ceph_path
        file = '{}{}'.format(config.file_url, config.file_name)
        send_file_m_req.create_folder(self.token, target, 'T1016')
        send_file_m_req.upload_file(self.token, file, target + 'T1016')
        # 1. 重命名iris.csv为reame.csv成功。
        send_file_m_req.rename_file_folder(self.token, target + 'T1016/' + config.file_name , 'rename.csv')
        # 2. 上传文件iris.csv，重名为rename.csv失败
        send_file_m_req.upload_file(self.token, file, target + 'T1016')
        send_file_m_req.rename_file_folder(self.token, target + 'T1016/' + config.file_name, 'rename.csv',resultcode = '400')

        # Reset ：删除文件夹
        send_file_m_req.delete_files_and_folders(self.token, paths= [target+'T1016'])

    def test_SKTE_T1017_folder_rename(self):
        # Title: 重命名文件夹
        # Owner：qingzhen
        # PreCondition：创建文件夹T1017_1和T1017_2。
        target = config.ceph_path
        send_file_m_req.create_folder(self.token, target, 'T1017_1')
        send_file_m_req.create_folder(self.token, target, 'T1017_2')
        # 1. 重命名文件夹T1017_1为T1017_rename成功
        send_file_m_req.rename_file_folder(self.token, target + 'T1017_1', 'T1017_rename')
        # 2. 重命名文件夹T1017_2为T1017_rename失败
        send_file_m_req.rename_file_folder(self.token, target + 'T1017_2', 'T1017_rename',resultcode = '400')
        # Reset ：删除文件夹
        send_file_m_req.delete_files_and_folders(self.token, paths=[target + 'T1017_rename', target + 'T1017_2'])

    @classmethod
    def teardown(cls):
        pass
