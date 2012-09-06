import pytest
import apps
from tests import Base_Test

class Aeolus_Test(Base_Test):
    '''
    Base aeolus test class
    '''

    @property
    def aeolus(self):
        return self.app

    @classmethod
    def setup_class(self):
        Base_Test.setup_class.im_func(self)
        # FIXME - assign self.api when API is available
        # self.api = ApiTasks(self.testsetup)

    @classmethod
    def teardown_class(self):
        Base_Test.teardown_class.im_func(self)

