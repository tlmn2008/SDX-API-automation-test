# -*- coding: utf-8 -*-

from configurations import config
from send_check.req_send import send_file_m_req
from send_check.req_send import send_user_m_req
from test_cases import base
from utilities.clean_env import delete_files


class TestFileDownload(base.Base):
    @classmethod
    def setup_class(cls):
        super(TestFileDownload, cls).setup_class(logger_name='file_download')
        cls.token = send_user_m_req.get_token_simple()
        # delete_files(cls.token)

    def test_SKTE_T993_download_file(self):
        filename = config.file_name
        file = '{}{}'.format(config.file_url, filename)
        target = config.ceph_path
        paths = []
        paths.append('{}{}'.format(target, filename))
        # 上传文件用于下载操作
        send_file_m_req.upload_file(self.token, file, target)
        # 下载文件
        send_file_m_req.download_file(self.token, filename, target)
        # 删除文件
        send_file_m_req.delete_files_and_folders(self.token, paths)


    @classmethod
    def teardown(cls):
        pass