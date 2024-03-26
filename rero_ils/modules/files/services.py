# -*- coding: utf-8 -*-
#
# RERO ILS
# Copyright (C) 2019-2024 RERO
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


"""Files services."""

from rero_invenio_files.records.services import FileServiceConfig, \
    RecordServiceConfig

from .components import DocumentReindexComponent, OperationLogsComponent, \
    OperationLogsFileComponent
from .permissions import FilePermissionPolicy


class RecordServiceConfig(RecordServiceConfig):
    """File record service."""

    # Common configuration
    permission_policy_cls = FilePermissionPolicy

    # Service components
    components = RecordServiceConfig.components + [OperationLogsComponent]


class RecordFileServiceConfig(FileServiceConfig):
    """Files service configuration."""

    # Common configuration
    permission_policy_cls = FilePermissionPolicy

    # maximum files per buckets
    max_files_count = 1000

    # Service components
    components = FileServiceConfig.components + [
        DocumentReindexComponent, OperationLogsFileComponent]