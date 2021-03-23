# -*- coding: utf-8 -*-
#
# RERO ILS
# Copyright (C) 2020 RERO
# Copyright (C) 2020 UCLouvain
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

"""SRU resource permissions."""

from invenio_records_permissions import RecordPermissionPolicy
from invenio_records_permissions.generators import AnyUser, Disable


class PermissionPolicy(RecordPermissionPolicy):
    """Objects permission policy. All actions allowed."""

    can_search = [AnyUser()]
    can_create = [Disable()]
    can_read = [AnyUser()]
    can_update = [Disable()]
    can_delete = [Disable()]
    can_read_files = [Disable()]
    can_update_files = [Disable()]
