# encoding=utf8
from __future__ import unicode_literals
from future.utils import iteritems

from builtins import str
from allure import MASTER_HELPER as ALLURE_HELPER

try:
    from ConfigParser import ConfigParser, NoSectionError  # PY2
except:
    from configparser import ConfigParser, NoSectionError  # PY3
from copy import deepcopy
import re

from allure.structure import TestLabel

ALLURE_PREFIX_MARKER = 'allure_prefix'
TESTRAIL_PREFIX_MARKER = 'testrail'
CASE_URL = "{}/index.php?/cases/view/"
DEFAULT_TESTRAIL_CONFIG_FILE = "testrail.cfg"
PARAMETERS = {}


class Data:
    """Класс для хранения информации по параметрам теста."""

    pass


def pytest_runtest_setup(item):
    """Вызывается для копирования параметризации теста перед его запуском."""
    request = item._request
    parameters = {}
    for key, value in sorted(iteritems(request._arg2fixturedefs)):
        if value and value[0].params:
            arg_value = request.getfuncargvalue(key)
            if isinstance(arg_value, bytes):
                arg_value = arg_value.decode('utf-8')
            parameters.update({key: arg_value})
    Data.PARAMETERS = deepcopy(parameters)


def pytest_runtest_makereport(item, call):
    """Добавление префикса теста и ссылки на TestRail в allure."""
    if call.when == 'call' and ALLURE_HELPER._allurelistener:
        request = item._request
        prefixes = ""
        parameters = ""
        allure_prefix_marker = request.node.get_closest_marker(ALLURE_PREFIX_MARKER)
        if allure_prefix_marker is not None:
            for prefix in allure_prefix_marker.kwargs.get('ids'):
                prefixes += "[{}]".format(prefix)
            prefixes += " "
        for key, value in sorted(iteritems(Data.PARAMETERS)):
            parameters = u"{parameters}, {key}={value}".format(parameters=parameters,
                                                               key=key,
                                                               value=value)
        parameters = re.sub(r'^,\s', '', parameters)
        method_name = re.search(r"(?<=^)[^\[]*", str(ALLURE_HELPER._allurelistener.test.name)).group(0)
        test_name = u"{prefixes}{method_name}({parameters})".format(prefixes=prefixes,
                                                                    method_name=method_name,
                                                                    parameters=parameters)
        ALLURE_HELPER._allurelistener.test.name = test_name

        testrail_prefix_marker = request.node.get_closest_marker(TESTRAIL_PREFIX_MARKER)
        if testrail_prefix_marker is not None:
            try:
                cfg_file_path = request.config.getoption('--tr-config', DEFAULT_TESTRAIL_CONFIG_FILE)
                url = request.config.getoption('--tr-url', None)
                if not url:
                    configparser = ConfigParser()
                    configparser.read(cfg_file_path)
                    url = configparser.get('API', 'url')
                case_url = CASE_URL.format(url)
                for testrail_id in testrail_prefix_marker.kwargs.get('ids'):
                    link = case_url + re.sub(r'\D', '', str(testrail_id))
                    ALLURE_HELPER._allurelistener.test.labels.append(TestLabel(name='testId', value=link))
            except NoSectionError as e:
                print("Can't add testrail link. Make sure that you have testrail.cfg in the "
                      "project root or set testrail.cfg path via --tr-config", e)
