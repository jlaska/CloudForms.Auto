#!/usr/bin/env python

import pytest
import apps
from data.large_dataset import Environment
from data.large_dataset import Content
from data.assert_response import *
from tests.aeolus2 import Aeolus_Test
import time

def setup_module(module):
    test_setup = pytest.config.pluginmanager.getplugin("mozwebqa")
    module.TestContent.aeolus = apps.initializeProduct(test_setup.TestSetup)

class TestContent(Aeolus_Test):
    '''
    Create images, build, push, launch
    '''

    def test_create_images(self, mozwebqa):
        '''
        Create component outlines from images
        '''
        page = self.aeolus.load_page('Aeolus')
        page.login()

        for cloud in Environment.clouds:
            for image in Content.images:
                page.new_image_from_url(cloud['name'], image)

    def test_build_images(self, mozwebqa):
        '''
        Build images
        '''
        page = self.aeolus.load_page('Aeolus')
        page.login()
        
        for cloud in Environment.clouds:
            for image in Content.images:
                page.build_image(cloud['name'], image['name'])

    def test_push_images(self, mozwebqa):
        '''
        Push images
        '''
        page = self.aeolus.load_page('Aeolus')
        page.login()

        for cloud in Environment.clouds:
            for image in Content.images:
                page.push_image(cloud['name'], image['name'])

    def test_create_app_blueprint(self, mozwebqa):
        '''
        Create App Blueprints
        '''
        page = self.aeolus.load_page('Aeolus')
        page.login()

        for image in Content.images:
            page.new_app_blueprint_from_image(image)

    # Eval guide: publish app blueprint to catalog?
    # separate launch and config of configserver?

    # do as self-service user might?
    def test_launch_apps(self, mozwebqa):
        '''
        Launch apps.
        Launches a single app per image, seleting the first app in the list
        '''
        page = self.aeolus.load_page('Aeolus')
        page.login()
        # TODO: link catalogs and images more elegantly
        catalog = Content.catalogs[1]['name']
        for image in Content.images:
            page.launch_app(catalog, image)
            time.sleep(10)

    ###
    # api function for reference
    # use/extend for polling status
    ###
    def test_poll_images(self, mozwebqa):
        '''
        poll image build and return status
        '''
        print "### Images ###"
        images = self.api.get_element_id_list("images", "image")
        for image_id in images:
            image_detail = self.api.get_detailed_info("images", image_id)
            print "%s (%s)" % (image_detail['name'], image_id)

        # return XML more complex, not verified
        print "### Target Images ###"
        target_images = self.api.get_element_id_list("target_images", "target_image")
        for target_image_id in target_images:
            target_image_detail = self.api.get_detailed_info("target_images", target_image_id)
            print "%s (%s)" % (target_image_detail['template'], target_image_id)


