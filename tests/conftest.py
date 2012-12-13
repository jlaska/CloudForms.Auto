#!/usr/bin/env python

import sys
import optparse
import logging
import ConfigParser
import requests
import re
import fnmatch
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
        filehandler = logging.FileHandler(logfile, 'w+')
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

    # Update test_config with any --keyval
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

    # Determine whether loglevel is specified in .cfg
    for opt in ['verbose', 'debug']:
        # If --verbose or --debug wasn't supplied, see if a value was provided
        # in .cfg
        if not getattr(config.option, opt) \
                and test_config.has_option('general', opt):
            setattr(config.option, opt, test_config.getboolean('general', opt))

    # In case --aeolus-provider includes regexp's, find matches
    from data.dataset import Provider
    all_provider_accounts = [a['provider_account_name'] for a in Provider.accounts]
    enabled_accounts = list()
    # For each configured account ...
    for account in all_provider_accounts:
        # Determine if a fnmatch-style expression was used ... and expand any matches
        if any ([True for expr in config.getvalue('aeolus-providers') \
                if fnmatch.fnmatch(account, expr)]):
            enabled_accounts.append(account)
    setattr(config.option, 'aeolus-providers', enabled_accounts)

    # Setup test logging
    setup_logger(config.option.verbose, \
            config.option.debug, \
            config.option.logfile)

# Add mozwebqa plugin to all tests
def pytest_runtest_setup(item):
    """
    pytest setup
    """

    pytest_mozwebqa = pytest.config.pluginmanager.getplugin("mozwebqa")
    pytest_mozwebqa.TestSetup.config = item.config

# Customize command-line arguments
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

    # Update .default and .help for '--credentials' option
    group = parser.getgroup('credentials', 'credentials')
    for opt in group.options:
        if opt.dest == 'credentials_file' and opt.default == optparse.NO_DEFAULT:
            opt.default = 'credentials.yaml'
            opt.help = opt.help + " (default: %default)"

    # Update .default and .help for '--baseurl' option
    group = parser.getgroup('selenium', 'selenium')
    for opt in group.options:
        if opt.dest == 'base_url' and opt.default == '':
            if test_config.has_option('general', 'baseurl'):
                opt.default = test_config.get('general', 'baseurl')
            opt.help = opt.help + " (default: %default)" #% opt.default
            break

    # Callback helper for list-style parameters
    def list_callback(option, opt_str, value, parser, *args, **kwargs):
        '''
        Alters the built-in action='append' behavior by replacing the
        defaults, with any values provided on the command-line.
        '''
        # Start with a fresh-hot list
        values = [value]
        # If the current option value isn't the default, append
        if getattr(parser.values, option.dest) != option.default:
            values += getattr(parser.values, option.dest)
        setattr(parser.values, option.dest, values)

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

    # TODO - Move to app-specific optgrp
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

    optgrp.addoption("--releasever", dest='releasevers', type="string",
            action="callback", callback=list_callback,
            default=test_config.getlist('general', 'releasevers'),
            help="Specify the release of the desired system templates (default: %default)")

    optgrp.addoption("--arch", "--basearch", dest='basearchs', type="string",
            action="callback", callback=list_callback,
            default=test_config.getlist('general', 'basearchs'),
            help="Specify the architecture of the desired system templates (default: %default)")

    optgrp.addoption("--instance-password", dest='instance-password',
            type="string", action="store",
            default=test_config.get('general', 'instance-password'),
            help="Specify the default password for applications (default: %default)")

    # Allow generic access to all parameters within cloudforms.cfg
    optgrp.addoption("--keyval", action="append",
            dest='keyval', default=[],
            help="Specify key=val pairs to override config values")

    # TODO - add parameters for each cloudforms.cfg [katello] option
    optgrp = parser.getgroup('katello_options', "Katello Test Options (--project=katello)")
    optgrp.addoption("--katello-url", action="store", dest='katello-url',
            default=test_config.get('katello', 'katello-url', raw=True),
            help="Specify URL for katello (default: %default)")

    optgrp.addoption("--katello-env", action="store", dest='katello-env',
            default=test_config.get('katello', 'env'),
            help="Specify default environment (default: %default)")

    optgrp.addoption("--katello-org", action="store", dest='katello-org',
            default=test_config.get('katello', 'org'),
            help="Specify default organization (default: %default)")

    # TODO - add parameters for each cloudforms.cfg [aeolus] option
    optgrp = parser.getgroup('aeolus_options', "Aeolus Test Options (--project=aeolus)")
    optgrp.addoption("--aeolus-url", action="store", dest='aeolus-url',
            default=test_config.get('aeolus', 'aeolus-url', raw=True),
            help="Specify URL for aeolus (default: %default)")

    optgrp.addoption("--aeolus-provider", dest='aeolus-providers', type="string",
            action="callback", callback=list_callback,
            default=test_config.getlist('aeolus', 'providers'),
            help="Specify which cloud providers will be tested (default: %default)")

    #optgrp.addoption("--aeolus-configserver", dest='aeolus-configservers', type="string",
    #        action="callback", callback=list_callback,
    #        default=test_config.getlist('aeolus', 'configserver'),
    #        help="Specify which providers to build a configserver in (default: %default)")

    optgrp.addoption("--aeolus-template-url", action="store",
            dest='aeolus-template-url', default=test_config.get('aeolus', 'template-url'),
            help="Specify URL format string for system templates (default: %default)")

    optgrp.addoption("--aeolus-custom-blueprint", action="store",
            dest='aeolus-custom-blueprint', default=test_config.get('aeolus', 'custom-blueprint'),
            help="Specify custom application blueprint template (default: %default)")

# Add pytest function argument: mozwebqa
def pytest_funcarg__mozwebqa(request):
    """Load mozwebqa plugin
    """
    pytest_mozwebqa = pytest.config.pluginmanager.getplugin("mozwebqa")
    return pytest_mozwebqa.TestSetup(request)

# Helper method for accessing a specific attribute of a cloud
def _get_cloud_attribute(name, key):
    from data.dataset import Environment
    for cloud in Environment.clouds:
        if cloud.get('name') == name:
            return cloud.get(key)
    logging.warn("Unable to discover cloud attribute '%s' for cloud '%s'" %
            (key, cloud))
    return None

# Add pytest function argument: max_running_instances
def pytest_funcarg__max_running_instances(request):
    return _get_cloud_attribute(
            request.getfuncargvalue("cloud"),
            'max_running_instances')

# Add pytest function argument: provider_accounts
def pytest_funcarg__provider_accounts(request):
    '''
    Determine which provider_accounts are enabled for the current value of pool_family
    '''
    return _get_cloud_attribute(
            request.getfuncargvalue("cloud"),
            'enabled_provider_accounts')

# Add pytest function argument: catalogs
def pytest_funcarg__catalogs(request):
    '''
    Determine the appropriate catalogs based on the current value of cloud
    '''

    # Hacky-hackity-hack
    if "cloud" in request.funcargnames:
        cloud = request.getfuncargvalue("cloud")
    elif "cloud_by_account_type" in funcargnames:
        (cloud, account) = request.getfuncargvalue("cloud_by_account_type")

    from data.dataset import Content
    catalog_list = list()
    for catalog in Content.catalogs:
        if catalog.get('cloud_parent') == cloud['name']:
            catalog_list.append(catalog)

    if len(catalog_list) == 0:
        logging.warn('Unable to discover funcarg__catalog')

    return catalog_list

# Add pytest function argument: configserver
def pytest_funcarg__configserver(request):
    from data.dataset import Content
    return Content.configserver

# Parameterize tests when specific arguments are requested
def pytest_generate_tests(metafunc):

    # Used when building images
    if 'cloud_by_account_type' in metafunc.funcargnames:
        from data.dataset import Environment, Provider
        test_set = list()
        id_list = list()

        # List of providers already included
        account_providers_seen = list()

        for c in Environment.clouds:
            for a in Provider.accounts:
                # Skip provider account if not enabled
                if a.get('provider_account_name') not in metafunc.config.getoption('aeolus-providers'):
                    continue
                # Skip provider account if we've already included it
                if a.get('type') in account_providers_seen:
                    '''ignore if we've already seen this provider account type'''
                    continue
                if a.get('provider_account_name') in c.get('enabled_provider_accounts', []):
                    id_list.append("%s-%s" % (c.get('name'), a.get('type')))
                    test_set.append((c, a))
                    account_providers_seen.append(a.get('type'))

        metafunc.parametrize('cloud_by_account_type', test_set, ids=id_list)

    # Used when pushing images
    if 'cloud_by_account' in metafunc.funcargnames:
        from data.dataset import Environment, Provider
        test_set = list()
        id_list = list()
        for c in Environment.clouds:
            for a in Provider.accounts:
                # Skip provider account if not enabled
                if a.get('provider_account_name') not in metafunc.config.getoption('aeolus-providers'):
                    continue
                if a.get('provider_account_name') in c.get('enabled_provider_accounts', []):
                    id_list.append("%s-%s" % (c.get('name'), a.get('provider_account_name')))
                    test_set.append((c, a))

        metafunc.parametrize('cloud_by_account', test_set, ids=id_list)

    # Used when launching images
    if 'zone_by_catalog' in metafunc.funcargnames:
        from data.dataset import Environment, Content, Provider
        # ids=[rp.get('name') for rp in Provider.cloud_resource_clusters])
        test_set = list()
        id_list = list()

        for cat in Content.catalogs:
            # Skip if catalog if the associated cluster isn't an enabled provider account
            # NOTE: this requires that resource_cluster and provider account names match
            if cat['resource_cluster'] not in metafunc.config.getoption('aeolus-providers'):
                continue

            for pool in Environment.pools:
                for cloud in Environment.clouds:
                    # If the cloud is the parent of both the pool *and* category ...
                    if cat.get('pool_parent') == pool.get('name') \
                            and cat.get('cloud_parent') == cloud.get('name'):
                        id_list.append("%s-%s-%s" % (cloud.get('name'), pool.get('name'), cat.get('name')))
                        test_set.append((cloud, pool, cat))
        metafunc.parametrize('zone_by_catalog', test_set, ids=id_list)

    # If *just* cloud is used, enumerate
    if 'cloud' in metafunc.funcargnames:
        ''' parametrize clouds that include enabled provider accounts'''
        from data.dataset import Environment, Provider
        test_list = list()
        id_list = list()

        # List of enabled provider account names (e.g. ec2-us-east-1, or rhevm etc...)
        enabled_providers = [a.get('provider_account_name') for a in Provider.accounts if a.get('provider_account_name') in metafunc.config.getoption('aeolus-providers')]

        # Parametrize clouds that include enabled_provider_types
        for c in Environment.clouds:
            # Include cloud if any of the provider accounts are enabled
            # The following performs a union of two lists
            if filter(c['enabled_provider_accounts'].__contains__, enabled_providers):
                test_list.append(c)
                id_list.append(c['name'])
        metafunc.parametrize("cloud", test_list, ids=id_list)

    # If *just* resource_zone is used, enumerate
    if 'resource_zone' in metafunc.funcargnames:
        from data.dataset import Environment
        metafunc.parametrize("resource_zone", \
                Environment.pools, \
                ids=[p.get('name') for p in Environment.pools])

    if 'catalog' in metafunc.funcargnames:
        from data.dataset import Content
        metafunc.parametrize("catalog", \
                Content.catalogs, \
                ids=[c.get('name') for c in Content.catalogs])

    if 'resource_cluster' in metafunc.funcargnames:
        from data.dataset import Provider
        metafunc.parametrize("resource_cluster", \
                Provider.cloud_resource_clusters, \
                ids=[rp.get('name') for rp in Provider.cloud_resource_clusters])

    if 'resource_profile' in metafunc.funcargnames:
        from data.dataset import Provider
        metafunc.parametrize("resource_profile", \
                Provider.resource_profiles, \
                ids=[rp.get('name') for rp in Provider.resource_profiles])

    if 'provider_account' in metafunc.funcargnames:
        from data.dataset import Provider
        metafunc.parametrize("provider_account", \
                Provider.accounts, \
                ids=[p.get('provider_account_name') for p in Provider.accounts])

    if 'provider' in metafunc.funcargnames:
        metafunc.parametrize("provider", metafunc.config.getoption('providers'))

    if 'releasever' in metafunc.funcargnames:
        metafunc.parametrize("releasever", metafunc.config.getoption('releasevers'))

    if 'basearch' in metafunc.funcargnames:
        metafunc.parametrize("basearch", metafunc.config.getoption('basearchs'))

    if 'image' in metafunc.funcargnames:
        image_list = list()
        # NOTE, instead of guessing the profile name, we should inspect 'resource_profiles'
        for releasever in metafunc.config.getoption('releasevers'):
            for basearch in metafunc.config.getoption('basearchs'):
                image_list.append(dict(
                    name="rhel-{basearch}-{releasever}".format(releasever=releasever, basearch=basearch),
                    profile="small-{basearch}".format(basearch=basearch),
                    releasever=releasever,
                    basearch=basearch))
        metafunc.parametrize("image", image_list, ids=[i.get('name') for i in image_list])
