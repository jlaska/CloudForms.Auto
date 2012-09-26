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
        Create images
        '''
        page = self.aeolus.load_page('Aeolus')
        page.login()

        # FIXME: loop on images
        cloud = Environment.pool_family_environments[0]['name']
        image = Content.images[0]
        page.new_image_from_url(cloud, image)

    def test_build_images(self, mozwebqa):
        '''
        Build images
        '''
        page = self.aeolus.load_page('Aeolus')
        page.login()
        
        # FIXME: loop on images
        image = Content.images[0]['name']
        page.build_image(image)

    def test_create_app_blueprint(self, mozwebqa):
        '''
        Create App Blueprint
        '''
        page = self.aeolus.load_page('Aeolus')
        page.login()
        # FIXME: loop on images
        image = Content.images[0]
        page.new_app_blueprint_from_image(image, Content.apps[2])

    def test_push_images(self, mozwebqa):
        '''
        Push images
        '''
        page = self.aeolus.load_page('Aeolus')
        page.login()
        image = Content.images[0]['name']
        page.push_image(image)

    def test_launch_app(self, mozwebqa):
        '''
        Launch
        '''
        page = self.aeolus.load_page('Aeolus')
        page.login()
        catalog = Content.catalogs[0]['name']
        image = Content.images[0]['name']
        app = Content.apps[2]['name']
        page.launch_app(catalog, image, app)
