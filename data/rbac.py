#!/usr/bin/env python

'''
Data for driving test_datadriven_rbac
PLIST: OrgName, ResourceType, AccessVerbs
ALLOWEDLIST: UI capabilities that should pass
DISALLOWEDLIST: UI capabilities that should fail
'''
PLIST = {'org': 'Global', 
         'perm_name': 'ReadOnlyOrg', 
         'permission_for': 'Organizations', 
         'verb': 'Read_Organization'}