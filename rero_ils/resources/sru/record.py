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

"""SRU resource record."""

from copy import deepcopy

from invenio_records_resources.records.systemfields.index import IndexField

from rero_ils.modules.documents.api import Document


class Dumper:
    """Interface for dumpers."""

    def dump(self, record, data):
        """Dump a record that can be used a source document for Elasticsearch.
        The job of this method is to create a Python dictionary from the record
        provided in the argument.
        If you overwrite this method without calling super, then you should
        ensure that you make a deep copy of the record dictionary, to avoid
        that changes to the dump affects the record.
        :param record: The record to dump.
        :param data: The initial dump data passed in by ``record.dumps()``.
        """
        data.update(deepcopy(dict(record)))
        return data

    def load(self, data, record_cls):
        """Load a record from the source document of an Elasticsearch hit.
        The job of this method, is to create a record of type ``record_cls``
        based on the input ``data``.
        :param data: A Python dictionary representing the data to load.
        :param records_cls: The record class to be constructed.
        :returns: A instance of ``record_cls``.
        """
        return record_cls.get_record_by_pid(data.get('pid'))


class Record(Document):
    """Overloades document record, needed by invenio_records-resources."""
    # Index field.
    index = IndexField(
        'documents-documentproject-v1.0.0',
        search_alias='documents'
    )

    # Class-level attribute to specify the default data dumper/loader.
    dumper = Dumper()
