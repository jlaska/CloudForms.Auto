import pytest
import apps
from tests import Base_Test

class Katello_Test(Base_Test):
    '''
    Base katello test class
    '''

    @property
    def katello(self):
        return self.app
