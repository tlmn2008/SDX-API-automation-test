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

    def test_skte_t1001_copy_file(self):
        # 上传文件用于拷贝
        filename = config.file_name  # 拷贝源文件名称
        file = '{}{}'.format(config.file_url, filename)  # 源文件及其路径
        target = config.ceph_path  # 文件上传的目的地址，同时也是拷贝文件的源地址
        send_file_m_req.upload_file(self.token, file, target)
        # 创建拷贝目的地址文件夹
        folder = 'T1001 copyfolder'
        send_file_m_req.create_folder(self.token, target, folder)
        # 拷贝文件
        copy_source = '{}{}'.format(config.ceph_path, config.file_name)
        copy_sources = []
        copy_sources.append(copy_source)  # 拷贝的源文件及其路径列表
        copy_target = '{}{}'.format(target, folder)  # 文件拷贝的目标地址
        send_file_m_req.copy_file(self.token, copy_sources, copy_target)
        # 校验拷贝结果
        filename_target = send_file_m_req.get_file_list(self.token, copy_target)  # 拷贝目的地址文件名列表
        if filename not in filename_target:
            logger.log_error('file/folder {} copy failed, target address do not find it'.format(filename))
            assert False
        filename_source = send_file_m_req.get_file_list(self.token, target)  # 拷贝源地址文件名列表
        if filename not in filename_source:
            logger.log_error('file/folder {} copy failed, source address do not find it'.format(filename))
            assert False
        # 删除文件和文件夹
        # paths = []
        # paths.append('{}{}'.format(target, config.file_name))
        # paths.append('{}{}'.format(target, folder))
        # send_file_m_req.delete_files_and_folders(self.token, paths)    # 批量删除文件和文件夹有bug，http://jira.iluvatar.ai:8080/browse/SDXTEST-468，文件和文件夹暂时分开删除
        # 删除文件
        path_file = []
        path_file.append('{}{}'.format(target, config.file_name))
        send_file_m_req.delete_files_and_folders(self.token, path_file)
        # 删除文件夹
        path_folder = []
        path_folder.append('{}{}'.format(target, folder))
        send_file_m_req.delete_files_and_folders(self.token, path_folder)

    def test_skte_t1002_copy_folder(self):
        # 上传文件用于文件夹拷贝
        filename = config.file_name  # 上传源文件名称
        file = '{}{}'.format(config.file_url, filename)  # 源文件及其路径
        source_folder = 'T1002'  # 需拷贝的源文件夹名称
        source_path = '{}{}'.format(config.ceph_path, source_folder)  # 文件上传的目的地址，同时也是拷贝目标
        send_file_m_req.upload_file(self.token, file, source_path)
        # 创建文件夹作为拷贝目的地址
        folder = 'T1002 copyfolder'
        send_file_m_req.create_folder(self.token, config.ceph_path, folder)
        # 拷贝文件夹
        copy_source = source_path
        copy_sources = []
        copy_sources.append(copy_source)  # 拷贝的源文件夹及其路径列表
        copy_target = '{}{}'.format(config.ceph_path, folder)  # 文件夹拷贝的目标地址
        send_file_m_req.copy_file(self.token, copy_sources, copy_target)
        # 校验拷贝结果
        foldername_target = send_file_m_req.get_file_list(self.token, copy_target)  # 拷贝目的地址文件名列表
        if source_folder not in foldername_target:
            logger.log_error('file/folder {} copy failed, target address do not find it'.format(source_folder))
            assert False
        foldername_target = send_file_m_req.get_file_list(self.token, config.ceph_path)  # 拷贝源地址文件名列表
        if source_folder not in foldername_target:
            logger.log_error('file/folder {} copy failed, source address do not find it'.format(source_folder))
            assert False
        # 删除文件夹
        path_folder = []
        path_folder.append(copy_source)
        path_folder.append(copy_target)
        send_file_m_req.delete_files_and_folders(self.token, path_folder)

    @classmethod
    def teardown(cls):
        pass
