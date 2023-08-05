# coding=utf-8
# pylint: disable=inconsistent-return-statements
import os
import re


class TestBase(object):

    def __init__(self):
        self.test_case_path = os.path.join(os.path.dirname(__file__), "..", "..", "..", "TestCase")
        self.modules = []
        self.tests = []
        self.module_list = []

    def get_all_script_path(self, script):
        list_script = script.split(';')
        path_list = []
        for single_script in list_script:
            path = self._get_full_path_script(single_script.strip())
            if path is not None:
                path_list.append(path)
        return path_list

    def _get_full_path_script(self, script):
        if script.find(':') != -1:
            file_name = script.split(':')
            if file_name[0].find('.py') == -1:
                file_path = self.get_file_path(self.test_case_path, file_name[0]+'.py')
            else:
                file_path = self.get_file_path(self.test_case_path, file_name[0])
            if file_path is not None:
                abs_path = file_path + ':' + file_name[1]
            else:
                abs_path = None
        else:
            abs_path = self.get_file_path(self.test_case_path, script)
        return abs_path

    def get_file_path(self, path, file_):
        _files = os.listdir(path)
        for item in _files:
            item_path = os.path.join(path, item)
            if os.path.isdir(item_path):
                ret = self.get_file_path(item_path, file_)
                if ret is not None:
                    return ret
            elif item == file_:
                return os.path.join(path, item)

    def get_all_modules(self, path):
        _files = os.listdir(path)
        for item in _files:
            item_path = os.path.join(path, item)
            if os.path.isdir(item_path):
                ret = self.get_all_modules(item_path)
                if ret is not None:
                    return ret
            elif ".py" in item and "__init__" not in item and ".pyc" not in item:
                self.module_list.append(item_path)

    def list_tests(self):
        for item in self.module_list:
            self.list_test_in_one_file(item)

    def list_test_in_one_file(self, file_path):
        module_name = os.path.basename(file_path).split(".")[0]
        file_ = open(file_path)
        class_name = None
        for line_ in file_.readlines():
            get_class_name = self.get_class_name(line_)
            if get_class_name:
                class_name = get_class_name[0]
            else:
                get_function_name = self.get_function_name(line_)
                if get_function_name:
                    test = "{}:{}.{}".format(module_name, class_name, get_function_name[0])
                    self.tests.append(test)

    def get_class_name(self, line):
        rets = re.findall("^\s*class\s+(Test[a-zA-Z0-9\_]+)\(", line)
        return rets

    def get_function_name(self, line):
        rets = re.findall("^\s+def\s+(test[a-zA-Z0-9\_]+)\(", line)
        return rets
