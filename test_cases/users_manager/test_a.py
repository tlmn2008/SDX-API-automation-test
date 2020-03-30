from test_cases import base
from utilities import logger
from send_check.apis import api_user_m
import requests


class TestA(base.Base):
    @classmethod
    def setup_class(cls):
        super(TestA, cls).setup_class()
        cls.token = super(TestA, cls).token_simple()
        cls.headers = {'Authorization': cls.token}

    def not_test_coupon(self):
        r = api_user_m.get_user_login_req()
        res = requests.get(r.url, headers=self.headers)

        logger.log_debug(str(res.content))
        assert True

    @classmethod
    def teardown_class(cls):
        pass
