import apps
import locators
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait

class Katello(apps.BaseProduct):
    '''test'''
    locators = locators.KatelloLocators()

class KatelloPage(apps.BasePage):
    '''Page class'''

    # "Katello - Open Source Systems Management"

    def __init__(self, **kwargs):
        apps.BasePage.__init__(self, **kwargs)

    # Katello specific page content

    @property
    def header(self):
        return HeaderRegion(mozwebqa=self._mozwebqa, locators=self.locators, open_url=False)

    def select_org(self, value):
        """
        Select an org from the available orgs.
        :param value: The org to look for, by text.
        """
        self.click(*self.locators.login_org_dropdown)
        for org in self.selectable_orgs():
            if value in org.name:
                return org
        raise Exception('Organization not found: %s' % value)

    def selectable_orgs(self):
        """
        Iterate over the available orgs in the login org selector.
        """
        return [self.LoginOrgSelector(dict(mozwebqa=self._mozwebqa, element=element))
            for element in self.selenium.find_elements(*self.locators.login_org_selector)]

    def is_tab_selected(self, tab_name):
        """
        Return True if the provided tab is active and displayed.

        Parameters:
            tab_name (string): Must match a key from the self.locators.tab_elements dictionary
        Returns:
            boolean
        """
        assert self.locators.tab_elements.has_key(tab_name), "Undefined tab_name ('%s') specified" % tab_name

        return self.selenium.find_element(*self.locators.selected_tab(tab_name)).is_displayed()

    def clear_search_criteria(self):
        """
        Select any existing text (ctrl-a), and press DELETE
        :param criteria: string
        """

        # FIXME - use the UI elements to clear the searchbox (e.g. query_button
        # and query_clear)
        search_locator = self.selenium.find_element(*self.locators.search_input_locator)
        ActionChains(self.selenium).move_to_element(search_locator)\
            .click()\
            .key_down(Keys.CONTROL)\
            .send_keys('a')\
            .send_keys(Keys.DELETE).perform()

    def enter_search_criteria(self, criteria):
        """
        Search for criteria
        :param criteria: string
        """

        # Input criteria and newline
        self.send_text_and_wait(criteria + "\n", *self.locators.search_input_locator)

class LoginOrgSelector(apps.BasePage):
    _name_locator = (By.CSS_SELECTOR, 'a.fl.clear')

    def __init__(self, **kwargs):
        apps.BasePage.__init__(self, **kwargs)
        self._root_element = kwargs.get('element')

    @property
    def name(self):
        name_text = self._root_element.find_element(*self._name_locator).text
        return name_text

    @property
    def is_displayed(self):
        return self.is_element_visible(*self._name_locator)

    def click(self):
        self._root_element.find_element(*self._name_locator).click()

class HeaderRegion(apps.BasePage):
    """
    Define actions specific to the *Header* Region of the page.
    """

    def click_logout(self):
        """
        Execute a left mouse click on the logout element.
        """
        self.click(*self.locators.logout_locator)

    @property
    def is_user_logged_in(self):
        """
        Return True if evidence exists that the user is logged in.
        """
        return self.is_element_visible(*self.locators.account_controller_locator)

    def click_hello(self):
        """
        Execute a left mouse click on the hello link locator.
        """
        self.click(*self.locators.account_controller_locator)

    @property
    def is_org_list_present(self):
        """
        Return True if evidence exists that the org switcher list is available
        """
        return self.is_element_visible(*self.locators.switcher_org_box_locator)

    def click_switcher(self):
        """
        Click the org switcher.
        """
        self.click(*self.locators.org_switcher_locator)

    def select_org_from_switcher(self, value=None):
        """
        Execute a left mouse click on an org from the org switcher.
        """
        orgs = self.selenium.find_elements(*self.locators.switcher_org_list_locator)
        for org in orgs:
            if org.text == value:
                org.click()
                break

        # I believe the following code selects the second org in the org list
        # ... not sure why this is useful
        #WebDriverWait(self.selenium, 20).until(lambda s: s.find_element(*self.locators.org_switcher_org_locator).is_displayed())
        #self.selenium.find_element(*self.locators.org_switcher_org_locator).click()

    @property
    def get_text_from_switcher(self):
        """
        Returns the current text from the org switcher.
        """
        return self.selenium.find_element(*self.locators.org_switcher_locator).text

    def filter_org_in_switcher(self, criteria):
        """
        Filter the org out of the switcher that you wish to use.
        """
        self.send_text(criteria, *self.locators.org_input_filter_locator)

    def click_filtered_result(self, criteria):
        """
        Execute a left mouse click on the filtered org.
        """
        _org_filtered_result_locator = (By.XPATH, "//a[contains(text(), '" + criteria + "')]")
        self.selenium.find_element(*_org_filtered_result_locator).click()

    def select_a_random_switcher_org(self):
        """
        Select a random org from the org switcher.
        """
        orgs = self.selenium.find_elements(*self.locators.switcher_org_list_locator)
        org = orgs[random.randint(0, len(orgs)-1)]
        org.click()
