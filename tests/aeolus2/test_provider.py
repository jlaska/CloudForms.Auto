#!/usr/bin/env python

import pytest
import apps
from tests.aeolus2 import Aeolus_Test
from data.large_dataset import Provider
from data.large_dataset import Environment
from data.assert_response import *
import logging
import time

def setup_module(module):
    test_setup = pytest.config.pluginmanager.getplugin("mozwebqa")
    module.TestProvider.aeolus = apps.initializeProduct(test_setup.TestSetup)

class TestProvider(Aeolus_Test):
    '''
    Test provider connections, create provider accounts and test connection,
    add or enable provider accounts to clouds
    '''

    @pytest.mark.provider_admin
    @pytest.mark.aeolus_setup
    def test_provider_connection(self, mozwebqa):
        '''
        test provider connection
        '''
        page = self.aeolus.load_page('Aeolus')
        #assert page.login() == aeolus_msg['login']
        page.login()

        for account in Provider.accounts:
            assert page.connection_test_provider(account) == \
                   aeolus_msg['connect_provider']

    @pytest.mark.provider_admin
    @pytest.mark.aeolus_setup
    def test_create_provider_account(self, mozwebqa):
        '''
        Create provider account and test provider account connection
        '''
        page = self.aeolus.load_page('Aeolus')
        #assert page.login() == aeolus_msg['login']
        page.login()

        # TODO: delete mock provider account to prevent launching to mock

        # create provider account
        for account in Provider.accounts:
            if account["type"] == "ec2":
                account = page.update_ec2_acct_credentials_from_config(account)
            assert page.create_provider_account(account) == \
                   aeolus_msg['add_provider_acct'] % account["provider_account_name"]

        # test provider account
        for account in Provider.accounts:
            assert page.connection_test_provider_account(account) == \
                   aeolus_msg['connect_provider_acct']

        # test cleanup
        #if page.test_cleanup == True:
        #    for account in Provider.accounts:
        #        assert page.delete_provider_account(account) == \
        #               aeolus_msg['delete_provider_acct']

    @pytest.mark.aeolus_setup
    def test_add_provider_account_cloud(self, mozwebqa):
        '''
        Add provider accounts to all clouds
        '''
        page = self.aeolus.load_page('Aeolus')
        page.login()

        for cloud in Environment.clouds:
            # tricky assert: string includes list of accts added
            #assert page.add_provider_accounts_cloud(environment['name']) ==\
            #    aeolus_msg['add_provider_accts']
            page.add_provider_accounts_cloud(cloud)

    def test_create_resource_profiles(self, mozwebqa):
        '''
        create cloud resource profiles
        '''
        page = self.aeolus.load_page('Aeolus')
        page.login()

        for profile in Provider.resource_profiles:
            page.new_cloud_resource_profile(profile)
