import pytest
import apps
import tests

@pytest.mark.nondestructive
@pytest.mark.sanity
class TestHomePage(tests.katello.Katello_Test):

    def test_verify_page_title(self):
        home_page = self.katello.load_page('Home')
        assert home_page.is_the_current_page

    def test_verify_login_branding(self):
        home_page = self.katello.load_page('Home')
        assert home_page.is_login_logo_present

    def test_verify_page_branding(self):
        home_page = self.katello.load_page('Home')

        # login
        home_page.login()
        assert home_page.is_successful
        # Select org from interstitial
        if pytest.config.version_cmp('1.1') >= 0:
            home_page.select_org(pytest.config.getvalue('katello-org'))
        assert home_page.is_dialog_cleared

        # Still have branding?
        assert home_page.is_logo_present

    def test_verify_login_fields(self):
        '''
        Test whether the username and password fields exist
        '''
        home_page = self.katello.load_page('Home')
        assert home_page.is_username_field_present
        assert home_page.is_password_field_present
        assert home_page.is_login_button_present

    def test_admin_login_logout(self):
        home_page = self.katello.load_page('Home')

        # login
        home_page.login()
        assert home_page.is_successful

        # Select org from interstitial
        if pytest.config.version_cmp('1.1') >= 0:
            home_page.select_org(pytest.config.getvalue('katello-org'))
        assert home_page.is_dialog_cleared

        # logout
        home_page.click_logout()
        assert home_page.is_dialog_cleared

        # Make sure we're looking at a login screen
        assert home_page.is_username_field_present
        assert home_page.is_password_field_present
        assert home_page.is_login_button_present

    @pytest.mark.skipif("pytest.config.version_cmp('1.1') < 0")
    def test_admin_login_search_org(self):
        home_page = self.katello.load_page('Home')

        # login
        home_page.login()
        assert home_page.is_successful
        # assert home_page.is_dialog_cleared

        # Filter org list
        org = pytest.config.getvalue('katello-org')
        home_page.header.filter_org_in_switcher(org)

        # Make sure our filtered value is visible
        assert org in [o.name for o in home_page.selectable_orgs()]

        # Now select it filtered item
        home_page.header.click_filtered_result(org)

        # Are we logged in?
        assert home_page.header.is_user_logged_in

        # Is the org we chose still selected?
        assert home_page.header.get_text_from_switcher == org

    def test_invalid_login(self):
        home_page = self.katello.load_page('Home')
        home_page.login(password="bogus_password")
        assert home_page.is_failed
        home_page.click_notification_close()
        assert home_page.is_dialog_cleared

        home_page = self.katello.load_page('Home')
        home_page.login(user="bogus_username")
        assert home_page.is_failed
        home_page.click_notification_close()
        assert home_page.is_dialog_cleared
