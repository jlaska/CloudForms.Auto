#!/usr/bin/env python

import pytest
import apps
from data.large_dataset import Environment
from data.large_dataset import Content
from data.assert_response import *
from tests.aeolus2 import Aeolus_Test

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
        Uses unique name and selects appropriate resource profile
        '''
        page = self.aeolus.load_page('Aeolus')
        page.login()

        for cloud in Environment.clouds:
            for image in Content.images:
                page.new_app_blueprint_from_image(cloud['name'], image)

    def test_launch_configserver(self, mozwebqa):
        '''
        Launch configserver
        '''
        page = self.aeolus.load_page('Aeolus')
        page.login()

        for catalog in Content.catalogs:
            for image in Content.images:
                if image['name'] == "ConfigServer":
                    app_name = "%s-%s" % \
                        (image['name'], catalog['cloud_parent'])
                    page.launch_app(catalog['name'], app_name)
                    # TODO: configure via cli, ssh...

    # Manual: configure config server
    # if ec2 get key, chmod
    # ssh
    # `aeolus-configserver-setup`, 'y', default, grab consumer key and secret
    # nav to cloud provider account, enter url, key, secret, assert notification

    def test_launch_apps(self, mozwebqa):
        '''
        Launch apps.
        '''
        page = self.aeolus.load_page('Aeolus')
        # TODO: login as self-service, less priveledged use
        page.login()
        # TODO: link catalogs and images more elegantly
        for catalog in Content.catalogs:
            for image in Content.images:
                if image['name'] != "ConfigServer":
                    app_name = "%s-%s" % \
                        (image['name'], catalog['cloud_parent'])
                    page.launch_app(catalog['name'], app_name)

    ###
    # FIXME: 
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


