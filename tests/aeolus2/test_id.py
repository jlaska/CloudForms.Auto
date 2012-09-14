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
    def test_get_ids_from_ui(self, mozwebqa):
        '''
        Cycle through UI and get IDs for these elements
         - users
         - groups
         - clouds
         - cloud resource zones
         - catalogs
        '''
        page = self.aeolus.load_page('Aeolus')
        page.login()

        print "### User IDs ###"
        for user in Admin.users:
            user["id"] = page.get_id_by_url("users", user["username"])
            print "%s (%s)" % (user["username"], user["id"])

        print "### User group IDs ###"
        for user_group in Admin.user_groups:
            user_group["id"] = page.get_id_by_url("user_groups", user_group["name"])
            print "%s (%s)" % (user_group["name"], user_group["id"])

        print "### Cloud IDs ###"
        for env in Environment.pool_family_environments:
            env["id"] = page.get_id_by_url("pool_families", env["name"])
            print "%s (%s)" % (env["name"], env["id"])

        print "### Cloud Resource Zone IDs ###"
        for pool in Environment.pools:
            pool["id"] = page.get_id_by_url("pools", pool["name"])
            print "%s (%s)" % (pool["name"], pool["id"])

        print "### Catalog IDs ###"
        for catalog in Content.catalogs:
            catalog["id"] = page.get_id_by_url("catalogs", catalog["name"])
            print "%s (%s)" % (catalog["name"], catalog["id"])

    def test_get_ids_from_api(self, mozwebqa):
        '''
        Get IDs for these elements
         - clouds
         - pools
         - providers
         - provider accounts
         - images
         - builds
         - target images
         - provider images
        '''
        print "### Clouds ###"
        pool_families = self.api.get_element_id_list("pool_families", "pool_family")
        for pool_fam_id in pool_families:
            pool_name = self.api.get_detailed_info("pool_families", pool_fam_id)
            print "%s (%s)" % (pool_name, pool_fam_id)

        print "### Pools ###"
        pools = self.api.get_element_id_list("pools", "pool")
        for pool_id in pools:
            pool_name = self.api.get_detailed_info("pools", pool_id)
            print "%s (%s)" % (pool_name, pool_id)

        print "### Providers ###"
        providers = self.api.get_element_id_list("providers", "provider")
        for provider_id in providers:
            provider_name = self.api.get_detailed_info("providers", provider_id)
            print "%s (%s)" % (provider_name, provider_id)

        print "### Provider Accounts ###"
        provider_accounts = self.api.get_element_id_list("provider_accounts", "provider_account")
        for provider_acct_id in provider_accounts:
            provider_acct_name = self.api.get_detailed_info("provider_accounts", provider_acct_id)
            print "%s (%s)" % (provider_acct_name, provider_acct_id)

        print "### Images ###"
        images = self.api.get_element_id_list("images", "image")
        for image_id in images:
            image_name = self.api.get_detailed_info("images", image_id)
            print "%s (%s)" % (image_name, image_id)

        # FIXME: target image name not being returned. fix api index[0] 
        print "### Target Images ###"
        target_images = self.api.get_element_id_list("target_images", "target_image")
        for target_image_id in target_images:
            target_image_name = self.api.get_detailed_info("target_images", target_image_id)
            print "%s (%s)" % (target_image_name, target_image_id)

        # FIXME: provider image name not being returned. fix api index[0]
        print "### Provider Images ###"
        provider_images = self.api.get_element_id_list("provider_images", "provider_image")
        for provider_image_id in provider_images:
            provider_image_name = self.api.get_detailed_info("provider_images", provider_image_id)
            print "%s (%s)" % (provider_image_name, provider_image_id)

