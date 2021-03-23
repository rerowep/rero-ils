# -*- coding: utf-8 -*-
#
# RERO ILS
# Copyright (C) 2019 RERO
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

"""SRU resource results."""

from invenio_records_resources.services.records.results import RecordItem, \
    RecordList, _current_host
from marshmallow_utils.links import LinksFactory


class DocumentItem(RecordItem):
    """Single document result."""

    def __init__(self, service, identity, record, errors=None,
                 links_config=None):
        """Constructor."""
        self._errors = errors
        self._identity = identity
        self._links_config = links_config
        self._record = record
        self._service = service
        self._data = None

    @property
    def id(self):
        """Get the record id."""
        return self._record.id

    @property
    def data(self):
        """Property to get the record."""
        if self._data:
            return self._data

        links = LinksFactory(host=_current_host, config=self._links_config)

        self._data = self._service.schema.dump(
            self._identity,
            self._record,
            record=self._record,
            links_namespace="documents",
            links_factory=links,
        )
        self._data.update(self._record)
        return self._data

class DocumentList(RecordList):
    """List of document result."""

    @property
    def hits(self):
        """Iterator over the hits."""
        links = LinksFactory(host=_current_host, config=self._links_config)

        for hit in self._results:
            # Load dump
            record = self._service.record_cls.loads(hit.to_dict())

            # Project the record
            projection = self._service.schema.dump(
                self._identity,
                record,
                pid=record.pid,
                record=record,
                links_namespace="record",
                links_factory=links
            )
            projection.update(record)
            yield projection
