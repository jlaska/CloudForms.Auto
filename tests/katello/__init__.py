import pytest
import apps
from api.katello.api import ApiTasks
from tests import Base_Test

@pytest.mark.katello
class Katello_Test(Base_Test):
    '''
    Base katello test class
    '''

    @classmethod
    def setup_class(self):
        """ setup any state specific to the execution of the given class (which
        usually contains tests).
        """
        Base_Test.setup_class.im_func(self)
        self.api = ApiTasks(self.testsetup)

    @classmethod
    def teardown_class(self):
        Base_Test.teardown_class.im_func(self)

    @property
    def katello(self):
        return self.app
