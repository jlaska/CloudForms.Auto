import os
import logging
import time
import apps
import pytest
import yaml, shutil
import copy
from data.dataset import Environment
from data.dataset import Content
from data.assert_response import *
from tests.aeolus2 import Aeolus_Test

class Test_ConfigServer(Aeolus_Test):
    '''
    Create configserver images, build, push, launch
    '''

    pytestmark = [pytest.mark.configserver, pytest.mark.setup]

    def test_create(self, cloud, configserver):
        '''
        Create component outlines for configserver images
        Supports a single configserver image
        '''
        page = self.aeolus.load_page('Aeolus')
        page.login()

        # Prepare the template URL
        image_url = pytest.config.getvalue('aeolus-template-url').format( \
                type='configserver',
                releasever=configserver.get('releasever', '6Server'),
                basearch=configserver.get('basearch', 'x86_64'))

        configserver['template'] = image_url

        page.create_image(cloud, configserver)

    def test_build(self, cloud_by_account_type, configserver):
        '''
        Build configserver images
        '''
        page = self.aeolus.load_page('Aeolus')
        page.login()

        (cloud, account) = cloud_by_account_type
        assert page.build_image(cloud, account, configserver), \
                "Unable to initiate image build"

    def test_verify_build(self, cloud_by_account_type, configserver):
        '''
        Verify images build successfully
        '''

        (cloud, account) = cloud_by_account_type

        page = self.aeolus.load_page('Aeolus')
        page.login()

        assert page.verify_image_build(cloud, account, configserver)

    def test_push(self, cloud_by_account, configserver):
        '''
        Push configserver images
        '''
        (cloud, account) = cloud_by_account

        page = self.aeolus.load_page('Aeolus')
        page.login()

        assert page.push_image(cloud, account, configserver),\
                "Unable to initiate image push"

    def test_verify_push(self, cloud_by_account, configserver):
        '''
        Verify a successful image push
        '''
        (cloud, account) = cloud_by_account

        page = self.aeolus.load_page('Aeolus')
        page.login()

        assert page.verify_image_push(cloud, account, configserver)

    def test_blueprint(self, cloud, configserver, catalogs):
        '''
        create default configserver blueprints
        '''
        page = self.aeolus.load_page('Aeolus')
        page.login()

        blueprint_name = page.get_app_name(configserver, cloud)

        msg = page.create_default_blueprint(cloud,
                configserver,
                blueprint_name,
                catalogs)
        assert msg == aeolus_msg['add_blueprint']

    def test_launch(self, zone_by_catalog, configserver):
        '''
        Launch configserver to enabled provider accounts
        '''
        page = self.aeolus.load_page('Aeolus')
        page.login()

        (cloud, zone, catalog) = zone_by_catalog
        app_name = page.get_app_name(configserver, cloud)
        # NOTE: application and blueprint names are the same.  This may cause a conflict
        msg = page.launch_app(cloud, zone, catalog, app_name, app_name)
        assert msg == aeolus_msg['launch_success']

    def test_verify_launch(self, zone_by_catalog, configserver):
        '''
        verify configserver launch
        '''
        page = self.aeolus.load_page('Aeolus')
        page.login()

        (cloud, zone, catalog) = zone_by_catalog
        app_name = page.get_app_name(configserver, cloud)

        assert page.verify_launch(cloud, zone, app_name)

    def test_setup(self, zone_by_catalog, configserver):
        '''
        Run aeolus-configserver-setup and add to provider
        '''
        page = self.aeolus.load_page('Aeolus')
        page.login()

        (cloud, zone, catalog) = zone_by_catalog
        app_name = page.get_app_name(configserver, cloud)

        (instance, credentials) = page.setup_configserver(cloud, zone, app_name)
        assert credentials is not None, "Failed to setup configserver"

        # The configserver should be operational
        assert Content.configserver['version'] == \
            page.get_configserver_version(instance.ip_address)

        # Save credentials to a local .yaml file
        logging.debug("Adding configserver credentials to 'credentials.yaml'")

        # Backup existing credentials.yaml
        if os.path.isfile('credentials.yaml') and not os.path.isfile('credentials.orig'):
            shutil.copyfile('credentials.yaml', 'credentials.orig')
            logging.debug("Backup credentials saved to 'credentials.orig'")

        # FIXME - Check whether credentials.yaml exists?
        data = yaml.load(file('credentials.yaml', 'r'))
        if not data.has_key('configservers') or data['configservers'] is None:
            data['configservers'] = dict()
        data['configservers'][instance.provider_account] = credentials
        yaml.safe_dump(data, file('credentials.yaml', 'w+'),
                default_flow_style=False)

    def test_add_to_provider_account(self, cloud_by_account, configserver):
        '''
        Enable configserver for configured provider accounts
        '''
        page = self.aeolus.load_page('Aeolus')
        page.login()

        (cloud, provider_account) = cloud_by_account

        # Gather information about configserver instance
        assert self.testsetup.credentials.has_key('configservers'), \
                "No configservers defined in credentials.yaml"
        provider_name = provider_account.get('provider_name')
        if not self.testsetup.credentials['configservers'].has_key(provider_name):
            pytest.skip("No configservers defined for provider '%s' in credentials.yaml" \
                    % provider_name)

        # Add credentials to each provider account
        msg = page.add_configserver_to_provider(cloud,
                provider_account,
                self.testsetup.credentials['configservers'][provider_name])

        assert msg == aeolus_msg['add_configserver']

    @pytest.mark.skipif("True")
    def test_setup_ec2_tunnel(self, cloud_by_account, configserver):
        '''
        Setup tunnel for configserver to communicate with katello
        See https://docspace.corp.redhat.com/docs/DOC-93629
        '''
        page = self.aeolus.load_page('Aeolus')
        page.login()

        (cloud, provider_account) = cloud_by_account

        app_name = page.get_app_name(configserver['name'], \
            cloud['name'])

        page.setup_ec2_tunnel_proxy(app_name)

class Test_Content(Aeolus_Test):
    '''
    Create configserver images, build, push, launch
    '''

    @pytest.mark.content
    def test_create(self, cloud, image):
        '''
        Create component outlines from images
        '''
        page = self.aeolus.load_page('Aeolus')
        page.login()

        # Prepare the template URL
        image_url = pytest.config.getvalue('aeolus-template-url').format( \
                type='tools',
                releasever=image.get('releasever'),
                basearch=image.get('basearch'))
        image['template'] = image_url

        page.create_image(cloud, image)

    @pytest.mark.content
    def test_build(self, cloud_by_account_type, image):
        '''
        Build images
        '''
        page = self.aeolus.load_page('Aeolus')
        page.login()

        (cloud, account) = cloud_by_account_type
        assert page.build_image(cloud, account, image), \
                "Unable to initiate image build"

    @pytest.mark.content
    def test_verify_build(self, cloud_by_account_type, image):
        '''
        Verify images build successfully
        '''

        (cloud, account) = cloud_by_account_type

        page = self.aeolus.load_page('Aeolus')
        page.login()

        assert page.verify_image_build(cloud, account, image), \
                "Image build failed"

    @pytest.mark.content
    def test_push(self, cloud_by_account, image):
        '''
        Push images
        '''
        page = self.aeolus.load_page('Aeolus')
        page.login()

        (cloud, account) = cloud_by_account
        assert page.push_image(cloud, account, image),\
                "Unable to initiate image push"

    @pytest.mark.content
    def test_verify_push(self, cloud_by_account, image):
        '''
        Verify a successful image push
        '''
        (cloud, account) = cloud_by_account

        page = self.aeolus.load_page('Aeolus')
        page.login()

        assert page.verify_image_push(cloud, account, image)

    @pytest.mark.content
    def test_blueprint(self, cloud, catalogs, image):
        '''
        create default configserver blueprints
        '''
        page = self.aeolus.load_page('Aeolus')
        page.login()

        blueprint_name = page.get_app_name(image, cloud)

        # HACK - RHEV doesn't support true i386, spoof as a x86_64 profile
        if "rhevm" in cloud['enabled_provider_accounts']:
            # The 'image' appears to be call-by-reference.  Changing 'image'
            # affects other generated test runs.
            # Upstream bug to track this # issue -
            # https://bitbucket.org/hpk42/pytest/issue/237/unexpected-behavior-when-modifying
            image = copy.copy(image)
            image['profile'] = 'small-x86_64'
            logging.warning("Adjusting blueprint ('%s') profile ('%s') for cloud '%s' to account for RHEV support" % \
                    (blueprint_name, image['profile'], cloud['name']))

        # Create custom blueprint
        msg = page.create_custom_blueprint(cloud,
                image,
                blueprint_name,
                pytest.config.getvalue('aeolus-custom-blueprint'),
                catalogs=catalogs)

        assert msg == aeolus_msg['update_blueprint']

    @pytest.mark.content
    @pytest.mark.launch
    def test_launch(self, zone_by_catalog, image):
        '''
        Launch configserver to enabled provider accounts
        '''
        page = self.aeolus.load_page('Aeolus')
        page.login()

        (cloud, zone, catalog) = zone_by_catalog
        app_name = page.get_app_name(image, cloud)
        # NOTE: application and blueprint names are the same.  This may cause a conflict
        msg = page.launch_app(cloud, zone, catalog, app_name, app_name)
        assert msg == aeolus_msg['launch_success']

    @pytest.mark.nondestructive
    @pytest.mark.content
    @pytest.mark.verify
    @pytest.mark.launch
    def test_verify_launch(self, zone_by_catalog, image):
        page = self.aeolus.load_page('Aeolus')
        page.login()

        (cloud, zone, catalog) = zone_by_catalog
        app_name = page.get_app_name(image, cloud)

        assert page.verify_launch(cloud, zone, app_name)

    @pytest.mark.nondestructive
    @pytest.mark.content
    @pytest.mark.verify
    @pytest.mark.launch
    @pytest.mark.skipif("True")
    def test_remote_command(self, zone_by_catalog, image):
        '''
        Run command on remote guest
        '''

        (cloud, zone, catalog) = zone_by_catalog
        app_name = page.get_app_name(image, cloud)

        page = self.aeolus.load_page('Aeolus')
        page.login()

        instances = self.list_application_instances(resource_zone, app_name)

        # FIXME - The following won't work yet ... need to revise arguments
        assert page.run_shell_command('uname -s', instance) == \
                aeolus_msg['kernel']

    @pytest.mark.verify
    @pytest.mark.registration
    @pytest.mark.skipif("True")
    def test_verify_registration(self, zone_by_catalog, image):
        '''
        Get hostname and confirm instance registered in katello
        '''

        page = self.aeolus.load_page('Aeolus')
        page.login()

        (cloud, zone, catalog) = zone_by_catalog
        app_name = page.get_app_name(image, cloud)

        # FIXME - The following won't work yet ... need to revise arguments
        cmd = "subscription-manager identity"
        page.run_shell_command(cmd, instance)
