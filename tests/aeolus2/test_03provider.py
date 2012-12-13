import pytest
import apps
from tests.aeolus2 import Aeolus_Test
from data.dataset import Provider
from data.dataset import Environment
from data.assert_response import *

class TestProvider(Aeolus_Test):
    '''
    Test provider connections, create provider accounts and test connection,
    add or enable provider accounts to clouds
    '''

    @pytest.mark.provider
    @pytest.mark.setup
    def test_connection(self, provider_account):
        '''
        test provider connection
        '''
        page = self.aeolus.load_page('Aeolus')
        page.login()

        response = page.connection_test_provider(provider_account)
        assert response == aeolus_msg['connect_provider']

    @pytest.mark.provider
    @pytest.mark.setup
    def test_create_account(self, provider_account):
        '''
        Create provider account and test provider account connection
        '''
        page = self.aeolus.load_page('Aeolus')
        page.login()

        # Merge credentials into provider dict
        creds = self.testsetup.credentials.get(provider_account['type'], {})
        provider_account.update(creds)

        # Create account
        response = page.create_provider_account(provider_account)
        assert response == aeolus_msg['add_provider_acct'] % \
            provider_account["provider_account_name"]

    @pytest.mark.provider
    @pytest.mark.setup
    def test_account_connection(self, provider_account):
        '''
        Test provider account connection
        '''
        page = self.aeolus.load_page('Aeolus')
        page.login()

        # test provider account
        response =  page.connection_test_provider_account(provider_account)
        assert response == aeolus_msg['connect_provider_acct']

    @pytest.mark.provider
    @pytest.mark.setup
    def test_add_accounts_to_cloud(self, cloud):
        '''
        Add provider accounts to clouds
        '''
        page = self.aeolus.load_page('Aeolus')
        page.login()

        page.add_provider_accounts_cloud(cloud)

    @pytest.mark.setup
    def test_create_resource_profile(self, resource_profile):
        '''
        create cloud resource profiles
        '''
        page = self.aeolus.load_page('Aeolus')
        page.login()

        page.new_cloud_resource_profile(resource_profile)

        # FIXME - assert?

    @pytest.mark.setup
    def test_create_cloud_resource_cluster(self, resource_cluster):
        '''
        create cloud resource clusters
        '''
        page = self.aeolus.load_page('Aeolus')
        page.login()

        assert page.new_cloud_resource_cluster(resource_cluster) == \
            aeolus_msg['add_cluster_mapping']
