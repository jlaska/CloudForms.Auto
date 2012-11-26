#!/usr/bin/env python

import sys
import optparse
import logging
import ConfigParser
import requests
import re
import string
import pytest
from distutils.version import StrictVersion

# Load test config file
class CloudFormsConfigParser(ConfigParser.SafeConfigParser):
    def getlist(self, section, option):
        return re.split(r'[,\s]+', self.get(section, option))

test_config = CloudFormsConfigParser()
cfg_file = 'cloudforms.cfg'

# Determine if an alternate .cfg file was requested via --config.
# Configuration is loaded prior to inspection of command-line options.
for i,arg in enumerate(sys.argv):
    if re.search(r'^--config\b', arg):
        try:
            cfg_file = arg.split('=',1)[1]
        except IndexError:
            cfg_file = sys.argv[i+1]
        break

# Read configuration, fail is missing
if len(test_config.read(cfg_file)) == 0:
    print "Unable to load config file: %s" % cfg_file
    sys.exit(1)

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

def pytest_configure(config):
    '''
    Merge .cfg and --param settings
    '''

    # Add method to determine if the version being tested is the same as, or
    # newer, than the version provided.  This is helpful for ensuring a test
    # only runs when support for a new feature exists.  For example:
    #    return  1 if x < --project-version   (1.0  < 1.1)
    #    return  0 if x == --project-version  (1.0 == 1.1)
    #    return -1 if x > --project-version   (1.2  > 1.1)
    config.version_cmp = lambda x: StrictVersion(config.getoption('project-version')).__cmp__(x)

    # This is weird, but handy ...
    # Interpolate any ConfigParser style variables in --aeolus-url and --katello-url
    for key in ['aeolus-url', 'katello-url']:
        # Convert ConfigParser interpolation syntax to str.format() friendly syntax
        url = re.sub(r'%\(([^\)]+)\)s', '{\\1}', config.getoption(key))
        url = url.format(baseurl=config.option.base_url)

        # Update the mozwebqa object
        setattr(config.option, key, url)

        # Update the ConfigParser object
        test_config.set(key.replace('-url',''), key, url)

    # TODO: This should probably move into apps/$app/__init__.py
    # Replace --baseurl with value appropriate for the specified --project
    if config.option.project and not config.option.collectonly:
        project = config.option.project.split('.',1)[0]
        config.option.base_url = getattr(config.option, '%s-url' % project)

    # TODO - Update test_config with any --keyval
    for param in config.option.keyval:
        try:
            (sect, key, val) = re.match(r'^([\w_-]*):?\b([\w_-]+)=(.*)$', param).groups()
        except AttributeError:
            raise Exception("Improper format for --keyval value '%s'" % param)

        # Update mozwebqa object
        if hasattr(config.option, key):
            setattr(config.option, key, val)

        # Update ConfigParser object
        if test_config.has_option(sect, key):
            test_config.set(sect, key, val)

    # Turn on verbosity / debugging if specified in .cfg
    for opt in ['verbose', 'debug']:
        if not getattr(config.option, opt) \
                and test_config.has_option('general', opt):
            setattr(config.option, opt, test_config.getboolean('general', opt))

    # Setup test logging
    setup_logger(config.option.verbose, \
            config.option.debug, \
            config.option.logfile)

def pytest_runtest_setup(item):
    """
    pytest setup
    """

    setattr(item, 'cfgfile', test_config)
    pytest_mozwebqa = pytest.config.pluginmanager.getplugin("mozwebqa")
    pytest_mozwebqa.TestSetup.config = item.config
    pytest_mozwebqa.TestSetup.cfgfile = item.cfgfile

def pytest_addoption(parser):
    """
    Add option to the py.test command line, option is specific to
    this project.
    """

    def is_true(val):
        '''
        return whether the provided string is intended to mean boolean True
        '''
        return re.match(r'^(true|yes|1|on)$', val, re.IGNORECASE) is not None

    # Update .default and .help for '--baseurl' option
    group = parser.getgroup('selenium', 'selenium')
    for opt in group.options:
        if opt.dest == 'base_url' and opt.default == '':
            if test_config.has_option('general', 'baseurl'):
                opt.default = test_config.get('general', 'baseurl')
            opt.help = opt.help + " (default: %default)" #% opt.default
            break

    # Add --logfile option to existing 'termincal reporting' option group
    optgrp = parser.getgroup("terminal reporting")
    optgrp.addoption("--logfile", action="store", dest='logfile',
            default=test_config.get('general', 'log_file', ''),
            help="Specify a file to record logging information (default: %default)")

    # Create a general test options
    optgrp = parser.getgroup('general_options', "General Test Options")
    optgrp.addoption("--config", action="store", dest='cfg_file',
            default=cfg_file,
            help="Specify test configuration file (default: %default)")

    optgrp.addoption("--project", action="store", dest='project', default=None,
            help="Specify project (e.g. sam, headpin, katello, katello.cfse, aeolus, cfce)")

    optgrp.addoption("--project-version", action="store",
            dest='project-version', default='1.1',
            help="Specify project version number (default: %default)")

    optgrp.addoption("--enable-ldap", action="store_true", dest='enable-ldap',
            default=test_config.getboolean('general', 'enable-ldap'),
            help="Specify whether LDAP authentication is enabled (default: %default)")

    optgrp.addoption("--test-cleanup", action="store_true",
            dest='test-cleanup', default=False,
            help="Specify whether to cleanup after test completion (default: %default)")

    # Allow generic access to all parameters within cloudforms.cfg
    optgrp.addoption("--keyval", action="append",
            dest='keyval', default=[],
            help="Specify key=val pairs to override config values")

    # TODO - add parameters for each cloudforms.cfg [katello] option
    optgrp = parser.getgroup('katello_options', "Katello Test Options (--project=katello)")
    optgrp.addoption("--katello-url", action="store", dest='katello-url',
            default=test_config.get('katello', 'katello-url', raw=True),
            help="Specify URL for katello (default: %default)")

    # TODO - add parameters for each cloudforms.cfg [aeolus] option
    optgrp = parser.getgroup('aeolus_options', "Aeolus Test Options (--project=aeolus)")
    optgrp.addoption("--aeolus-url", action="store", dest='aeolus-url',
            default=test_config.get('aeolus', 'aeolus-url', raw=True),
            help="Specify URL for aeolus (default: %default)")

def pytest_funcarg__mozwebqa(request):
    """Load mozwebqa plugin
    """
    pytest_mozwebqa = pytest.config.pluginmanager.getplugin("mozwebqa")
    return pytest_mozwebqa.TestSetup(request)
