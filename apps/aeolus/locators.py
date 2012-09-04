import apps.locators
from selenium.webdriver.common.by import By

class AeolusLocators(apps.locators.BaseLocators):
    """
    Locators for aeolus pages are contained within.
    """

    page_title = "Aeolus Conductor"
    username_text_field = (By.NAME, "login")
    password_text_field = (By.ID, "password-input")
    login_locator = (By.NAME, "commit")
