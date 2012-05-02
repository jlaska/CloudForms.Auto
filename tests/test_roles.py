#!/usr/bin/env python
# Purpose           : Calls tests and assertions related to roles.
# Contributors      : Eric L. Sammons (irc: eanxgeek)

import pytest
from unittestzero import Assert
from pages.home import Home
from pages.administration import RolesTab
from pages.administration import AdministrationTab
from api.api import ApiTasks
import time

from data.datadrv import *

xfail = pytest.mark.xfail

class TestRoles:
    def test_confirm_default_roles(self, mozwebqa):
        roles = ["Administrator", "Read Everything"]
    
        home_page = Home(mozwebqa)
        home_page.login()
        Assert.true(home_page.is_successful)

        rolestab = RolesTab(mozwebqa)

        home_page.tabs.click_tab("administration_tab")
        try:
            home_page.jquery_wait()
        finally:
            home_page.tabs.click_tab("roles_administration")
    
        for role in roles:
            rolestab.role(role).click()
            Assert.true(rolestab.is_permissions_visible)
            Assert.true(rolestab.is_users_visible)
            
            home_page.jquery_wait()
            displayed_role = rolestab.get_breadcrumb_role_name
            Assert.equal(displayed_role, role, "Expected role was not found")

    def test_add_user_to_administrator_role(self, mozwebqa):
        home_page = Home(mozwebqa)
        sysapi = ApiTasks(mozwebqa)
        rolestab = RolesTab(mozwebqa)
        
        username = "admin%s" % home_page.random_string()
        email = username + "@example.com"
        password = home_page.random_string()
        
        sysapi.create_user(username, password, email)
        
        home_page.login()
        Assert.true(home_page.is_successful)   
        
        home_page.tabs.click_tab("administration_tab")
        home_page.jquery_wait(20)
        home_page.tabs.click_tab("roles_administration")
            
        rolestab.role("Administrator").click()
        rolestab.click_role_users()
        
        rolestab.role_user(username).add_user()
        Assert.true(rolestab.is_remove_visible)  
        
    def test_add_user_to_readeverything_role(self, mozwebqa):
        home_page = Home(mozwebqa)
        sysapi = ApiTasks(mozwebqa)
        rolestab = RolesTab(mozwebqa)
        
        username = "readevery%s" % home_page.random_string()
        email = username + "@example.com"
        password = home_page.random_string()
        
        sysapi.create_user(username, password, email)
        
        home_page.login()
        Assert.true(home_page.is_successful)   
        
        home_page.tabs.click_tab("administration_tab")
        home_page.jquery_wait(30)
        home_page.tabs.click_tab("roles_administration")
            
        rolestab.role("Read Everything").click()
        rolestab.click_role_users()
        
        rolestab.role_user(username).add_user()
        Assert.true(rolestab.is_remove_visible)
        
    def test_create_new_role(self, mozwebqa):
        home_page = Home(mozwebqa)
        rolestab = RolesTab(mozwebqa)
        
        home_page.login()
        Assert.true(home_page.is_successful)   
        
        home_page.tabs.click_tab("administration_tab")
        home_page.jquery_wait(30)
        home_page.tabs.click_tab("roles_administration")
        
        role_name = "plainrole%s" % home_page.random_string()
        home_page.jquery_wait(20)
        home_page.click_new()
        home_page.jquery_wait(20)
        rolestab.create_new_role(role_name)
        home_page.jquery_wait(20)
        rolestab.save_role()
        Assert.true(home_page.is_successful)
        
    def test_create_role_name_already_taken(self, mozwebqa):
        home_page = Home(mozwebqa)
        rolestab = RolesTab(mozwebqa)
        
        home_page.login()
        Assert.true(home_page.is_successful)   
        
        home_page.tabs.click_tab("administration_tab")
        home_page.jquery_wait(30)
        home_page.tabs.click_tab("roles_administration")
        
        role_name = "plainrole%s" % home_page.random_string()
        home_page.jquery_wait(20)
        home_page.click_new()
        home_page.jquery_wait(20)
        rolestab.create_new_role(role_name)
        home_page.jquery_wait(20)
        rolestab.save_role()
        Assert.true(home_page.is_successful)
        
        home_page.jquery_wait(20)
        home_page.click_new()
        home_page.jquery_wait(20)
        rolestab.create_new_role(role_name)
        home_page.jquery_wait(20)
        rolestab.save_role()
        Assert.true(home_page.is_failed)

    @pytest.mark.challenge    
    def test_datadriven_rbac(self, mozwebqa, org, perm_name, resource, verb):
        
        scenarios = [scenario1, scenario2]
        '''
        class TestSampleWithScenarios:
            scenarios = [scenario1, scenario2]
    
            @pytest.mark.skip_selenium
            def test_demo(self, org, perm_name, resource, verb):
                assert isinstance(org, str)
        '''
        sysapi = ApiTasks(mozwebqa)
        home_page = Home(mozwebqa)
        rolestab = RolesTab(mozwebqa)
        
        role_name = "role_%s%s" % (scenario, home_page.random_string())
        perm_name = "perm_%s" % (scenario)
        username = "user%s" % home_page.random_string()
        email = username + "@example.com"
        password = "redhat%s" % (home_page.random_string())
        
        sysapi.create_user(username, password, email)
        
        home_page.login()
        
        home_page.tabs.click_tab("administration_tab")
        home_page.tabs.click_tab("roles_administration")
        home_page.click_new()
        rolestab.create_new_role(role_name)
        rolestab.save_role()
        
        rolestab.click_role_permissions()
        time.sleep(5)

        if not rolestab.role_org(values['org']):
            sysapi.create_org(values['org'])
            time.sleep(4)
            
        rolestab.role_org(values['org']).click()
        time.sleep(2)
        rolestab.click_add_permission()
        
        rolestab.select_resource_type(values['resource'])
        home_page.click_next()
        home_page.select('verbs', values['verb'])
        home_page.click_next()
        
        rolestab.enter_permission_name(perm_name)
        rolestab.enter_permission_desc('Added by QE test.')
        rolestab.click_permission_done()
        Assert.true(home_page.is_successful)
        
        rolestab.click_root_roles()
        time.sleep(5)
        rolestab.click_role_users()
        time.sleep(5)
            
        rolestab.role_user(username).add_user()
        
        home_page.header.click_logout()
        home_page.login(username, password)
        Assert.true(home_page.is_successful)
        home_page.header.click_logout()
    

