# ##############################################################################
#  Author: echel0n <echel0n@sickrage.ca>
#  URL: https://sickrage.ca/
#  Git: https://git.sickrage.ca/SiCKRAGE/sickrage.git
#  -
#  This file is part of SiCKRAGE.
#  -
#  SiCKRAGE is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#  -
#  SiCKRAGE is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  -
#  You should have received a copy of the GNU General Public License
#  along with SiCKRAGE.  If not, see <http://www.gnu.org/licenses/>.
# ##############################################################################

import os
import re
from abc import ABC

from tornado.web import authenticated

import sickrage
from sickrage.core.helpers import read_file_buffered
from sickrage.core.webserver.handlers.base import BaseHandler


class LogsHandler(BaseHandler, ABC):
    def initialize(self):
        self.logs_menu = [
            {'title': _('Clear Warnings'), 'path': '/logs/clearWarnings/',
             'requires': self.have_warnings(),
             'icon': 'fas fa-trash'},
            {'title': _('Clear Errors'), 'path': '/logs/clearErrors/',
             'requires': self.have_errors(),
             'icon': 'fas fa-trash'},
        ]

    @authenticated
    def get(self, *args, **kwargs):
        level = self.get_argument('level', sickrage.app.log.ERROR)

        return self.render(
            "/logs/errors.mako",
            header="Logs &amp; Errors",
            title="Logs &amp; Errors",
            topmenu="system",
            submenu=self.logs_menu,
            logLevel=level,
            controller='logs',
            action='errors'
        )

    def have_errors(self):
        if len(sickrage.app.log.error_viewer.get()) > 0:
            return True

    def have_warnings(self):
        if len(sickrage.app.log.warning_viewer.get()) > 0:
            return True


class LogsClearWarningsHanlder(BaseHandler, ABC):
    @authenticated
    def get(self, *args, **kwargs):
        sickrage.app.log.warning_viewer.clear()
        self.redirect("/logs/view/")


class LogsClearErrorsHanlder(BaseHandler, ABC):
    @authenticated
    def get(self, *args, **kwargs):
        sickrage.app.log.error_viewer.clear()
        self.redirect("/logs/view/")


class LogsClearAllHanlder(BaseHandler, ABC):
    @authenticated
    def get(self, *args, **kwargs):
        sickrage.app.log.warning_viewer.clear()
        sickrage.app.log.error_viewer.clear()
        self.redirect("/logs/view/")


class LogsViewHandler(BaseHandler, ABC):
    @authenticated
    def get(self, *args, **kwargs):
        min_level = self.get_argument('minLevel', None) or sickrage.app.log.INFO
        log_filter = self.get_argument('logFilter', '')
        log_search = self.get_argument('logSearch', '')
        max_lines = self.get_argument('maxLines', None) or 500

        log_name_filters = {
            '': 'No Filter',
            'DAILYSEARCHER': _('Daily Searcher'),
            'BACKLOG': _('Backlog'),
            'SHOWUPDATER': _('Show Updater'),
            'VERSIONUPDATER': _('Check Version'),
            'SHOWQUEUE': _('Show Queue'),
            'SEARCHQUEUE': _('Search Queue'),
            'FINDPROPERS': _('Find Propers'),
            'POSTPROCESSOR': _('Postprocessor'),
            'SUBTITLESEARCHER': _('Find Subtitles'),
            'TRAKTSEARCHER': _('Trakt Checker'),
            'EVENT': _('Event'),
            'ERROR': _('Error'),
            'TORNADO': _('Tornado'),
            'Thread': _('Thread'),
            'MAIN': _('Main'),
        }

        log_files = [sickrage.app.log.logFile] + \
                    ["{}.{}".format(sickrage.app.log.logFile, x) for x in
                     range(int(sickrage.app.log.logNr))]

        levels_filtered = '|'.join(
            [x for x in sickrage.app.log.logLevels.keys() if
             sickrage.app.log.logLevels[x] >= int(min_level)])

        log_regex = re.compile(
            r"(?P<entry>^\d+\-\d+\-\d+\s+\d+\:\d+\:\d+\s+(?:{})[\s\S]+?(?:{})[\s\S]+?$)".format(levels_filtered,
                                                                                                log_filter),
            re.S + re.M)

        data = []

        try:
            for logFile in [x for x in log_files if os.path.isfile(x)]:
                data += list(reversed(re.findall("((?:^.+?{}.+?$))".format(log_search),
                                                 "\n".join(next(read_file_buffered(logFile, reverse=True)).splitlines()),
                                                 re.M + re.I)))
                max_lines -= len(data)
                if len(data) == max_lines:
                    raise StopIteration
        except StopIteration:
            pass

        return self.render(
            "/logs/view.mako",
            header="Log File",
            title="Logs",
            topmenu="system",
            logLines="\n".join(log_regex.findall("\n".join(data))),
            minLevel=int(min_level),
            logNameFilters=log_name_filters,
            logFilter=log_filter,
            logSearch=log_search,
            controller='logs',
            action='view'
        )
