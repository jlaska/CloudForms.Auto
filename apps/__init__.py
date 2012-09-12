import os
import sys
import importlib
import inspect
import glob
import locators as bl
import logging
import apps.locators

# Enable debug
# logging.getLogger().setLevel(logging.DEBUG)

from unittestzero import Assert
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotVisibleException

def initializeProduct(mozwebqa):
    '''
    Return an initialized product class
    '''

    assert hasattr(mozwebqa, 'project'), "Expecting project attribute"

    return getProductClass(mozwebqa.project, \
        getattr(mozwebqa, 'version', None))(mozwebqa)

def getProductClass(product=None, version=None):
    '''
    Find and return a subclass of BaseProduct matching the supplied name.

    Args:
        product (str): module name to search for
        version (str):

    Returns:
        __class__: subclass of BaseProduct

    Raises:
        AssertError, ImportError, NotImplementedError
    '''

    # Check argument(s)
    assert isinstance(product, str), "Invalid product type supplied (%s != str)" % type(product)

    # Ensure product is prefixed with 'apps.'
    if not product.startswith('apps.'):
        product = 'apps.' + product

    # Determine 'package' argument to import_module
    # Converts 'apps.katello.cfse' -> 'apps.katello'
    package = product[0:product.rindex('.')]
    obj = importlib.import_module(product, package)

    # Find the subclass of BaseProduct
    for (name, cls) in inspect.getmembers(obj, inspect.isclass):
        if issubclass(cls, BaseProduct):
            return cls

    # If we get here ... we didn't find a matching class
    raise NotImplementedError("No class BaseProduct subclass matching '%s' found" % product)

class BaseProduct(object):
    """
    Base class for all Products
    """
    locators = apps.locators.BaseLocators()

    def __init__(self, mozwebqa=None):
        """
        Default values for all products; likely won't be used
        as we focus on the differences.
        """
        # Ensure caller is a derived instance
        if self.__class__ == BaseProduct:
            raise NotImplementedError("Please sub-class")

        self._mozwebqa = mozwebqa

        assert self.locators is not None, "No locators defined"
        # self.locators = apps.locators.BaseLocators()

        # Dynamically build the locators
        # self.locators = self._load_locators()
        logging.debug("Loaded locators: %s" % self.locators)

        # Dynamically build the list of application pages
        self.pages = self._load_all_pages()
        logging.debug("Loaded pages: %s" % self.pages.values())

    def _load_all_pages(self):
        '''
        Cache all page modules for the current product.  Scans for modules
        matching the glob expression 'page_*.py'.  Any subclasses of BasePage
        within the module are saved to self.pages as a dictionary.
        '''

        # initialize pages dict
        pages = dict()

        # Walk through the class inheritance list
        for cls in inspect.getmro(self.__class__):

            logging.debug("Inspecting class: %s" % cls)

            # Stop when we reach the base new-style class
            if cls is object:
                break

            # Determine the relative module path
            modpath = os.path.realpath(inspect.getmodule(cls).__path__[0])
            logging.debug("modpath for %s: %s" % (cls, modpath))

            # Determine PWD
            pwd = os.path.realpath(os.environ.get('PWD',''))
            logging.debug("pwd: %s" % (pwd))

            # Determine common prefix between pwd and modpath
            prefix = os.path.commonprefix([pwd, modpath])
            # If needed, add common prefix to sys.path
            if prefix not in sys.path:
                logging.debug("Adding '%s' to sys.path" % prefix)
                sys.path.insert(0, prefix)

            # Find applicable page_ modules
            logging.debug("Looking for pages in: %s" % modpath)
            modules = glob.glob("%s/page_*.py" % modpath)

            # Inspect each module for a BasePage class
            for mod_file in modules:

                logging.debug("Inspecting page module: %s" % mod_file)

                # Convert mod_file to a module name
                # '/path/to/foo/bar/baz.py' -> 'foo.bar.baz'
                # Drop .py extension
                mod_file = os.path.splitext(mod_file)[0]
                # Remove the common directory prefix
                modname = mod_file.replace(prefix, '')
                # replace '/' with '.'
                modname = modname.replace('/', '.')
                # Remove a prefixing '.'
                if modname.startswith('.'):
                    modname = modname[1:]

                # Determine 'package' argument to import_module
                # Converts 'apps.katello.cfse' -> 'apps.katello'
                package = modname[0:modname.rindex('.')]

                # import module
                logging.debug("importlib.import_module('%s', '%s')" % (modname, package))
                obj = importlib.import_module(modname, package)

                # Look for a subclass of type BasePage
                for (name, cls) in inspect.getmembers(obj, inspect.isclass):
                    # If a subclass of BasePage, and we haven't already loaded
                    # this object ... remember this page
                    if issubclass(cls, BasePage) and not pages.has_key(name):
                        logging.debug("found page: %s" % name)
                        pages[name] = cls

            # Scan the parent for matching modules
            modpath = os.path.dirname(modpath)

        return pages

    def load_page(self, page, **kwargs):
        '''
        Convenience method to return a properly initialized page (derived from
        BasePage)
        '''
        # A case-insensative search for a match
        for k in [page, page.lower()]:
            if self.pages.has_key(k):
                # Add universal mozwebqa object
                if not kwargs.has_key('mozwebqa'):
                    kwargs['mozwebqa'] = self._mozwebqa
                # Add app-specific locators
                if not kwargs.has_key('locators'):
                    kwargs['locators'] = self.locators
                return self.pages[k](**kwargs)

        raise NotImplementedError("No page matching '%s' found" % page)

class BasePage(object):
    """
    Base class for all Pages; sets up the default page.

    :param base_url: url of the application.
    :param timeout: default is 10, can be overridden.
    :param project: Name of project to be tested (sam, headpin, cfse, katello)
    :param org: org selector for katello
    """
    def __init__(self, **kwargs):
        assert kwargs.has_key('mozwebqa'), "Initialized without 'mozwebqa' keyword"
        assert not kwargs.get('mozwebqa', None) is None, "BasePage.mozwebqa initialized with None'"
        self._mozwebqa = kwargs.get('mozwebqa', None)

        if kwargs.has_key('locators'):
            self.locators = kwargs.get('locators')

    @property
    def selenium(self):
        return self._mozwebqa.selenium
    @property
    def base_url(self):
        return self._mozwebqa.base_url
    @property
    def timeout(self):
        return self._mozwebqa.timeout
    @property
    def project(self):
        return self._mozwebqa.project
    @property
    def org(self):
        return self._mozwebqa.org

    def login(self, user="admin", password="password"):
        self.send_text(user, *self.locators.username_text_field)
        self.send_text(password, *self.locators.password_text_field)
        self.click(*self.locators.login_locator)
        #return self.get_text(*self.locators.confirmation_msg)

    # FIXME - Should random_string be part of the BasePage, or more a shared test object?
    def random_string(self):
        """
        Generates a random *alphanumeric* string between 4 and 6 characters
        in length.
        """
        chars = string.ascii_letters + string.digits
        return "".join(random.choice(chars) for x in range(random.randint(4, 6)))

    @property
    def page_title(self):
        """
        Returns the page's title.
        """
        WebDriverWait(self.selenium, 20).until(lambda s: self.selenium.title)
        return self.selenium.title

    @property
    def redhat_logo_title(self):
        """
        Returns the title attribute for the Red Hat logo.
        """
        return self.selenium.find_element(*self.locators.redhat_logo_link_locator).get_attribute('title')

    def send_characters(self, text, *locator):
        WebDriverWait(self.selenium, 60).until(lambda s: s.find_element(*locator).is_enabled())
        input_locator = self.selenium.find_element(*locator)
        for c in text:
            input_locator.send_keys(c)

    def send_text(self, text, *locator):
        """
        Sends text to locator, one character at a time.
        """
        WebDriverWait(self.selenium, 60).until(lambda s: s.find_element(*locator).is_enabled())
        input_locator = self.selenium.find_element(*locator)
        input_locator.send_keys(text)

    def send_text_and_wait(self, text, *locator):
        self.send_text(text, *locator)
        self.jquery_wait()

    def select(self, locatorid, value):
        """
        Selects options in locatorid by value.
        """
        Select(self.selenium.find_element_by_id(locatorid)).select_by_value(value)

    def return_to_previous_page(self):
        """
        Simulates a Back (Return to prior page).
        """
        self.selenium.back()

    def mouse_to_element(self, *locator):
        WebDriverWait(self.selenium, 60).until(lambda s: s.find_element(*locator).is_displayed())
        element = self.selenium.find_element(*locator)
        ActionChains(self.selenium).move_to_element(element).perform()

    @property
    def is_the_current_page(self):
        """
        Returns True if page title matches expected page title.
        """
        if self.locators.page_title:
            WebDriverWait(self.selenium, 10).until(lambda s: self.selenium.title)
        Assert.equal(self.selenium.title, self.locators.page_title,
                     "Expected page title: %s. Actual page title: %s" % (self.locators.page_title, self.selenium.title))
        return True

    def jquery_wait(self, timeout=20):
        """
        For Active jQuery to complete, default timeout is 20 seconds.
        """
        WebDriverWait(self.selenium, timeout).until(lambda s: s.execute_script("return jQuery.active == 0"))

    @property
    def is_successful(self):
        """
        Returns True if test is successful resulting in the success notification locator being displayed.
        """
        self.selenium.implicitly_wait(4)
        return WebDriverWait(self.selenium, 6).until(lambda s: s.find_element(*self.locators.success_notification_locator).is_displayed())

    @property
    def is_dialog_cleared(self):
        """
        Returns True if the success and notification locators are *NOT* present
        """
        self.selenium.implicitly_wait(2)
        results = list()
        for loc in [self.locators.success_notification_locator, \
                    self.locators.error_notification_locator]:
            try:
                results.append(WebDriverWait(self.selenium, 6).until_not(lambda s: s.find_element(*loc).is_displayed()))
            except Exception, e:
                # Assume failure means we couldn't find the locator
                results.append(True)
        self.selenium.implicitly_wait(self._mozwebqa.default_implicit_wait)
        return False not in results

    @property
    def is_failed(self):
        """
        Returns True if the error notification locator is displayed.
        """
        self.selenium.implicitly_wait(4)
        try:
            return self.selenium.find_element(*self.locators.error_notification_locator).is_displayed()
        except Exception, e:
            return False
        finally:
            self.selenium.implicitly_wait(self._mozwebqa.default_implicit_wait)

    def get_url_current_page(self):
        """
        Returns the url of the current page.
        """
        return(self.selenium.current_url)

    def is_element_present(self, *locator):
        """
        Returns True if locator is present.
        """
        try:
            WebDriverWait(self.selenium, 5).until(lambda s: s.find_element(*locator))
            return True
        except Exception as e:
            return False

    def is_element_visible(self, *locator):
        """
        Returns True if locator is visible.
        """
        try:
            return WebDriverWait(self.selenium, 10).until(lambda s: s.find_element(*locator).is_displayed())
        except Exception as e:
            return False

    def is_element_editable(self, *locator):
        """
        Returns True if the element can be edited.
        """
        return WebDriverWait(self.selenium, 10).until(lambda s: s.find_element(*locator).is_enabled())

    def get_location(self, *locator):
        """
        Returns the location of locator.
        """
        try:
            return self.selenium.find_element(*locator).location
        except NoSuchElementException, ElementNotVisibleException:
            return False

    def get_text(self, *locator):
        return self.selenium.find_element(*locator).text

    #
    # Basic navigation helpers
    #
    def go_to_home_page(self):
        # from --baseurl= arg
        self.selenium.get(self.base_url)

    def go_to_url(self, url):
        # pass in url
        self.selenium.get(url)

    def go_to_page_view(self, view):
        # pass in view, e.g. system for katello/system
        self.selenium.get(self.base_url + "/" + view)

    def url_by_text(self, css, name):
        _text_locator = (By.XPATH, "//%s[text() = '%s']" % (css, name))
        return self.selenium.find_element(*_text_locator).get_attribute("href")

    #
    # Click functions
    #
    def click(self, *locator):
        """
        Executes a Left Mouse Click on locator.
        """
        WebDriverWait(self.selenium, 60).until(lambda s: s.find_element(*locator).is_displayed())
        click_locator = self.selenium.find_element(*locator)
        ActionChains(self.selenium).move_to_element_with_offset(click_locator, 3, 3).click().perform()

    def click_and_wait(self, *locator):
        self.click(*locator)
        self.jquery_wait()

    def click_by_text(self, css, name):
        _text_locator = (By.XPATH, "//%s[text() = '%s']" % (css, name))
        self.selenium.find_element(*_text_locator).click()

    def click_next(self):
        """ Click the *Next* button.
        """
        self.click(*self.locators.next_button_locator)

    def click_close(self):
        """
        Click the *Close* button.
        """
        self.click(*self.locators.close_item_locator)

    def click_remove(self):
        """
        Click on *Remove item* locator.
        """
        self.click(*self.locators.remove_item_locator)

    def click_new(self):
        """
        Click on the *New item* locator.
        """
        self.click(*self.locators.new_item_locator)

    def click_confirm(self):
        """
        Click on the *Confirm* locator.
        """
        self.click(*self.locators.confirmation_yes_locator)

    def click_popup_confirm(self):
        """
        Confirm javascript popup
        """
        alert = self.selenium.switch_to_alert()
        alert.accept()

    def click_tab(self, tab):
        """
        Execute a left mouse click on `tab`.
        :param tab: str tab to click
        """
        self.click_and_wait(*self.locators.tab_elements[tab])
    '''
    @property
    def redhat_logo_image_source(self):
        """
        Returns the src attribute for the Red Hat Logo image locator.
        """
        return self.selenium.find_element(*self._amo_logo_image_locator).get_attribute('src')
    '''

    #
    # UI elements
    #

    @property
    def is_footer_version_text_visible(self):
        """
        Return True if the Footer version Text is visible.
        """
        return self.selenium.find_element(*self.locators.footer_version_text_locator).text

    @property
    def is_redhat_logo_visible(self):
        """
        Return True if the appropriate logo is visible. ::

            This is dependent on the project name passed at runtime.
        """
        return self.is_element_visible(*self.locators._logo_locator)

    def click_redhat_logo(self):
        """
        Will execute a left mouse click on the Logo locator.
        """
        self.click(*self.locators.redhat_logo_link_locator)

    def clear_text_input(self, *locator):
        '''
        Generic method for clearing all text from a text input field.
        '''
        field_locator = self.selenium.find_element(*locator)
        ActionChains(self.selenium).move_to_element(field_locator)\
            .click()\
            .key_down(Keys.CONTROL)\
            .send_keys('a')\
            .send_keys(Keys.DELETE).perform()
