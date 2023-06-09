# Copyright (C) 2019-2022 Greenbone AG
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
import importlib.util
import subprocess
import sys
from typing import Optional

from autohooks.api import error, ok, out
from autohooks.api.git import get_staged_status, stash_unstaged_changes
from autohooks.config import Config
from autohooks.precommit.run import ReportProgress


def check_ruff_installed() -> None:
    if importlib.util.find_spec("ruff") is None:
        raise RuntimeError(
            "Could not find ruff. Please add ruff to your python environment"
        )


def precommit(
    config: Optional[Config] = None,
    report_progress: Optional[ReportProgress] = None,
    **kwargs,  # pylint: disable=unused-argument
) -> int:
    check_ruff_installed()

    files = [f for f in get_staged_status() if str(f.path).endswith(".py")]

    if not files:
        ok("No staged files to format.")
        return 0

    if report_progress:
        report_progress.init(len(files))

    with stash_unstaged_changes(files):
        ret = 0
        for file in files:
            try:
                subprocess.run(
                    ["ruff", "check", str(file.path)],
                    check=True,
                    capture_output=True,
                )
                ok(f"ruff {str(file.path)}")
            except subprocess.CalledProcessError as e:  # pylint: disable=C0103
                ret = e.returncode
                format_errors = (
                    e.stdout.decode(
                        encoding=sys.getdefaultencoding(), errors="replace"
                    )
                    .rstrip()
                    .split("\n")
                )
                for line in format_errors:
                    if ".py" in line:
                        error(line)
                    else:
                        out(line)
                continue
            finally:
                if report_progress:
                    report_progress.update()

        if ret:
            error("ruff check raised some errors")
        else:
            ok("ruff check was successful")
        return ret
