# -*- coding: utf-8 -*-
from configurations import config
from send_check.req_send import send_file_m_req
from send_check.req_send import send_user_m_req
from test_cases import base
from utilities import logger


class TestFileUpload(base.Base):
    @classmethod
    def setup_class(cls):
        super(TestFileUpload, cls).setup_class(logger_name='file_upload')
        cls.token = send_user_m_req.get_token_simple()

    def test_skte_t996_move_file(self):
        # 上传文件用于移动
        filename = config.file_name    # 移动源文件名称
        file = '{}{}'.format(config.file_url, filename)    # 源文件及其路径
        target = config.ceph_path    # 文件上传的目的地址，同时也是移动文件的源地址
        send_file_m_req.upload_file(self.token, file, target)
        # 创建文件夹作为移动目的地址
        folder = 'T996 movefolder'
        send_file_m_req.create_folder(self.token, target, folder)
        # 移动文件
        move_source = '{}{}'.format(config.ceph_path, config.file_name)
        move_sources = []
        move_sources.append(move_source)    # 移动的源文件及其路径列表
        move_target = '{}{}'.format(target, folder)    # 文件移动的目标地址
        send_file_m_req.move_file(self.token, move_sources, move_target)
        # 校验移动结果
        filename_target = send_file_m_req.get_file_list(self.token, move_target)    # 移动目的地址文件名列表
        if filename not in filename_target:
            logger.log_error('file/folder {} move failed, target address do not find it'.format(filename))
            assert False
        filename_source = send_file_m_req.get_file_list(self.token, target)    # 移动源地址文件名列表
        if filename in filename_source:
            logger.log_error('file/folder {} move failed, source address have not moved it away'.format(filename))
            assert False
        # 删除文件夹
        path_folder =[]
        path_folder.append('{}{}'.format(target, folder))
        send_file_m_req.delete_files_and_folders(self.token, path_folder)

    def test_skte_t997_move_folder(self):
        # 上传文件用于文件夹移动
        filename = config.file_name    # 上传源文件名称
        file = '{}{}'.format(config.file_url, filename)    # 源文件及其路径
        source_folder = 'T997'  # 需移动的源文件夹名称
        source_path = '{}{}'.format(config.ceph_path, source_folder)  # 文件上传的目的地址，同时也是移动目标
        send_file_m_req.upload_file(self.token, file, source_path)
        # 创建文件夹作为移动目的地址
        folder = 'T997 movefolder'
        send_file_m_req.create_folder(self.token, config.ceph_path, folder)
        # 移动文件夹
        move_source = source_path
        move_sources = []
        move_sources.append(move_source)    # 移动的源文件夹及其路径列表
        move_target = '{}{}'.format(config.ceph_path, folder)    # 文件夹移动的目标地址
        send_file_m_req.move_file(self.token, move_sources, move_target)
        # 校验移动结果
        foldername_target = send_file_m_req.get_file_list(self.token, move_target)    # 移动目的地址文件名列表
        if source_folder not in foldername_target:
            logger.log_error('file/folder {} move failed, target address do not find it'.format(source_folder))
            assert False
        foldername_target = send_file_m_req.get_file_list(self.token, config.ceph_path)    # 移动源地址文件名列表
        if source_folder in foldername_target:
            logger.log_error('file/folder {} move failed, source address have not moved it away'.format(source_folder))
            assert False
        # 删除文件夹
        path_folder = []
        path_folder.append(move_target)
        send_file_m_req.delete_files_and_folders(self.token, path_folder)

    @classmethod
    def teardown(cls):
        pass
