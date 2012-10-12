import pytest
import apps
from tests.katello2 import Katello_Test

class TestUsers(Katello_Test):

    @classmethod
    def setup_class(self):
        Katello_Test.setup_class.im_func(self)

        # List to trac orgs to cleanup
        self._cleanup_users = list()

    @classmethod
    def teardown_class(self):
        # Remove any left-over user accounts
        if self.testsetup.test_cleanup:
            for name in self._cleanup_users:
                for match in self.api.list_users(name=name):
                    self.api.destroy_user(match['id'])

        # Call parent cleanup
        Katello_Test.teardown_class.im_func(self)

    def test_create_new_user(self, mozwebqa):
        '''
        Test to create a new User, no org, no environment.
        '''

        # Login
        home_page = self.load_page('Home')
        home_page.login()
        assert home_page.is_dialog_cleared

        # FIXME - use data/
        administration = self.load_page('User_Administration')
        new_user_name = self.random_str("newuser-")
        password = self.random_str()
        email_addr = new_user_name + "@example.com"
        administration.create_new_user(new_user_name, password, password, email_addr)
        self._cleanup_users.append(new_user_name)

        assert home_page.is_successful
        assert administration.user(new_user_name).is_displayed

    def test_duplicate_user_disallowed(self, mozwebqa):
        """
        Returns Pass if creating a existing user fails.
        """

        # Create new user using API
        new_user_name = self.random_str("dupuser-")
        password = self.random_str()
        email_addr = new_user_name + "@example.com"
        self.api.create_user(new_user_name, password, email_addr)
        self._cleanup_users.append(new_user_name)

        # Logi
        home_page = self.load_page('Home')
        home_page.login()
        assert home_page.is_dialog_cleared

        # Attempt to create duplicate user
        administration = self.load_page('User_Administration')
        administration.create_new_user(new_user_name, password, password, email_addr)
        assert home_page.is_failed

    def test_remove_a_user(self, mozwebqa):
        '''
        Test to remove a single user.
        '''
        # Create user using API
        new_user_name = self.random_str("rmuser-")
        password = self.random_str()
        email_addr = new_user_name + "@example.com"
        self.api.create_user(new_user_name, password, email_addr)
        self._cleanup_users.append(new_user_name)

        # Login to UI
        home_page = self.load_page('Home')
        home_page.login()
        assert home_page.is_dialog_cleared

        # Find existing user
        administration = self.load_page('User_Administration')
        home_page.enter_search_criteria(new_user_name)

        # Remove user
        administration.user(new_user_name).click()
        home_page.click_remove()
        home_page.click_confirm()
        assert home_page.is_successful

    def test_user_search(self, mozwebqa):
        # Create 4 users with random names
        for i in range(4):
            new_user_name = self.random_str()
            password = self.random_str()
            email_addr = new_user_name + "@example.com"
            self.api.create_user(new_user_name, password, email_addr)
            self._cleanup_users.append(new_user_name)

        # Create 4 users with name: searchuser-*
        for i in range(4):
            new_user_name = self.random_str("searchuser-")
            password = self.random_str()
            email_addr = new_user_name + "@example.com"
            self.api.create_user(new_user_name, password, email_addr)
            self._cleanup_users.append(new_user_name)

        # Login to UI
        home_page = self.load_page('Home')
        home_page.login()
        assert home_page.is_dialog_cleared

        # Search for users matching 'searchuser-*'
        administration = self.load_page('User_Administration')
        administration.enter_search_criteria("searchuser-*")
        assert len(administration.users) >= 4
        assert all([user.name.startswith("searchuser-") \
            for user in administration.users])

        # Search for all other users (NOT 'searchuser-*')
        administration.clear_search_criteria()
        administration.enter_search_criteria("username:* NOT username:searchuser-*")
        assert len(administration.users) >= 4
        assert all([not org.name.startswith("searchuser-") \
            for org in administration.users])

    def test_change_user_password_valid_as_admin(self, mozwebqa):

        # Create new user using API
        new_user_name = self.random_str("chgpasswd-")
        password = self.random_str()
        email_addr = new_user_name + "@example.com"
        self.api.create_user(new_user_name, password, email_addr)
        self._cleanup_users.append(new_user_name)

        # Login to UI
        home_page = self.load_page('Home')
        home_page.login()
        assert home_page.is_dialog_cleared

        # Search for users matching 'searchuser-*'
        administration = self.load_page('User_Administration')
        home_page.enter_search_criteria(new_user_name)
        administration.user(new_user_name).click()
        new_password = self.random_str()
        administration.change_password(new_password)
        assert home_page.is_successful

    def test_change_user_password_does_not_match_as_admin(self, mozwebqa):

        # Create new user using API
        new_user_name = self.random_str("chgpasswd-")
        password = self.random_str()
        email_addr = new_user_name + "@example.com"
        self.api.create_user(new_user_name, password, email_addr)
        self._cleanup_users.append(new_user_name)

        # Login to UI
        home_page = self.load_page('Home')
        home_page.login()
        assert home_page.is_dialog_cleared

        # Load users page
        administration = self.load_page('User_Administration')
        home_page.enter_search_criteria(new_user_name)
        administration.user(new_user_name).click()
        new_password = self.random_str()
        confirm_password = self.random_str()
        administration.change_password(new_password, confirm_password)
        assert administration.passwords_do_not_match_visible

    def test_login_non_admin(self, mozwebqa):

        # Create non-admin user to test with
        new_user_name = self.random_str("random-")
        password = self.random_str()
        email_addr = new_user_name + "@example.com"
        self.api.create_user(new_user_name, password, email_addr)
        self._cleanup_users.append(new_user_name)

        # Login to UI
        home_page = self.load_page('Home')
        home_page.login(new_user_name, password)
        assert home_page.is_dialog_cleared
