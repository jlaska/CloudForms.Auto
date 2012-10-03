#!/usr/bin/env python

import pytest
import apps
from tests.aeolus2 import Aeolus_Test
from data.large_dataset import Environment
from data.large_dataset import Content
from data.assert_response import *
import logging
import time

def setup_module(module):
    test_setup = pytest.config.pluginmanager.getplugin("mozwebqa")
    module.TestClouds.aeolus = apps.initializeProduct(test_setup.TestSetup)


class TestClouds(Aeolus_Test):
    '''
    Create clouds, pools, catalogs and cloud resource profile (front end)
    '''

    @pytest.mark.environment
    @pytest.mark.aeolus_setup
    def test_create_clouds(self, mozwebqa):
        '''
        create new clouds
        '''
        page = self.aeolus.load_page('Aeolus')
        #assert page.login() == aeolus_msg['login']
        page.login()

        for cloud in Environment.clouds:
            assert page.new_environment(cloud) == aeolus_msg['add_pool_family']

        # test cleanup
        #if self.testsetup.test_cleanup:
        #    for environment in Environment.pool_family_environments:
        #        assert page.delete_environment(environment) == \
        #               aeolus_msg['delete_pool_family']

    def test_new_pools(self, mozwebqa):
        '''
        create new pools
        '''
        page = self.aeolus.load_page('Aeolus')
        #assert page.login() == aeolus_msg['login']
        page.login()

        # workaround. Select dropdown not working
        # capture pool_family_environment IDs from "/pool_families/" view
        for cloud in Environment.clouds:
            cloud['id'] = page.get_id_by_url("pool_families", cloud['name'])

        for cloud in Environment.clouds:
            for pool in Environment.pools:
                if cloud['name'] in pool['environment_parent']:
                    assert page.new_pool_by_id(cloud, pool) == \
                        aeolus_msg['add_pool']

        #for pool in Environment.pools:
        #    assert page.new_pool_by_id(pool) == aeolus_msg['add_pool']

        # select dropdown not working
        #for pool in Environment.pools:
        #    page.get_id_by_url("pool_families", pool)
        #    assert page.new_pool(pool) == aeolus_msg['add_pool']

        # test cleanup
        #if self.testsetup.test_cleanup:
        #    for pool in Environment.pools:
        #        assert page.delete_pool(pool) == \
        #               aeolus_msg['delete_pool'] % pool["name"]


    def test_create_catalogs(self, mozwebqa):
        '''
        create new catalogs
        '''
        page = self.aeolus.load_page('Aeolus')
        page.login()

        for catalog in Content.catalogs:
            assert page.new_catalog(catalog) == aeolus_msg['add_catalog']

        # test cleanup
        #if self.testsetup.test_cleanup:
        #    for catalog in Content.catalogs:
        #        assert page.delete_catalog(catalog) == aeolus_msg['delete_catalog']

