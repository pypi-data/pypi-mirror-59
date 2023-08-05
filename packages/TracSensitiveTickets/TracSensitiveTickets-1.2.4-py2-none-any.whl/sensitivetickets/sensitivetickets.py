# -*- coding: utf-8 -*-
#
# Copyright (C) 2008 Sebastian Benthall
# Copyright (C) 2009 Jeff Hammel
# Copyright (C) 2010 Rowan Wookey
# Copyright (C) 2012-2013 Daniel Kahn Gillmor <dkg@fifthhorseman.net>
# Copyright (C) 2016 Ryan J Ollos <ryan.j.ollos@gmail.com>
# All rights reserved.
#
# This software is licensed as described in the file COPYING, which
# you should have received as part of this distribution.
#

from trac.config import BoolOption
from trac.core import Component, implements
from trac.env import IEnvironmentSetupParticipant
from trac.perm import IPermissionPolicy, IPermissionRequestor
from trac.resource import ResourceNotFound
from trac.ticket.api import ITicketManipulator
from trac.ticket.model import Ticket
from trac.timeline.api import ITimelineEventProvider
from trac.util import as_bool, as_int, to_list
from trac.util.datefmt import from_utimestamp, to_utimestamp


class SensitiveTicketsPolicy(Component):
    """Prevent public access to security sensitive tickets.

    Add the SENSITIVE_VIEW permission as a pre-requisite for any
    other permission check done on tickets that have been marked (through
    the UI) as "Sensitive".

    Enable the plugin in trac.ini with:

    {{{
    [components]
    sensitivetickets.* = enabled
    }}}

    Once this plugin is enabled, you'll have to insert it at the appropriate
    place in your list of permission policies, e.g.

    {{{
    [trac]
    permission_policies = SensitiveTicketsPolicy, AuthzPolicy,
                          DefaultPermissionPolicy, LegacyAttachmentPolicy
    }}}

    This plugin also adds the SENSITIVE_ACTIVITY_VIEW permission,
    which is narrower in scope than SENSITIVE_VIEW.  Accounts with
    SENSITIVE_ACTIVITY_VIEW will be able to see activity on sensitive
    material in the timeline, but will only be able to identify it by
    ticket number, comment number, and timestamp.  All other content
    will be redacted.

    SENSITIVE_ACTIVITY_VIEW can be useful (for example) for providing
    a notification daemon the ability to tell that some activity
    happened without leaking the content of that activity.
    """

    implements(IEnvironmentSetupParticipant, IPermissionPolicy,
               IPermissionRequestor, ITicketManipulator,
               ITimelineEventProvider)

    allow_reporter = BoolOption(
        'sensitivetickets', 'allow_reporter', False,
        """Whether the reporter of a sensitive ticket should have access to
        that ticket even if they do not have SENSITIVE_VIEW privileges.
        """)

    allow_cc = BoolOption(
        'sensitivetickets', 'allow_cc', False,
        """Whether users listed in the cc field of a sensitive ticket
        should have access to that ticket even if they do not have
        SENSITIVE_VIEW privileges.
        """)

    allow_owner = BoolOption(
        'sensitivetickets', 'allow_owner', True,
        """Whether the owner of a sensitive ticket should have access to
        that ticket even if they do not have SENSITIVE_VIEW privileges.
        """)

    limit_sensitivity = BoolOption(
        'sensitivetickets', 'limit_sensitivity', False,
        """With limit_sensitivity set to true, users cannot set the
        sensitivity checkbox on a ticket unless they are authenticated
        and would otherwise be permitted to deal with the ticket if it
        were marked sensitive. This prevents users from marking the tickets
        of other users as "sensitive".
        """)

    # IPermissionPolicy methods

    def check_permission(self, action, username, resource, perm):
        # We add the 'SENSITIVE_VIEW' pre-requisite for any action
        # other than 'SENSITIVE_VIEW' itself, as this would lead
        # to recursion.
        if action == 'SENSITIVE_VIEW':
            return

        # Check whether we're dealing with a ticket resource
        while resource:
            if resource.realm == 'ticket':
                break
            resource = resource.parent

        if resource and resource.realm == 'ticket' and \
                resource.id is not None:
            tid = as_int(resource.id, None)
            if tid is not None:
                bypass = False
                try:
                    ticket = Ticket(self.env, int(resource.id))
                except ResourceNotFound:
                    sensitive = 1  # Fail safe to prevent a race condition.
                else:
                    sensitive = ticket['sensitive']
                    if as_bool(sensitive):
                        bypass = self.bypass_sensitive_view(ticket, username)

                if as_bool(sensitive):
                    if 'SENSITIVE_VIEW' not in perm and not bypass:
                        return False

    # IPermissionRequestor methods

    def get_permission_actions(self):
        return ['SENSITIVE_VIEW', 'SENSITIVE_ACTIVITY_VIEW']

    # ITicketManipulator methods:

    def validate_ticket(self, req, ticket):
        if not self.limit_sensitivity:
            return []
        sensitive = 1
        try:
            sensitive = ticket['sensitive']
        except:
            pass
        if as_bool(sensitive):
            if req.authname is 'anonymous':
                return [(None, "Sorry, you cannot create or update a "
                               "sensitive ticket without at least logging "
                               "in first")]
            if self.bypass_sensitive_view(ticket, req.authname):
                return []
            req.perm(ticket.resource).require('SENSITIVE_VIEW')
        return []

    # IEnvironmentSetupParticipant methods

    def environment_created(self):
        if self.environment_needs_upgrade():
            self.upgrade_environment()

    def environment_needs_upgrade(self):
        return 'sensitive' not in self.config['ticket-custom']

    def upgrade_environment(self):
        custom = self.config['ticket-custom']
        custom.set('sensitive', 'checkbox')
        custom.set('sensitive.label', "Sensitive")
        custom.set('sensitive.value', '0')
        self.config.save()

    # ITimelineEventProvider methods

    def get_timeline_filters(self, req):
        if 'SENSITIVE_ACTIVITY_VIEW' in req.perm and \
                'SENSITIVE_VIEW' not in req.perm:
            yield ('sensitive_activity', 'Activity on sensitive tickets',
                   False)

    def get_timeline_events(self, req, start, stop, filters):
        if 'sensitive_activity' in filters and \
                'SENSITIVE_ACTIVITY_VIEW' in req.perm and \
                'SENSITIVE_VIEW' not in req.perm:
            ts_start = to_utimestamp(start)
            ts_stop = to_utimestamp(stop)

            if 'ticket_details' in filters:
                # Only show sensitive ticket changes (edits, closure) if
                # the 'ticket_details' filter is on.
                for tid, t, cid in self.env.db_query("""
                        SELECT DISTINCT t.id,tc.time,tc.oldvalue
                        FROM ticket_change tc
                         INNER JOIN ticket t ON t.id = tc.ticket
                          AND tc.time >= %s AND tc.time <= %s AND tc.field = %s
                         INNER JOIN ticket_custom td ON t.id = td.ticket
                          AND td.name = %s AND td.value = %s
                        ORDER BY tc.time
                        """, (ts_start, ts_stop, 'comment', 'sensitive', '1')):
                    yield ('sensitive_activity', from_utimestamp(t),
                           'redacted', (tid, cid))
            # Always show new sensitive tickets.
            for tid, t in self.env.db_query("""
                    SELECT DISTINCT id, time FROM
                    ticket t INNER JOIN ticket_custom tc ON t.id = tc.ticket
                     AND t.time >= %s AND t.time <= %s
                     AND tc.name = %s AND tc.value = %s
                    ORDER BY time
                    """, (ts_start, ts_stop, 'sensitive', '1')):
                yield ('sensitive_activity', from_utimestamp(t), 'redacted',
                       (tid, None))

    def render_timeline_event(self, context, field, event):
        tid, cid = event[3]
        if field == 'title':
            return 'Sensitive Activity'
        elif field == 'description':
            return '[REDACTED]'
        elif field == 'url':
            href = context.href.ticket(tid)
            if cid:
                href += '#comment:' + str(cid)
            return href

    # Private methods

    def bypass_sensitive_view(self, ticket, username):
        """Returns whether the sensitivetickets permission allows a
        bypass of the SENSITIVE_VIEW setting for a given ticket
        """
        if username == 'anonymous':
            return False
        return (self.allow_owner and ticket['owner'] == username) or \
               (self.allow_reporter and ticket['reporter'] == username) or \
               (self.allow_cc and
                username in to_list(ticket['cc'], r'[;,\s]+'))
