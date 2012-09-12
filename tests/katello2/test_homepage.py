import pytest
import apps
import tests

@pytest.mark.nondestructive
class TestHomePage(tests.katello2.Katello_Test):

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
        assert home_page.is_dialog_cleared

        # Still have branding?
        assert home_page.is_login_logo_present

    def test_username_password_text_fields_present(self):
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
        assert home_page.is_dialog_cleared

        # FIXME -- make this version specific
        # home_page.select_org(home_page.org).click()

        # logout
        home_page.click_logout()
        assert home_page.is_dialog_cleared

        # Make sure we're looking at a login screen
        assert home_page.is_username_field_present
        assert home_page.is_password_field_present
        assert home_page.is_login_button_present

    def test_invalid_login(self):
        home_page = self.katello.load_page('Home')
        home_page.login("admin", "badpassword")
        assert home_page.is_failed
        home_page.click_notification_close()
        assert home_page.is_dialog_cleared

        home_page = self.katello.load_page('Home')
        home_page.login("bogus_username", "password")
        assert home_page.is_failed
        home_page.click_notification_close()
        assert home_page.is_dialog_cleared
