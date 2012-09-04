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
