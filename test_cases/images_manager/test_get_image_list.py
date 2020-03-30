# -*- coding: utf-8 -*-
from test_cases import base
from utilities import logger
from send_check.req_send import send_req
from send_check.apis import api_image_m
from send_check.req_send import send_user_m_req
from configurations import config


class TestGetImageList(base.Base):
    @classmethod
    def setup_class(cls):
        super(TestGetImageList, cls).setup_class(logger_name='get_image_list')
        # cls.token = super(TestGetImageList, cls).token_simple()
        cls.token = send_user_m_req.get_token_simple()

    def test_get_all_image_list(self):
        # 获取所有image list

        req = api_image_m.get_all_image_list_req(self.token)
        # 最多显示100条
        count = 100
        req.param.update({'count': count})
        res = send_req.send_request(req)
        try:
            total = res['total']
        except KeyError:
            logger.log_error('Can not get "total" from response.')
            raise Exception('Key "total" can not be found!')

        if total > count:
            total = count
        # 检查list中image的个数与total相同
        if len(res['data']) != total:
            logger.log_error('The count of image info is wrong, total is {}, but get {}'.format(total, len(res['data'])))
            assert False

    def test_get_image_info_by_name(self):
        # 根据image name查询image信息

        req = api_image_m.get_all_image_list_req(self.token)
        # 设置查询的image name
        req.param.update({'name': config.jupyter_image_name})
        res = send_req.send_request(req)

        if len(res['data']) == 0:
            logger.log_error('Got empty result.')
            assert False

        # 模糊查询结果可能为多个，逐个检查名称
        for i in res['data']:
            if config.jupyter_image_name not in i['name']:
                logger.log_error('Found unexpected image info: {}, no relationship with image "{}"'.format
                                 (i['name'], config.jupyter_image_name))
                assert False

    @classmethod
    def teardown_class(cls):
        pass
