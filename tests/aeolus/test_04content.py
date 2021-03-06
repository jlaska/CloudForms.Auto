import os
import logging
import time
import apps
import pytest
import yaml, shutil
import copy
import xml.etree.ElementTree as xmltree
import urlparse
from data.dataset import Content
from data.assert_response import *
from tests.aeolus import Aeolus_Test

class Test_ConfigServer(Aeolus_Test):
    '''
    Create configserver images, build, push, launch
    '''

    @pytest.mark.configserver
    @pytest.mark.nondestructive
    def test_create(self, cloud, configserver):
        '''
        Create component outlines for configserver images
        Supports a single configserver image
        '''
        page = self.aeolus.load_page('Aeolus')
        page.login()

        # Prepare the template URL
        fmt_args = {'katello-url': pytest.config.getvalue('katello-url'),
                    'env': pytest.config.getvalue('katello-env'),
                    'releasever': configserver.get('releasever'),
                    'basearch': configserver.get('basearch'),
                    'type': 'configserver',}
        image_url = pytest.config.getvalue('aeolus-template-url').format( \
                        **fmt_args)
        configserver['template'] = image_url

        # Create image
        page.create_image(cloud, configserver)

        # FIXME: conductor offers no response upon successful image creation.
        # We should request fixing conductor, or inspect to ensure the created
        # image is available.

    @pytest.mark.configserver
    @pytest.mark.nondestructive
    def test_build(self, cloud_by_account_type, configserver):
        '''
        Build configserver images
        '''
        page = self.aeolus.load_page('Aeolus')
        page.login()

        (cloud, account) = cloud_by_account_type
        assert page.build_image(cloud, account, configserver), \
                "Unable to initiate image build"

    @pytest.mark.configserver
    @pytest.mark.nondestructive
    def test_verify_build(self, cloud_by_account_type, configserver):
        '''
        Verify images build successfully
        '''

        (cloud, account) = cloud_by_account_type

        page = self.aeolus.load_page('Aeolus')
        page.login()

        assert page.verify_image_build(cloud, account, configserver)

    @pytest.mark.configserver
    @pytest.mark.nondestructive
    def test_push(self, cloud_by_account, configserver):
        '''
        Push configserver images
        '''
        (cloud, account) = cloud_by_account

        page = self.aeolus.load_page('Aeolus')
        page.login()

        assert page.push_image(cloud, account, configserver),\
                "Unable to initiate image push"

    @pytest.mark.configserver
    @pytest.mark.nondestructive
    def test_verify_push(self, cloud_by_account, configserver):
        '''
        Verify a successful image push
        '''
        (cloud, account) = cloud_by_account

        page = self.aeolus.load_page('Aeolus')
        page.login()

        assert page.verify_image_push(cloud, account, configserver)

    @pytest.mark.configserver
    @pytest.mark.nondestructive
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

        # FIXME: we should match the response exactly, but since we create a
        # blueprint and enable *all* catalogs, the following ensures that at
        # *least* the requested catalogs are present in the response
        for cat in catalogs:
            assert cat.get('name') in msg

    @pytest.mark.configserver
    @pytest.mark.nondestructive
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

    @pytest.mark.configserver
    @pytest.mark.nondestructive
    def test_verify_launch(self, zone_by_catalog, configserver):
        '''
        verify configserver launch
        '''
        page = self.aeolus.load_page('Aeolus')
        page.login()

        (cloud, zone, catalog) = zone_by_catalog
        app_name = page.get_app_name(configserver, cloud)

        assert page.verify_launch(cloud, zone, app_name)

    @pytest.mark.configserver
    @pytest.mark.nondestructive
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
        logging.debug("Adding configserver credentials to 'credentials.yml'")

        # Backup existing credentials.yml
        if os.path.isfile('credentials.yml') and not os.path.isfile('credentials.orig'):
            shutil.copyfile('credentials.yml', 'credentials.orig')
            logging.debug("Backup credentials saved to 'credentials.orig'")

        # FIXME - Check whether credentials.yml exists?
        # TODO - use mozwebqa.credentials instead
        data = yaml.load(file('credentials.yml', 'r'))
        if not data.has_key('configservers') or data['configservers'] is None:
            data['configservers'] = dict()
        data['configservers'][instance.provider_account] = credentials
        yaml.safe_dump(data, file('credentials.yml', 'w+'),
                default_flow_style=False)

    @pytest.mark.configserver
    @pytest.mark.nondestructive
    def test_add_to_provider_account(self, cloud_by_account, configserver):
        '''
        Enable configserver for configured provider accounts
        '''
        page = self.aeolus.load_page('Aeolus')
        page.login()

        (cloud, provider_account) = cloud_by_account

        # Gather information about configserver instance
        assert self.testsetup.credentials.has_key('configservers'), \
                "No configservers defined in credentials.yml"
        provider_name = provider_account.get('provider_name')
        if not self.testsetup.credentials['configservers'].has_key(provider_name):
            pytest.skip("No configservers defined for provider '%s' in credentials.yml" \
                    % provider_name)

        # Add credentials to each provider account
        msg = page.add_configserver_to_provider(cloud,
                provider_account,
                self.testsetup.credentials['configservers'][provider_name])

        assert msg == aeolus_msg['add_configserver']

    @pytest.mark.configserver
    @pytest.mark.skipif("True")
    @pytest.mark.nondestructive
    def test_setup_ssh_tunnel(self, zone_by_catalog, configserver):
        '''
        Setup tunnel for configserver to communicate with katello
        See https://docspace.corp.redhat.com/docs/DOC-93629
        '''
        page = self.aeolus.load_page('Aeolus')
        page.login()

        (cloud, zone, catalog) = zone_by_catalog
        app_name = page.get_app_name(configserver, cloud)

        # TODO - It would be nice to more dynamically determine if tunnelling
        # between the configserver and katello was required
        if any(['ec2' in pa for pa in cloud['enabled_provider_accounts']]):
            page.open_ssh_tunnel_ports(zone, app_name)
            page.bind_cfse_ports(zone, app_name)
        else:
            pytest.skip("SSH Tunnel not needed for cloud: %s" % \
                    cloud.get("name"))

class Test_Content(Aeolus_Test):
    '''
    Create configserver images, build, push, launch
    '''

    @pytest.mark.content
    @pytest.mark.nondestructive
    def test_create(self, cloud, image):
        '''
        Create component outlines from images
        '''
        page = self.aeolus.load_page('Aeolus')
        page.login()

        # Prepare the template URL
        fmt_args = {'katello-url': pytest.config.getvalue('katello-url'),
                    'env': pytest.config.getvalue('katello-env'),
                    'releasever': image.get('releasever'),
                    'basearch': image.get('basearch'),
                    'type': 'tools',}
        image_url = pytest.config.getvalue('aeolus-template-url').format( \
                        **fmt_args)
        image['template'] = image_url

        # Create image
        page.create_image(cloud, image)

    @pytest.mark.content
    @pytest.mark.nondestructive
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
    @pytest.mark.nondestructive
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
    @pytest.mark.nondestructive
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
    @pytest.mark.nondestructive
    def test_verify_push(self, cloud_by_account, image):
        '''
        Verify a successful image push
        '''
        (cloud, account) = cloud_by_account

        page = self.aeolus.load_page('Aeolus')
        page.login()

        assert page.verify_image_push(cloud, account, image)

    @pytest.mark.content
    @pytest.mark.nondestructive
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

        # Helper method to set XML parameters
        def set_parameter_value(xml_root, param_name, value):
            found = False
            expr = ".//parameter[@name='%s']/value" % param_name
            for match in xml_root.findall(expr):
                match.text = value
                found = True
            assert found, "No matches found for: %s" % expr

        # Customize application blueprint XML using .cfg values
        # Attempt to load the custom blueprint XML
        blueprint_file = pytest.config.getvalue('aeolus-custom-blueprint')
        assert os.path.isfile(blueprint_file), "File not found: %s" % \
                blueprint_file
        blueprint_tree = xmltree.parse(blueprint_file)
        root = blueprint_tree.getroot()
        # Replace KATELLO_HOST
        katello_host = urlparse.urlparse(pytest.config.getvalue('katello-url')).hostname
        set_parameter_value(root, 'KATELLO_HOST', katello_host)
        # Replace KATELLO_ORG
        set_parameter_value(root, 'KATELLO_ORG', pytest.config.getvalue('katello-org'))
        # Replace KATELLO_ENV
        set_parameter_value(root, 'KATELLO_ENV', pytest.config.getvalue('katello-env'))

        # TODO - Determine when RELEASEVER locking is needed
        # Replace RELEASEVER
        # set_parameter_value(root, 'RELEASEVER', image.get('releasever','Auto'))

        # Replace SSH_TUNNEL_IP
        set_parameter_value(root, 'SSH_TUNNEL_IP', image.get('general','ec2_tunnel_host'))

        # Load and validate katello credentials
        assert self.testsetup.credentials.has_key('katello-user'), \
                "Missing credentials section for 'katello-user'"
        creds = self.testsetup.credentials.get('katello-user', {})
        assert creds.has_key('username'), \
                "Missing 'username' for 'katello-user'"
        assert creds.has_key('password'), \
                "Missing 'password' for 'katello-user'"

        # Replace KATELLO_USER
        set_parameter_value(root, 'KATELLO_USER', creds.get('username'))
        # Replace KATELLO_PASS
        set_parameter_value(root, 'KATELLO_PASS', creds.get('password'))

        # FIXME - replace SSH_TUNNEL_IP

        # Create custom blueprint
        msg = page.create_custom_blueprint(cloud, image, blueprint_name,
                blueprint_tree,
                catalogs=catalogs)

        assert msg == aeolus_msg['update_blueprint']

    @pytest.mark.content
    @pytest.mark.launch
    @pytest.mark.nondestructive
    def test_launch(self, zone_by_catalog, image):
        '''
        Launch configserver to enabled provider accounts
        '''
        page = self.aeolus.load_page('Aeolus')
        page.login(role="user")

        (cloud, zone, catalog) = zone_by_catalog
        app_name = page.get_app_name(image, cloud)
        # NOTE: application and blueprint names are the same.  This may cause a conflict
        msg = page.launch_app(cloud, zone, catalog, app_name, app_name)
        assert msg == aeolus_msg['launch_success']

    @pytest.mark.content
    @pytest.mark.verify
    @pytest.mark.launch
    @pytest.mark.nondestructive
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
    @pytest.mark.nondestructive
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

    @pytest.mark.nondestructive
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

    @pytest.mark.content
    @pytest.mark.destructive
    def test_unregister(self, zone_by_catalog, image):
        page = self.aeolus.load_page('Aeolus')
        page.login()

        (cloud, zone, catalog) = zone_by_catalog
        app_name = page.get_app_name(image, cloud)
        assert 0 == page.ssh_unregister(cloud, zone, app_name)

    @pytest.mark.destructive
    @pytest.mark.content
    def test_stop(self, zone_by_catalog, image):
        '''
        Launch configserver to enabled provider accounts
        '''
        page = self.aeolus.load_page('Aeolus')
        page.login()

        (cloud, zone, catalog) = zone_by_catalog
        app_name = page.get_app_name(image, cloud)
        msg = page.stop_app(cloud, zone, catalog, app_name)
        assert msg == aeolus_msg['stop_queued']

    @pytest.mark.destructive
    @pytest.mark.content
    def test_verify_stop(self, zone_by_catalog, image):
        page = self.aeolus.load_page('Aeolus')
        page.login()

        (cloud, zone, catalog) = zone_by_catalog
        app_name = page.get_app_name(image, cloud)

        assert page.verify_stop(cloud, zone, app_name)

    @pytest.mark.destructive
    @pytest.mark.content
    def test_delete_app(self, zone_by_catalog, image):
        page = self.aeolus.load_page('Aeolus')
        page.login()

        (cloud, zone, catalog) = zone_by_catalog
        app_name = page.get_app_name(image, cloud)
        msg = page.delete_app(cloud, zone, catalog, app_name)
        assert msg == aeolus_msg['delete_queued'] % app_name
