#!/usr/bin/env python

import apps.aeolus
import time, re, logging
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

class Aeolus(apps.aeolus.Conductor_Page):

    def __init__(self, **kwargs):
        apps.aeolus.Conductor_Page.__init__(self, **kwargs)
        self.go_to_home_page()
        logging.info('load home page')

    def logout(self):
        self.go_to_page_view("logout")
        logging.info('logout')
        return self.selenium.title

    def get_id_by_url(self, view, element):
        '''
        go to view and screen scrape URL for ID
        '''
        self.go_to_page_view(view)
        url = self.url_by_text("a", element)
        element_id = re.search(".+/(\d+)$", url)
        return element_id.group(1)

    def get_provider_id_by_url(self, element):
        '''
        screen scrape URL for ID
        '''
        # FIXME: same as get_id_by_url but called from page_aeolus, not test
        #self.go_to_page_view(view)
        url = self.url_by_text("a", element)
        element_id = re.search(".+/(\d+)$", url)
        return element_id.group(1)

    ###
    # user and groups admin
    ###
    def create_user(self, user):
        '''
        create user from dictionary
        '''
        self.go_to_page_view("users/new")
        self.send_text(user["fname"], *self.locators.user_first_name_field)
        self.send_text(user["lname"], *self.locators.user_last_name_field)
        self.send_text(user["email"], *self.locators.user_email_field)
        self.send_text(user["username"], *self.locators.user_username_field)
        self.send_text(user["passwd"], *self.locators.user_password_field)
        self.send_text(user["passwd"], *self.locators.user_password_confirmation_field)
        self.send_text(user["max_instances"], *self.locators.user_quota_max_running_instances_field)
        self.selenium.find_element(*self.locators.user_submit_locator).click()
        logging.info("create user '%s'" % user)
        return self.get_text(*self.locators.response)

    def delete_user(self, username):
        '''
        delete user
        '''
        self.go_to_page_view("users")
        self.click_by_text("a", username)
        self.selenium.find_element(*self.locators.user_delete_locator).click()
        alert = self.selenium.switch_to_alert()
        alert.accept()
        logging.info("delete user '%s'" % username)
        return self.get_text(*confirmation_msg)

    def create_user_group(self, user_group):
        '''
        create user group from dictionary
        '''
        self.go_to_page_view("user_groups/new")
        self.send_text(user_group["name"], *self.locators.user_group_name_field)
        self.send_text(user_group["description"], *self.locators.user_group_description_field)
        self.selenium.find_element(*self.locators.user_group_submit_locator).click()
        logging.info("create user group '%s'" % user_group)
        return self.get_text(*self.locators.response)

    def delete_user_group(self, name):
        '''
        delete user group
        '''
        self.go_to_page_view("user_groups")
        self.click_by_text("a", name)
        self.selenium.find_element(*self.locators.user_group_delete_locator).click()
        alert = self.selenium.switch_to_alert()
        alert.accept()
        logging.info("delete user group '%s'" % name)
        return self.get_text(*self.locators.response)

    def add_user_to_group(self, group_id, user_id):
        '''
        add user to user group
        '''
        _member_checkbox = (By.ID, "member_checkbox_%s" % user_id)
        self.go_to_page_view("user_groups/%s/add_members" % group_id)
        self.selenium.find_element(*_member_checkbox).click()
        self.selenium.find_element(*self.locators.user_group_save).click()
        logging.info("add user '%s' to group '%s'" % (user_id, group_id))
        return self.get_text(*self.locators.response)

    def delete_user_from_group(self, group_id, user_id):
        '''
        delete user from user group
        '''
        _member_checkbox = (By.ID, "member_checkbox_%s" % user_id)
        self.go_to_page_view("user_groups/%s" % group_id)
        self.selenium.find_element(*_member_checkbox).click()
        self.selenium.find_element(*self.locators.user_group_delete).click()
        alert = self.selenium.switch_to_alert()
        alert.accept()
        logging.info("delete user '%s' from group '%s'" % (user_id, group_id))
        return self.get_text(*self.locators.response)

    def add_selfservice_quota(self, quota):
        '''
        set self-service default
        '''
        self.go_to_page_view("settings/self_service")
        self.send_text(quota, *self.locators.instances_quota)
        # FIXME: submit not working
        self.selenium.find_element(*self.locators.instances_quota).send_keys(Keys.RETURN)
        logging.info("add self-service quota '%s'" % quota)
        return self.get_text(*self.locators.response)

    ###
    # provider and provider accounts
    ###
    def create_provider_account(self, acct):
        '''
        create provider account
        '''
        self.go_to_page_view("providers")
        self.click_by_text("a", acct['provider_name'])
        self.selenium.find_element(*self.locators.prov_acct_details_locator).click()
        self.selenium.find_element(*self.locators.prov_acct_new_account_field).click()
        self.send_text(acct["provider_account_name"], *self.locators.prov_acct_name_field)
        self.send_text(acct["username_access_key"], *self.locators.prov_acct_access_key_field)
        self.send_text(acct["password_secret_access_key"], *self.locators.prov_acct_secret_access_key_field)
        if acct["type"] == "ec2":
            self.send_text(acct["account_number"], *self.locators.prov_acct_number_field)
            self.send_text(acct["private_key_file"], *self.locators.prov_acct_x509_private_field)
            self.send_text(acct["public_cert_file"], *self.locators.prov_acct_x509_public_field)
        self.send_text(acct["provider_account_priority"], *self.locators.prov_acct_prior_field)
        self.send_text(acct["provider_account_quota"], *self.locators.prov_acct_quota_field)
        self.selenium.find_element(*self.locators.prov_acct_save_locator).click()
        logging.info("create provider account '%s'" % acct["provider_account_name"])
        return self.get_text(*self.locators.response)

    def delete_provider_account(self, acct):
        '''
        delete provider account
        '''
        self.go_to_page_view("providers")
        self.click_by_text("a", acct['provider_name'])
        self.selenium.find_element(*self.locators.prov_acct_details_locator).click()
        self.click_by_text("a", acct['provider_account_name'])
        self.click_by_text("a", "Edit")
        self.click_by_text("a", "Delete Account")
        alert = self.selenium.switch_to_alert()
        alert.accept()
        logging.info("delete provider account '%s'" % acct['provider_account_name'])
        return self.get_text(*self.locators.response)

    def connection_test_provider_account(self, acct):
        '''
        test provider account connection
        '''
        self.go_to_page_view("providers")
        self.click_by_text("a", acct['provider_name'])
        self.selenium.find_element(*self.locators.prov_acct_details_locator).click()
        self.click_by_text("a", acct['provider_account_name'])
        self.click_by_text("a", "Test Connection")
        logging.info("test provider account connection '%s'" % acct['provider_account_name'])
        return self.get_text(*self.locators.response)

    def connection_test_provider(self, acct):
        '''
        test provider connection
        '''
        self.go_to_page_view("providers")
        self.click_by_text("a", acct['provider_name'])
        self.click_by_text("a", "Test Connection")
        logging.info("test provider connection '%s'" % acct['provider_name'])
        return self.get_text(*self.locators.response)

    def update_ec2_acct_credentials_from_config(self, account):
        '''
        add in private data from data/.ini file
        '''
        config_file = 'data/private_data.ini'
        from ConfigParser import SafeConfigParser

        parser = SafeConfigParser()
        parser.read(config_file)
        for (key, val) in parser.items('ec2_credentials'):
            account[key] = val
        return account

    ###
    # clouds/pool families/environments and cloud resource zones/pools
    ###
    def new_environment(self, env):
        '''
        create new environment or pool family
        '''
        self.go_to_page_view("pool_families/new")
        self.send_text(env["name"], *self.locators.env_name_field)
        self.send_text(env["max_running_instances"], *self.locators.env_max_running_instances_field)
        self.selenium.find_element(*self.locators.env_submit_locator).click()
        logging.info("create cloud '%s'" % env['name'])
        return self.get_text(*self.locators.response)

    def delete_environment(self, env):
        '''
        delete environment or pool family
        '''
        self.go_to_page_view("pool_families")
        self.click_by_text("a", env["name"])
        self.selenium.find_element(*self.locators.pool_family_delete_locator).click()
        self.click_popup_confirm()
        logging.info("delete cloud '%s'" % env['name'])
        return self.get_text(*self.locators.response)

    def new_pool(self, pool):
        '''
        create new pool in environment
        '''
        self.go_to_page_view("pools/new")
        self.send_text(pool["name"], *self.locators.pool_name_field)
        self.select_dropdown(pool["environment_parent"], *self.locators.pool_family_parent_field)
        # enabled by default
        #if pool["enabled"] == True:
        #    self.selenium.find_element(*self.locators.pool_enabled_checkbox).click()
        self.selenium.find_element(*self.locators.pool_save_locator).click()
        logging.info("create pool '%s'" % pool['name'])
        return self.get_text(*self.locators.response)

    # use if new_pool dropdown doesn't work
    def new_pool_by_id(self, env, pool):
        '''
        create new pool in environment by id
        '''
        self.go_to_page_view("pools/new?pool_family_id=%s" % env['id'])
        name = "%s" % (pool["name"])
        self.send_text(name, *self.locators.pool_name)
        # enabled by default in 1.1
        #if pool["enabled"] == True:
        #    self.selenium.find_element(*self.locators.pool_enabled_checkbox).click()
        self.selenium.find_element(*self.locators.pool_save).click()
        logging.info("create pool '%s'" % pool['name'])
        return self.get_text(*self.locators.response)

    def delete_pool(self, pool):
        '''
        delete environment or pool family
        '''
        self.go_to_page_view("pools")
        self.click_by_text("a", pool["name"])
        self.selenium.find_element(*self.locators.pool_delete_locator).click()
        self.click_popup_confirm()
        logging.info("delete pool '%s'" % pool['name'])
        return self.get_text(*self.locators.response)

    def add_provider_accounts_cloud(self, cloud):
        '''
        add or enable all provider accounts to cloud/pool family
        '''
        self.go_to_page_view('pool_families')
        self.click_by_text("a", cloud['name'])
        self.selenium.find_element(*self.locators.env_prov_acct_details).click()
        self.selenium.find_element(*self.locators.env_add_prov_acct_button).click()
        for account in cloud['enabled_provider_accounts']:
            account_id = self.get_provider_id_by_url(account)
            account_locator = (By.ID, "account_checkbox_%s" % account_id)
            self.selenium.find_element(*account_locator).click()
        self.selenium.find_element(*self.locators.save_button).click()
        logging.info("Add provider accounts to cloud '%s'" % cloud['name'])
        return self.get_text(*self.locators.response)

    ###
    # content: catalogs and images
    ###
    def new_catalog(self, catalog):
        '''
        create new catalog
        '''
        self.go_to_page_view("catalogs/new")
        self.send_text(catalog["name"], *self.locators.catalog_name_field)
        self.select_dropdown(catalog["pool_parent"], *self.locators.catalog_family_parent_field)
        self.selenium.find_element(*self.locators.catalog_save_locator).click()
        logging.info("create catalog '%s'" % catalog['name'])
        return self.get_text(*self.locators.response)

    def delete_catalog(self, catalog):
        self.go_to_page_view("catalogs")
        self.click_by_text("a", catalog["name"])
        self.selenium.find_element(*self.locators.catalog_delete_locator).click()
        self.click_popup_confirm()
        logging.info("delete catalog '%s'" % catalog['name'])
        return self.get_text(*self.locators.response)

    def new_cloud_resource_profile(self, profile):
        self.go_to_page_view("hardware_profiles/new")
        self.send_text(profile["name"], *self.locators.hwp_name_field)
        self.send_text(profile["memory"], *self.locators.hwp_memory_field)
        self.send_text(profile["cpu_count"], *self.locators.hwp_cpu_field)
        self.send_text(profile["storage"], *self.locators.hwp_storage_field)
        self.select_dropdown(profile["arch"], *self.locators.hwp_arch_field)
        logging.info("create cloud resource profile '%s'" % profile['name'])
        self.selenium.find_element(*self.locators.save_button).click()

    def new_image_from_url(self, cloud, image):
        '''
        create new image from url
        '''
        self.go_to_page_view("pool_families")
        self.click_by_text("a", cloud)
        self.selenium.find_element(*self.locators.image_details).click()
        self.click_by_text("a", "New Image")
        self.selenium.find_element_by_link_text("From URL").click()
        self.send_text(image['name'], *self.locators.new_image_name_field)
        self.send_text(image['template_url'], *self.locators.new_image_url_field)
        self.selenium.find_element(*self.locators.new_image_edit_box).click()
        self.selenium.find_element(*self.locators.new_image_continue_button).click()
        logging.info("create image '%s' in cloud '%s'" % (image['name'], cloud))
        self.selenium.find_element(*self.locators.save_button).click()

    def new_app_blueprint_from_image(self, cloud, image):
        '''
        creates initial app blueprint
        accepts default name and first catalog in list of catalogs
        '''
        self.go_to_page_view("pool_families")
        self.click_by_text("a", cloud)
        self.selenium.find_element(*self.locators.image_details).click()
        self.click_by_text("a", image['name'])
        self.click_by_text("a", "New Application Blueprint from Image")
        self.selenium.find_element(*self.locators.blueprint_name).clear()
        self.send_text("%s-%s" % (image['name'], cloud), \
            *self.locators.blueprint_name)
        self.select_dropdown(image['profile'], 
            *self.locators.resource_profile_dropdown)
        # selecting catalog is tricky due to hidden elements
        # it's not pretty but javascript is one approach that works
        # selects first catalog in list
        self.selenium.execute_script("el = " +\
            "document.getElementsByClassName('catalog_link');"\
            "el.onmouseover=(function(){document.getElementById" +\
            "('catalog_id_').click();}());")
        logging.info("create application blueprint '%s'" % image['name'])
        self.selenium.find_element(*self.locators.save_button).click()

    def build_image(self, cloud, image):
        '''
        build all images
        '''
        self.go_to_page_view("pool_families")
        self.click_by_text("a", cloud)
        self.selenium.find_element(*self.locators.image_details).click()
        self.click_by_text("a", image)
        logging.info("Build image '%s' in cloud '%s'" % \
            (image, cloud))
        self.selenium.find_element(*self.locators.build_all).click()

    def push_image(self, cloud, image):
        '''
        push all images
        '''
        # FIXME: use API to confirm images built
        self.go_to_page_view("pool_families")
        self.click_by_text("a", cloud)
        self.selenium.find_element(*self.locators.image_details).click()
        self.click_by_text("a", image)
        logging.info("push image '%s' to all providers in cloud '%s'" % \
            (image, cloud))
        self.selenium.find_element(*self.locators.push_all).click()

    def launch_app(self, catalog, app_name):
        '''
        launch all apps

        direct nav to catalogs, select catalog by name
        select image by name, click launch
        create unique app name with otherwise default opts
        '''
        # FIXME: use API to confirm images pushed
        self.go_to_page_view("catalogs")
        self.click_by_text("a", catalog)
        self.click_by_text("a", app_name)
        self.selenium.find_element(*self.locators.launch).click()
        #self.selenium.find_element(*self.locators.app_name_field).clear()
        #self.send_text(image['apps'][0], *self.locators.app_name_field)
        self.selenium.find_element(*self.locators.next_button).click()
        logging.info("Launch app '%s' in catalog '%s'" % \
            (app_name, catalog))
        self.selenium.find_element(*self.locators.launch).click()
