#!/usr/bin/env python

import pytest
import apps
from data.small_dataset import *
#from data.assert_response import *
from tests.aeolus2 import Aeolus_Test

def setup_module(module):
    test_setup = pytest.config.pluginmanager.getplugin("mozwebqa")
    module.TestId.aeolus = apps.initializeProduct(test_setup.TestSetup)

class TestId(Aeolus_Test):

    @pytest.mark.get_id
    def test_get_ids(self, mozwebqa):
        '''
        Cycle through and get IDs for these elements
         - users
         - groups
         - clouds
         - cloud resource zones
         - catalogs
        '''
        page = self.aeolus.load_page('Aeolus')
        page.login()

        # user IDs
        for user in Admin.users:
            user["id"] = page.get_id_by_url("users", user["username"])
            print "%s (%s)" % (user["username"], user["id"])

        # user group IDs
        for user_group in Admin.user_groups:
            user_group["id"] = page.get_id_by_url("user_groups", user_group["name"])
            print "%s (%s)" % (user_group["name"], user_group["id"])

        # Cloud IDs
        for env in Environment.pool_family_environments:
            env["id"] = page.get_id_by_url("pool_families", env["name"])
            print "%s (%s)" % (env["name"], env["id"])

        # Cloud Resource Zone IDs
        for pool in Environment.pools:
            pool["id"] = page.get_id_by_url("pools", pool["name"])
            print "%s (%s)" % (pool["name"], pool["id"])

        # Catalog IDs
        for catalog in Content.catalogs:
            catalog["id"] = page.get_id_by_url("catalogs", catalog["name"])
            print "%s (%s)" % (catalog["name"], catalog["id"])

