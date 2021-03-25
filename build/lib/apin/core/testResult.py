"""
Author:柠檬班-木森
Time:2020/8/26   11:25
E-mail:3247119728@qq.com
"""
import json
import re
import traceback
import unittest
import sys
import time
from io import StringIO
from apin.core.parsersetting import ENV

origin_stdout = sys.stdout

from apin.core import log


def output2console(s):
    """将stdout内容输出到console"""
    tmp_stdout = sys.stdout
    sys.stdout = origin_stdout
    print(s, end='')
    sys.stdout = tmp_stdout


class OutputRedirector(object):
    """ Wrapper to redirect stdout or stderr """

    def __init__(self, fp):
        self.fp = fp

    def write(self, s):
        self.fp.write(s)
        # output2console(s)
        origin_stdout.write(str(s))

    def writelines(self, lines):
        self.fp.writelines(lines)

    def flush(self):
        self.fp.flush()


stdout_redirector = OutputRedirector(sys.stdout)
stderr_redirector = OutputRedirector(sys.stderr)


class TestResult(unittest.TestResult):
    """ 测试结果记录"""

    def __init__(self):
        super().__init__()

        self.fields = {
            "success": 0,
            "all": 0,
            "fail": 0,
            "skip": 0,
            "error": 0,
            "begin_time": "",
            "results": [],
            "testClass": set()
        }
        self.sys_stdout = None
        self.sys_stderr = None
        self.outputBuffer = None

    def startTest(self, test):
        """
        当测试用例测试即将运行时调用
        :return:
        """
        super().startTest(test)
        self.start_time = time.time()
        self.outputBuffer = StringIO()
        stdout_redirector.fp = self.outputBuffer
        stderr_redirector.fp = self.outputBuffer
        self.sys_stdout = sys.stdout
        self.sys_stderr = sys.stderr
        sys.stdout = stdout_redirector
        sys.stderr = stderr_redirector

    def complete_output(self):
        if self.sys_stdout:
            sys.stdout = self.sys_stdout
            sys.stderr = self.sys_stderr
            self.sys_stdout = None
            self.sys_stderr = None
        return self.outputBuffer.getvalue()

    def stopTest(self, test):
        """
        当测试用列执行完成后进行调用
        :return:
        """
        # 获取用例的执行时间
        test.run_time = '{:.3}s'.format((time.time() - self.start_time))
        test.class_name = test.__class__.__qualname__
        test.method_name = test.__dict__['_testMethodName']
        test.method_doc = test.shortDescription()
        self.fields['results'].append(test)
        self.fields["testClass"].add(test.class_name)

        self.complete_output()

    def stopTestRun(self, title=None):
        """
        测试用例执行完手动调用统计测试结果的相关数据
        :param title:
        :return:
        """
        self.fields['fail'] = len(self.failures)
        self.fields['error'] = len(self.errors)
        self.fields['skip'] = len(self.skipped)
        self.fields['all'] = sum(
            [self.fields['fail'], self.fields['error'], self.fields['skip'], self.fields['success']])
        self.fields['testClass'] = list(self.fields['testClass'])

    def addSuccess(self, test):
        """用例执行通过，成功数量+1"""
        self.fields["success"] += 1
        test.state = '成功'
        log.info("{}执行——>【通过】\n".format(test))
        logs = [getattr(test, 'base_info'),
                getattr(test, 'requests_log_info'),
                getattr(test, 'response_log_info')]
        log.debug("当前运行环境全局变量有：\n{}\n".format(json.dumps(ENV, ensure_ascii=False, indent=2)))
        log.debug("当前运行环境局部变量有：\n{}\n".format(json.dumps(getattr(test, 'env'), ensure_ascii=False, indent=2)))
        output = self.complete_output()
        logs.append(output)
        test.run_info = logs

    def addFailure(self, test, err):
        """
        :param test: 测试用例
        :param err:  错误信息
        :return:
        """
        super().addFailure(test, err)
        logs = [getattr(test, 'base_info'),
                getattr(test, 'requests_log_info'),
                getattr(test, 'response_log_info')]
        test.state = '失败'
        log.debug("当前运行环境全局变量有：\n{}\n".format(json.dumps(ENV, ensure_ascii=False, indent=2)))
        log.debug("当前运行环境局部变量有：\n{}\n".format(json.dumps(getattr(test, 'env'), ensure_ascii=False, indent=2)))
        log.warning("{}执行——>【失败】\n".format(test))
        # 保存错误信息
        output = self.complete_output()
        logs.append(output)
        # logs.extend(traceback.format_exception(*err))
        logs.append(err[1])
        log.warning(err[1])
        test.run_info = logs

    def addSkip(self, test, reason):
        """
        修改跳过用例的状态
        :param test:测试用例
        :param reason: 相关信息
        :return: None
        """
        super().addSkip(test, reason)
        test.state = '跳过'
        log.info("{}执行--【跳过Skip】\n".format(test))
        logs = [reason]
        test.run_info = logs

    def addError(self, test, err):
        """
        修改错误用例的状态
        :param test: 测试用例
        :param err:错误信息
        :return:
        """
        super().addError(test, err)
        test.state = '错误'
        logs = []
        # logs.extend(traceback.format_exception(*err))
        log.error('\n' + "".join(traceback.format_exception(*err)))
        log.debug("当前运行环境全局变量有：\n{}\n".format(json.dumps(ENV, ensure_ascii=False, indent=2)))
        log.debug("当前运行环境局部变量有：\n{}\n".format(json.dumps(getattr(test, 'env'), ensure_ascii=False, indent=2)))
        logs.append(err[1])
        log.error(err[1])

        log.error("{}执行——>【错误Error】\n".format(test))
        test.run_info = logs
        if test.__class__.__qualname__ == '_ErrorHolder':
            test.run_time = 0
            res = re.search(r'(.*)\(.*\.(.*)\)', test.description)
            test.class_name = res.group(2)
            test.method_name = res.group(1)
            test.method_doc = test.shortDescription()
            self.fields['results'].append(test)
            self.fields["testClass"].add(test.class_name)
        else:
            output = self.complete_output()
            logs.append(output)


class ReRunResult(TestResult):

    def __init__(self, count, interval):
        super().__init__()
        self.count = count
        self.interval = interval
        self.run_cases = []

    def startTest(self, test):
        if not hasattr(test, "count"):
            super().startTest(test)

    def stopTest(self, test):
        if test not in self.run_cases:
            self.run_cases.append(test)
            super().stopTest(test)

    def addFailure(self, test, err):
        """
        :param test: 测试用例
        :param err:  错误信息
        :return:
        """
        if not hasattr(test, 'count'):
            test.count = 0
        if test.count < self.count:
            test.count += 1
            sys.stderr.write("{}执行——>【失败Failure】\n".format(test))
            for string in traceback.format_exception(*err):
                sys.stderr.write(string)
            sys.stderr.write("================{}重运行第{}次================\n".format(test, test.count))

            time.sleep(self.interval)
            test.run(self)
        else:
            super().addFailure(test, err)
            if test.count != 0:
                sys.stderr.write("================重运行{}次完毕================\n".format(test.count))

    def addError(self, test, err):
        """
        修改错误用例的状态
        :param test: 测试用例
        :param err:错误信息
        :return:
        """
        if not hasattr(test, 'count'):
            test.count = 0
        if test.count < self.count:
            test.count += 1
            sys.stderr.write("{}执行——>【错误Error】\n".format(test))
            for string in traceback.format_exception(*err):
                sys.stderr.write(string)
            sys.stderr.write("================{}重运行第{}次================\n".format(test, test.count))
            time.sleep(self.interval)
            test.run(self)
        else:
            super().addError(test, err)
            if test.count != 0:
                sys.stderr.write("================重运行{}次完毕================\n".format(test.count))
