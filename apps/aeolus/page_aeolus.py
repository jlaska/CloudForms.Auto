#!/usr/bin/env python

import apps.aeolus
import time, re, logging
import xml.etree.ElementTree as xmltree
import requests
import os
import stat
import tempfile
import urllib2
import subprocess
import re
from data.assert_response import *
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

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
        self.selenium.find_element(*self.locators.user_quota_max_running_instances_field).clear()
        self.send_text(user["max_instances"], *self.locators.user_quota_max_running_instances_field)
        self.selenium.find_element(*self.locators.user_submit_locator).submit()
        logging.info("create user '%s'" % user['username'])
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
        self.selenium.find_element(*self.locators.user_group_submit_locator).submit()
        logging.info("create user group '%s'" % user_group['name'])
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
        if not self.selenium.find_element(*_member_checkbox).\
            get_attribute('checked'):
            self.selenium.find_element(*_member_checkbox).click()
        self.selenium.find_element(*self.locators.user_group_save).submit()
        logging.info("add user '%s' to group '%s'" % (user_id, group_id))
        return self.get_text(*self.locators.response)

    def delete_user_from_group(self, group_id, user_id):
        '''
        delete user from user group
        '''
        _member_checkbox = (By.ID, "member_checkbox_%s" % user_id)
        self.go_to_page_view("user_groups/%s" % group_id)
        if not self.selenium.find_element(*_member_checkbox).\
            get_attribute('checked'):
            self.selenium.find_element(*_member_checkbox).click()
        self.selenium.find_element(*self.locators.user_group_delete).click()
        alert = self.selenium.switch_to_alert()
        alert.accept()
        logging.info("delete user '%s' from group '%s'" % (user_id, group_id))
        return self.get_text(*self.locators.response)

    def grant_permissions(self, filter_type, entity):
        '''
        Add permissions to user or group
        '''
        self.go_to_page_view("permissions/new")
        # init var for logging purposes
        entity_name = None
        if filter_type == "group":
            self.select_dropdown("User Group", \
                *self.locators.permissions_filter)
            self.send_text_and_wait(entity['name'], \
                *self.locators.entities_search)
            entity_name = entity['name']
        elif filter_type == "user":
            self.select_dropdown("User", \
                *self.locators.permissions_filter) 
            self.send_text_and_wait(entity['username'], \
                *self.locators.entities_search)
            entity_name = entity['username']
        else:
            logging.info("No matching filter found: %s" % filter_type)

        self.selenium.find_element(*self.locators.entities_search).\
            send_keys(Keys.RETURN)
        time.sleep(1)
        for permission in entity['permissions']:
            self.select_dropdown(permission, *self.locators.role_dropdown)
            self.selenium.find_element(*self.locators.save_button).click()
            logging.info("added permissions '%s' to %s '%s'" %\
                (permission, filter_type, entity_name))

    def add_selfservice_quota(self, quota):
        '''
        set self-service default
        '''
        self.go_to_page_view("settings/self_service")
        self.selenium.find_element(*self.locators.instances_quota).clear()
        self.send_text(quota, *self.locators.instances_quota)
        self.selenium.find_element(*self.locators.instances_quota).submit()
        logging.info("add self-service quota '%s'" % quota)
        return self.get_text(*self.locators.response)

    ###
    # provider and provider accounts
    ###
    def create_provider_account(self, acct):
        '''
        create provider account
        '''
        logging.info("Creating provider account '%s'" % \
            acct["provider_account_name"])

        self.go_to_page_view("providers")
        self.click_by_text("a", acct['provider_name'])
        self.selenium.find_element(*self.locators.prov_acct_details_locator)\
            .click()
        self.selenium.find_element(*self.locators.prov_acct_new_account_field)\
            .click()
        self.send_text(acct["provider_account_name"], \
            *self.locators.prov_acct_name_field)
        self.send_text(acct["username_access_key"], \
            *self.locators.prov_acct_access_key_field)
        self.send_text(acct["password_secret_access_key"], \
            *self.locators.prov_acct_secret_access_key_field)
        if acct["type"] == "ec2":
            self.send_text(acct["account_number"], \
                *self.locators.prov_acct_number_field)
            self.send_text(acct["private_key_file"], \
                *self.locators.prov_acct_x509_private_field)
            self.send_text(acct["public_cert_file"], \
                *self.locators.prov_acct_x509_public_field)
        self.send_text(acct["provider_account_priority"], \
            *self.locators.prov_acct_prior_field)
        self.selenium.find_element(*self.locators.prov_acct_quota_field).clear()
        self.send_text(acct["provider_account_quota"], \
            *self.locators.prov_acct_quota_field)
        self.selenium.find_element(*self.locators.prov_acct_save_locator)\
            .submit()
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

    def connection_test_provider(self, acct):
        '''
        test provider connection
        '''
        logging.info("Testing provider connection '%s'" % acct['provider_name'])
        self.go_to_page_view("providers")
        self.click_by_text("a", acct['provider_name'])
        self.click_by_text("a", "Test Connection")
        return self.get_text(*self.locators.response)

    def connection_test_provider_account(self, acct):
        '''
        test provider account connection
        '''

        logging.info("Testing provider account connection '%s'" % acct['provider_account_name'])
        self.go_to_page_view("providers")
        self.click_by_text("a", acct['provider_name'])
        self.selenium.find_element(*self.locators.prov_acct_details_locator).click()
        # NOTE: when the provider name and account name match, the following doesn't work
        self.click_by_text("div[@class='content']//a", acct['provider_account_name'])
        self.click_by_text("a", "Test Connection")
        return self.get_text(*self.locators.response)

    def get_credentials_from_config(self, section):
        '''
        get credentials from data/.ini file
        '''
        # FIXME: move to apps/__init__.py as cross-project helper method
        config_file = 'data/private_data.ini'
        from ConfigParser import SafeConfigParser
        parser = SafeConfigParser()
        parser.read(config_file)
        credentials = dict()
        for (key, val) in parser.items(section):
            credentials[key] = val
        return credentials

    ###
    # clouds/pool families/environments and cloud resource zones/pools
    ###
    def new_environment(self, cloud):
        '''
        create new environment or pool family
        '''
        logging.info("Creating cloud '%s'" % cloud['name'])

        self.go_to_page_view("pool_families")
        self.selenium.find_element(*self.locators.pool_family_create_locator).click()
        self.send_text(cloud['name'], *self.locators.env_name_field)

        if cloud.get('max_running_instances', '').isdigit():
            self.send_text(cloud['max_running_instances'],
                    *self.locators.env_max_running_instances_field)

        self.selenium.find_element(*self.locators.env_submit_locator).submit()
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
        self.select_dropdown(pool["environment_parent"], \
            *self.locators.pool_family_parent_field)
        if self.selenium.find_element(*self.locators.pool_unlim_quota_checkbox).get_attribute('checked'):
            self.selenium.find_element(*self.locators.pool_unlim_quota_checkbox).click()
        self.find_element(*self.locators.pool_quota_field).clear()
        self.send_text(pool["quota"], *self.locators.pool_quota_field)
        if not self.selenium.find_element(*self.locators.pool_enabled_checkbox).get_attribute('checked'):
            self.selenium.find_element(*self.locators.pool_enabled_checkbox).click()
        self.selenium.find_element(*self.locators.pool_save_locator).submit()
        logging.info("create pool '%s'" % pool['name'])
        return self.get_text(*self.locators.response)

    # use if new_pool dropdown doesn't work
    def new_pool_by_id(self, cloud_id, pool):
        '''
        create new pool in environment by id
        '''
        logging.info("Creating pool '%s'" % pool['name'])

        self.go_to_page_view("pools/new?pool_family_id=%s" % cloud_id)
        self.send_text(pool['name'], *self.locators.pool_name)
        if not self.selenium.find_element(*self.locators.pool_enabled_checkbox).get_attribute('checked'):
            self.selenium.find_element(*self.locators.pool_enabled_checkbox).click()
        self.selenium.find_element(*self.locators.pool_save).submit()
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
        enable provider account to cloud/pool family
        '''
        logging.info("Adding provider accounts to cloud '%s'" % cloud['name'])
        self.go_to_page_view('pool_families')
        self.click_by_text("a", cloud['name'])
        self.selenium.find_element(*self.locators.env_prov_acct_details).click()
        self.selenium.find_element(*self.locators.env_add_prov_acct_button).click()
        for account in cloud['enabled_provider_accounts']:
            account_id = self.get_provider_id_by_url(account)
            account_locator = (By.ID, "account_checkbox_%s" % account_id)
            if not self.selenium.find_element(*account_locator).get_attribute('checked'):
                self.selenium.find_element(*account_locator).click()
        self.selenium.find_element(*self.locators.save_button).submit()
        return self.get_text(*self.locators.response)

    ###
    # content: catalogs and images
    ###
    def new_catalog(self, catalog):
        '''
        create new catalog
        '''
        logging.info("Creating catalog '%s' with zone '%s'" % (catalog['name'], catalog['pool_parent']))

        self.go_to_page_view("catalogs")
        self.selenium.find_element(*self.locators.catalog_new_button).click()
        self.send_text(catalog['name'], *self.locators.catalog_name_field)
        self.select_dropdown(catalog['pool_parent'], *self.locators.catalog_family_parent_field)
        self.selenium.find_element(*self.locators.catalog_save_locator).submit()
        return self.get_text(*self.locators.response)

    def delete_catalog(self, catalog):
        logging.info("Deleting catalog '%s'" % catalog['name'])
        self.go_to_page_view("catalogs")
        self.click_by_text("a", catalog["name"])
        self.selenium.find_element(*self.locators.catalog_delete_locator).click()
        self.click_popup_confirm()
        return self.get_text(*self.locators.response)

    def new_cloud_resource_profile(self, profile):
        logging.info("Creating cloud resource profile '%s'" % profile['name'])
        self.go_to_page_view("hardware_profiles/new")
        self.send_text(profile["name"], *self.locators.hwp_name_field)
        self.send_text(profile["memory"], *self.locators.hwp_memory_field)
        self.send_text(profile["cpu_count"], *self.locators.hwp_cpu_field)
        self.send_text(profile["storage"], *self.locators.hwp_storage_field)
        self.select_dropdown(profile["arch"], *self.locators.hwp_arch_field)
        self.selenium.find_element(*self.locators.save_button).submit()

    def new_cloud_resource_cluster(self, cluster):
        logging.info("Creating cloud resource cluster '%s'" % cluster['name'])
        self.go_to_page_view("realms/new")
        self.send_text(cluster["name"], *self.locators.cluster_name)
        self.send_text(cluster["description"], *self.locators.cluster_desc)
        self.selenium.find_element(*self.locators.cluster_save).submit()
        logging.info("Adding mapping to cloud resource cluster '%s'" % \
            cluster['name'])
        response = self.add_cloud_resource_cluster_mapping(cluster)
        return response

    def add_cloud_resource_cluster_mapping(self, cluster):
        self.go_to_page_view("realms")
        self.click_by_text("a", cluster['name'])
        self.selenium.find_element(*self.locators.cluster_map_provider).click()
        self.select_dropdown(cluster["provider"], *self.locators.cluster_provider_select)
        self.selenium.find_element(*self.locators.cluster_provider_submit).submit()
        return self.get_text(*self.locators.response)

    def new_image_from_url(self, cloud, image, template_base_url):
        '''
        create new image from url
        '''
        logging.info("Creating image '%s' in cloud '%s'" % \
            (image['name'], cloud['name']))

        self.go_to_page_view("pool_families")
        self.click_by_text("a", cloud['name'])
        self.selenium.find_element(*self.locators.image_details).click()
        self.click_by_text("a", "New Image")
        self.selenium.find_element_by_link_text("From URL").click()
        self.send_text(image['name'], *self.locators.new_image_name_field)
        template = template_base_url + image['template']
        self.send_text(template, *self.locators.new_image_url_field)
        if "rhevm" in cloud['enabled_provider_accounts'] and \
            "i386" in image['profile']:
            if not self.selenium.find_element(*self.locators.new_image_edit_box).get_attribute('checked'):
                self.selenium.find_element(*self.locators.new_image_edit_box).click()
            self.selenium.find_element(*self.locators.new_image_continue_button).click()
            self.update_component_outline_for_rhev_i386("x86_64")
            self.selenium.find_element(*self.locators.save_image).submit()
        else:
            if self.selenium.find_element(*self.locators.new_image_edit_box).\
                get_attribute('checked'):
                self.selenium.find_element(*self.locators.new_image_edit_box).click()
            self.selenium.find_element(*self.locators.new_image_continue_button).click()
        self.selenium.find_element(*self.locators.save_button).submit()

    def create_image(self, cloud, image):

        logging.info("Creating image '%s' in cloud '%s'" % (image['name'], cloud['name']))

        self.go_to_page_view("pool_families")
        self.click_by_text("a", cloud['name'])
        self.selenium.find_element(*self.locators.image_details).click()
        self.click_by_text("a", "New Image")
        self.selenium.find_element_by_link_text("From URL").click()
        self.send_text(image['name'], *self.locators.new_image_name_field)
        self.send_text(image['template'], *self.locators.new_image_url_field)

        # Determine <arch> value by inspecting template
        import urllib2
        fd = urllib2.urlopen(image['template'])
        xml = xmltree.fromstring(fd.read())
        fd.close()
        template_arch = xml.find("./os/arch").text

        # Customize RHEVM images
        if 'rhevm' in cloud['enabled_provider_accounts'] and template_arch:
            logging.debug("Customizing i386 RHEV image")
            # Check [X] Edit before saving
            if not self.selenium.find_element(*self.locators.new_image_edit_box).get_attribute('checked'):
                self.selenium.find_element(*self.locators.new_image_edit_box).click()
            self.selenium.find_element(*self.locators.new_image_continue_button).click()
            # Change image <arch> from i386 to x86_64
            self.update_component_outline_for_rhev_i386("x86_64")
            # Save changes and continue
            self.selenium.find_element(*self.locators.save_image).submit()
        else:
            # Uncheck [ ] Edit before saving
            if self.selenium.find_element(*self.locators.new_image_edit_box).get_attribute('checked'):
                self.selenium.find_element(*self.locators.new_image_edit_box).click()
            # Continue
            self.selenium.find_element(*self.locators.new_image_continue_button).click()

        # Save the image
        self.selenium.find_element(*self.locators.save_button).submit()

        # TODO - return success somehow

    def update_component_outline_for_rhev_i386(self, arch):
        '''
        edit component outline textbox
        '''
        text_area = self.selenium.find_element(*self.locators.new_image_textbox)
        data = text_area.text
        tree = xmltree.fromstring(data)
        for match in tree.findall("./os[arch='i386']/arch"):
            match.text = 'x86_64'

        # Clear the <textarea>
        text_area.clear()

        # Note, this is a large amount of text, and using send_text() or
        # send_characters() is too slow.
        self.selenium.execute_script("arguments[0].value = arguments[1]",
                text_area, xmltree.tostring(tree, 'utf-8'))

    def clean_app_name(self, app_name):
        '''
        Remove illegal characters from app name
        Only lower-case and upper-case letters, numbers, '_', '-' allowed
        '''
        return re.sub(r'[.,_!@#$%^&*()+=~`<>?/:;{}|\\\[\]]', '-', app_name)

    def get_app_name(self, image, cloud):
        app_name = "%s-%s" % (image['name'], cloud['name'])
        return self.clean_app_name(app_name)

    def create_custom_blueprint(self, cloud, image, blueprint_name, custom_blueprint_xml, catalogs=[]):

        logging.info("Creating custom blueprint '%s' for image '%s' (%s) in cloud '%s'" % \
            (blueprint_name, image['name'], image['profile'], cloud['name']))

        # TODO - Navigate using the /catalogs interface instead

        # TODO - Discover image uuid, assembly hwp and name.
        # self.go_to_page_view("catalogs")
        # self.click_by_text("a", catalog[0]['name'])
        # self.selenium.find_element(*self.locators.new_deployable).click()
        # self.send_text(blueprint_name, *self.locators.blueprint_name)
        # self.send_text(custom_blueprint_xml, *self.locators.deployable_xml)
        # self.selenium.find_element(*self.locators.save_button).submit()
        # self.click_by_text("a", blueprint_name)
        # locator = (By.ID, "catalog_entry_deployable_id")
        # elements = self.selenium.find_elements(*locator)
        # while elements:
        #     self.selenium.find_element(*self.locators.deployable_add_catalog_button).click()
        #     elements = self.selenium.find_elements(*locator)
        # TODO - edit XML and add custom <services>

        self.go_to_page_view("pool_families")
        self.click_by_text("a", cloud['name'])
        self.selenium.find_element(*self.locators.image_details).click()
        self.click_by_text("a", image['name'])
        self.click_by_text("a", "New Application Blueprint from Image")
        self.selenium.find_element(*self.locators.blueprint_name).clear()
        self.send_text(blueprint_name, *self.locators.blueprint_name)

        # FIXME - should the caller be responsible for adjusting the profile?
        # If RHEV, select x86_64 anyway
        if 'rhevm' in cloud['enabled_provider_accounts']:
            logging.warning("Using alternate profile (%s) for possible rhevm deployment" % image['profile'])
            image['profile'] = 'small-x86_64'

        self.select_dropdown(image['profile'],
            *self.locators.resource_profile_dropdown)

        # Mouse over catalog selection
        locator = (By.XPATH, "//span[@class='catalog_link']")
        element = self.selenium.find_element(*locator)
        hover = ActionChains(self.selenium).move_to_element(element).perform()

        # FIXME - the following won't work.  We need the ability to select specific catalogs
        #for name in [c['name'] for c in catalogs]:
        #    locator = (By.XPATH, "//div[@class='catalog_list']//div[contains(text(),'%s')]/input[@id='catalog_id_']" % name)
        #    self.click(*locator)

        locator = (By.ID, "catalog_id_")
        for item in self.selenium.find_elements(*locator):
            item.click()

        self.selenium.find_element(*self.locators.save_button).submit()

        # If a custom blueprint was provided ... use it
        if custom_blueprint_xml is not None:
            '''
            uses data from api to create custom blueprint
            based on blueprint template found in dataset
            '''

            logging.info("Customizing application blueprint")

            # Select show/hide image details
            self.click_by_text("a", "Show/Hide")

            # Edit the XML
            self.click(*self.locators.edit_xml_button)

            # Obtain existing XML from <textarea>
            assert self.is_element_visible(*self.locators.deployable_xml), \
                    "Unable to obtain deployment XML from <textarea>"
            text_area = self.selenium.find_element(*self.locators.deployable_xml)
            blueprint_root = xmltree.fromstring(text_area.text)

            # Coerce the custom_blueprint_xml argument into a xmltree.Element object
            if isinstance(custom_blueprint_xml, xmltree.ElementTree):
                custom_root = custom_blueprint_xml.getroot()
            elif isinstance(custom_blueprint_xml, xmltree.Element):
                custom_root = custom_blueprint_xml
            else:
                custom_root = xmltree.fromstring(custom_blueprint_xml)

            # If the blueprint_root already has <services>, append custom
            # <service>'s to it
            if blueprint_root.find(".//assembly/services"):
                # For each <assembly> in the current blueprint
                for current_services in blueprint_root.findall('.//assembly/services'):
                    # Add custom <services>
                    for custom_service in custom_root.findall('.//service'):
                        current_services.append(custom_service)

            # Otherwise, add a new <services> element to each <assembly>
            else:
                # For each <assembly> in the current blueprint
                for current_assembly in blueprint_root.findall('.//assembly'):
                    # Add custom <services>
                    for custom_services in custom_root.findall('.//services'):
                        current_assembly.append(custom_services)

            # Clear the <textarea>
            text_area.clear()

            # Add custom XML to <textarea>
            # Note, this is a large amount of text, and using send_text() or
            # send_characters() is too slow
            self.selenium.execute_script("arguments[0].value = arguments[1]",
                    text_area, xmltree.tostring(blueprint_root))

            # Click the save button
            self.selenium.find_element(*self.locators.save_button).submit()

        return self.get_text(*self.locators.response)

    def create_default_blueprint(self, cloud, image, blueprint_name, catalogs=[]):
        '''
        creates default app blueprint
        '''
        logging.info("Creating default blueprint '%s' for image '%s' in cloud '%s'" % \
            (blueprint_name, image['name'], cloud['name']))

        self.go_to_page_view("pool_families")
        self.click_by_text("a", cloud['name'])
        self.selenium.find_element(*self.locators.image_details).click()
        self.click_by_text("a", image['name'])
        self.click_by_text("a", "New Application Blueprint from Image")
        self.selenium.find_element(*self.locators.blueprint_name).clear()
        self.send_text(blueprint_name, *self.locators.blueprint_name)
        self.select_dropdown(image['profile'],
            *self.locators.resource_profile_dropdown)

        # Mouse over catalog selection
        locator = (By.XPATH, "//span[@class='catalog_link']")
        element = self.selenium.find_element(*locator)
        hover = ActionChains(self.selenium).move_to_element(element).perform()

        # FIXME - the following won't work.  We need the ability to select specific catalogs
        #for name in [c['name'] for c in catalogs]:
        #    locator = (By.XPATH, "//div[@class='catalog_list']//div[contains(text(),'%s')]/input[@id='catalog_id_']" % name)
        #    self.click(*locator)

        locator = (By.ID, "catalog_id_")
        for item in self.selenium.find_elements(*locator):
            item.click()

        self.selenium.find_element(*self.locators.save_button).submit()

        return self.get_text(*self.locators.response)

    def build_all_images(self, pool_family, image_name):
        '''
        build all images
        '''
        logging.info("Build image '%s' in pool family '%s'" % (image_name,
            pool_family))
        self.go_to_page_view("pool_families")
        self.click_by_text("a", pool_family)
        self.selenium.find_element(*self.locators.image_details).click()
        self.click_by_text("a", image_name)
        self.selenium.find_element(*self.locators.build_all).click()

    def build_image(self, cloud, provider_account, image):
        '''
        build image for specified provider_account
        '''
        logging.info("Build image '%s' in cloud family '%s' for provider '%s'" %
                (image['name'], cloud['name'], provider_account['provider_name']))
        self.go_to_page_view("pool_families")
        self.click_by_text("a", cloud['name'])
        self.selenium.find_element(*self.locators.image_details).click()
        self.click_by_text("a", image['name'])

        # Return the element matching <input value='Build'> that is a child of
        # a <form> where the action attribute contains the desired provider
        # type.  For example:
        #       <form action="do_something_rhevm_something">
        #          <input value='Build'>
        locator = (By.XPATH, \
                "//form[contains(@action,'%s')]//input[@value='Build']" \
                % provider_account['type'].lower())
        try:
            self.click(*locator)
            return True
        except Exception as e:
            pass

        return False

    def verify_image_build(self, cloud, provider_account, image):
        '''
        check if image is built for specified provider account
        '''
        logging.info("Verifying build status for '%s' to '%s'" %
                (image['name'], provider_account['type']))

        self.go_to_page_view("pool_families")
        self.click_by_text("a", cloud['name'])
        self.selenium.find_element(*self.locators.image_details).click()
        self.click_by_text("a", image['name'])

        # Return the element matching <input value='Build'> that is a child of
        # a <form> where the action attribute contains the desired provider
        # type.  For example:
        #       <form action="do_something_rhevm_something">
        #          <input value='Build'>
        # xpath="//div[@class='build-actions']/h3[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'),'rhev-m')]/..//input[@value='Delete']"
        # xpath="//table[@class='light_table']//td[contains(text(),'%s')]/../../../../..//input[@value='Delete']"

        locator = (By.XPATH, \
                "//table[@class='light_table']//td[contains(text(),'%s')]/ancestor::li//input[@type='submit']" \
                % provider_account['type'].lower())
        # return self.is_element_present(*locator, wait=900).get_attribute('value').lower() == 'delete'
        # return self.is_text_present("Delete", *locator, wait=900)
        return self.is_attribute_present('value', 'Delete', *locator, wait=900)

    def push_all_images(self, cloud, image_name):
        '''
        push all images
        '''
        logging.info("Pushing image '%s' to all providers in cloud '%s'" % \
            (image_name, cloud['name']))

        self.go_to_page_view("pool_families")
        self.click_by_text("a", cloud['name'])
        self.selenium.find_element(*self.locators.image_details).click()
        self.click_by_text("a", image_name)
        self.selenium.find_element(*self.locators.push_all).click()

    def push_image(self, cloud, provider_account, image):
        '''
        Push image to desired provider
        '''
        logging.info("Initiating image push for '%s' to '%s'" %
                (image['name'], provider_account['provider_account_name']))

        self.go_to_page_view("pool_families")
        self.click_by_text("a", cloud['name'])
        self.selenium.find_element(*self.locators.image_details).click()
        self.click_by_text("a", image['name'])

        # Look through the light_table for a row matching our provider, and return the <input value='Push'>
        locator = (By.XPATH, \
                # "//table[@class='light_table']//td[contains(text(),'%s')]/..//input[@value='Push']" \
                "//table[@class='light_table']//td[contains(text(),'%s')]/ancestor::tr//input[@value='Push']" \
                % provider_account['provider_account_name'].lower())
        self.click(*locator)

        return self.get_text(*self.locators.response)

    def verify_image_push(self, cloud, provider_account, image):
        '''
        Verify if image is pushed to desired provider account
        '''
        logging.info("Initiating image push for '%s' to '%s'" %
                (image['name'], provider_account['provider_account_name']))

        self.go_to_page_view("pool_families")
        self.click_by_text("a", cloud['name'])
        self.selenium.find_element(*self.locators.image_details).click()
        self.click_by_text("a", image['name'])

        # Look through the light_table for a row matching our provider, and return the <input class='delete_image'>
        locator = (By.XPATH, \
                # "//table[@class='light_table']//td[contains(text(),'%s')]/ancestor::tr//input[@class='delete_image']" \
                "//table[@class='light_table']//td[contains(text(),'%s')]/ancestor::tr//input[@type='submit']" \
                % provider_account['provider_account_name'].lower())

        # return self.is_element_visible(*locator, wait=900)
        return self.is_attribute_present('class', 'delete_image', *locator, wait=900)

    def launch_app(self, cloud, resource_zone, catalog, blueprint_name, app_name):
        '''
        direct nav to zones, select zone by name
        create unique app name with otherwise default opts
        '''
        logging.info("Launching app '%s' into cloud '%s'" % \
            (app_name, cloud['name']))

        # Start at the /pools view
        self.go_to_page_view("pools")
        # Click the zone
        self.click_by_text("a", resource_zone['name'])
        # Click the 'New Application' button
        self.selenium.find_element(*self.locators.new_deployable).click()
        # Input application name
        self.send_text(app_name, *self.locators.app_name_field)
        # Select Blueprint
        self.select_dropdown(blueprint_name,
            *self.locators.blueprint_select)
        # TODO: select cluster
        self.select_dropdown(catalog['resource_cluster'],
            *self.locators.cluster_select)

        # Click 'Next'
        self.selenium.find_element(*self.locators.next_button).click()

        # If image customization was configured, proceed
        try:
            submit = self.selenium.find_element(*self.locators.submit_params)
            submit.click()
            # sleep for manual verification, update params
            time.sleep(10)
        except Exception as e:
            pass

        # Launch
        self.selenium.find_element(*self.locators.launch).click()

        return self.get_text(*self.locators.response)

    def launch_app_by_catalog(self, cloud, catalog, blueprint_name, app_name):
        '''
        direct nav to catalogs, select catalog by name
        create unique app name with otherwise default opts
        '''
        logging.info("Launching app '%s' into catalog '%s'" % \
            (app_name, catalog['name']))

        # Start at the /catalogs view
        self.go_to_page_view("catalogs")
        # Click the catalog by name
        self.click_by_text("a", catalog['name'])
        # Click the application name
        self.click_by_text("a", app_name)
        # Select 'Launch'
        self.selenium.find_element(*self.locators.launch).click()
        # Select 'Next'
        self.selenium.find_element(*self.locators.next_button).click()

        # If image customization was configured, proceed
        try:
            submit = self.selenium.find_element(*self.locators.submit_params)
            submit.click()
            # sleep for manual verification, update params
            time.sleep(10)
        except Exception as e:
            pass

        # launch
        self.selenium.find_element(*self.locators.launch).click()

    def get_ip_addr(self, app_name):
        '''
        return app IP address
        '''
        status = self.verify_launch(app_name)
        return status['ip']

    def verify_launch(self, cloud, resource_zone, app_name):
        '''
        Verifies the provided application has the following characteristics:
            len(instances) == 1
            state.lower() = 'running'
            is_valid_ip_address
        '''
        # FIXME - what about multi-instance applications
        instances = self.list_application_instances(resource_zone, app_name)
        assert len(instances) == 1, "Unexpected number of instances"
        for instance in instances:
            logging.info("Instance '%s' (state:'%s', ip:'%s', provider_account:'%s')" %
                    (instance.name, instance.state, instance.ip_address, instance.provider_account))
            assert instance.is_running, "Unexpected instance state: %s" % instance.state
            assert instance.is_valid_ip_address, "Unexpected instance IP Address: %s" % instance.ip_address

        return True

    def list_applications(self, cloud=None, resource_zone=None):
        # Start at the /pools view
        self.go_to_page_view("pools")

        # If a zone is provided, select it
        if resource_zone is not None:
            # Click the catalog by name
            self.click_by_text("a", resource_zone['name'])

        app_locator = (By.XPATH, "//li[@class='deployment']")
        return [Application(mozwebqa=self._mozwebqa, \
                            locators=self.locators, \
                            root_element=element) \
                for element in self.selenium.find_elements(*app_locator)]

    def list_application_instances(self, resource_zone, app_name):
        '''
        Return status of all launched apps, or single app if app_name provided
        '''
        # HACK - Workaround https://bugzilla.redhat.com/show_bug.cgi?id=874828
        app_name = self.clean_app_name(app_name)

        # Start at the /pools view
        self.go_to_page_view("pools")
        # Click the catalog by name
        self.click_by_text("a", resource_zone['name'])
        # Click the application name
        self.click_by_text("a", app_name)

        instance_locator = (By.XPATH, "//li[@class='instance']")
        return [Instance(mozwebqa=self._mozwebqa, \
                            locators=self.locators, \
                            root_element=element, \
                            resource_zone=resource_zone, \
                            app_name=app_name) \
                for element in self.selenium.find_elements(*instance_locator)]

    def download_ec2_key(self, app_name):
        (username, password) = self.get_login_credentials('admin')

        self.go_to_page_view("pools")
        self.click_by_text("a", app_name)
        url = self.url_by_text("a", "Download key")
        ec2_key_string = requests.get(url, verify=False, \
            auth=(username, password)).text
        ec2_key_file = tempfile.NamedTemporaryFile(delete=False)
        ec2_key_file.write(ec2_key_string)

        return ec2_key_file.name

    def setup_ec2_tunnel_proxy(self, app_name):
        '''
        Run commands to enable configserver SSH tunnel proxy
        '''
        ip_addr = self.get_ip_addr(app_name)
        ec2_key_file = self.download_ec2_key(app_name)
        ports = self.cfgfile.getlist('general', 'ec2_tunnel_ports')

        # 'iptables-save' prints running config to stdout
        # 'service iptables save' makes changes permanent
        cmds = ["sed -i \"s/GatewayPorts no/GatewayPorts yes/g\" /etc/ssh/sshd_config",
            "grep -i gatewa /etc/ssh/sshd_config",
            "service sshd restart",
            "iptables-save",
            "iptables -A INPUT -p tcp --dport %s -j ACCEPT" % ports[0],
            "iptables -A INPUT -p tcp --dport %s -j ACCEPT" % ports[1],
            "iptables -A INPUT -p tcp --dport 8080 -j ACCEPT",
            "iptables-save",
            "service iptables save",
            "service iptables restart"]
        for cmd in cmds:
            print "Running '%s'" % cmd
            self.run_shell_command(cmd, ip_addr, ec2_key_file)
        # TODO: how to confirm changes? Probe ports?

    def bind_cfse_ports(self, app_name):
        '''
        open ssh tunnel from CFSE to EC2 configserver
        '''
        # FIXME: This is... a mess (not working)
        # We need the EC2 key on the CFSE host (scp?)
        # and then run ssh on CFSE host to open tunnel to EC2 configserver
        # It would probably be better to send a shell script over 
        # to the CFSE host and execute it from there
        ip_addr = self.get_ip_addr(app_name)
        ec2_key_file = self.download_ec2_key(app_name)
        se_host = self.cfgfile.get('katello', 'katello-url').replace("/katello", "")
        se_host = se_host.replace("https://", "")
        # ec2_tunnel_ports = 1443 5674
        ports = self.cfgfile.getlist('general', 'ec2_tunnel_ports')
        cmd_template = "ssh -i {key} -o StrictHostKeyChecking=no -R :8080:{cfse}:80 -R :{port1}:{cfse}:443 -R :{port2}:{cfse}:{port2} root@{ec2_ip}"
        bind_cmd = cmd_template.format(key=ec2_key_file, cfse=se_host, \
            port1=ports[0], port2=ports[1], ec2_ip=ip_addr)
        copy_ec2_cmd = "sshpass -p {passwd} scp {key} root@{host}:/tmp/\."
        copy_ec2_cmd = copy_ec2_cmd.format(
            passwd=self.cfgfile.get('general', 'instance_passwd'),
            key=ec2_key_file,
            host=se_host)
        print copy_ec2_cmd
        os.system(copy_ec2_cmd)
        cmds = ["cat /etc/ssh/ssh_config",
            bind_cmd,
            "cat /etc/ssh/ssh_config"]
        for cmd in cmds:
            print "Runnning '%s'" % cmd
            self.run_shell_command(cmd, se_host)

    def get_ssh_cmd_template(self, ip_addr, ec2_key_file=None):
        '''
        return base SSH command template
        uses 'instance_passwd' from configure.ini or ec2 ssh key if provided
        '''
        cmd_template = None
        if ec2_key_file is None:
            cmd_template = "sshpass -p %s ssh -o StrictHostKeyChecking=no root@%s" % \
                    (self._mozwebqa.config.getvalue('instance-password'), ip_addr)
        else:
            cmd_template = "ssh -i %s -o StrictHostKeyChecking=no root@%s" \
                % (ec2_key_file, ip_addr)
        return cmd_template

    def setup_configserver(self, cloud, resource_zone, app_name):
        '''
        run aeolus-configserver-setup
        '''

        # Initialize configserver credentials
        credentials = None

        # Gather information about instance
        instance = self.list_application_instances(resource_zone, app_name)[0]

        # Download EC2 SSH key (optional)
        ec2_key_file = None
        if instance.key_url is not None:
            ec2_key_file = instance.download_ssh_key()
            logging.debug("Download ssh key: %s" % ec2_key_file)

        cmd = self.get_ssh_cmd_template(instance.ip_address,
                ec2_key_file) + \
            " 'echo y | aeolus-configserver-setup'"

        logging.debug("Setting up configserver: %s" % cmd)
        try:
            subprocess.check_call(cmd, shell=True)
        except subprocess.CalledProcessError, e:
            logging.error("Error running aeolus-configserver-setup: %s" % e)
            return (instance, credentials)

        # Return configserver oauth credentials
        credentials = self.get_configserver_credentials(instance.ip_address,
                ec2_key_file)

        return (instance, credentials)

    def get_configserver_credentials(self, ip_addr, ec2_key_file=None):
        '''
        return configserver credentials
        '''
        # Initialize credential dictionary
        creds = dict(endpoint="https://%s" % ip_addr)

        # Obtain oauth key
        cmd_template = self.get_ssh_cmd_template(ip_addr, ec2_key_file)
        # There may be multiple oauth tokens, we want the newest (-c)
        key_cmd = cmd_template + \
            " 'ls -c1 /var/lib/aeolus-configserver/configs/oauth/'"

        # FIXME - all calls to subprocess should be isolated in another module
        p_open = subprocess.Popen(key_cmd, shell=True, stdout=subprocess.PIPE)
        (stdout, stderr) = p_open.communicate()
        creds['key'] = stdout.split('\n')[0].strip()

        # Obtain oauth secret
        secret_cmd = cmd_template + \
            " 'cat /var/lib/aeolus-configserver/configs/oauth/%s'" % \
            creds['key']
        p_open = subprocess.Popen(secret_cmd, shell=True, stdout=subprocess.PIPE)
        (stdout, stderr) = p_open.communicate()
        creds['secret'] = stdout.strip()

        return creds

    def get_configserver_version(self, ip_addr):
        '''
        return configserver version
        '''

        # Initialize return code
        cs_version = None

        # FIXME - handle cases when configserver isn't running in DocumentRoot
        url = "https://%s/version" % ip_addr
        configserver_xml = requests.get(url, verify=False)

        # Check status code
        if configserver_xml.status_code != requests.codes.ok:
            logging.error("Failed to get Configserver version: %s [%s]" % (url,
                configserver_xml.status_code))
        else:
            tree = xmltree.fromstring(configserver_xml.text)
            cs_version = tree.find("application-version").text

        return cs_version

    def add_configserver_to_provider(self, cloud, provider_account, cs):
        '''
        add configserver to provider
        '''
        logging.info("Adding configserver to provider account %s: %s" % \
            (provider_account['provider_account_name'], cs))

        self.go_to_page_view('pool_families')
        self.click_by_text("a", cloud['name'])
        self.selenium.find_element(*self.locators.env_prov_acct_details).click()
        self.click_by_text("a", provider_account['provider_account_name'])
        self.click_by_text("a", "Add")
        self.send_text(cs['endpoint'], *self.locators.configserver_endpoint)
        self.send_text(cs['key'], *self.locators.configserver_key)
        self.send_text(cs['secret'], *self.locators.configserver_secret)
        self.selenium.find_element(*self.locators.save_button).submit()
        return self.get_text(*self.locators.response)

#
# FIXME - describe what UI element this object is intended to track
#
class Application(apps.aeolus.Conductor_Page):

    _name_locator = (By.CSS_SELECTOR, "h3.name > a")
    _state_locator = (By.CSS_SELECTOR, "span.status")
    _instances_locator = (By.XPATH, ".//li[@class='instances']/dd")
    #_instances_locator = (By.CSS_SELECTOR, "dl.statistics > ul > li.right > dd")
    _uptime_locator = (By.XPATH, ".//li[@class='uptime']/dd")
    #_uptime_locator = (By.CSS_SELECTOR, "dl.statistics > ul > li.left > dd")

    def __init__(self, **kwargs):
        self._root_element = kwargs.get('root_element', None)
        kwargs['open_url'] = False # don't reload this page
        apps.BasePage.__init__(self, **kwargs)

    @property
    def name(self):
        return self._root_element.find_element(*self._name_locator).text

    @property
    def state(self):
        return self._root_element.find_element(*self._state_locator).text

    @property
    def uptime(self):
        return self._root_element.find_element(*self._uptime_locator).text

    @property
    def instances(self):
        return self._root_element.find_element(*self._instances_locator).text

    def click(self):
        return self._root_element.find_element(*self._name_locator).click()

#
# FIXME - describe what UI element this object is intended to track
#
class Instance(apps.aeolus.Conductor_Page):

    _name_locator = (By.XPATH, ".//h3[@class='name']/a")
    _state_locator = (By.XPATH, ".//dt[@class='state']/../dd")
    _ip_address_locator = (By.XPATH, ".//dt[@class='ip_address']/../dd")
    _uptime_locator = (By.XPATH, ".//dt[@class='uptime']/../dd")
    _key_url_locator = (By.XPATH, ".//dd/a[text()='Download key']")

    def __init__(self, **kwargs):
        self._root_element = kwargs.get('root_element', None)
        kwargs['open_url'] = False # don't reload this page
        apps.BasePage.__init__(self, **kwargs)

        # Populate data
        for key in ['resource_zone', 'app_name']:
            setattr(self, key, kwargs.get(key, None))

        for attr in ['name', 'state', 'uptime', 'ip_address',]:
            locator = getattr(self, '_%s_locator' % attr)
            setattr(self, attr, self._root_element.find_element(*locator).text)

        self.key_url = self._get_key_url()
        self.provider_account = self._get_provider_account()

    @property
    def _name(self):
        return self._root_element.find_element(*self._name_locator).text

    @property
    def _state(self):
        return self._root_element.find_element(*self._state_locator).text

    @property
    def _uptime(self):
        return self._root_element.find_element(*self._uptime_locator).text

    @property
    def _ip_address(self):
        return self._root_element.find_element(*self._ip_locator).text

    @property
    def is_running(self):
        return self.state.lower() == 'running'

    def _get_key_url(self):
        try:
            # WebDriverWait(self._root_element, 3).until(lambda s: s.find_element(*self._key_url_locator).is_displayed())
            return self._root_element.find_element(*self._key_url_locator).get_attribute('href')
        except Exception, e:
            logging.warn("Exception: %s" % e)
            return None

    def _get_provider_account(self):
        # Click on the instance name
        self._root_element.find_element(*self._name_locator).click()

        # Locate the cloud provider name
        locator = (By.XPATH, "//table[@class='properties_table']//td[text()='Cloud Resource Provider']/following-sibling::td")
        provider_account = self.selenium.find_element(*locator).text

        # Click back
        self.return_to_previous_page()

        return provider_account

    @property
    def is_valid_ip_address(self):

        # Valid IP and hostname regular expressions
        valid_ip_regexp = "^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$"
        valid_hostname_regexp = "^(([a-zA-Z0-9]|[a-zA-Z0-9][a-zA-Z0-9\-]*[a-zA-Z0-9])\.)*([A-Za-z0-9]|[A-Za-z0-9][A-Za-z0-9\-]*[A-Za-z0-9])$"

        ip = self.ip_address
        for regexp in [valid_ip_regexp, valid_hostname_regexp]:
            if re.match(regexp, ip):
                return True
        return False

    def download_ssh_key(self, role='admin'):
        logging.debug("Downloading ssh key from '%s'" % self.key_url)

        (username, password) = self.get_login_credentials(role)

        ec2_key_string = requests.get(self.key_url, verify=False, \
            auth=(username, password)).text

        ec2_key_file = tempfile.NamedTemporaryFile(delete=False)
        ec2_key_file.write(ec2_key_string)
        # ec2_key_file.close()

        return ec2_key_file.name

