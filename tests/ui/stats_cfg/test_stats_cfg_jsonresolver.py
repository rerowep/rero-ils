# -*- coding: utf-8 -*-
#
# RERO ILS
# Copyright (C) 2019-2023 RERO
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, version 3 of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

"""Statistics configuration JSON Resolver tests."""

import pytest
from invenio_records.api import Record
from jsonref import JsonRefError


def test_stats_cfg_jsonresolver(stats_cfg_martigny):
    """Test statistics configuration json resolver."""
    rec = Record.create({
        'stats_cfg': {'$ref': 'https://bib.rero.ch/api/stats_cfg/stats_cfg1'}
    })
    assert rec.replace_refs().get('stats_cfg') == {
        'type': 'stacfg', 'pid': 'stats_cfg1'
    }

    # deleted record
    stats_cfg_martigny.delete()
    with pytest.raises(JsonRefError):
        rec.replace_refs().dumps()

    # non existing record
    rec = Record.create({
        'stats_cfg': {'$ref': 'https://bib.rero.ch/api/stats_cfg/n_e'}
    })
    with pytest.raises(JsonRefError):
        rec.replace_refs().dumps()
