#!/usr/bin/env python

import pytest
import apps
import time
import logging
from tests.katello2 import Katello_Test


def setup_module(module):
    test_setup = pytest.config.pluginmanager.getplugin("mozwebqa")
    module.TestNav.katello = apps.initializeProduct(test_setup.TestSetup)

class TestNav(Katello_Test):

    @pytest.mark.saucelabs
    def test_login_and_nav(self, mozwebqa):
        '''
        Login and cycle through select pages to test browser rendering

        Page views:
        users, new user, single user, edit user,
        roles, new role, single role,
        organizations, single org, edit org,
        subscriptions, new subscription, activation keys, new activation key,
        subscriptions history, 
        providers, new provider, Red Hat provider, product repositories,
        filters, new filter, GPG keys, new GPG key, sync schedules
        content search, system templates, new sys template,
        promotions, single promotion, new promotion,
        changesets, single changeset, notices,
        systems, new systems, system groups, new system group
        environments, new environment
        '''
        page = self.katello.load_page('Home')
        page.login()
        #time.sleep(15)
        page.select_org(self.testsetup.org)
        assert not page.is_failed

        workflow = ['users', 'users#panel=new', 
            'users#panel=user_1&panelpage=edit',
            'roles', 'roles#panel=new', 
            'roles/#panel=role_1', 'organizations', 'organizations', 
            'organizations#panel=organization_ACME_Corporation&panelpage=edit',
            'subscriptions', 'subscriptions#panel=new',
            'activation_keys', 'activation_keys#panel=new',
            'subscriptions/history',
            'providers', 'providers#panel=new', 'providers/redhat_provider', 
            'providers#panel=provider_3&panelpage=products_repos',
            'filters', 'filters#panel=new', 'gpg_keys', 'gpg_keys#panel=new',
            'sync_management/index', 'sync_plans', 'sync_plans#panel=new',
            'sync_schedules/index',
            'content_search', 'system_templates', 'system_templates#panel=new',
            'promotions', 'promotions/Dev', 'promotions#panel=new',
            'changesets', 'changesets#env_id=3', 'notices', 'systems', 
            'systems#panel=new', 'system_groups', 'system_groups#panel=new',
            'systems/environments', 'systems/environments#panel=new'
            # 400 (bad request), 403 (forbidden), 404 (not found)
            '%400_bad_request%', '404_not_found', 'roles/unknown_action'
            ]
        for view in workflow:
            page.go_to_page_view(view)
            assert not page.is_failed

    def test_error_pages(self, mozwebqa):
        '''
        Login and cycle through known error pages:
        400 (bad request), 403 (forbidden), 404 (not found)
        '''
        page = self.katello.load_page('Home')
        page.login()

        workflow = ['%400_bad_request%', '404_not_found', 
        'roles/unknown_action']
        for view in workflow:
            page.go_to_page_view(view)
            assert not page.is_failed

    def test_sauce_debug(self, mozwebqa):
        page = self.katello.load_page('Home')
        page.login()
        page.wait_for_id("Dashboard")
        assert page.page_title == "CloudForms System Engine - Open Source Systems Management"
        page.go_to_page_view("systems")
        time.sleep(3)

