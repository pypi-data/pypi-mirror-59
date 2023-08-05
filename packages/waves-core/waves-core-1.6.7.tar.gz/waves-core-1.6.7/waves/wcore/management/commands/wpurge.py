from __future__ import unicode_literals, absolute_import

import logging
import os

from waves.wcore.management.daemoncommand import DaemonCommand
from waves.wcore.management.runner import PurgeDaemon
from waves.wcore.settings import waves_settings

logger = logging.getLogger('waves.daemon')


class Command(DaemonCommand):
    """
    Dedicated command to summarize current WAVES specific settings
    """
    help = 'Managing WAVES job queue states'
    SLEEP_TIME = 2
    pidfile = os.path.join(waves_settings.DATA_ROOT, 'waves_purge.pid')
    pidfile_timeout = 5
    _class = PurgeDaemon
