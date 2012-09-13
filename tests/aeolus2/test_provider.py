#!/usr/bin/env python

import pytest
import apps
from tests.aeolus2 import Aeolus_Test
from data.large_dataset import Provider
from data.assert_response import *
import time

def setup_module(module):
    test_setup = pytest.config.pluginmanager.getplugin("mozwebqa")
    module.TestProvider.aeolus = apps.initializeProduct(test_setup.TestSetup)

class TestProvider(Aeolus_Test):

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

    #@pytest.mark.xfail
    @pytest.mark.provider_admin
    @pytest.mark.aeolus_setup
    def test_create_provider_account(self, mozwebqa):
        '''
        Create provider account and test provider account connection
        '''
        page = self.aeolus.load_page('Aeolus')
        #assert page.login() == aeolus_msg['login']
        page.login()

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

