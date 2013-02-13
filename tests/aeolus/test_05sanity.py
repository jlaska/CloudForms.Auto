import pytest
import apps
from tests.aeolus import Aeolus_Test

@pytest.mark.sanity
class TestLogin(Aeolus_Test):

    def test_verify_page_title(self):
        page = self.load_page('Home')
        assert page.is_the_current_page

    def test_verify_login_branding(self):
        page = self.load_page('Home')
        assert page.is_login_logo_present

    def test_verify_page_branding(self):
        page = self.load_page('Home')
        page.login()
        assert not page.is_failed

        # Still have branding?
        assert page.is_logo_present

    def test_valid_login(self):
        page = self.load_page('Aeolus')
        page.login()
        assert not page.is_failed

    def test_invalid_login(self):
        page = self.load_page('Aeolus')
        page.login(password="badpassword")
        assert page.is_failed

        page = self.load_page('Aeolus')
        page.login(user="baduser")
        assert page.is_failed

    def test_verify_login_fields(self):
        '''
        Test whether the username and password fields exist
        '''
        page = self.load_page('Aeolus')
        assert page.is_username_field_present
        assert page.is_password_field_present
        assert page.is_login_button_present
