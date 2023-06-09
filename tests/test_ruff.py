# Copyright (C) 2020-2022 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
# pylint: disable-all

import unittest
from pathlib import Path
from unittest import TestCase
from unittest.mock import patch

from autohooks.api.git import StatusEntry

from autohooks.plugins.ruff.ruff import check_ruff_installed, precommit


def get_test_config_path(name):
    return Path(__file__).parent / name


class AutohooksPylintTestCase(TestCase):
    def test_ruff_installed(self):
        with self.assertRaises(RuntimeError), patch(
            "importlib.util.find_spec", return_value=None
        ):
            check_ruff_installed()

    @patch("autohooks.plugins.ruff.ruff.ok")
    def test_precommit_no_files(self, _ok_mock):
        ret = precommit()
        self.assertFalse(ret)

    @unittest.skip("still to do")
    def test_precommit_errors(
        self,
        staged_mock,
        _error_mock,
        _out_mock,
        _ok_mock,  # _mock_stdout
    ):
        ret = precommit()
        self.assertTrue(ret)

    @patch("autohooks.plugins.ruff.ruff.ok")
    @patch("autohooks.plugins.ruff.ruff.out")
    @patch("autohooks.plugins.ruff.ruff.error")
    @patch("autohooks.plugins.ruff.ruff.get_staged_status")
    def test_precommit_ok(
        self,
        staged_mock,
        _error_mock,
        _out_mock,
        _ok_mock,  # _mock_stdout
    ):
        test_case_list = [
            "test_ruff.exe",
            str(Path(__file__)),
        ]
        for test_case in test_case_list:
            with self.subTest(test_case):
                staged_mock.return_value = [
                    StatusEntry(
                        status_string=f"M  {test_case}",
                        root_path=Path(__file__).parent,
                    )
                ]
                ret = precommit()
                # Returncode 0 -> no errors
                self.assertFalse(ret)
