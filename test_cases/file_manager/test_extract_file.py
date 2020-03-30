# -*- coding: utf-8 -*-
from configurations import config
from send_check.req_send import send_file_m_req
from send_check.req_send import send_user_m_req
from test_cases import base
from utilities import logger
from utilities.clean_env import delete_files

class TestZipFile(base.Base):
    @classmethod
    def setup_class(cls):
        super(TestZipFile, cls).setup_class(logger_name='zip_file')
        cls.token = send_user_m_req.get_token_simple()
        # delete_files(cls.token)

    def test_SKTE_T1020_extract_file(self):
        # Title: 解压文件
        # Owner：qingzhen
        # PreCondition：创建测试目录T1020，上传zip文件到该目录成功
        zip_file = '{}{}'.format(config.file_url, config.zip_file_name)
        target = config.ceph_path
        send_file_m_req.create_folder(self.token, target, 'T1020')
        zip_file_path = '{}T1020'.format(target)
        zip_file_path_full = '{}/{}'.format(zip_file_path, config.zip_file_name)
        send_file_m_req.upload_file(self.token, zip_file, zip_file_path )
        # 1. 解压zip文件成功
        send_file_m_req.extract_file(self.token, zip_file_path_full, zip_file_path)
        # 2. 查看解压文件,目录结构如下 iris / iris1 (iris1.csv) + iris2 (iris2.csv + iris3.csv)
        folder_iris1_files = send_file_m_req.get_file_list(self.token, '{}/iris/iris1'.format(zip_file_path))
        if 'iris1.csv' not in folder_iris1_files:
            logger.log_error('iris1.csv not include in folder T1020/iris/iris1, actually files under folder are {}'.format(folder_iris1_files))
            assert False

        folder_iris2_files = send_file_m_req.get_file_list(self.token, '{}/iris/iris2'.format(zip_file_path))  #
        if 'iris2.csv' not in folder_iris2_files:
            logger.log_error('iris2.csv not include in folder T1020/iris/iris2, actually files under folder are {}'.format(
                    folder_iris2_files))
            assert False

        if 'iris3.csv' not in folder_iris2_files:
            logger.log_error(
                'iris3.csv not include in folder T1020/iris/iris2, actually files under folder are {}'.format(
                    folder_iris2_files))
            assert False

        # Reset：删除zip文件及文件夹
        send_file_m_req.delete_files_and_folders(self.token, paths= [target+'T1020'])

    @classmethod
    def teardown(cls):
        pass
