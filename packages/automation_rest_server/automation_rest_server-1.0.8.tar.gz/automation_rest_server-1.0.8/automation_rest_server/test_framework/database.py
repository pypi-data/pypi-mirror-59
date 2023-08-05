# coding=utf-8
# pylint: disable=broad-except, import-error
import datetime
import threading
import pymysql as mysql
from utils import log
from test_framework.state import State
from utils.system import get_ip_address
from test_framework.test_result import TestResult


class SqlConnection(object):

    def __init__(self, host="172.29.129.8", port=3306, user="tester", passwd="Cnex!321", db_name="production_test"):
        self.host = host
        self.port = port
        self.user = user
        self.passwd = passwd
        self.db_name = db_name
        self.conn = mysql.connect(host=self.host, port=self.port, user=self.user,
                                  passwd=self.passwd, db=self.db_name, charset="utf8")
        self.cursor = self.conn.cursor()

    def reconnect(self):
        self.conn = mysql.connect(host=self.host, port=self.port, user=self.user,
                                  passwd=self.passwd, db=self.db_name, charset="utf8")
        self.cursor = self.conn.cursor()

    def __del__(self):
        self.cursor.close()
        self.conn.close()

    def ping(self):
        return self.conn.ping()

    def get_datetime(self):
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return current_time

    def insert_to_table(self, table, **kwargs):
        col_str = ""
        value_str = ""
        for key, value in kwargs.items():
            col_str = "`{}`".format(key) if col_str == "" else "{},`{}`".format(col_str, key)
            value_str = "'{}'".format(value) if value_str == "" else "{},'{}'".format(value_str, value)
        insert_command = "INSERT INTO {}({}) VALUES({})".format(table, col_str, value_str)
        self.cursor.execute(insert_command)
        self.conn.commit()

    def insert_test_result(self, **kwargs):
        self.insert_to_table("test_results", **kwargs)

    def exist_key(self, test_key):
        sql_command = "SELECT test_key from test_results WHERE test_key='{}'".format(test_key)
        self.cursor.execute(sql_command)
        result = self.cursor.fetchone()
        return result

    def update_test_states(self, test_key, **kwargs):
        str_date = ""
        for key, value in kwargs.items():
            temp_str = "{}='{}'".format(key, value)
            str_date = temp_str if str_date == "" else "{},{}".format(str_date, temp_str)
            if key == "result":
                if value == 3:
                    temp_str = "{}='{}'".format("start_time", self.get_datetime())
                    str_date = "{},{}".format(str_date, temp_str)
                elif value in [0, 1]:
                    temp_str = "{}='{}'".format("end_time", self.get_datetime())
                    str_date = "{},{}".format(str_date, temp_str)
        update_command = "UPDATE test_results SET {} where test_key='{}'".format(str_date, test_key)
        self.cursor.execute(update_command)
        self.conn.commit()

    def update_test_to_abnormal_end(self, ip_addr):
        update_command = "UPDATE test_results SET result='15' where ip='{}' AND (result='3' OR result='2')".format(ip_addr)
        self.cursor.execute(update_command)
        self.conn.commit()

    def create_table(self, table_name, col_attrs):
        str_col = None
        for item in list(col_attrs):
            if str_col is None:
                str_col = "`{}` {}".format(item["name"], item["type"])
            else:
                str_col = "{}, `{}` {}".format(str_col, item["name"], item["type"])

        command = "CREATE TABLE {} ({})".format(table_name, str_col)
        print(command)
        self.cursor.execute(command)
        self.conn.commit()

    def get_last_index(self, table_name='tests'):
        command = "select `index` from {} ORDER by `index` desc".format(table_name)
        self.cursor.execute(command)
        result = self.cursor.fetchone()
        index = result[0] if result else 0
        return index
try:
    SQL = SqlConnection()
except Exception as all_exception:
    log.ERR(all_exception)


def decorate_add_tests(func):
    def func_wrapper(*args, **kwargs):
        ret = func(*args, **kwargs)
        if ret is not None:
            try:
                SQL.ping()
                SQL.insert_test_result(test_key=ret, test_name=args[1], result=State.NOT_START, ip=get_ip_address())
            except Exception as all_exception:
                log.ERR(all_exception)
        return ret
    return func_wrapper


def decorate_update_test_state(func):
    def func_wrapper(*args, **kwargs):
        ret = func(*args, **kwargs)
        test_result = TestResult()
        logs = test_result.get_test_suite_test_msg(args[3])
        logs = mysql.escape_string(logs)
        try:
            SQL.ping()
            SQL.update_test_states(args[1], result=args[2], test_log=logs)
        except Exception as all_exception:
            log.ERR(all_exception)
        return ret
    return func_wrapper


def update_abnormal_end_tests():
    local_ip = get_ip_address()
    thread_ = threading.Thread(target=SQL.update_test_to_abnormal_end, args=(local_ip,))
    thread_.setDaemon(True)
    thread_.start()
