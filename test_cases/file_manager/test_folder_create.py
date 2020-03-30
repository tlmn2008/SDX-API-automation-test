# -*- coding: utf-8 -*-
from configurations import config
from send_check.req_send import send_file_m_req
from send_check.req_send import send_user_m_req
from test_cases import base
from utilities.clean_env import delete_files


class TestFolderCreate(base.Base):
    @classmethod
    def setup_class(cls):
        super(TestFolderCreate, cls).setup_class(logger_name='folder_create')
        cls.token = send_user_m_req.get_token_simple()
        # delete_files(cls.token)

    def test_SKTE_T984_new_folder_create(self):
        # Title: 新建文件夹
        # Owner：qingzhen
        # PreCondition：NA
        target = config.ceph_path
        # 1. 创建文件夹
        send_file_m_req.create_folder(self.token, target, 'T984')

        # 2. 创建同名文件夹失败
        send_file_m_req.create_folder(self.token, target, 'T984',  resultcode= '400')

        # Reset ：删除文件夹
        send_file_m_req.delete_files_and_folders(self.token, paths= [target+'T984'])

    @classmethod
    def teardown(cls):
        pass
