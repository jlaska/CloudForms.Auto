import pytest
import apps
from data.dataset import Environment
from data.dataset import Content
from data.assert_response import *
from tests.aeolus2 import Aeolus_Test
import time

class TestContent(Aeolus_Test):
    '''
    Create images, build, push, launch
    '''

    @pytest.mark.setup
    @pytest.mark.configserver
    def test_create_configserver_images(self, mozwebqa):
        '''
        Create component outlines for configserver images
        Supports a single configserver image
        '''
        page = self.aeolus.load_page('Aeolus')
        page.login()

        clouds = page.get_configserver_provider_list(Environment.clouds)

        if clouds == False:
            pytest.fail("No configserver providers specified.")
        for cloud in clouds:
            page.new_image_from_url(cloud, Content.configserver, \
                page.cfgfile.get('aeolus', 'sys_templates_baseurl'))

    @pytest.mark.setup
    @pytest.mark.configserver
    def test_build_configserver(self, mozwebqa):
        '''
        Build configserver images
        '''
        page = self.aeolus.load_page('Aeolus')
        page.login()

        clouds = page.get_configserver_provider_list(Environment.clouds)

        for cloud in clouds:
            page.build_image(cloud['name'], Content.configserver['name'])

    @pytest.mark.setup
    @pytest.mark.configserver
    def test_create_configserver_blueprint(self, mozwebqa):
        '''
        create default configserver blueprints
        '''
        page = self.aeolus.load_page('Aeolus')
        page.login()

        clouds = page.get_configserver_provider_list(Environment.clouds)
        catalogs = page.get_catalog_list(Content.catalogs, clouds)

        for catalog in catalogs:
            deployable = page.get_app_name(Content.configserver['name'], \
                catalog['cloud_parent'])
            page.new_default_blueprint(catalog['cloud_parent'],\
                Content.configserver, deployable)

    @pytest.mark.setup
    @pytest.mark.configserver
    def test_push_configserver(self, mozwebqa):
        '''
        Push configserver images
        '''
        page = self.aeolus.load_page('Aeolus')
        page.login()

        clouds = page.get_configserver_provider_list(Environment.clouds)

        for cloud in clouds:
            while not page.verify_image_build(cloud['name'], \
                Content.configserver['name']):
                time.sleep(30)
            else:
                page.push_image(cloud['name'], Content.configserver['name'])

    @pytest.mark.setup
    @pytest.mark.configserver
    def test_launch_configserver(self, mozwebqa):
        '''
        Launch configserver to enabled provider accounts
        '''
        page = self.aeolus.load_page('Aeolus')
        page.login()

        clouds = page.get_configserver_provider_list(Environment.clouds)
        catalogs = page.get_catalog_list(Content.catalogs, clouds)

        for catalog in catalogs:
            app_name = page.get_app_name(Content.configserver['name'], \
                catalog['cloud_parent'])
            while not page.verify_image_push(catalog['name'], app_name, \
                Content.configserver):
                time.sleep(30)
            else:
                page.launch_app(catalog['name'], app_name, Content.configserver)

    @pytest.mark.setup
    @pytest.mark.configserver
    def test_verify_configserver_launch(self, mozwebqa):
        '''
        verify configserver launch
        '''
        page = self.aeolus.load_page('Aeolus')
        page.login()

        clouds = page.get_configserver_provider_list(Environment.clouds)
        catalogs = page.get_catalog_list(Content.catalogs, clouds)

        for catalog in catalogs:
            app_name = page.get_app_name(Content.configserver['name'], \
                catalog['cloud_parent'])
            while not page.verify_launch(app_name):
                time.sleep(10)

    @pytest.mark.setup
    @pytest.mark.configserver
    def test_setup_configservers(self, mozwebqa):
        '''
        Run aeolus-configserver-setup and add to provider
        '''
        page = self.aeolus.load_page('Aeolus')
        page.login()

        clouds = page.get_configserver_provider_list(Environment.clouds)

        for cloud in clouds:
            app_name = page.get_app_name(Content.configserver['name'], \
                cloud['name'])

            ip_addr = page.get_ip_addr(app_name)
            while not page.verify_launch(app_name):
                time.sleep(10)
            else:
                ec2_key_file = None
                if 'ec2' in cloud['enabled_provider_accounts']:
                    ec2_key_file = page.download_ec2_key(app_name)
                page.setup_configserver(ip_addr, ec2_key_file)
                # assert true?

    @pytest.mark.setup
    @pytest.mark.configserver
    def test_verify_configservers(self, mozwebqa):
        '''
        Verify configserver version
        '''
        page = self.aeolus.load_page('Aeolus')
        page.login()

        clouds = page.get_configserver_provider_list(Environment.clouds)
        catalogs = page.get_catalog_list(Content.catalogs, clouds)

        for catalog in catalogs:
            app_name = page.get_app_name(Content.configserver['name'], \
                catalog['cloud_parent'])
            ip_addr = page.get_ip_addr(app_name)
            assert Content.configserver['version'] == \
                page.get_configserver_version(ip_addr)

    @pytest.mark.setup
    @pytest.mark.configserver
    def test_add_configserver_to_provider(self, mozwebqa):
        '''
        Run aeolus-configserver-setup and add to provider
        '''
        page = self.aeolus.load_page('Aeolus')
        page.login()

        clouds = page.get_configserver_provider_list(Environment.clouds)

        for cloud in clouds:
            app_name = page.get_app_name(Content.configserver['name'], \
                cloud['name'])

            ip_addr = page.get_ip_addr(app_name)
            ec2_key = None
            if 'ec2' in cloud['enabled_provider_accounts']:
                ec2_key = page.download_ec2_key(app_name)
            creds = page.get_configserver_credentials(ip_addr, ec2_key)
            creds['endpoint'] = "https://%s" % ip_addr
            assert page.add_configserver_to_provider(cloud, creds) == \
                aeolus_msg['add_configserver']

    @pytest.mark.setup
    @pytest.mark.configserver
    def test_setup_ec2_tunnel(self, mozwebqa):
        '''
        Setup tunnel for configserver to communicate with katello
        See https://docspace.corp.redhat.com/docs/DOC-93629
        '''
        page = self.aeolus.load_page('Aeolus')
        page.login()

        clouds = page.get_configserver_provider_list(Environment.clouds)

        for cloud in clouds:
            if [acct.startswith('ec2') \
                for acct in cloud['enabled_provider_accounts']]:
                app_name = page.get_app_name(Content.configserver['name'], \
                    cloud['name'])
                # commands run on configserver
                page.setup_ec2_tunnel_proxy(app_name)
                # command run on CFSE
                # FIXME: need to manually create tunnel on CFSE
                #page.bind_cfse_ports(app_name)
            else:
                pytest.skip("No EC2 configserver. No tunnel required.")

    @pytest.mark.content
    def test_create_images(self, mozwebqa):
        '''
        Create component outlines from images
        '''
        page = self.aeolus.load_page('Aeolus')
        page.login()

        clouds = page.get_provider_list(Environment.clouds)
        images = page.get_image_list(Content.images)
        for cloud in clouds:
            for image in images:
                page.new_image_from_url(cloud, image, \
                    page.cfgfile.get('aeolus', 'sys_templates_baseurl'))

    @pytest.mark.content
    def test_build_images(self, mozwebqa):
        '''
        Build images
        '''
        page = self.aeolus.load_page('Aeolus')
        page.login()

        clouds = page.get_provider_list(Environment.clouds)
        images = page.get_image_list(Content.images)
        for cloud in clouds:
            for image in images:
                page.build_image(cloud['name'], image['name'])

    @pytest.mark.content
    def test_push_images(self, mozwebqa):
        '''
        Push images
        '''
        page = self.aeolus.load_page('Aeolus')
        page.login()

        clouds = page.get_provider_list(Environment.clouds)
        images = page.get_image_list(Content.images)
        for cloud in clouds:
            for image in images:
                # 'while not' used to loop until image built
                # FIXME: better way?
                while not page.verify_image_build(cloud['name'], image['name']):
                    time.sleep(30)
                else:
                    page.push_image(cloud['name'], image['name'])

    @pytest.mark.content
    def test_create_blueprint(self, mozwebqa):
        '''
        create custom blueprints if defined in dataset
        otherwise the default blueprint is created
        '''
        page = self.aeolus.load_page('Aeolus')
        page.login()

        dataset_imgs = page.get_image_list(Content.images)
        clouds = page.get_provider_list(Environment.clouds)
        catalogs = page.get_catalog_list(Content.catalogs, clouds)

        for catalog in catalogs:
            for dataset_img in dataset_imgs:
                deployable = page.get_app_name(dataset_img['name'], \
                    catalog['cloud_parent'])
                if page.cfgfile.get('aeolus', 'custom_blueprint', '') == '':
                    # default blueprint
                    page.new_default_blueprint(catalog['cloud_parent'],\
                        dataset_img, deployable)
                else:
                    # custom blueprint, update with image uid from api
                    (login_user, login_pass) = page.get_login_credentials('admin')
                    api_images = self.api.get_image_list(login_user, login_pass)
                    for api_img in api_images:
                        if dataset_img['name'] == api_img['name']:
                            if catalog['cloud_parent'] == api_img['env']:
                                blueprint_file = \
                                    page.create_custom_blueprint(api_img, \
                                        dataset_img, page.cfgfile.get('aeolus', 'custom_blueprint'))
                                page.upload_custom_blueprint(blueprint_file, \
                                    catalog['name'], api_img, \
                                    dataset_img, deployable)

    @pytest.mark.content
    @pytest.mark.launch
    def test_launch_apps(self, mozwebqa):
        '''
        Launch apps.
        '''
        page = self.aeolus.load_page('Aeolus')
        page.login(role="user")

        images = page.get_image_list(Content.images)
        clouds = page.get_provider_list(Environment.clouds)
        catalogs = page.get_catalog_list(Content.catalogs, clouds)
        for catalog in catalogs:
            for image in images:
                app_name = page.get_app_name(image['name'], \
                    catalog['cloud_parent'])
                # 'while not' used to loop until image pushed
                # FIXME: better way?
                while not page.verify_image_push(catalog['name'], app_name, image):
                    time.sleep(30)
                else:
                    page.launch_app(catalog['name'], app_name, image)

    @pytest.mark.nondestructive
    @pytest.mark.content
    @pytest.mark.verify
    @pytest.mark.launch
    def test_verify_running_status(self, mozwebqa):
        '''
        verify app launch
        '''
        page = self.aeolus.load_page('Aeolus')
        page.login()

        images = page.get_image_list(Content.images)
        clouds = page.get_provider_list(Environment.clouds)
        catalogs = page.get_catalog_list(Content.catalogs, clouds)

        for catalog in catalogs:
            for image in images:
                app_name = page.get_app_name(image['name'], \
                    catalog['cloud_parent'])
                # 'while not' used to loop until image pushed
                # FIXME: better way?
                while not page.verify_launch(app_name):
                    time.sleep(10)
                else:
                    app = page.verify_launch(app_name)
                    assert app['status'] == aeolus_msg['running']

    @pytest.mark.nondestructive
    @pytest.mark.content
    @pytest.mark.verify
    @pytest.mark.launch
    def test_remote_command(self, mozwebqa):
        '''
        Run command on remote guest
        '''
        page = self.aeolus.load_page('Aeolus')
        page.login()

        clouds = page.get_provider_list(Environment.clouds)
        images = page.get_image_list(Content.images)

        for cloud in clouds:
            for image in images:
                app_name = page.get_app_name(image['name'], \
                    cloud['name'])
                ip_addr = page.get_ip_addr(app_name)
                ec2_key_file = None
                if [acct.startswith('ec2') \
                    for acct in cloud['enabled_provider_accounts']]:
                    ec2_key_file = page.download_ec2_key(app_name)
                assert page.run_shell_command('uname -s', ip_addr, \
                    ec2_key_file) == aeolus_msg['kernel']

    @pytest.mark.verify
    def test_get_launch_status(self, mozwebqa):
        '''
        Get status table of all apps regardless of dataset
        '''
        page = self.aeolus.load_page('Aeolus')
        page.login()

        # TODO: make this useful or discard
        print page.get_launch_status()

    @pytest.mark.verify
    @pytest.mark.registration
    def test_verify_registration(self, mozwebqa):
        '''
        Get hostname and confirm instance registered in katello
        '''
        page = self.aeolus.load_page('Aeolus')
        page.login()

        clouds = page.get_provider_list(Environment.clouds)

        for cloud in clouds:
            app_name = page.get_app_name(image['name'], \
                catalog['cloud_parent'])
            ip_addr = page.get_ip_addr(app_name)
            ec2_key_file = None
            if 'ec2' in cloud['enabled_provider_accounts']:
                ec2_key_file = page.download_ec2_key(app_name)

            for cmd in ['hostname', 'arch', 'uname -r', 'uname -s']:
                print page.run_shell_command(cmd, ip_addr, ec2_key_file)
            # TODO:
            # assert hostname == katello.api.get_hostname(ip_addr)
