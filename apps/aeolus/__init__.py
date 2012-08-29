import apps

class Conductor(apps.BaseProduct):
    '''Product class'''

class ConductorPage(apps.BasePage):
    '''Page class'''

    def __init__(self, **kwargs):
        apps.BasePage.__init__(self, **kwargs)

        # Conductor specific page content
