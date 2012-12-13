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
        "permissions" : ['Global Cloud Resource Zone User'] },
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
        {"fname" : "Joe",
        "lname" : "User",
        "email" : "juser@example.com",
        "username" : "juser",
        "passwd" : "jpassword",
        "max_instances" : "20",
        "user_groups" : ['qe','cfmanagers'],
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
        "permissions" : [] },
        ]

    selfservice_quota = "10"

class Provider(object):
    '''
    Define providers and provider accounts
    '''
    # provider_name string must match conductor
    # valid account types: "ec2", "rhevm", "vsphere"
    accounts = [

        {"type" : "rhevm",
        "provider_name" : "rhevm-default",
        "provider_account_name" : "rhevm",
        "provider_account_priority" : "",
        "provider_account_quota" : "32" },

        {"type" : "vsphere",
        "provider_name" : "vsphere-default",
        "provider_account_name" : "vsphere",
        "provider_account_priority" : "",
        "provider_account_quota" : "32" },

        {"type" : "ec2",
        "provider_name" : "ec2-ap-northeast-1",
        "provider_account_name" : "ec2-ap-northeast-1",
        "provider_account_priority" : "",
        "provider_account_quota" : "32" },

        {"type" : "ec2",
        "provider_name" : "ec2-ap-southeast-1",
        "provider_account_name" : "ec2-ap-southeast-1",
        "provider_account_priority" : "",
        "provider_account_quota" : "32" },

        {"type" : "ec2",
        "provider_name" : "ec2-eu-west-1",
        "provider_account_name" : "ec2-eu-west-1",
        "provider_account_priority" : "",
        "provider_account_quota" : "32" },

        {"type" : "ec2",
        "provider_name" : "ec2-sa-east-1",
        "provider_account_name" : "ec2-sa-east-1",
        "provider_account_priority" : "",
        "provider_account_quota" : "32" },

        {"type" : "ec2",
        "provider_name" : "ec2-us-east-1",
        "provider_account_name" : "ec2-us-east-1",
        "provider_account_priority" : "",
        "provider_account_quota" : "32" },

        {"type" : "ec2",
        "provider_name" : "ec2-us-west-1",
        "provider_account_name" : "ec2-us-west-1",
        "provider_account_priority" : "",
        "provider_account_quota" : "32" },

        {"type" : "ec2",
        "provider_name" : "ec2-us-west-2",
        "provider_account_name" : "ec2-us-west-2",
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

    # Create a cluster for each provider
    cloud_resource_clusters = [
            dict(name=a['provider_name'],
                 description='Cluster %s' % a['provider_name'],
                 provider=a['provider_name']) for a in accounts]

class Environment(object):
    '''
    Define environments and pools
    '''
    clouds = [
        {"name" : "Private",
        "max_running_instances" : "24",
        "enabled_provider_accounts" : \
            [a['provider_account_name'] for a in Provider.accounts if a['type'] in ['rhevm','vsphere']]
            #[
            #    Provider.accounts[0]['provider_account_name'],
            #    Provider.accounts[1]['provider_account_name']
            #]
            },
        {"name" : "Public_EC2",
        "max_running_instances" : "24",
        "enabled_provider_accounts" : \
            [a['provider_account_name'] for a in Provider.accounts if a['type'] in ['ec2']]
            #[
            #    Provider.accounts[4]['provider_account_name'],
            #    Provider.accounts[6]['provider_account_name']
            #]
            }
        ]

    pools = [
        {"name" : "RHEV",
        "environment_parent" : clouds[0]['name'],
        "quota" : "10",
        "enabled" : True},
        {"name" : "vSphere",
        "environment_parent" : clouds[0]['name'],
        "quota" : "10",
        "enabled" : True},
        {"name" : "APAC-NE",
        "environment_parent" : clouds[1]['name'],
        "quota" : "10",
        "enabled" : True},
        {"name" : "APAC-SE",
        "environment_parent" : clouds[1]['name'],
        "quota" : "10",
        "enabled" : True},
        {"name" : "EU",
        "environment_parent" : clouds[1]['name'],
        "quota" : "10",
        "enabled" : True},
        {"name" : "SouthAmerica",
        "environment_parent" : clouds[1]['name'],
        "quota" : "10",
        "enabled" : True},
        {"name" : "US-East",
        "environment_parent" : clouds[1]['name'],
        "quota" : "10",
        "enabled" : True},
        {"name" : "US-West1",
        "environment_parent" : clouds[1]['name'],
        "quota" : "10",
        "enabled" : True},
        {"name" : "US-West2",
        "environment_parent" : clouds[1]['name'],
        "quota" : "10",
        "enabled" : True}

        ]

class Content(object):
    '''
    Define catalogs, images and deployables
    '''
    catalogs = [
        {"name" : "Private apps-RHEV",
        "pool_parent" : Environment.pools[0]['name'],
        "cloud_parent" : "Private",
        "resource_cluster" : Provider.cloud_resource_clusters[0]['name']},
        {"name" : "Private apps-vSphere",
        "pool_parent" : Environment.pools[1]['name'],
        "cloud_parent" : "Private",
        "resource_cluster" : Provider.cloud_resource_clusters[1]['name']},
        {"name" : "Public apps-APNE",
        "pool_parent" : Environment.pools[2]['name'],
        "cloud_parent" : "Public_EC2",
        "resource_cluster" : Provider.cloud_resource_clusters[2]['name']},
        {"name" : "Public apps-APSE",
        "pool_parent" : Environment.pools[3]['name'],
        "cloud_parent" : "Public_EC2",
        "resource_cluster" : Provider.cloud_resource_clusters[3]['name']},
        {"name" : "Public apps-EU",
        "pool_parent" : Environment.pools[4]['name'],
        "cloud_parent" : "Public_EC2",
        "resource_cluster" : Provider.cloud_resource_clusters[4]['name']},
        {"name" : "Public apps-SA",
        "pool_parent" : Environment.pools[5]['name'],
        "cloud_parent" : "Public_EC2",
        "resource_cluster" : Provider.cloud_resource_clusters[5]['name']},
        {"name" : "Public apps-US-East",
        "pool_parent" : Environment.pools[6]['name'],
        "cloud_parent" : "Public_EC2",
        "resource_cluster" : Provider.cloud_resource_clusters[6]['name']},
        {"name" : "Public apps-US-West1",
        "pool_parent" : Environment.pools[7]['name'],
        "cloud_parent" : "Public_EC2",
        "resource_cluster" : Provider.cloud_resource_clusters[7]['name']},
        {"name" : "Public apps-US-West2",
        "pool_parent" : Environment.pools[8]['name'],
        "cloud_parent" : "Public_EC2",
        "resource_cluster" : Provider.cloud_resource_clusters[8]['name']},
        ]

    configserver = {"name" : "ConfigServer",
        "template" : "rhel-x86_64-6Server-cf-configserver.xml",
        "version" : "0.4.11",
        "profile" : "small-x86_64"}

    images = [
        # RHEL-6Server
        {"name" : "rhel-i386-6Server",
        "template" : "rhel-i386-6Server-cf-tools.xml",
        "profile" : "small-i386"},

        {"name" : "rhel-x86_64-6Server",
        "template" : "rhel-x86_64-6Server-cf-tools.xml",
        "profile" : "small-x86_64"},

        # RHEL-6.3
        {"name" : "rhel-i386-6.3",
        "template" : "rhel-i386-6.3-cf-tools.xml",
        "profile" : "small-i386"},

        {"name" : "rhel-x86_64-6.3",
        "template" : "rhel-x86_64-6.3-cf-tools.xml",
        "profile" : "small-x86_64"},

        # RHEL-6.2
        {"name" : "rhel-i386-6.2",
        "template" : "rhel-i386-6.2-cf-tools.xml",
        "profile" : "small-i386"},

        {"name" : "rhel-x86_64-6.2",
        "template" : "rhel-x86_64-6.2-cf-tools.xml",
        "profile" : "small-x86_64"},

        # RHEL-5Server
        {"name" : "rhel-i386-5Server",
        "template" : "rhel-i386-5Server-cf-tools.xml",
        "profile" : "small-i386"},

        {"name" : "rhel-x86_64-5Server",
        "template" : "rhel-x86_64-5Server-cf-tools.xml",
        "profile" : "small-x86_64"},

        # RHEL-5.9
        {"name" : "rhel-i386-5.9",
        "template" : "rhel-i386-5.9-cf-tools.xml",
        "profile" : "small-i386"},

        {"name" : "rhel-x86_64-5.9",
        "template" : "rhel-x86_64-5.9-cf-tools.xml",
        "profile" : "small-x86_64"},

        # RHEL-5.8
        {"name" : "rhel-i386-5.8",
        "template" : "rhel-i386-5.8-cf-tools.xml",
        "profile" : "small-i386"},

        {"name" : "rhel-x86_64-5.8",
        "template" : "rhel-x86_64-5.8-cf-tools.xml",
        "profile" : "small-x86_64"},

        # RHEL-5.7
        {"name" : "rhel-i386-5.7",
        "template" : "rhel-i386-5.7-cf-tools.xml",
        "profile" : "small-i386"},

        {"name" : "rhel-x86_64-5.7",
        "template" : "rhel-x86_64-5.7-cf-tools.xml",
        "profile" : "small-x86_64"},

        ]


