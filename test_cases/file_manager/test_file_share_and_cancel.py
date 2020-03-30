# -*- coding: utf-8 -*-

from configurations import config
from send_check.req_send import send_file_m_req
from send_check.req_send import send_user_m_req
from test_cases import base
from utilities import logger
from utilities.common_method import get_uuid_from_token


class TestFileDelete(base.Base):
    @classmethod
    def setup_class(cls):
        super(TestFileDelete, cls).setup_class(logger_name='file_delete')
        cls.token = send_user_m_req.get_token_simple()

    def test_skte_t1014_t1029_share_and_cancel_file(self):
        filename = config.file_name  # 上传文件名称
        file = '{}{}'.format(config.file_url, filename)  # 源文件及其路径
        target = config.ceph_path  # 上传路径
        filePath = '{}{}'.format(target, filename)  # 上传后文件及其路径
        # 上传文件用于共享/取消共享操作
        send_file_m_req.upload_file(self.token, file, target)
        # 共享文件给全局
        uuid = get_uuid_from_token(self.token)  # 文件所有者的uuid，同时也是文件共享者的uuid
        share_uuid = send_file_m_req.share_file(self.token, owner_uuid=uuid, sharePath=filePath, isGlobal=True)
        # 验证文件共享结果: 1)共享用户在“我的共享”文件夹下可看到共享文件 2）被共享用户在“接收的共享”文件夹下可看到被共享文件
        my_share_file = send_file_m_req.get_shared_file_list(self.token, owner_id=uuid)  # 共享用户查看"我的共享"文件夹，返回其下可查看到的文件列表
        if filename not in my_share_file:
            logger.log_error('user {} cannot find shared file {}'.format(config.user_name_a, filename))
            assert False
        shareuser_token = send_user_m_req.get_token_simple(config.user_name_b, config.user_passwd_b)  # 被共享用户的token
        sharer_uuid = get_uuid_from_token(shareuser_token)  # 被共享用户的uuid
        share_file_list = send_file_m_req.get_shared_file_list(shareuser_token,
                                                               user_id=sharer_uuid)  # 被共享用户查看"接收的共享"，返回其下可查看到的文件列表
        if filename not in share_file_list:
            logger.log_error('user {} cannot find shared file {}'.format(config.user_name_b, filename))
            assert False
        # 取消共享文件
        send_file_m_req.cancel_shared_file(self.token, share_uuid)
        # 验证文件共享结果: 1)共享用户的“我的共享”文件夹下已移除共享文件 2）被共享用户已在“接收的共享”文件夹下移除被共享文件
        my_share_file = send_file_m_req.get_shared_file_list(self.token, owner_id=uuid)  # 共享用户查看"我的共享"文件夹，返回其下可查看到的文件列表
        if filename in my_share_file:
            logger.log_error('user {} should not find unshared file {}'.format(config.user_name_a, filename))
            assert False
        share_file_list = send_file_m_req.get_shared_file_list(shareuser_token,
                                                               user_id=sharer_uuid)  # 被共享用户查看"接收的共享"，返回其下可查看到的文件列表
        if filename in share_file_list:
            logger.log_error('user {} should not find unshared file {}'.format(config.user_name_b, filename))
            assert False
        # 删除文件
        paths = []
        paths.append(filePath)
        send_file_m_req.delete_files_and_folders(self.token, paths)

    def test_skte_t1023_t1030_share_and_cancel_files_in_bulk(self):
        target = config.ceph_path  # 上传路径
        filename1 = 'iris.csv'  # 上传文件名称
        file1 = '{}{}'.format(config.file_url, filename1)  # 源文件及其路径
        filePath1 = '{}{}'.format(target, filename1)  # 上传后文件及其路径
        filename2 = 'iris.txt'
        file2 = '{}{}'.format(config.file_url, filename2)
        filePath2 = '{}{}'.format(target, filename2)
        paths = []
        paths.append(filePath1)
        paths.append(filePath2)
        # 上传文件用于共享/取消共享操作
        send_file_m_req.upload_file(self.token, file1, target)
        send_file_m_req.upload_file(self.token, file2, target)
        # 共享文件给用户
        uuid = get_uuid_from_token(self.token)  # 文件所有者的uuid，同时也是文件共享者的uuid
        shareuser_token = send_user_m_req.get_token_simple(config.user_name_b, config.user_passwd_b)  # 被共享用户的token
        sharer_uuid = get_uuid_from_token(shareuser_token)  # 被共享用户的uuid
        share_uuid = send_file_m_req.share_files_batch(self.token, sharePaths=paths, owner_id=uuid, share_id=uuid,
                                                       users=[sharer_uuid])
        # 验证文件共享结果: 1)共享用户在“我的共享”文件夹下可看到共享文件 2）被共享用户在“接收的共享”文件夹下可看到被共享文件
        my_share_file = send_file_m_req.get_shared_file_list(self.token, owner_id=uuid)  # 共享用户查看"我的共享"文件夹，返回其下可查看到的文件列表
        if filename1 and filename2 not in my_share_file:
            logger.log_error(
                'user {} cannot find shared file {} and {}'.format(config.user_name_a, filename1, filename2))
            assert False
        share_file_list = send_file_m_req.get_shared_file_list(shareuser_token,
                                                               user_id=sharer_uuid)  # 被共享用户查看"接收的共享"，返回其下可查看到的文件列表
        if filename1 and filename2 not in share_file_list:
            logger.log_error(
                'user {} cannot find shared file {} and {}'.format(config.user_name_b, filename1, filename2))
            assert False
        # 取消共享文件
        send_file_m_req.cancel_shared_file(self.token, share_uuid)
        # 验证文件共享结果: 1)共享用户的“我的共享”文件夹下已移除共享文件 2）被共享用户已在“接收的共享”文件夹下移除被共享文件
        my_share_file = send_file_m_req.get_shared_file_list(self.token, owner_id=uuid)  # 共享用户查看"我的共享"文件夹，返回其下可查看到的文件列表
        if filename1 and filename2 in my_share_file:
            logger.log_error(
                'user {} should not find unshared file {} and {}'.format(config.user_name_a, filename1, filename2))
            assert False
        share_file_list = send_file_m_req.get_shared_file_list(shareuser_token,
                                                               user_id=sharer_uuid)  # 被共享用户查看"接收的共享"，返回其下可查看到的文件列表
        if filename1 and filename2 in share_file_list:
            logger.log_error(
                'user {} should not find unshared file {} and {}'.format(config.user_name_b, filename1, filename2))
            assert False
        # 删除文件
        send_file_m_req.delete_files_and_folders(self.token, paths)

    @classmethod
    def teardown(cls):
        pass
