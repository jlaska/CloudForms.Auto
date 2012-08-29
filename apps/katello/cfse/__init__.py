import apps.katello
import locators

class CFSE(apps.katello.Katello):
    '''System Engine branded katello'''
    locators = locators.CFSELocators()

class CFSEPage(apps.katello.KatelloPage):
    '''CFSE Page class'''

    # "CloudForms System Engine - Systems Management"

    def __init__(self, **kwargs):
        apps.katello.KatelloPage.__init__(self, **kwargs)
