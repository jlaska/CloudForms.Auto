#!/usr/bin/env python

# generated from generate_dataset.py
# based on list definitions in raw_data.py

        
class Admin(object):
    '''
    Define users and groups
    '''
    user_groups = [
        {"name" : "admin", 
        "description" : "Global admins. With great power comes great responsibility"},
        {"name" : "cfadmins", 
        "description" : "Global admins. With great power comes great responsibility"},
        {"name" : "qe", 
        "description" : "real QE users"},
        {"name" : "cfusers", 
        "description" : "Limited privilege users"}
        ]

    users = [
        {"fname" : "Auto",
        "lname" : "Roboto",
        "email" : "admin@redhat.com",
        "username" : "automation",
        "passwd" : "redhat",
        "max_instances" : "",
        "user_groups" : ['admin'] },
        {"fname" : "Aaron",
        "lname" : "Weitekamp",
        "email" : "aweiteka@redhat.com",
        "username" : "aweiteka-admin",
        "passwd" : "redhat",
        "max_instances" : "20",
        "user_groups" : ['qe','cfadmins'] },
        {"fname" : "Aaron",
        "lname" : "Weitekamp",
        "email" : "aweiteka@redhat.com",
        "username" : "aweiteka-user",
        "passwd" : "redhat",
        "max_instances" : "20",
        "user_groups" : ['cfusers'] },
        {"fname" : "James",
        "lname" : "Laska",
        "email" : "jlaska@redhat.com",
        "username" : "jlaska",
        "passwd" : "redhat",
        "max_instances" : "20",
        "user_groups" : ['qe','cfadmins'] },
        {"fname" : "Milan",
        "lname" : "Falenik",
        "email" : "mfalesni@redhat.com",
        "username" : "mfalesni",
        "passwd" : "redhat",
        "max_instances" : "20",
        "user_groups" : ['qe','cfadmins'] },
        {"fname" : "Gabriel",
        "lname" : "Szasz",
        "email" : "gszasz@redhat.com",
        "username" : "gszasz",
        "passwd" : "redhat",
        "max_instances" : "20",
        "user_groups" : ['qe','cfadmins'] }
        ]

    selfservice_quota = "10"
        
class Provider(object):
    '''
    Define providers and provider accounts
    '''
    # provider_name string must match conductor
    # valid account types: "ec2", "rhevm", "vsphere"
    accounts = [

        # more than one ec2 account supported?
        {"type" : "ec2",
        "provider_name" : "ec2-us-east-1",
        "provider_account_name" : "Public cloud east",
        "username_access_key" : "",
        "password_secret_access_key" : "",
        "account_number" : "",
        "key_file" : "",
        "key_cert_file" : "",
        "provider_account_priority" : "",
        "provider_account_quota" : "" },

        {"type" : "rhevm",
        "provider_name" : "rhevm-default",
        "provider_account_name" : "rhevm",
        "username_access_key" : "admin@internal",
        "password_secret_access_key" : "dog8code",
        "provider_account_priority" : "",
        "provider_account_quota" : "" },

        {"type" : "vsphere",
        "provider_name" : "vsphere-default",
        "provider_account_name" : "vsphere",
        "username_access_key" : "Administrator",
        "password_secret_access_key" : "R3dhat!",
        "provider_account_priority" : "",
        "provider_account_quota" : "" }
        ]

    resource_profiles = [
        {"name" : "small-i386",
        "memory" : "512",
        "cpu_count" : "1",
        "storage" : "",
        "arch" : "i386"}
        ]

class Environment(object):
    '''
    Define environments and pools
    '''
    clouds = [
        {"name" : "Dev",
        "max_running_instances" : "14",
        "enabled_provider_accounts" : ['rhevm']},
        {"name" : "Test",
        "max_running_instances" : "23",
        "enabled_provider_accounts" : ['vsphere']},
        {"name" : "Production",
        "max_running_instances" : "21",
        "enabled_provider_accounts" : ['Public cloud east']}
        ]

    pools = [
        {"name" : "CloudForms-dev",
        "environment_parent" : ['Dev'],
        "quota" : "24",
        "enabled" : True},
        {"name" : "CloudForms-test",
        "environment_parent" : ['Test'],
        "quota" : "24",
        "enabled" : True},
        {"name" : "CloudForms-prod",
        "environment_parent" : ['Production'],
        "quota" : "24",
        "enabled" : True}
        ]

class Content(object):
    '''
    Define catalogs, images and deployables
    '''
    catalogs = [
        {"name" : "CF tools-dev",
        "pool_parent" : 'CloudForms-dev',
        "cloud_parent" : "Dev"},
        {"name" : "CF tools-test",
        "pool_parent" : 'CloudForms-test',
        "cloud_parent" : "Test"},
        {"name" : "CF tools-prod",
        "pool_parent" : 'CloudForms-prod',
        "cloud_parent" : "Production"}
        ]

    images = [
        {"name" : "ConfigServer",
        "template_url" : "https://qeblade40.rhq.lab.eng.bos.redhat.com/templates/Dev/rhel-x86_64-6Server-cf-configserver.xml",
        "profile" : "small-x86_64",
        "blueprint" : "data/blueprint_templates/blueprint_test_cfse_registration.xml"},

        {"name" : "CFtools-x86_64-6Serv",
        "template_url" : "https://qeblade40.rhq.lab.eng.bos.redhat.com/templates/Dev/rhel-x86_64-6Server-cf-tools.xml",
        "profile" : "small-x86_64",
        "blueprint" : "data/blueprint_templates/blueprint_test_cfse_registration.xml"},

        {"name" : "CFtools-x86_64-5Serv",
        "template_url" : "https://qeblade40.rhq.lab.eng.bos.redhat.com/templates/Dev/rhel-x86_64-5Server-cf-tools.xml",
        "profile" : "small-x86_64",
        "blueprint" : "data/blueprint_templates/blueprint_test_cfse_registration.xml"},

        {"name" : "CFtools-i386-5Serv",
        "template_url" : "https://qeblade40.rhq.lab.eng.bos.redhat.com/templates/Dev/rhel-i386-5Server-cf-tools.xml",
        "profile" : "small-i386",
        "blueprint" : "data/blueprint_templates/blueprint_test_cfse_registration.xml"},

        {"name" : "CFtools-i386-6Serv",
        "template_url" : "https://qeblade40.rhq.lab.eng.bos.redhat.com/templates/Dev/rhel-i386-6Server-cf-tools.xml",
        "profile" : "small-i386",
        "blueprint" : "data/blueprint_templates/blueprint_test_cfse_registration.xml"}

        ]

