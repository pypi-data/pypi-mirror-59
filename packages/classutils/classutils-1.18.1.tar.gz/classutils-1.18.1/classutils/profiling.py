# -*- coding: utf-8 -*-

import logging_helper; logging = logging_helper.setup_logging()

import cProfile
import StringIO
import pstats
from classutils.decorators import deprecated

# NOTE: This file is DEPRACATED in favour of the decorator!


class ProfilingMixIn(object):

    u"""
    Add this mixin to a class to make profiling parts of the code simple.
    Just add a call to enable_profiling immediately before the code you
    want to profile and add a call to disable_profiling_and_log_pstats
    immediately after.
    """

    @deprecated
    def enable_profiling(self):
        self._profile = cProfile.Profile()
        self._profile.enable()

    @deprecated
    def disable_profiling_and_log_pstats(self,
                                         sortby=u'cumulative'):
        self._profile.disable()
        s = StringIO.StringIO()
        ps = pstats.Stats(self._profile, stream=s).sort_stats(sortby)
        ps.print_stats()
        logging.info(s.getvalue())
