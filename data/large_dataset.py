#!/usr/bin/env python

# generated from generate_dataset.py
# based on list definitions in raw_data.py

        
class Admin(object):
    '''
    Define users and groups
    '''
    user_groups = [
        {"name" : "admin", 
        "description" : "This is the admin group."},
        {"name" : "development", 
        "description" : "This is the development group."},
        {"name" : "test", 
        "description" : "This is the test group."},
        {"name" : "production", 
        "description" : "This is the production group."}]

    users = [
        {"fname" : "John",
        "lname" : "Smith",
        "email" : "john.smith@redhat.com",
        "username" : "jsmith",
        "passwd" : ">bOM~WFDI;Omv2~WnJir",
        "max_instances" : "1",
        "user_groups" : ['production', 'admin', 'test'] },
        {"fname" : "Susan",
        "lname" : "Johnson",
        "email" : "susan.johnson@mozilla.org",
        "username" : "sjohnson",
        "passwd" : "Wz|ZH$Hh7Fi~L",
        "max_instances" : "8",
        "user_groups" : ['production', 'admin'] },
        {"fname" : "Ringo",
        "lname" : "Williams",
        "email" : "ringo.williams@mit.edu",
        "username" : "rwilliams",
        "passwd" : "jWi@@Yy",
        "max_instances" : "1",
        "user_groups" : ['admin', 'development', 'production'] },
        {"fname" : "Aaron",
        "lname" : "Jones",
        "email" : "aaron.jones@redhat.com",
        "username" : "ajones",
        "passwd" : "y#mj&y@(c1M",
        "max_instances" : "8",
        "user_groups" : ['development'] },
        {"fname" : "Mary",
        "lname" : "Brown",
        "email" : "mary.brown@mit.edu",
        "username" : "mbrown",
        "passwd" : "<m(.l%>9",
        "max_instances" : "8",
        "user_groups" : ['development', 'admin'] },
        {"fname" : "Nancy",
        "lname" : "David",
        "email" : "nancy.david@mozilla.org",
        "username" : "ndavid",
        "passwd" : "NYi0C",
        "max_instances" : "9",
        "user_groups" : ['development'] },
        {"fname" : "James",
        "lname" : "Miller",
        "email" : "james.miller@mozilla.org",
        "username" : "jmiller",
        "passwd" : "X2Z(!L6",
        "max_instances" : "5",
        "user_groups" : ['production', 'test', 'development'] },
        {"fname" : "John",
        "lname" : "Wilson",
        "email" : "john.wilson@mozilla.org",
        "username" : "jwilson",
        "passwd" : ".WB>&9@Q",
        "max_instances" : "3",
        "user_groups" : ['admin', 'development'] },
        {"fname" : "John",
        "lname" : "Moore",
        "email" : "john.moore@apache.org",
        "username" : "jmoore",
        "passwd" : "j)WQx,y~1W99,jRb$Ds",
        "max_instances" : "9",
        "user_groups" : ['production', 'admin'] },
        {"fname" : "James",
        "lname" : "Anderson",
        "email" : "james.anderson@mit.edu",
        "username" : "janderson",
        "passwd" : "(hXGw%",
        "max_instances" : "7",
        "user_groups" : ['admin', 'development'] },
        {"fname" : "John",
        "lname" : "Jackson",
        "email" : "john.jackson@apache.org",
        "username" : "jjackson",
        "passwd" : "*m2@UISJ(1!gX`",
        "max_instances" : "3",
        "user_groups" : ['admin', 'test'] },
        {"fname" : "Eric",
        "lname" : "White",
        "email" : "eric.white@redhat.com",
        "username" : "ewhite",
        "passwd" : "|^s>btq&",
        "max_instances" : "4",
        "user_groups" : ['admin'] },
        {"fname" : "Paul",
        "lname" : "Robinson",
        "email" : "paul.robinson@mozilla.org",
        "username" : "probinson",
        "passwd" : "oRBzXI8",
        "max_instances" : "9",
        "user_groups" : ['development', 'production', 'test'] },
        {"fname" : "Susan",
        "lname" : "King",
        "email" : "susan.king@apache.org",
        "username" : "sking",
        "passwd" : "c8r,ixih4HX.",
        "max_instances" : "10",
        "user_groups" : ['production'] },
        {"fname" : "Elizabeth",
        "lname" : "Lopez",
        "email" : "elizabeth.lopez@redhat.com",
        "username" : "elopez",
        "passwd" : "Gytnw0oM&o9N&6#<;Lw",
        "max_instances" : "5",
        "user_groups" : ['production'] }]

    selfservice_quota = "4"
        
class Provider(object):
    '''
    Define providers and provider accounts
    '''
    # provider_name string must match conductor
    # valid account types: "ec2", "rhevm", "vsphere"
    accounts = [
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
        "provider_account_quota" : "" }]
        
class Environment(object):
    '''
    Define environments and pools
    '''
    pool_family_environments = [
        {"name" : "IT",
        "max_running_instances" : "22",
        "enabled_provider_accounts" : ['vsphere']},
        {"name" : "CloudForms",
        "max_running_instances" : "18",
        "enabled_provider_accounts" : ['ec2-ap-northeast-1', 'ec2-sa-east-1', 'ec2-us-west-1', 'ec2-ap-southeast-1', 'ec2-sa-east-1', 'rhevm', 'ec2-us-west-2']},
        {"name" : "Support",
        "max_running_instances" : "15",
        "enabled_provider_accounts" : ['ec2-us-west-1', 'ec2-us-west-2', 'ec2-sa-east-1', 'ec2-eu-west-1', 'ec2-ap-northeast-1']},
        {"name" : "Operations",
        "max_running_instances" : "14",
        "enabled_provider_accounts" : ['ec2-eu-west-1', 'ec2-ap-northeast-1', 'rhevm', 'ec2-ap-southeast-1', 'ec2-sa-east-1']}]

    pools = [
        {"name" : "dev",
        "environment_parent" : ['Support', 'IT', 'CloudForms'],
        "quota" : "15",
        "enabled" : True},
        {"name" : "test",
        "environment_parent" : ['Operations', 'CloudForms', 'Support'],
        "quota" : "14",
        "enabled" : True},
        {"name" : "stage",
        "environment_parent" : ['CloudForms', 'IT', 'Support'],
        "quota" : "11",
        "enabled" : True},
        {"name" : "production",
        "environment_parent" : ['Support', 'CloudForms', 'IT'],
        "quota" : "8",
        "enabled" : True}]

class Content(object):
    '''
    Define catalogs, images and deployables
    '''
    catalogs = [
        {"name" : "IT",
        "pool_parent" : ['stage', 'test', 'production']},
        {"name" : "development",
        "pool_parent" : ['production', 'stage', 'dev']},
        {"name" : "web services",
        "pool_parent" : ['dev', 'production', 'stage']},
        {"name" : "engineering tools",
        "pool_parent" : ['test', 'stage', 'dev']},
        {"name" : "operations",
        "pool_parent" : ['dev', 'stage', 'production']}]

    images_from_url = [
        {"name" : "rhel6-x86_64",
        "template_url" : "https://qeblade40.rhq.lab.eng.bos.redhat.com/templates/Dev/rhel-x86_64-6Server-cf-tools.xml"},

        {"name" : "rhel5-x86_64",
        "template_url" : "https://qeblade40.rhq.lab.eng.bos.redhat.com/templates/Dev/rhel-x86_64-5Server-cf-tools.xml"},

        {"name" : "rhel5-i386",
        "template_url" : "https://qeblade40.rhq.lab.eng.bos.redhat.com/templates/Dev/rhel-i386-5Server-cf-tools.xml"}]
        
    deployables = [
        {"name" : "Katello_1.1",
        "hwp" : ['medium-x86_64'],
        "catalog" : ['engineering tools', 'development']},
        {"name" : "Aeolus_1.1",
        "hwp" : ['large-x86_64', 'small-x86_64'],
        "catalog" : ['engineering tools', 'web services', 'operations', 'development']},
        {"name" : "Wordpress",
        "hwp" : ['small-x86_64'],
        "catalog" : ['operations']},
        {"name" : "DNS Server",
        "hwp" : ['medium-x86_64', 'small-x86_64'],
        "catalog" : ['engineering tools']},
        {"name" : "CloudEngine_1.1",
        "hwp" : ['small-x86_64'],
        "catalog" : ['engineering tools', 'operations', 'development', 'web services']},
        {"name" : "SystemEngine_1.1",
        "hwp" : ['large-x86_64', 'small-x86_64'],
        "catalog" : ['web services', 'IT', 'development', 'operations']}]

