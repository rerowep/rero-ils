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

"""SRU resource parser."""

import pycql
from elasticsearch_dsl import Q
from invenio_records_resources.services.errors import \
    QuerystringValidationError
from invenio_records_resources.services.records.params import ParamInterpreter, \
    QueryParser
from pycql import ast


class SruStrParam(ParamInterpreter):
    """Evaluate the 'q' parameter."""

    def apply(self, identity, search, params):
        """Evaluate the query str on the search."""
        query_str = params.get('query')
        if not query_str:
            return search

        try:
            parser_cls = self.config.search_query_parser_cls
            query = parser_cls(identity).parse(query_str)
            return search.query(query)
        except SyntaxError:
            # TOOD: raise a proper type of exception
            raise Exception("Failed to parse query.")


class SruParser(QueryParser):
    """Parse query string into a Elasticsearch DSL Q object."""

    pre_mapping = {
        ' and ': ' AND ',
        ' or ': ' OR ',
        ' not ': ' NOT ',
        'dc.title': 'dc_title',
        'dc.possessingInstitution': 'dc_possessingInstitution'
        # 'floatMetaAttribute': 'record_metas__float_meta_attribute',
        # 'intMetaAttribute': 'record_metas__int_meta_attribute',
        # 'strMetaAttribute': 'record_metas__str_meta_attribute',
        # 'datetimeMetaAttribute': 'record_metas__datetime_meta_attribute',
        # 'choiceMetaAttribute': 'record_metas__choice_meta_attribute',
    }
    post_mapping = {
        '__': '.',
        'dc_title': 'autocomplete_title',
        'dc_possessingInstitution': 'library__pid'
        # 'floatMetaAttribute': 'record_metas__float_meta_attribute',
        # 'intMetaAttribute': 'record_metas__int_meta_attribute',
        # 'strMetaAttribute': 'record_metas__str_meta_attribute',
        # 'datetimeMetaAttribute': 'record_metas__datetime_meta_attribute',
        # 'choiceMetaAttribute': 'record_metas__choice_meta_attribute',
    }

    def parse(self, query_str):
        """Parse the query."""
        query_str = self.apply_mapping(query_str, self.pre_mapping)
        query_ast = pycql.parse(query_str)
        query = self.to_filter(query_ast)
        if query:
            query = self.apply_mapping(query, self.post_mapping)
        else:
            # Could not parse the query string try the query string directly
            query = query_str
        print('----->', query_str)
        print('+++++>', query)

        return Q('query_string', query=query, analyze_wildcard=True)

    def apply_mapping(self, query_str, mapping):
        """Apply mapping to query string."""
        for key, value in mapping.items():
            query_str = query_str.replace(key, value)
        return query_str


    def to_filter(self, node):
        """Ast filter."""
        to_filter = self.to_filter
        if isinstance(node, ast.NotConditionNode):
            return negate(to_filter(node.sub_node))
        elif isinstance(node, ast.CombinationConditionNode):
            return combine(
                to_filter(node.lhs),
                to_filter(node.rhs),
                node.op
            )
        elif isinstance(node, ast.ComparisonPredicateNode):
            return compare(
                to_filter(node.lhs),
                to_filter(node.rhs),
                node.op
            )
    #     elif isinstance(node, ast.BetweenPredicateNode):
    #         return filters.between(
    #             to_filter(node.lhs), to_filter(node.low),
    #             to_filter(node.high), node.not_
    #         )
    #     elif isinstance(node, ast.BetweenPredicateNode):
    #         return filters.between(
    #             to_filter(node.lhs), to_filter(node.low),
    #             to_filter(node.high), node.not_
    #         )
        elif isinstance(node, ast.AttributeExpression):
            return node.name

        elif isinstance(node, ast.LiteralExpression):
            return node.value

        return node


def negate(sub_filter):
    """ Negate a filter, opposing its meaning.

    :param sub_filter: the filter to negate
    :return: the negated filter
    """
    return f'-({sub_filter})'


def combine(lhs, rhs, combinator='AND'):
    """ Combine filters using a logical combinator

    :param lhs: the left filter to combine
    :param rhs: the right filter to combine
    :param combinator: a string: "AND" / "OR"
    :return: the combined filter
    """
    assert combinator in ('AND', 'OR')
    return f'({lhs}) {combinator} ({rhs})'


def compare(lhs, rhs=None, op='=', negate_result=False):
    """ Compare a filter with an expression using a comparison operation

    :param lhs: the field to compare
    :param rhs: the filter expression
    :param op: a string denoting the operation.
    :return: a comparison expression object
    """
    result = f'{lhs}{op}{rhs}'
    if op == '=':
        result = f'{lhs}:{rhs}'
    if op == '=' and lhs == 'anywhere':
        result = rhs
    if negate_result:
        result = f' -({result})'
    return result


# def between(lhs, low, high, negate=False):
#     """ Create a filter to match elements that have a value within a
#         certain range.
#
#     :param lhs: the field to compare
#     :param low: the lower value of the range
#     :param high: the upper value of the range
#     :param not_: whether the range shall be inclusive (the default) or
#                  exclusive
#     :return: a comparison expression object
#     """
#     l_op = Operator("<=")
#     g_op = Operator(">=")
#     if negate:
#         return not_(and_(g_op.function(lhs, low), l_op.function(lhs, high)))
#     return and_(g_op.function(lhs, low), l_op.function(lhs, high))
