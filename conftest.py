#!/usr/bin/env python

import sys
import optparse
import logging
import py

def setup_logger(verbose=False, debug=False, logfile=None):
    '''setup logging'''

    # create logger
    logger = logging.getLogger()
    logger.propagate = False

    # log output to stdout by default
    plainformatter = logging.Formatter("%(asctime)s %(levelname)s: %(message)s", "%b %d %H:%M:%S")
    console_stdout = logging.StreamHandler(sys.stdout)
    console_stdout.setFormatter(plainformatter)
    logger.addHandler(console_stdout)

    # define a logging instance for the /var/log/snake.log logfile
    if logfile:
        filelogger = logging.getLogger("filelogging")
        filelogger.propagate = False
        filehandler = logging.FileHandler(logfile, 'a')
        formatter = logging.Formatter("%(asctime)s %(levelname)s: %(message)s", "%b %d %H:%M:%S")
        filehandler.setFormatter(formatter)
        filelogger.addHandler(filehandler)

        # add filelogger to the root logger
        logger.addHandler(filelogger)

    # setup default logLevel
    if debug:
        logger.setLevel(logging.DEBUG)
    elif verbose:
        logger.setLevel(logging.INFO)
    else:
        logger.setLevel(logging.WARN)

def pytest_runtest_setup(item):
    """
    pytest setup
    """
    pytest_mozwebqa = py.test.config.pluginmanager.getplugin("mozwebqa")
    pytest_mozwebqa.TestSetup.project = item.config.option.project
    pytest_mozwebqa.TestSetup.org = item.config.option.org

    # Setup test logging
    setup_logger(item.config.option.verbose,
        item.config.option.debug,
        item.config.option.logfile)

def pytest_addoption(parser):
    """
    Add option to the py.test command line, option is specific to
    this project.
    """

    # Add --logfile option to existing 'termincal reporting' option group
    optgrp = parser.getgroup("terminal reporting")
    optgrp.addoption("--logfile", action="store", dest='logfile',
            default='cloudforms_test.log',
            help="Specify a file to record logging information (default: %default)")

    # Create a general test options
    optgrp = parser.getgroup('general_options', "General Test Options")
    optgrp.addoption("--project", action="store", dest='project', default=None,
            help="Specify project (e.g. sam, headpin, katello, katello.cfse, aeolus, cfce)")

    optgrp.addoption("--project-version", action="store",
            dest='project-version', default='1.1',
            help="Specify project version number (default: %default)")

    optgrp.addoption("--test-cleanup", action="store_true",
            dest='test-cleanup', default=False,
            help="Specify whether to cleanup after test completion (default: %default)")

    # TODO - add parameters for each configure.ini [katello] option
    optgrp = parser.getgroup('katello_options', "Katello Test Options (--project=katello)")
    optgrp.addoption("--org", action="store", dest='org',
            default="ACME_Corporation",
            help="Specify an organization to use for testing (default: %default)")
    optgrp.addoption("--env", action="store", dest='env', default="Dev",
            help="Specify an environment to use for testing (default: %default)")

    # TODO - add parameters for each configure.ini [aeolus] option
    optgrp = parser.getgroup('aeolus_options', "Aeolus Test Options (--project=aeolus)")
    optgrp.addoption("--releasever", action="append", dest='releasever',
            default=['6Server', '5Server'],
            help="Specify which RHEL $releasever values to use when testing images (default: %default)")
    optgrp.addoption("--basearch", action="append", dest='basearch',
            default=['i386', 'x86_64'],
            help="Specify which RHEL $basearch values to use when testing images (default: %default)")

def pytest_funcarg__mozwebqa(request):
    """Load mozwebqa plugin
    """
    pytest_mozwebqa = py.test.config.pluginmanager.getplugin("mozwebqa")
    return pytest_mozwebqa.TestSetup(request)
