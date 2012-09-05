#!/usr/bin/env python
# Name              : test_organizations.py
# Purpose           : Calls tests and assertions related to organizations.
# Contributors      : Eric L Sammons (eanxgeek)

import pytest
import apps
from api.api import ApiTasks
import random
import time

from tests.katello2 import Katello_Test

@pytest.mark.nondestructive
class TestOrganizations(Katello_Test):

    @classmethod
    def setup_class(self):
        Katello_Test.setup_class.im_func(self)

        # List to trac orgs to cleanup
        self._cleanup_orgs = list()

    @classmethod
    def teardown_class(self):
        # Remove any left-over orgs
        if self.testsetup.test_cleanup:
            for name in self._cleanup_orgs:
                self.api.destroy_org(name)

        # Call parent cleanup
        Katello_Test.teardown_class.im_func(self)

    def test_create_new_org(self):
        """
        Returns Pass if creating a new org is successfull
        """
        home_page = self.load_page('Home')
        home_page.login()
        assert home_page.is_successful
        assert home_page.is_dialog_cleared

        home_page.click_tab('organizations')
        assert home_page.is_tab_selected('organizations')

        org_page = self.load_page('OrganizationsTab')
        new_org_name = self.random_str(prefix="Org_")
        org_page.create_new_org(new_org_name)
        self._cleanup_orgs.append(new_org_name)

        assert org_page.is_successful
        assert org_page.organization(new_org_name).is_displayed
        assert org_page.is_org_details_tab_present
        assert org_page.is_org_history_tab_present

    def test_duplicate_org_disallowed(self, mozwebqa):
        """
        Returns PASS if trying to create a org that exists
        fails.
        """
        home_page = self.katello.load_page('Home')
        new_org_name = self.random_str(prefix="duporg_")
        self.api.create_org(new_org_name)

        home_page.login()
        home_page.click_tab("organizations")

        org_page = self.load_page('OrganizationsTab')
        org_page.create_new_org(new_org_name)
        self._cleanup_orgs.append(new_org_name)

        assert home_page.is_failed

    @pytest.mark.bugzilla(772575)
    def test_recreate_previously_deleted_org(self, mozwebqa):
        home_page = self.katello.load_page('Home')
        home_page.login()
        assert home_page.is_successful

        home_page.click_tab("organizations")

        _new_org_name = self.random_str(prefix="recreateorg_")
        self.api.create_org(_new_org_name)

        home_page.click_tab("organizations")
        assert home_page.is_the_current_page

        org_page = self.load_page('OrganizationsTab')
        home_page.enter_search_criteria("recreateorg*")
        org_page.organization(_new_org_name).click()
        assert org_page.is_block_active
        org_page.remove_visible_org()
        assert home_page.is_successful

        # Wait for async remove to complete
        time.sleep(15)

        home_page.click_tab("organizations")
        assert home_page.is_the_current_page

        org_page.create_new_org(_new_org_name)
        self._cleanup_orgs.append(_new_org_name)
        assert home_page.is_successful

    def test_create_new_org_w_env(self, mozwebqa):
        '''
        Test to create a new org, with environment.
        '''
        home_page = self.katello.load_page('Home')
        home_page.login()
        assert home_page.is_successful
        assert home_page.header.is_user_logged_in

        home_page.click_tab("organizations")
        assert home_page.is_the_current_page

        ENVIRONMENTS = ["DEV", "TEST", "STAGE", "PROD"]
        randenv = random.choice(ENVIRONMENTS)

        org_page = self.load_page('OrganizationsTab')
        new_org_name = self.random_str(prefix="Org_")

        org_page.create_new_org(new_org_name, randenv)
        self._cleanup_orgs.append(new_org_name)
        assert home_page.is_successful
        assert org_page.organization(new_org_name).is_displayed
        assert org_page.is_org_details_tab_present
        assert org_page.is_org_history_tab_present

    def test_search_orgs(self,mozwebqa):

        # Create 4 randomly named orgs
        for i in range(1,5):
            org_name = self.random_str()
            self._cleanup_orgs.append(org_name)
            self.api.create_org(org_name)

        # Create 4 semi-randomly named orgs
        for i in range(1,5):
            org_name = self.random_str(prefix="SearchOrg_")
            self._cleanup_orgs.append(org_name)
            self.api.create_org(org_name)

        home_page = self.katello.load_page('Home')
        home_page.login()
        assert home_page.is_successful

        home_page.click_tab("organizations")

        # Search for matching orgs
        org_page = self.load_page('OrganizationsTab')
        org_page.enter_search_criteria("SearchOrg_*")
        assert len(org_page.organizations) > 0
        assert all([org.name.startswith("SearchOrg_") for org in org_page.organizations])

        # Search for all other orgs
        org_page.clear_search_criteria()
        org_page.enter_search_criteria("name:* NOT name:SearchOrg_*")
        assert len(org_page.organizations) > 0
        assert all([not org.name.startswith("SearchOrg_") for org in org_page.organizations])

