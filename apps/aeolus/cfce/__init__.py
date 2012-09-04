import apps.aeolus
import locators
# import apps.aeolus.cfce.locators

class CFCE(apps.aeolus.Conductor):
    '''Cloud Engine branded conductor'''
    locators = locators.CFCE_Locators()
    # locators = apps.aeolus.cfce.locators.CFCE_Locators()

class CFCE_Page(apps.aeolus.Conductor_Page):
    '''Cloud Engine Page class'''

    def __init__(self, **kwargs):
        apps.aeolus.Conductor_Page.__init__(self, **kwargs)

