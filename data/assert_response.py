#!/usr/bin/env python

aeolus_msg = {
    'cfce_title' : 'CloudForms Cloud Engine',
    'login' : 'Login successful',
    'logout' : 'Aeolus Conductor | Login',
    'add_user' : 'User registered',
    'delete_user' : 'User has been successfully deleted.',
    'add_user_group' : 'User Group added',
    'delete_user_group' : 'Deleted user group %s',
    'add_user_to_group' : 'These users have been added: %s',
    'delete_user_from_group' : 'These users have been removed: %s',
    'add_pool_family' : 'Cloud was added.',
    'delete_pool_family' : 'Cloud was deleted',
    'add_pool' : 'Cloud Resource Zone added.',
    'delete_pool' : 'Pool %s was deleted.',
    'add_catalog' : 'Catalog created',
    'delete_catalog' : 'Catalog deleted',
    'connect_provider' : 'Successfully connected to Cloud Resource Provider',
    'connect_provider_acct' : 'Test Connection Success: Valid Account Details',
    'add_provider_acct' : 'Account %s was added.',
    'delete_provider_acct' : 'Provider account was deleted',
    'update_settings' : 'Settings Updated',
    'add_provider_accts' : 'These Cloud Resource Provider Account have been added: %s',
    # partial string, invalid assert
    'add_blueprint' : 'Application Blueprint added to Catalog %s.',
    'add_configserver' : 'Config Server added.',
    'add_cluster' : 'Cloud Resource Cluster was added',
    'add_cluster_mapping' : 'Cloud Resource Cluster mapping was added.',
    'update_blueprint' : 'Application Blueprint updated successfully',
    'launch_ready' : 'All Images are pushed and recent.',
    'launch_success' : 'Application launched.',
    'stop_queued' : 'stop action was successfully queued.',
    'delete_queued' : 'The Application %s was scheduled for deletion.',
    'running' : 'Running',
    'kernel' : 'Linux'
    }

# see src/app/controllers for message text source
# https://github.com/Katello/katello/tree/master/src/app/controllers
katello_msg = {
    "cfse_title" : "CloudForms System Engine - Open Source Systems Management",
    "add_sys_template" : "System Template '%s' was created.",
    "delete_sys_template" : "Template '%s' was deleted.",
    "add_org" : "Organization '%s' was created."
    }
