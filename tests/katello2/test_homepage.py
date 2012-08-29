import time
import pytest
import apps
import logging

@pytest.mark.nondestructive
class TestHomePage(object):

    def test_verify_page_title(self, mozwebqa):
        katello = apps.getProductClass(mozwebqa.project)(mozwebqa)
        home_page = katello.load_page('Home')
        assert home_page.is_the_current_page

    def test_username_password_text_fields_present(self, mozwebqa):
        '''
        Test whether the username and password fields exist
        '''
        katello = apps.getProductClass(mozwebqa.project)(mozwebqa)
        home_page = katello.load_page('Home')
        assert home_page.is_username_field_present
        assert home_page.is_password_field_present

    def test_admin_login_logout(self, mozwebqa):
        katello = apps.getProductClass(mozwebqa.project)(mozwebqa)
        home_page = katello.load_page('Home')

        # login
        home_page.login()
        assert home_page.is_successful
        assert home_page.is_dialog_cleared

        # FIXME -- make this version specific
        # home_page.select_org(home_page.org).click()

        # logout
        home_page.click_logout()
        assert home_page.is_successful
        assert home_page.is_dialog_cleared
        # Make sure we're looking at a login screen
        assert home_page.is_username_field_present
        assert home_page.is_password_field_present

    def test_invalid_login(self, mozwebqa):
        katello = apps.getProductClass(mozwebqa.project)(mozwebqa)
        home_page = katello.load_page('Home')
        home_page.login("admin", "badpassword")
        assert home_page.is_failed
        home_page.click_notification_close()
        assert home_page.is_dialog_cleared
        home_page.login("bogus_username", "password")
        assert home_page.is_failed
