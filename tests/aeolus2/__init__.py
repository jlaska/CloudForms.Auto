import pytest
import apps
from tests import Base_Test
from api.aeolus.api import ApiTasks

@pytest.mark.aeolus
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
        self.api = ApiTasks(self.testsetup)

    @classmethod
    def teardown_class(self):
        Base_Test.teardown_class.im_func(self)

