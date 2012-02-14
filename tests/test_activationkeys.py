#!/usr/bin/env python 

import pytest
from unittestzero import Assert
from pages.home import Home
from pages.systems import ActivationKeysTab
from pages.contentmgmt import ContentManagementTab
from api.api import ApiTasks
import time

xfail = pytest.mark.xfail

class TestActivationKeys:
    _activationkey_manifest = "/var/tmp/ActivationKeys_M1.zip"
    
    def test_create_activation_key(self, mozwebqa):
        home_page = Home(mozwebqa)
        home_page.login()
        Assert.true(home_page.is_successful)
        
        home_page.tabs.click_tab("systems_tab")
        home_page.tabs.click_tab("activation_keys")
        
        activationkeys = ActivationKeysTab(mozwebqa)
        
        new_activationkey_name = "newactivkey-%s" % home_page.random_string()
        activationkeys.click_new()
        activationkeys.enter_activation_key_name(new_activationkey_name)
        activationkeys.enter_activation_key_description(new_activationkey_name)
        activationkeys.click_save()
        Assert.true(home_page.is_successful)
        
    def test_remove_activationkey(self, mozwebqa):
        home_page = Home(mozwebqa)
        home_page.login()
        Assert.true(home_page.is_successful)
        
        home_page.tabs.click_tab("systems_tab")
        home_page.tabs.click_tab("activation_keys")
        
        activationkeys = ActivationKeysTab(mozwebqa)
        
        new_activationkey_name = "rmactivkey-%s" % home_page.random_string()
        activationkeys.click_new()
        activationkeys.enter_activation_key_name(new_activationkey_name)
        activationkeys.enter_activation_key_description(new_activationkey_name)
        activationkeys.click_save()
        Assert.true(home_page.is_successful)
        
        home_page.enter_search_criteria(new_activationkey_name)
        activationkeys.activationkey(new_activationkey_name).click()
        
        Assert.true(activationkeys.is_block_active)
        home_page.click_remove()
        home_page.click_confirm()
        Assert.true(home_page.is_successful)
        
    def test_activation_key_workflow(self, mozwebqa):
        ###
        # Create a org specific to this test.
        ###
        home_page = Home(mozwebqa)
        api = ApiTasks()
        _new_org_name = "activationkeyorg%s" % home_page.random_string()
        api.create_org(_new_org_name)
        api.create_envs(_new_org_name)
        ###
        # Login
        ###
        home_page.login()
        Assert.true(home_page.is_successful)
        ###
        # Change to the newly created org
        ###
        home_page.header.click_switcher()
        home_page.header.filter_org_in_switcher(_new_org_name)
        home_page.header.click_filtered_result(_new_org_name)
        ###
        # Navigate to Content Management and load manifest
        ###
        cm = ContentManagementTab(mozwebqa)
        home_page.tabs.click_tab("content_management_tab")
        Assert.true(home_page.is_the_current_page)
        cm.enter_manifest(self._activationkey_manifest)
        Assert.true(home_page.is_successful)
        ###
        # Navigate to Activation Keys
        ###
        activationkeys = ActivationKeysTab(mozwebqa)
        home_page.tabs.click_tab("systems_tab")
        home_page.tabs.click_tab("activation_keys")
        ### Create Activation Key
        _new_activationkey_name = "workflowactivkey-%s" % home_page.random_string()
        activationkeys.click_new()
        activationkeys.enter_activation_key_name(_new_activationkey_name)
        activationkeys.enter_activation_key_description(_new_activationkey_name)
        activationkeys.click_save()
        Assert.true(home_page.is_successful)
        Assert.true(activationkeys.is_block_active)

        activationkeys.click_available_subscriptions()
        Assert.true(activationkeys.is_filter_visible)
        #subscription_object = activationkeys.select_random_sub
        #print subscription_object
        #activationkeys.subscription(subscription_object).click()
        activationkeys.select_a_random_sub()
        time.sleep(20)
        activationkeys.click_add_sub()
        time.sleep(10)
        #activationkeys.select_subscription()
        #home_page.wait_for_ajax()
        activationkeys.click_submit_button()
        Assert.true(home_page.is_successful)
        time.sleep(5)
        
        
        