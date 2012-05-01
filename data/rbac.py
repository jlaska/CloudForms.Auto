#!/usr/bin/env python

'''
Data for driving test_datadriven_rbac
PLIST: OrgName, ResourceType, AccessVerbs
ALLOWEDLIST: UI capabilities that should pass
DISALLOWEDLIST: UI capabilities that should fail
'''


''' 
THIS IS THE SIMPLIFIED FORMAT FOR THE PURPOSES OF THIS CHALLENGE.
THINGS CAN AND LIKELY SHOULD CHANGE IF PYTHON / PYTEST ARE SELECTED.

USE THE FOLLOWING DICTIONARIES FOR REFERENCE ONLY, _NOT_ FOR
ACTUAL LOGIC.

####
# Used as a reference for now, likely won't be used in code
####
resource_types = [ roles, users, activation_keys, organizations, environments, providers, all]

verbs = {'roles' : ['create', 'delete', 'update', 'read'],
            'users': ['create', 'delete', 'update', 'read'], 
            'activation_keys': ['manage_all', 'read_all'],
            'organizations': [create, delete, delete_systems, update, update_systems, read,
                                    read_systems, register_systems, delete_systems], 
            'environments': [update_systems, read_contents, read_systems, register_systems,
                                   delete_systems], 
            'providers': [update, read]}
                                   
####
# What's allowed or not, /me ponders how to implement (reference these)
# one idea, a key value pair where the key can be referenced in PLIST either by
# verb or another, TBD
####
                                   
ALLOWED = {'Global_Read_Only': [Assert.true(something), 
                                                    Assert.true(somethingelse)],
                      'SOME_ORG_ADMIN': [....]}
DISALLOWED = {'Global_Read_Only': [Assert.false(should_fail),
                                                         Assert.false(should_fail)],
                          'SOME_ORG_ADMIN': [....]}
'''

PLIST = {'Global_Read_Only': {'org': 'Global Permissions', 
                              'perm_name': 'ReadOnlyGlobal', 
                              'resource': 'organizations', 
                              'verb': 'read'},
         'Org_Read_Only': {'org': 'Org_Read_Only1',
                           'perm_name': 'ReadOnlyOnOrg',
                           'resource': 'organizations',
                           'verb': 'read'}}