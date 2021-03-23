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

"""SRU resource."""


from flask import g
from flask_resources.context import resource_requestctx
from flask_resources.parsers import URLArgsParser
from invenio_records_resources.resources import RecordResource, \
    RecordResourceConfig

from .schema import RecordLinksSchema, SearchLinksSchema, SruArgsSchema


class ResourceConfig(RecordResourceConfig):
    """SRU resource configuration."""

    list_route = "/sru"
    item_route = f"{list_route}/<pid_value>"

    links_config = {
        "record": RecordLinksSchema,
        "search": SearchLinksSchema
    }

    request_url_args_parser = {
        "search": URLArgsParser(SruArgsSchema)
    }


class Resource(RecordResource):
    """Custom record resource"."""

    default_config = ResourceConfig

    def search(self):
        """Perform a search over the items."""
        identity = g.identity
        hits = self.service.search(
            identity=identity,
            params=resource_requestctx.url_args,
            links_config=self.config.links_config,
            es_preference=self._get_es_preference()
        )
        return hits.to_dict(), 200

    def read(self):
        """Read an item."""
        item = self.service.read(
            resource_requestctx.route["pid_value"],
            g.identity,
            links_config=self.config.links_config,
        )
        return item.to_dict(), 200
