""" Daemonized WAVES system commands """
from __future__ import unicode_literals

import logging
import os
import tempfile

from .daemoncommand import DaemonCommand
from waves.wcore.management.runner import JobQueueRunDaemon, PurgeDaemon
from waves.wcore.settings import waves_settings

logger = logging.getLogger('waves.daemon')


class JobQueueCommand(DaemonCommand):
    """
    Dedicated command to summarize current WAVES specific settings
    """
    help = 'Managing WAVES job queue states'
    SLEEP_TIME = 2
    pidfile = os.path.join(tempfile.gettempdir(), 'waves_queue.pid')
    pidfile_timeout = 5
    _class = JobQueueRunDaemon

    def handle(self, **options):
        import warnings
        warnings.warn("This method is deprecated: please use ./manage.py wqueue start instead")
        exit(0)


class PurgeDaemonCommand(DaemonCommand):
    help = 'Clean up old jobs '
    SLEEP_TIME = 86400
    pidfile_path = os.path.join(waves_settings.DATA_ROOT, 'waves_clean.pid')
    _class = PurgeDaemon

    def handle(self, **options):
        import warnings
        warnings.warn("This method is deprecated: please use ./manage.py wpurge start instead")
        exit(0)
