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

"""SRU resource services."""

from invenio_records_resources.services import RecordService, \
    RecordServiceConfig
from invenio_records_resources.services.records.components import \
    MetadataComponent
from invenio_records_resources.services.records.params import PaginationParam, \
    QueryParser, QueryStrParam, SortParam
from invenio_records_resources.services.records.search import terms_filter

from .parser import SruParser, SruStrParam
# from .identities import system_identity
from .permissions import PermissionPolicy
from .record import Record
from .results import DocumentItem, DocumentList
from .schema import RecordSchema


def _(x):
    """Identity function used to trigger string extraction."""
    return x


class ServiceConfig(RecordServiceConfig):
    """Object service configuration.
    Needs both configs, with File overwritting the record ones.
    """

    permission_policy_cls = PermissionPolicy
    record_cls = Record
    schema = RecordSchema
    result_item_cls = DocumentItem
    result_list_cls = DocumentList

    # # Search configuration
    search_query_parser_cls = SruParser
    search_sort_options = {
        "bestmatch": dict(
            title=_('Best match'),
            fields=['_score'],  # ES defaults to desc on `_score` field
        ),
        "newest": dict(
            title=_('Newest'),
            fields=['-_created'],
        ),
        "oldest": dict(
            title=_('Oldest'),
            fields=['_created'],
        )
    }
    search_params_interpreters_cls = [
        SruStrParam,
        PaginationParam,
        SortParam,
    ]
    search_facets_options = None


class Service(RecordService):
    """Object service."""

    default_config = ServiceConfig

    def search(self, identity, params=None, links_config=None,
               es_preference=None, **kwargs):
        """Search for records matching the querystring."""
        self.require_permission(identity, 'search')

        # Prepare and execute the search
        params = params or {}
        search_result = self._search(
            'search', identity, params, es_preference, **kwargs).execute()

        return self.result_list(
            self,
            identity,
            search_result,
            params,
            links_config=links_config
        )

    def read(self, id_, identity, links_config=None):
        """Retrieve a record."""
        # TODO: change back to this if documents works with
        # invenio-records-resources
        # record = self.record_cls.pid.resolve(id_)
        record = self.record_cls.get_record_by_pid(id_)
        self.require_permission(identity, "read", record=record)

        # Run components
        for component in self.components:
            if hasattr(component, 'read'):
                component.read(identity, record=record)

        return self.result_item(
            self,
            identity,
            record,
            links_config=links_config
        )
