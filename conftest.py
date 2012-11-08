#!/usr/bin/env python

import sys
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
    pytest_mozwebqa.TestSetup.product_version = item.config.option.product_version
    pytest_mozwebqa.TestSetup.test_cleanup = item.config.option.test_cleanup

    # Setup test logging
    setup_logger(item.config.option.verbose,
        item.config.option.debug,
        item.config.option.logfile)

def pytest_addoption(parser):
    """
    Add option to the py.test command line, option is specific to
    this project.
    """
    parser.addoption("--project",
                     action="store",
                     dest='project',
                     metavar='str',
                     default=None,
                     help="Specify project (e.g. sam, headpin, katello, katello.cfse, aeolus, cfce)")

    parser.addoption("--logfile",
                     action="store",
                     dest='logfile',
                     metavar='str',
                     default='cloudforms_test.log',
                     help="Specify a file to record logging information (default: %default)")

    parser.addoption("--org",
                     action="store",
                     dest='org',
                     metavar='str',
                     default="ACME_Corporation",
                     help="Specify an organization to use for testing (default: %default)")

    parser.addoption("--product_version",
                     action="store",
                     dest='product_version',
                     metavar='str',
                     default='1.1',
                     help="Specify product version number (default: %default)")

    parser.addoption("--test_cleanup",
                     action="store_true",
                     dest='test_cleanup',
                     metavar='bool',
                     default=False,
                     help="Specify whether to cleanup after test completion (default: %default)")


def pytest_funcarg__mozwebqa(request):
    """Load mozwebqa plugin
    """
    pytest_mozwebqa = py.test.config.pluginmanager.getplugin("mozwebqa")
    return pytest_mozwebqa.TestSetup(request)
