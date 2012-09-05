import pytest
import apps
import random
import string

class Base_Test(object):
    '''
    Base class
    '''
    @classmethod
    def setup_class(self):
        """ setup any state specific to the execution of the given class (which
        usually contains tests).
        """
        self.testsetup = pytest.config.pluginmanager.getplugin("mozwebqa").TestSetup
        self.app = apps.initializeProduct(self.testsetup)

    @classmethod
    def teardown_class(self):
        '''
        Perform any required test teardown
        '''

    def load_page(self, page_name):
        '''
        Description:
            Convenience method to return an initialized application page
        Returns:
            object of type BasePage
        '''
        return self.app.load_page(page_name)

    def random_str(self, prefix="", str_len=5, suffix=""):
        '''
        Description:
            Return a string containing a random sample of ascii letters and digits
        Parameters:
            prefix (string): prefix random string with supplied string
            str_len (digit): length of string to generate
            suffix (string): append random string with supplied suffix
        Returns:
            string
        '''
        return prefix + ''.join(random.sample(string.ascii_letters + string.digits, str_len)) + suffix
