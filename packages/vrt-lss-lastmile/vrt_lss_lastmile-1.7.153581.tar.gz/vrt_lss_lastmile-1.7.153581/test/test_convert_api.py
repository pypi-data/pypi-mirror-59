# coding: utf-8

"""
    VeeRoute.LSS Lastmile

    Программный интерфейс для универсального планирования задач последней мили  # noqa: E501

    OpenAPI spec version: 1.7.153581
    Contact: support@veeroute.com
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

from __future__ import absolute_import

import unittest

import vrt_lss_lastmile
from api.convert_api import ConvertApi  # noqa: E501
from vrt_lss_lastmile.rest import ApiException


class TestConvertApi(unittest.TestCase):
    """ConvertApi unit test stubs"""

    def setUp(self):
        self.api = api.convert_api.ConvertApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_convert_to_json(self):
        """Test case for convert_to_json

        Конвертация задачи и результата планирования  # noqa: E501
        """
        pass

    def test_convert_to_xlsx(self):
        """Test case for convert_to_xlsx

        Конвертация задачи и результата планирования  # noqa: E501
        """
        pass


if __name__ == '__main__':
    unittest.main()
