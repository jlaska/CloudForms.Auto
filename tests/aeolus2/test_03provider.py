import pytest
import apps
from tests.aeolus2 import Aeolus_Test
from data.dataset import Provider
from data.dataset import Environment
from data.assert_response import *

@pytest.mark.setup
class TestProvider(Aeolus_Test):
    '''
    Test provider connections, create provider accounts and test connection,
    add or enable provider accounts to clouds
    '''

    @pytest.mark.provider
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

    @pytest.mark.provider
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
                creds = page.cfgfile.items('credentials-ec2')
                for (key, val) in creds:
                    account[key] = val

            assert page.create_provider_account(account) == \
                   aeolus_msg['add_provider_acct'] % \
                       account["provider_account_name"]

        # test provider account
        for account in Provider.accounts:
            assert page.connection_test_provider_account(account) == \
                   aeolus_msg['connect_provider_acct']

        # test cleanup
        #if page.test_cleanup == True:
        #    for account in Provider.accounts:
        #        assert page.delete_provider_account(account) == \
        #               aeolus_msg['delete_provider_acct']

    @pytest.mark.provider
    def test_add_provider_account_cloud(self, mozwebqa):
        '''
        Add provider accounts to clouds
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
