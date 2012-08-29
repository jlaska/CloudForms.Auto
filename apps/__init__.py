#!/usr/bin/env python

import importlib
import inspect
import glob
import os
import locators as bl
import logging

# Enable debug
# logging.getLogger().setLevel(logging.DEBUG)

from unittestzero import Assert
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotVisibleException

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

    # '''Older deprecated python 2.* way ...'''
    # import imputil
    # # FIXME - this only works for first-order modules (e.g. 'apps.*').  Anything else (e.g. 'apps.katello.cfse') will need special handling
    # found =  imputil.imp.find_module(product, ['apps'])
    # obj = imputil.imp.load_module(product, found[0], found[1], found[2])
    # return obj

class BaseProduct(object):
    """
    Base class for all Products
    """
    def __init__(self, mozwebqa=None):
        """
        Default values for all products; likely won't be used
        as we focus on the differences.
        """
        self._mozwebqa = mozwebqa
        self._locators = self._load_locators()
        logging.debug("Loaded locators: %s" % self._locators)
        self._pages = self._load_all_pages()
        logging.debug("Loaded pages: %s" % self._pages.values())

        # Ensure caller is a derived instance
        if self.__class__ == BaseProduct:
            raise NotImplementedError("Please sub-class")

    def _load_all_pages(self):
        '''
        Cache all page modules for the current product.  Scans for modules
        matching the glob expression 'page_*.py'.  Any subclasses of BasePage
        are saved to the self._pages as a dictionary.
        '''

        # initialize pages dict
        pages = dict()

        # Get a relative path to the current module
        modpath = inspect.getmodule(self).__path__[0]
        modpath = modpath.replace(os.environ.get('PWD',''),'')
        if modpath.startswith('/'):
            modpath = modpath[1:]

        while modpath:
            logging.debug("(pages): looking for pages in: %s" % modpath)

            # Find other modules matching a specific glob pattern
            modules = glob.glob("%s/page_*.py" % modpath)
            for mod in modules:
                # skip __init__.py
                if '__init__.py' in mod or 'locators.py' in mod:
                    continue

                # remove .py
                mod = mod[:-3]
                # replace '/' with '.'
                modname = mod.replace('/', '.')

                # Determine 'package' argument to import_module
                # Converts 'apps.katello.cfse' -> 'apps.katello'
                package = modname[0:modname.rindex('.')]

                # import module
                logging.debug("(pages): importlib.import_module('%s', '%s')" % (modname, package))
                obj = importlib.import_module(modname, package)

                # Find the subclass of BasePage
                for (name, cls) in inspect.getmembers(obj, inspect.isclass):
                    # If a subclass of BasePage, and we haven't already loaded
                    # this object
                    if issubclass(cls, BasePage) and not pages.has_key(name):
                        logging.debug("(pages): found page: %s" % name)
                        pages[name] = cls

            # Scan the parent for matching modules
            modpath = os.path.dirname(modpath)

        return pages

    def _load_locators(self):

        # initialize Locators object
        locators = None

        # Get a relative path to the current module
        modpath = inspect.getmodule(self).__path__[0]
        modpath = modpath.replace(os.environ.get('PWD',''),'')
        if modpath.startswith('/'):
            modpath = modpath[1:]

        # FIXME - Can find do this for us instead?
        while modpath and locators is None:
            logging.debug("(locators): looking for locators in: %s" % modpath)

            # Find other modules matching a specific glob pattern
            modules = glob.glob("%s/locators.py" % modpath)
            for mod in modules:

                # remove .py
                mod = mod[:-3]
                # replace '/' with '.'
                modname = mod.replace('/', '.')

                # Determine 'package' argument to import_module
                # Converts 'apps.katello.cfse' -> 'apps.katello'
                package = modname[0:modname.rindex('.')]

                # import module
                logging.debug("(locators): importlib.import_module('%s', '%s')" % (modname, package))
                obj = importlib.import_module(modname, package)

                # Find the subclass of BaseLocators
                for (name, cls) in inspect.getmembers(obj, inspect.isclass):
                    # If a subclass of BaseLocators, and we haven't already loaded
                    # this object
                    if issubclass(cls, bl.BaseLocators):
                        # FIXME ... scan for desired version
                        logging.debug("(locators): found locator: %s" % name)
                        locators = cls
                        break

            # Scan the parent for matching modules
            modpath = os.path.dirname(modpath)

        return locators

    def load_page(self, page, **kwargs):
        '''
        Returns a BasePage subclass
        '''
        # A case-insensative search for a match
        for k in [page, page.lower()]:
            if self._pages.has_key(k):
                # Add universal mozwebqa object
                if not kwargs.has_key('mozwebqa'):
                    kwargs['mozwebqa'] = self._mozwebqa
                # Add app-specific locators
                if not kwargs.has_key('locators'):
                    kwargs['locators'] = self._locators
                return self._pages[k](**kwargs)

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

        if kwargs.get('open_url', True):
            self.selenium.get(self.base_url)

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

    def enter_search_criteria(self, criteria):
        """
        Search for criteria
        :param criteria: string
        """
        self.send_text_and_wait(criteria + "\n", *self.locators.search_input_locator)
###
#
# from page.py
#
###
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
        Returns True if the success and notification locators have cleared.
        """
        self.selenium.implicitly_wait(2)
        try:
            no_success = WebDriverWait(self.selenium, 6).until_not(lambda s: s.find_element(*self.locators.success_notification_locator).is_displayed())
            no_error = WebDriverWait(self.selenium, 6).until_not(lambda s: s.find_element(*self.locators.error_notification_locator).is_displayed())
            return no_success and no_error
        except Exception, e:
            return False
        finally:
            self.selenium.implicitly_wait(self._mozwebqa.default_implicit_wait)

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

    #
    # Click functions
    #
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
        # FIXME: no more BaseProductFactory class ... this won't work
        myProject = BaseProductFactory.get(self.project)
        if myProject._logo_locator:
            return self.is_element_visible(*myProject._logo_locator)

    def click_redhat_logo(self):
        """
        Will execute a left mouse click on the Logo locator.
        """
        self.click(*self.locators.redhat_logo_link_locator)
