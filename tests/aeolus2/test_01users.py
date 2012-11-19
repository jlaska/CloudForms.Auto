import pytest
import apps
from data.dataset import Admin
from data.assert_response import *
from tests.aeolus2 import Aeolus_Test

# FIXME - the following causes pytest to skip all methods in 'Aeolus_Test'
## @pytest.mark.skipif("config.getvalue('enable-ldap')")
@pytest.mark.nonldap
@pytest.mark.setup
class TestUsers(Aeolus_Test):
    '''
    Create users and groups, then add users to those groups
    Use default credentials until users, groups and permissions are defined
    '''

    pytestmark = pytest.mark.skipif("config.getvalue('enable-ldap')")

    def test_create_users(self):
        '''
        Create users
        '''
        page = self.aeolus.load_page('Aeolus')
        page.login(user='admin', password='password')
        #assert page.login() == aeolus_msg['login']

        for user in Admin.users:
            assert page.create_user(user) == aeolus_msg['add_user']

        # TODO: not needed if teardown_class working
        # test cleanup
        #if pytest.config.getvalue('test.cleanup') == True:
        #    for user in Admin.users:
        #        assert page.delete_user(user["username"]) == \
        #               "User has been successfully deleted."

        #if page.product_ver == '1.0.1':
        #    page.logout()
        #else:
        #    assert page.logout() == "Aeolus Conductor | Login"


    @pytest.mark.skipif("config.getvalue('project-version') == '1.0.1'")
    def test_create_user_groups(self):
        '''
        create user groups
        '''
        page = self.aeolus.load_page('Aeolus')
        page.login(user='admin', password='password')
        #assert page.login() == aeolus_msg['login']

        for user_group in Admin.user_groups:
            assert page.create_user_group(user_group) == "User Group added"

        # test cleanup
        #if pytest.config.getvalue('test-cleanup') == True:
        #    for user_group in Admin.user_groups:
        #        assert page.delete_user_group(user_group["name"]) == \
        #               "Deleted user group " + user_group["name"]

        #assert page.logout() == "Aeolus Conductor | Login"

    @pytest.mark.skipif("config.getvalue('project-version') == '1.0.1'")
    def test_add_users_to_user_groups(self):
        page = self.aeolus.load_page('Aeolus')
        page.login(user='admin', password='password')
        #assert page.login() == aeolus_msg['login']

        # capture user IDs from "/users/" view
        for user in Admin.users:
            user["id"] = page.get_id_by_url("users", user["username"])

        # capture user_group IDs from "/user_groups/" view
        for user_group in Admin.user_groups:
            user_group["id"] = page.get_id_by_url("user_groups", user_group["name"])

        # add users to groups
        for group in Admin.user_groups:
            for user in Admin.users:
                if group['name'] in user['user_groups']:
                    assert page.add_user_to_group(group['id'], user['id']) ==\
                        aeolus_msg['add_user_to_group'] % \
                            user['fname'] + ' ' + user['lname']

         # test cleanup
         #if pytest.config.getvalue('test-cleanup')
         #    for group in Admin.user_groups:
         #        for user in Admin.users:
         #            if group['name'] in user['user_groups']:
         #                assert page.delete_user_from_group(group['id'], \
         #                    user['id']) == \
         #                    aeolus_msg['delete_user_from_group'] % \
         #                    user['fname'] + ' ' + user['lname']

    @pytest.mark.setup
    def test_add_permissions(self):
        page = self.aeolus.load_page('Aeolus')
        page.login(user='admin', password='password')

        for user_group in Admin.user_groups:
            page.grant_permissions("group", user_group)
        for user in Admin.users:
            page.grant_permissions("user", user)


    @pytest.mark.setup
    def test_add_selfservice_quota(self):
        page = self.aeolus.load_page('Aeolus')
        page.login()

        assert page.add_selfservice_quota(Admin.selfservice_quota) == \
            aeolus_msg['update_settings']
        page.add_selfservice_quota(Admin.selfservice_quota)
