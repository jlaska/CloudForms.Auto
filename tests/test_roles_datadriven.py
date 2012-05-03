import pytest
from unittestzero import Assert
from pages.home import Home
from pages.administration import RolesTab
from pages.administration import AdministrationTab
from api.api import ApiTasks
import time

from data.datadrv import *

class TestRolesDataDriven(object):
    scenarios = [scenario1, scenario2]
    
    @pytest.mark.challenge    
    def test_datadriven_rbac(self, mozwebqa, org, perm_name, resource, verbs):

        sysapi = ApiTasks(mozwebqa)
        home_page = Home(mozwebqa)
        rolestab = RolesTab(mozwebqa)
        
        role_name = "role_%s" % (home_page.random_string())
        perm_name = "perm_%s" % (home_page.random_string())
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

        if not rolestab.role_org(org):
            sysapi.create_org(org)
            time.sleep(4)
            
        rolestab.role_org(org).click()
        time.sleep(2)
        rolestab.click_add_permission()
        
        rolestab.select_resource_type(resource)
        home_page.click_next()
        for v in verbs:
            home_page.select('verbs', v)
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