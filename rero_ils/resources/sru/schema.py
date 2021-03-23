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

"""SRU resource schema."""

from invenio_records_resources.resources import search_link_params, \
    search_link_when
from invenio_records_resources.resources.records.schemas_url_args import \
    SearchURLArgsSchema
from invenio_records_resources.services.records.schema import BaseRecordSchema
from marshmallow import Schema, fields, post_load, validate
from marshmallow_utils.fields import Link
from uritemplate import URITemplate


class RecordSchema(BaseRecordSchema):
    """Schema for records v1 in JSON."""

    metadata = fields.Dict()


class RecordLinksSchema(Schema):
    """Schema for a record's links."""

    # NOTE:
    #   - /api prefix is needed here because above are mounted on /api
    self_ = Link(
        template=URITemplate("/api/SRU/{pid_value}"),
        permission="read",
        # TODO: change back to this if documents works with
        # invenio-records-resources
        # params=lambda record: {'pid_value': record.pid.pid_value},
        params=lambda record: {'pid_value': record.pid},
        data_key="self"  # To avoid using self since is python reserved key
    )


class SearchLinksSchema(Schema):
    """Schema for a search result's links."""

    # NOTE:
    #   - /api prefix is needed here because api routes are mounted on /api
    self = Link(
        template=URITemplate("/api/SRU{?params*}"),
        permission="search",
        params=search_link_params(0),
    )
    prev = Link(
        template=URITemplate("/api/SRU{?params*}"),
        permission="search",
        params=search_link_params(-1),
        when=search_link_when(-1)
    )
    next = Link(
        template=URITemplate("/api/SRU{?params*}"),
        permission="search",
        params=search_link_params(+1),
        when=search_link_when(+1)
    )


class SruArgsSchema(SearchURLArgsSchema):
    """Schema for search URL args."""

    sort = fields.String()
    page = fields.Int(validate=validate.Range(min=1))
    size = fields.Int(validate=validate.Range(min=1))
    query = fields.String()
    operation = fields.String(validate=validate.Equal('searchRetrieve'))
    version = fields.Float(validate=validate.Equal(1.1))
