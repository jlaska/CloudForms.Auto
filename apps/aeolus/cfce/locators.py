from apps.aeolus.locators import AeolusLocators
from selenium.webdriver.common.by import By

class CFCE_Locators_1_1_x(AeolusLocators):
    """
    Locators for CFCE pages are contained within.
    """

    # Page title
    page_title = "CloudForms Cloud Engine | Login"
    login_logo = (By.XPATH, "//img[@alt='Login-card-logo-product']")
    logo_link = (By.XPATH, "//a[contains(text(),'CloudForms Cloud Engine')]")
