# coding: utf-8

"""
    VeeRoute.LSS Merchandiser

    Программный интерфейс для планирования работ торговых предствителей.  # noqa: E501

    OpenAPI spec version: 1.7.153581
    Contact: support@veeroute.com
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

from __future__ import absolute_import

import unittest

import vrt_lss_merchandiser
from api.check_api import CheckApi  # noqa: E501
from vrt_lss_merchandiser.rest import ApiException


class TestCheckApi(unittest.TestCase):
    """CheckApi unit test stubs"""

    def setUp(self):
        self.api = api.check_api.CheckApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_check(self):
        """Test case for check

        Проверка доступности сервиса  # noqa: E501
        """
        pass


if __name__ == '__main__':
    unittest.main()
