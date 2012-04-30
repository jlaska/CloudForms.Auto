#!/usr/bin/env python

#####
# Name            : base.py
# Purpose         : Common elements and controls
# Contributor     : Eric L Sammons
#####

import re

from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait

from pages.page import Page
from pages.page import BaseProductFactory

import time
import string
import random

class Base(Page):

    _current_page_locator = (By.CSS_SELECTOR, ".paginator .num > a:nth-child(1)")
    _redhat_logo_link_locator = (By.CSS_SELECTOR, "#head header a")
    _sam_header_locator = (By.CSS_SELECTOR, "#head header h1")
    _success_notification_locator = (By.CSS_SELECTOR, "div.jnotify-notification.jnotify-notification-success")
    _error_notification_locator = (By.CSS_SELECTOR, "div.jnotify-notification.jnotify-notification-error")
    _sam_h1_locator = (By.CSS_SELECTOR, "h1")
    _hello_link_locator = (By.XPATH, "//a[contains(@href, '/users?id=')]")
    _search_form_locator = (By.XPATH, "//form[@id='search_form']")
    _search_input_locator = (By.XPATH, "//input[@id='search']")
    _search_button_locator = (By.XPATH, "//button[@id='search_button']")
    _footer_version_text_locator = (By.CSS_SELECTOR, "div.grid_16.ca.light_text")
    _new_item_locator = (By.ID, "new")
    _remove_item_locator = (By.CSS_SELECTOR, "a.remove_item")
    _close_item_locator = (By.CSS_SELECTOR, "a.close")
    _confirmation_yes_locator = (By.XPATH, "//span[@class='ui-button-text'][text()='Yes']")
    _next_button_locator = (By.ID, "next_button")
    
    def random_string(self):
        chars = string.ascii_letters + string.digits
        return "".join(random.choice(chars) for x in range(random.randint(8, 16)))
    '''
    def send_characters_to_locator(self, *locator, string_to_send):
        for k in string_to_send:
            locator.send_keys(k)
    '''
    @property
    def page_title(self):
        WebDriverWait(self.selenium, 20).until(lambda s: self.selenium.title)
        return self.selenium.title

    @property
    def redhat_logo_title(self):
        return self.selenium.find_element(*self._redhat_logo_link_locator).get_attribute('title')
    
    def enter_search_criteria(self, criteria):
        search_input_locator = self.selenium.find_element(*self._search_input_locator)
        for c in criteria:
            search_input_locator.send_keys(c)
        time.sleep(2)
        search_input_locator.send_keys("\n")
        time.sleep(2)
    
    def click_next(self):
        self.click(*self._next_button_locator)
        
    def click_close(self):
        self.selenium.find_element(*self._close_item_locator).click()
        
    def click_remove(self):
        self.selenium.find_element(*self._remove_item_locator).click()

    def click_new(self):
        self.selenium.find_element(*self._new_item_locator).click()
            
    def click_confirm(self):
        WebDriverWait(self.selenium, 60).until(lambda s: s.find_element(*self._confirmation_yes_locator).is_displayed())
        confirm_button_locator = self.selenium.find_element(*self._confirmation_yes_locator)
        ActionChains(self.selenium).move_to_element(confirm_button_locator).\
            click().perform()

    @property
    def redhat_logo_image_source(self):
        return self.selenium.find_element(*self._amo_logo_image_locator).get_attribute('src')

    def is_footer_version_text_visible(self):
        #return self.selenium.find_elements_by_partial_link_text('Subscription Asset Manager Version')
        return self.selenium.find_element(*self._footer_version_text_locator).text
    
    @property
    def is_redhat_logo_visible(self):
        myProject = BaseProductFactory.get(self.project)
        if myProject._logo_locator:
            return self.is_element_visible(*myProject._logo_locator)
      
    def click_redhat_logo(self):
        self.selenium.find_element(*self._redhat_logo_link_locator).click()
        
    def click_hello_link(self):
        self.selenium.find_element(*self._hello_link_locator).click()
    
    @property
    def is_sam_h1_visible(self):
        return self.is_element_visible(*self._sam_h1_locator)
    
    def click_sam_h1(self):
        try:
            self.selenium.find_element(*self._sam_h1_locator).click()
            return True
        except:
            throw ("The header element should be visible, it's not, do something!") 
    
    @property
    def get_location_sam_h1(self):
        return self.get_location(*self._sam_h1_locator)

    @property
    def current_page(self):
        return int(self.selenium.find_element(*self._current_page_locator).text)

    @property
    def header(self):
        return Base.HeaderRegion(self.testsetup)
    
    @property
    def tabs(self):
        return Base.TabRegion(self.testsetup)

    class HeaderRegion(Page):

        _account_controller_locator = (By.CSS_SELECTOR, "li.hello")
        _logout_locator = (By.XPATH, "//a[normalize-space(.)='Logout']")
        #_org_switcher_locator = (By.CSS_SELECTOR, "a#switcherButton")
        _org_switcher_locator = (By.ID, "switcherButton")
        _org_switcher_org_locator = (By.CSS_SELECTOR, "a[href*='org_id=2']")
        _org_input_filter_locator = (By.CSS_SELECTOR, "input#orgfilter_input")
        _org_filtered_button_locator = (By.CSS_SELECTOR, "button.filter_button")
        _switcher_org_list_locator = (By.CSS_SELECTOR, "a.fl.clear")
        _dashboard_tab_active_locator = (By.CSS_SELECTOR, "li#dashboard.dashboard.top_level.active.selected")
        
        def click_logout(self):
            self.selenium.find_element(*self._logout_locator).click()

        @property
        def is_user_logged_in(self):
            return self.is_element_visible(*self._account_controller_locator)
        
        def click_hello(self):
            self.selenium.find_element(*self._account_controller_locator).click()
        
        def click_switcher(self):
            self.selenium.find_element(*self._org_switcher_locator).click()
        
        def click_org_from_switcher(self):
            WebDriverWait(self.selenium, 20).until(lambda s: s.find_element(*self._org_switcher_org_locator).is_displayed())
            self.selenium.find_element(*self._org_switcher_org_locator).click()
        
        @property
        def get_text_from_switcher(self):
            return self.selenium.find_element(*self._org_switcher_locator).text 
        
        def filter_org_in_switcher(self, criteria):
            org_input_filter = self.selenium.find_element(*self._org_input_filter_locator)
            for c in criteria:
                org_input_filter.send_keys(c)
            
        def click_filtered_result(self, criteria):
            _org_filtered_result_locator = (By.XPATH, "//a[contains(text(), '" + criteria + "')]")
            self.selenium.find_element(*_org_filtered_result_locator).click()
        
        def select_a_random_switcher_org(self):
            orgs = self.selenium.find_elements(*self._switcher_org_list_locator)
            org = orgs[random.randint(0, len(orgs)-1)]
            org.click()
            
        @property
        def is_dashboard_selected(self):
            return self.selenium.find_element(*self._dashboard_tab_active_locator).is_displayed()

    
    class TabRegion(Page):
        ''' 
        Define elements of the tab region and 
        appropriate actions on those elements.
        '''
        _tab_elements = {'dashboard_tab' : (By.XPATH, "//a[.='Dashboard']"),
                         'content_management_tab' : (By.XPATH, "//a[.='Content Management']"),
                         'providers' : (By.XPATH, "//a[.='Content Providers']"),
                         'systems_tab' : (By.XPATH, "//a[.='Systems']"), 
                         'systems_all' : (By.XPATH, "//a[.='All']"), 
                         'systems_by_environment' : (By.XPATH, "//a[.='By Environments']"), 
                         'activation_keys' : (By.XPATH, "//a[.='Activation Keys']"), 
                         'organizations_tab' : (By.XPATH, "//a[.='Organizations']"),
                         'organizations_all' : (By.XPATH, "//a[.='List']"),
                         'organizations_subscriptions' : (By.XPATH, "//a[.='Subscriptions']"), 
                         'administration_tab' : (By.XPATH, "//a[.='Administration']"),
                         'users_administration': (By.XPATH, "//a[.='Users']"),
                         'roles_administration' : (By.XPATH, "//a[.='Roles']"),}
        
        def click_tab(self, tab):
            WebDriverWait(self.selenium, 20).until(lambda s: s.find_element(*self._tab_elements[tab])).click()
            #self.selenium.find_element(*self._tab_elements[tab]).click()
            
