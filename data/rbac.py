#!/usr/bin/env python

'''
Data for driving test_datadriven_rbac
PLIST: OrgName, ResourceType, AccessVerbs
ALLOWEDLIST: UI capabilities that should pass
DISALLOWEDLIST: UI capabilities that should fail
'''

PLIST = {'org': 'Global Permission', 
         'perm_name': 'ReadOnlyOrg', 
         'resource': 'organizations', 
         'verb': 'Read_Organization'}