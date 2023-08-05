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
from api.plan_api import PlanApi  # noqa: E501
from vrt_lss_lastmile.rest import ApiException


class TestPlanApi(unittest.TestCase):
    """PlanApi unit test stubs"""

    def setUp(self):
        self.api = api.plan_api.PlanApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_delete_result(self):
        """Test case for delete_result

        Удаление результата планирования  # noqa: E501
        """
        pass

    def test_get_result(self):
        """Test case for get_result

        Получение результата планирования  # noqa: E501
        """
        pass

    def test_plan(self):
        """Test case for plan

        Планирование, синхронный вызов.  # noqa: E501
        """
        pass

    def test_run_plan(self):
        """Test case for run_plan

        Запуск процесса планирования  # noqa: E501
        """
        pass


if __name__ == '__main__':
    unittest.main()
