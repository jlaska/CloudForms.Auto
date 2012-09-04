import pytest
import apps

class Base_Test(object):
    '''
    Base class
    '''
    @classmethod
    def setup_class(self):
        """ setup any state specific to the execution of the given class (which
        usually contains tests).
        """
        test_setup = pytest.config.pluginmanager.getplugin("mozwebqa")
        self.app = apps.initializeProduct(test_setup.TestSetup)

