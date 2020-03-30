# -*- coding: utf-8 -*-
from configurations import config
from send_check.req_send import send_file_m_req
from send_check.req_send import send_user_m_req
from test_cases import base
from utilities.clean_env import delete_files


class TestFileUpload(base.Base):
    @classmethod
    def setup_class(cls):
        super(TestFileUpload, cls).setup_class(logger_name='file_upload')
        cls.token = send_user_m_req.get_token_simple()
        # delete_files(cls.token)

    def test_SKTE_T985_upload_file(self):
        file = '{}{}'.format(config.file_url, config.file_name)
        target = config.ceph_path
        paths = []
        paths.append('{}{}'.format(target, config.file_name))
        send_file_m_req.upload_file(self.token, file, target)
        send_file_m_req.delete_files_and_folders(self.token, paths)

    @classmethod
    def teardown(cls):
        pass
