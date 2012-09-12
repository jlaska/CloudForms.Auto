#!/usr/bin/env python

import pytest
import apps
from data.large_dataset import Admin
from data.assert_response import *
from tests.aeolus2 import Aeolus_Test

def setup_module(module):
    test_setup = pytest.config.pluginmanager.getplugin("mozwebqa")
    module.TestAdmin.aeolus = apps.initializeProduct(test_setup.TestSetup)

class TestAdmin(Aeolus_Test):

    @classmethod
    def setup_class(self):
        Aeolus_Test.setup_class.im_func(self)

        # List to trac users to cleanup
        self._cleanup_users = list()

    @classmethod
    def teardown_class(self):
        # Remove users
        if self.testsetup.test_cleanup:
            for name in self._cleanup_users:
                # FIXME
                assert Aeolus.delete_user(name) == \
                    aeolus_msg['delete_user']

        # Call parent cleanup
        Aeolus_Test.teardown_class.im_func(self)

    @pytest.mark.user_admin
    @pytest.mark.aeolus_setup
    def test_create_users(self, mozwebqa):
        '''
        Create users
        '''
        page = self.aeolus.load_page('Aeolus')
        page.login()
        #assert page.login() == aeolus_msg['login']

        for user in Admin.users:
            assert page.create_user(user) == aeolus_msg['add_user']
            self._cleanup_users.append(user['username'])

        # TODO: not needed if teardown_class working
        # test cleanup
        #if page.test_cleanup == True:
        #    for user in Admin.users:
        #        assert page.delete_user(user["username"]) == \
        #               "User has been successfully deleted."

        #if page.product_ver == '1.0.1':
        #    page.logout()
        #else:
        #    assert page.logout() == "Aeolus Conductor | Login"

    @pytest.mark.skipif("config.getvalue('product_version') == '1.0.1'")
    @pytest.mark.user_admin
    @pytest.mark.aeolus_setup
    def test_create_user_groups(self, mozwebqa):
        '''
        create user groups
        '''
        page = self.aeolus.load_page('Aeolus')
        page.login()
        #assert page.login() == aeolus_msg['login']

        for user_group in Admin.user_groups:
            assert page.create_user_group(user_group) == "User Group added"

        # test cleanup
        #if page.test_cleanup == True:
        #    for user_group in Admin.user_groups:
        #        assert page.delete_user_group(user_group["name"]) == \
        #               "Deleted user group " + user_group["name"]

        #assert page.logout() == "Aeolus Conductor | Login"

    @pytest.mark.skipif("config.getvalue('product_version') == '1.0.1'")
    def test_add_users_to_user_groups(self, mozwebqa):
        page = self.aeolus.load_page('Aeolus')
        page.login()
        #assert page.login() == aeolus_msg['login']

        # move to aeolus_page.py
        # capture user IDs from "/users/" view
        for user in Admin.users:
            user["id"] = page.get_user_id(user["username"])

        # capture user_group IDs from "/user_groups/" view
        for user_group in Admin.user_groups:
            user_group["id"] = page.get_user_group_id(user_group["name"])

        # add users to groups
        for group in Admin.user_groups:
            for user in Admin.users:
                if group['name'] in user['user_groups']:
                    assert page.add_user_to_group(group['id'], user['id']) ==\
                        aeolus_msg['add_user_to_group'] % \
                            user['fname'] + ' ' + user['lname']

         # test cleanup
         #if self.testsetup.test_cleanup:
         #    for group in Admin.user_groups:
         #        for user in Admin.users:
         #            if group['name'] in user['user_groups']:
         #                assert page.delete_user_from_group(group['id'], \
         #                    user['id']) == \
         #                    aeolus_msg['delete_user_from_group'] % \
         #                    user['fname'] + ' ' + user['lname']

    @pytest.mark.xfail
    def test_add_selfservice_quota(self, mozwebqa):
        page = self.aeolus.load_page('Aeolus')
        page.login()

        #assert page.add_selfservice_quota(Admin.selfservice_quota) == aeolus_msg['update_settings']
        page.add_selfservice_quota(Admin.selfservice_quota)
