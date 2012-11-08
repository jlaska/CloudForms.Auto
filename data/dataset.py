# generated from generate_dataset.py
# based on list definitions in raw_data.py

class Admin(object):
    '''
    Define users and groups
    '''
    user_groups = [
        {"name" : "admin", 
        "description" : "Global admins. With great power comes great responsibility",
        "permissions" : ['Global Administrator'] },
        {"name" : "cfmanagers", 
        "description" : "Global admins. With great power comes great responsibility",
        "permissions" : ['Global Administrator'] },
        {"name" : "qe", 
        "description" : "real QE users",
        "permissions" : [] },
        {"name" : "cfusers", 
        "description" : "Limited privilege users",
        "permissions" : ['Global Cloud Resource Zone User'] }
        ]

    users = [
        {"fname" : "Auto",
        "lname" : "Roboto",
        "email" : "admin@redhat.com",
        "username" : "automation",
        "passwd" : "redhat",
        "max_instances" : "",
        "user_groups" : ['admin'],
        "permissions" : [] },
        {"fname" : "Aaron",
        "lname" : "Weitekamp",
        "email" : "aweiteka@redhat.com",
        "username" : "aweiteka-admin",
        "passwd" : "redhat",
        "max_instances" : "20",
        "user_groups" : ['qe','cfmanagers'],
        "permissions" : ['Global Administrator'] },
        {"fname" : "Aaron",
        "lname" : "Weitekamp",
        "email" : "aweiteka@redhat.com",
        "username" : "aweiteka-user",
        "passwd" : "redhat",
        "max_instances" : "20",
        "user_groups" : ['cfusers'],
        "permissions" : [] },
        {"fname" : "James",
        "lname" : "Laska",
        "email" : "jlaska@redhat.com",
        "username" : "jlaska",
        "passwd" : "redhat",
        "max_instances" : "20",
        "user_groups" : ['qe','cfmanagers'],
        "permissions" : [] },
        {"fname" : "Milan",
        "lname" : "Falenik",
        "email" : "mfalesni@redhat.com",
        "username" : "mfalesni",
        "passwd" : "redhat",
        "max_instances" : "20",
        "user_groups" : ['qe','cfmanagers'],
        "permissions" : [] },
        {"fname" : "Gabriel",
        "lname" : "Szasz",
        "email" : "gszasz@redhat.com",
        "username" : "gszasz",
        "passwd" : "redhat",
        "max_instances" : "20",
        "user_groups" : ['qe','cfmanagers'],
        "permissions" : [] }
        ]

    selfservice_quota = "10"
        
class Provider(object):
    '''
    Define providers and provider accounts
    '''
    # provider_name string must match conductor
    # valid account types: "ec2", "rhevm", "vsphere"
    accounts = [

        # TODO: support multiple ec2 accounts
        {"type" : "ec2",
        "provider_name" : "ec2-us-east-1",
        "provider_account_name" : "ec2",
        "username_access_key" : "",
        "password_secret_access_key" : "",
        "account_number" : "",
        "key_file" : "",
        "key_cert_file" : "",
        "provider_account_priority" : "",
        "provider_account_quota" : "32" },

        {"type" : "rhevm",
        "provider_name" : "rhevm-default",
        "provider_account_name" : "rhevm",
        "username_access_key" : "admin@internal",
        "password_secret_access_key" : "dog8code",
        "provider_account_priority" : "",
        "provider_account_quota" : "32" },

        {"type" : "vsphere",
        "provider_name" : "vsphere-default",
        "provider_account_name" : "vsphere",
        "username_access_key" : "Administrator",
        "password_secret_access_key" : "R3dhat!",
        "provider_account_priority" : "",
        "provider_account_quota" : "32" }
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
        "max_running_instances" : "24",
        "enabled_provider_accounts" : ['rhevm']},
        {"name" : "Test",
        "max_running_instances" : "24",
        "enabled_provider_accounts" : ['vsphere']},
        {"name" : "Production",
        "max_running_instances" : "24",
        "enabled_provider_accounts" : ['ec2']}
        ]

    pools = [
        {"name" : "CloudForms-dev",
        "environment_parent" : ['Dev'],
        "quota" : "10",
        "enabled" : True},
        {"name" : "CloudForms-test",
        "environment_parent" : ['Test'],
        "quota" : "10",
        "enabled" : True},
        {"name" : "CloudForms-prod",
        "environment_parent" : ['Production'],
        "quota" : "10",
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
        #{"name" : "ConfigServer",
        #"template" : "rhel-x86_64-6Server-cf-configserver.xml",
        #"profile" : "small-x86_64"},

        {"name" : "rhel-x86_64-6Server",
        "template" : "rhel-x86_64-6Server-cf-tools.xml",
        "profile" : "small-x86_64"},

        {"name" : "rhel-x86_64-5Serv",
        "template" : "rhel-x86_64-5Server-cf-tools.xml",
        "profile" : "small-x86_64"},

        {"name" : "rhel-i386-5Serv",
        "template" : "rhel-i386-5Server-cf-tools.xml",
        "profile" : "small-i386"},

        {"name" : "rhel-i386-6Serv",
        "template" : "rhel-i386-6Server-cf-tools.xml",
        "profile" : "small-i386"}

        ]

