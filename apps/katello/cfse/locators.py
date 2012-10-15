from apps.katello.locators import KatelloLocators
from selenium.webdriver.common.by import By

class CFSELocators_1_1_x(KatelloLocators):
    """
    Locators for katello pages are contained within.
    """

    # Page title
    page_title = "CloudForms System Engine - Open Source Systems Management"
    login_logo = (By.XPATH, "//img[@alt='Red Hat CloudForms System Engine Logo']")
    logo_link = (By.XPATH, "//a[contains(text(),'CloudForms System Engine')]")

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
