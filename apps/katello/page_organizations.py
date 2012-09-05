import apps.katello
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait

class OrganizationsTab(apps.katello.KatelloPage):

    def __init__(self, **kwargs):
        kwargs['open_url'] = False # don't reload this page
        apps.katello.KatelloPage.__init__(self, **kwargs)

    # Define page specific locators
    _org_create_new_locator = (By.XPATH, "//a[@id='new']")
    _new_orgname_field_locator = (By.XPATH, "//input[@id='name']")
    _new_orgdesc_field_locator = (By.XPATH, "//textarea[@id='description']")
    _new_orgenv_name_field_locator = (By.XPATH, "//input[@id='envname']")
    _new_orgenvdesc_field_locator = (By.XPATH, "//textarea[@id='envdescription']")
    _new_org_save_button_locator = (By.XPATH, "//input[@id='organization_save']")

    _org_history_tab_locator = (By.XPATH, "//li[@id='history']")
    _org_details_tab_locator = (By.XPATH, "//li[@id='details']")

    _org_list_locator = (By.CSS_SELECTOR, "div.block")
    _org_block_active_locator = (By.CSS_SELECTOR, "div.block.active")
    _org_remove_item_locator = (By.CSS_SELECTOR, "a.remove_item")
    _confirmation_yes_locator = (By.XPATH, "//span[@class='ui-button-text'][text()='Yes']")

    def create_new_org(self, orgname, envname=None):
        new_org_locator = self.selenium.find_element(*self._org_create_new_locator)
        ActionChains(self.selenium).move_to_element(new_org_locator).\
            click().perform()

        # Input org name
        self.send_text(orgname, *self._new_orgname_field_locator)

        # Input org description
        self.send_text("This is a test organization, created by CloudForms.Auto", *self._new_orgdesc_field_locator)

        # Input default environment
        if envname != None:
            self.send_text(envname, *self._new_orgenv_name_field_locator)
            self.send_text("This is a test organization, created by CloudForms.Auto", *self._new_orgenvdesc_field_locator)

        org_save_button_locator = self.selenium.find_element(*self._new_org_save_button_locator)
        ActionChains(self.selenium).move_to_element(org_save_button_locator).\
            click().perform()

        #WebDriverWait(self.selenium, 20).until(lambda s: self.is_element_present(*self._org_block_active_locator))

    def remove_visible_org(self):
        WebDriverWait(self.selenium, 20).until(lambda s: s.find_element(*self._org_remove_item_locator).is_displayed())

        remove_button_locator = self.selenium.find_element(*self._org_remove_item_locator)
        ActionChains(self.selenium).move_to_element(remove_button_locator).\
            click().perform()

        WebDriverWait(self.selenium, 20).until(lambda s: s.find_element(*self._confirmation_yes_locator).is_displayed())

        confirm_button_locator = self.selenium.find_element(*self._confirmation_yes_locator)
        ActionChains(self.selenium).move_to_element(confirm_button_locator).\
            click().perform()

    def is_search_correct(self, criteria):
        WebDriverWait(self.selenium, 60).until(lambda s: s.find_element(*self._org_list_locator).is_displayed())
        for org in self.organizations:
            if criteria not in org.name:
                raise Exception('%s does not match Search Criteria %s' % (org.name, criteria))
        return True

    @property
    def is_org_details_tab_present(self):
        return self.is_element_present(*self._org_details_tab_locator)

    @property
    def is_org_history_tab_present(self):
        return self.is_element_present(*self._org_history_tab_locator)

    def organization(self, value):
        for organization in self.organizations:
            if value == organization.name:
                return organization
        raise Exception('Organization not found: %s' % value)

    @property
    def is_block_active(self):
        return self.is_element_present(*self._org_block_active_locator)

    @property
    def organizations(self):
        return [Organization(mozwebqa=self._mozwebqa, \
                             locators=self.locators, \
                             root_element=element) \
            for element in self.selenium.find_elements(*self._org_list_locator)]

class Organization(apps.katello.KatelloPage):

    _name_locator = (By.CSS_SELECTOR, "div.column_1.one-line-ellipsis")

    def __init__(self, **kwargs):
        self._root_element = kwargs.get('root_element', None)
        kwargs['open_url'] = False # don't reload this page
        apps.BasePage.__init__(self, **kwargs)

    @property
    def name(self):
        name_text = self._root_element.find_element(*self._name_locator).text
        return name_text

    @property
    def is_displayed(self):
        return self.is_element_visible(*self._name_locator)

    def click(self):
        self._root_element.find_element(*self._name_locator).click()
