import apps.katello
import locators

class SAM(apps.katello.Katello):
    '''SAM branded katello'''
    locators = locators.SAMLocators()

class SAMPage(apps.katello.KatelloPage):
    '''SAM Page class'''

    def __init__(self, **kwargs):
        apps.katello.KatelloPage.__init__(self, **kwargs)

