import pytest
import apps
from tests.aeolus import Aeolus_Test
from data.dataset import Environment
from data.dataset import Content
from data.assert_response import *

class Test_Environment(Aeolus_Test):
    '''
    Create clouds, pools, catalogs and cloud resource profile (front end)
    '''

    @pytest.mark.setup
    def test_create_cloud(self, cloud):
        '''
        create a new cloud
        '''
        page = self.aeolus.load_page('Aeolus')
        page.login()

        response = page.new_environment(cloud)
        assert response == aeolus_msg['add_pool_family']

    @pytest.mark.setup
    def test_create_zone(self, resource_zone):
        '''
        create a cloud resource zone
        '''
        page = self.aeolus.load_page('Aeolus')
        page.login()

        # workaround. Select dropdown not working
        # capture pool_family_environment IDs from "/pool_families/" view
        cloud_id = page.get_id_by_url("pool_families",
                resource_zone['environment_parent'])

        assert page.new_pool_by_id(cloud_id, resource_zone) == \
            aeolus_msg['add_pool']

    @pytest.mark.setup
    def test_create_catalog(self, catalog):
        '''
        create new catalog
        '''
        page = self.aeolus.load_page('Aeolus')
        page.login()

        assert page.new_catalog(catalog) == aeolus_msg['add_catalog']
