# -*- coding: utf-8 -*-
"""
Tests for helpers functions/classes.
"""

__author__ = 'Grzegorz Latuszek, Marcin Usielski'
__copyright__ = 'Copyright (C) 2018-2019, Nokia'
__email__ = 'grzegorz.latuszek@nokia.com, marcin.usielski@nokia.com'

import mock
import pytest


def test_instance_id_returns_id_in_hex_form_without_0x():
    from moler.helpers import instance_id
    from six.moves import builtins
    # 0xf0a1 == 61601 decimal
    with mock.patch.object(builtins, "id", return_value=61601):
        instance = "moler object"
        assert "0x" not in instance_id(instance)
        assert instance_id(instance) == "f0a1"


def test_converterhelper_k():
    from moler.util.converterhelper import ConverterHelper
    converter = ConverterHelper.get_converter_helper()
    bytes_value, value_in_units, unit = converter.to_bytes("2.5K")
    assert 2560 == bytes_value
    assert 2.5 == value_in_units
    assert 'k' == unit


def test_converterhelper_m():
    from moler.util.converterhelper import ConverterHelper
    converter = ConverterHelper.get_converter_helper()
    bytes_value, value_in_units, unit = converter.to_bytes(".3m", False)
    assert 300000 == bytes_value
    assert 0.3 == value_in_units
    assert 'm' == unit


def test_converterhelper_wrong_unit():
    from moler.util.converterhelper import ConverterHelper
    converter = ConverterHelper.get_converter_helper()
    with pytest.raises(ValueError):
        converter.to_bytes("3UU", False)


def test_converterhelper_seconds():
    from moler.util.converterhelper import ConverterHelper
    converter = ConverterHelper.get_converter_helper()
    value, value_in_units, unit = converter.to_seconds_str("3m")
    assert 180 == value
    assert 3 == value_in_units
    assert 'm' == unit


def test_converterhelper_seconds_ms():
    from moler.util.converterhelper import ConverterHelper
    converter = ConverterHelper.get_converter_helper()
    value = converter.to_seconds(0.408, "ms")
    assert pytest.approx(0.000408, 0.000001) == value


def test_converterhelper_seconds_wrong_unit():
    from moler.util.converterhelper import ConverterHelper
    converter = ConverterHelper.get_converter_helper()
    with pytest.raises(ValueError):
        converter.to_seconds_str("3UU")


def test_copy_list():
    from moler.helpers import copy_list
    src = [1]
    dst = copy_list(src, deep_copy=True)
    assert src == dst
    dst[0] = 2
    assert src != dst


def test_copy_dict():
    from moler.helpers import copy_dict
    src = {'a': 1}
    dst = copy_dict(src, deep_copy=True)
    assert src == dst
    dst['a'] = 2
    assert src != dst


def test_regex_helper():
    from moler.cmd import RegexHelper
    regex_helper = RegexHelper()
    assert regex_helper is not None
    match = regex_helper.match(r"\d+(\D+)\d+", "111ABC222")
    assert match is not None
    assert match == regex_helper.get_match()
    assert regex_helper.group(1) == "ABC"


def test_groups_at_regex_helper():
    import re
    from moler.cmd import RegexHelper
    regex_helper = RegexHelper()
    if regex_helper.search_compiled(re.compile(r"(\d+)_([A-Z]+)(\w+),(\d+)"), "111_ABCef,222"):
        ones, uppers, lowers, twos = regex_helper.groups()
    assert ones == '111'
    assert uppers == 'ABC'
    assert lowers == 'ef'
    assert twos == '222'
