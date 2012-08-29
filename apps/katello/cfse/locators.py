#!/usr/bin/env python

from apps.katello.locators import KatelloLocators
from selenium.webdriver.common.by import By


class CFSELocators(KatelloLocators):
    """
    Locators for katello pages are contained within.
    """

    # Page title
    page_title = "CloudForms System Engine - Systems Management"

    # ID for login password
    password_text_field = (By.ID, "password")
