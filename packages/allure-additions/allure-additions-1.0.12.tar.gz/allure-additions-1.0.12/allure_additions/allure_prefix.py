# encoding=utf8

import pytest


def allure_prefix(*prefixes):
    """Добавление маркера префиксов названия теста в Allure."""
    return pytest.mark.allure_prefix(ids=prefixes)
