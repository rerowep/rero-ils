# -*- coding: utf-8 -*-
#
# RERO ILS
# Copyright (C) 2021 RERO
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

"""Permissions for stats."""

from functools import wraps

from flask import abort
from flask_login import current_user

from rero_ils.modules.permissions import RecordPermission

from ..permissions import record_permission_factory
from ...permissions import admin_permission, monitoring_permission


class StatPermission(RecordPermission):
    """Stat permissions."""

    @classmethod
    def list(cls, user, record=None):
        """List permission check.

        :param user: Logged user.
        :param record: Record to check.
        :return: True is action can be done.
        """
        # Operation allowed only for admin members
        return admin_permission.require().can() \
            or monitoring_permission.require().can()

    @classmethod
    def read(cls, user, record):
        """Read permission check.

        :param user: Logged user.
        :param record: Record to check.
        :return: True is action can be done.
        """
        return admin_permission.require().can() \
            or monitoring_permission.require().can()

    @classmethod
    def create(cls, user, record=None):
        """Create permission check.

        :param user: Logged user.
        :param record: Record to check.
        :return: True is action can be done.
        """
        return False

    @classmethod
    def update(cls, user, record):
        """Update permission check.

        :param user: Logged user.
        :param record: Record to check.
        :return: True is action can be done.
        """
        return False

    @classmethod
    def delete(cls, user, record):
        """Delete permission check.

        :param user: Logged user.
        :param record: Record to check.
        :return: True if action can be done.
        """
        return False


def stats_ui_permission_factory(record, *args, **kwargs):
    """Permission for stats detailed view."""
    return record_permission_factory(
            action='read', record=record, cls=StatPermission)


def check_logged_as_admin(fn):
    """Decorator to check if the current logged user is logged as an admin.

    If no user is connected: return 401 (unauthorized)
    If current logged user has not the `admin` role: return 403 (forbidden)
    """
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if not current_user.is_authenticated:
            abort(401)
        if not admin_permission.require().can():
            abort(403)
        return fn(*args, **kwargs)
    return wrapper