import apps.katello
import locators
# import apps.katello.cfse.locators

class CFSE(apps.katello.Katello):
    '''System Engine branded katello'''
    locators = locators.CFSELocators()
    # locators = apps.katello.cfse.locators.CFSELocators()

class CFSEPage(apps.katello.KatelloPage):
    '''CFSE Page class'''

    # "CloudForms System Engine - Systems Management"

    def __init__(self, **kwargs):
        apps.katello.KatelloPage.__init__(self, **kwargs)
