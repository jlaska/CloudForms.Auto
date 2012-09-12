from apps.katello.locators import KatelloLocators
from selenium.webdriver.common.by import By

class CFSELocators_1_1_x(KatelloLocators):
    """
    Locators for katello pages are contained within.
    """

    # Page title
    page_title = "CloudForms System Engine - Systems Management"
    login_card_logo = (By.XPATH, "//img[contains(@alt, 'CloudForms System Engine Logo') and contains(@src, '/rh-logo.png')]")

class CFSELocators_1_0_x(KatelloLocators):
    """
    System Engine 1.0.x locators
    """

    # Page title
    page_title = "CloudForms System Engine - Systems Management"

    # ID for login password
    password_text_field = (By.ID, "password")
    # ID for login button
    login_locator = (By.NAME, "commit")
