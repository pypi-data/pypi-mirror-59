# coding=utf-8

from test_framework.test_runner import Runner
from utils import log
from test_framework.test_base import TestBase


class TestCase(TestBase):


    def __init__(self, test_case_name=None):
        super(TestCase, self).__init__()
        self.test_name = test_case_name
        self.runner = None
        self.get_all_modules(self.test_case_path)
        self.list_tests()

    def get_test_cases(self):
        return self.tests

    def list_and_filter_tests(self, filters):
        filter_result = []
        for item in self.tests:
            if filters.lower() == "all":
                filter_result.append(item)
                continue
            if filters in item:
                filter_result.append(item)
        return filter_result

    def run(self, test_name=None):
        if test_name is not None:
            self.test_name = test_name
        self.runner = Runner()
        test_path = self.get_all_script_path(self.test_name)
        if not test_path:
            log.ERR("TestCase not find: %s", self.test_name)
        else:
            self.runner.process_run(self.test_name, test_path[0], 1, 0)
        return self.runner.get_results()
