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
        "description" : "Limited privilege users"}]

    users = [
        {"fname" : "Admin",
        "lname" : "Joe",
        "email" : "admin@redhat.com",
        "username" : "admin",
        "passwd" : "password",
        "max_instances" : "",
        "user_groups" : ['admin'] },
        {"fname" : "Aaron",
        "lname" : "Weitekamp",
        "email" : "aweiteka@redhat.com",
        "username" : "aweiteka-admin",
        "passwd" : "password",
        "max_instances" : "10",
        "user_groups" : ['admin,qe,cfadmins'] },
        {"fname" : "Aaron",
        "lname" : "Weitekamp",
        "email" : "aweiteka@redhat.com",
        "username" : "aweiteka-admin",
        "passwd" : "password",
        "max_instances" : "10",
        "user_groups" : ['admin,qe,cfadmins'] },
        {"fname" : "Aaron",
        "lname" : "Weitekamp",
        "email" : "aweiteka@redhat.com",
        "username" : "aweiteka-user",
        "passwd" : "password",
        "max_instances" : "10",
        "user_groups" : ['cfusers'] },
        {"fname" : "Linda",
        "lname" : "Smith",
        "email" : "linda.smith@redhat.com",
        "username" : "lsmith",
        "passwd" : "password",
        "max_instances" : "10",
        "user_groups" : ['test', 'admin'] },
        {"fname" : "John",
        "lname" : "Johnson",
        "email" : "john.johnson@apache.org",
        "username" : "jjohnson",
        "passwd" : "password",
        "max_instances" : "9",
        "user_groups" : ['development', 'test', 'admin'] },
        {"fname" : "Ringo",
        "lname" : "Williams",
        "email" : "ringo.williams@mit.edu",
        "username" : "rwilliams",
        "passwd" : "password",
        "max_instances" : "4",
        "user_groups" : ['production'] },
        {"fname" : "Elizabeth",
        "lname" : "Jones",
        "email" : "elizabeth.jones@apache.org",
        "username" : "ejones",
        "passwd" : "password",
        "max_instances" : "9",
        "user_groups" : ['development', 'admin'] },
        {"fname" : "Mary",
        "lname" : "Brown",
        "email" : "mary.brown@mit.edu",
        "username" : "mbrown",
        "passwd" : "KLyK~tD#U",
        "max_instances" : "7",
        "user_groups" : ['test', 'development'] },
        {"fname" : "John",
        "lname" : "David",
        "email" : "john.david@apache.org",
        "username" : "jdavid",
        "passwd" : "EJ9&LU",
        "max_instances" : "9",
        "user_groups" : ['test'] },
        {"fname" : "Paul",
        "lname" : "Miller",
        "email" : "paul.miller@mit.edu",
        "username" : "pmiller",
        "passwd" : "ptvq~v",
        "max_instances" : "3",
        "user_groups" : ['test', 'production', 'admin'] },
        {"fname" : "George",
        "lname" : "Wilson",
        "email" : "george.wilson@apache.org",
        "username" : "gwilson",
        "passwd" : "ER<|BlNZsT>*i5cj&KiS",
        "max_instances" : "9",
        "user_groups" : ['development'] },
        {"fname" : "Paul",
        "lname" : "Moore",
        "email" : "paul.moore@redhat.com",
        "username" : "pmoore",
        "passwd" : "8N,V%zLq%*",
        "max_instances" : "1",
        "user_groups" : ['development', 'test', 'admin'] },
        {"fname" : "Eric",
        "lname" : "Anderson",
        "email" : "eric.anderson@apache.org",
        "username" : "eanderson",
        "passwd" : "8iNg>loYjkJn~E",
        "max_instances" : "7",
        "user_groups" : ['production'] },
        {"fname" : "Nancy",
        "lname" : "Jackson",
        "email" : "nancy.jackson@redhat.com",
        "username" : "njackson",
        "passwd" : "$GAjY*stm",
        "max_instances" : "2",
        "user_groups" : ['admin'] },
        {"fname" : "Paul",
        "lname" : "White",
        "email" : "paul.white@redhat.com",
        "username" : "pwhite",
        "passwd" : "uhR5IKHLy9>b>hxNU",
        "max_instances" : "4",
        "user_groups" : ['test', 'development', 'admin'] },
        {"fname" : "Linda",
        "lname" : "Robinson",
        "email" : "linda.robinson@mozilla.org",
        "username" : "lrobinson",
        "passwd" : "cLYT;`Dr,R|1@m`S8)",
        "max_instances" : "7",
        "user_groups" : ['development', 'production'] },
        {"fname" : "Eric",
        "lname" : "King",
        "email" : "eric.king@redhat.com",
        "username" : "eking",
        "passwd" : "Ew,%4fY5nnw;",
        "max_instances" : "5",
        "user_groups" : ['production'] },
        {"fname" : "George",
        "lname" : "Lopez",
        "email" : "george.lopez@mozilla.org",
        "username" : "glopez",
        "passwd" : "Rm>N,1I",
        "max_instances" : "6",
        "user_groups" : ['production', 'test'] }]

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

        # unique account number required?
        #{"type" : "ec2",
        #"provider_name" : "ec2-eu-west-1",
        #"provider_account_name" : "Public cloud west",
        #"username_access_key" : "",
        #"password_secret_access_key" : "",
        #"account_number" : "",
        #"key_file" : "",
        #"key_cert_file" : "",
        #"provider_account_priority" : "",
        #"provider_account_quota" : "" },

        #{"type" : "ec2",
        #"provider_name" : "ec2-eu-west-1",
        #"provider_account_name" : "Public cloud EU",
        #"username_access_key" : "",
        #"password_secret_access_key" : "",
        #"account_number" : "",
        #"key_file" : "",
        #"key_cert_file" : "",
        #"provider_account_priority" : "",
        #"provider_account_quota" : "" },

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
        "max_running_instances" : "14",
        "enabled_provider_accounts" : ['rhevm', 'ec2-sa-east-1', 'ec2-ap-northeast-1', 'ec2-us-west-2', 'ec2-eu-west-1', 'ec2-ap-southeast-1', 'ec2-sa-east-1', 'ec2-us-west-1']},
        {"name" : "CloudForms",
        "max_running_instances" : "23",
        "enabled_provider_accounts" : ['ec2-us-west-2', 'ec2-eu-west-1', 'ec2-us-west-1', 'ec2-ap-northeast-1', 'ec2-sa-east-1', 'rhevm', 'vsphere', 'ec2-sa-east-1', 'ec2-ap-southeast-1']},
        {"name" : "Support",
        "max_running_instances" : "21",
        "enabled_provider_accounts" : ['ec2-eu-west-1', 'ec2-us-west-2', 'rhevm']},
        {"name" : "Operations",
        "max_running_instances" : "21",
        "enabled_provider_accounts" : ['ec2-sa-east-1']}]

    pools = [
        {"name" : "dev",
        "environment_parent" : ['CloudForms'],
        "quota" : "18",
        "enabled" : True},
        {"name" : "qe",
        "environment_parent" : ['Operations'],
        "quota" : "11",
        "enabled" : True},
        {"name" : "stage",
        "environment_parent" : ['IT'],
        "quota" : "17",
        "enabled" : True},
        {"name" : "production",
        "environment_parent" : ['Support'],
        "quota" : "9",
        "enabled" : True}]

class Content(object):
    '''
    Define catalogs, images and deployables
    '''
    catalogs = [
        {"name" : "IT",
        "pool_parent" : 'stage'},
        {"name" : "development",
        "pool_parent" : 'dev'},
        {"name" : "web services",
        "pool_parent" : 'production'},
        {"name" : "engineering tools",
        "pool_parent" : 'test'}]

    images = [

        {"name" : "rhel-x86_64-6Server-cf-se",
        "template_url" : "https://qeblade40.rhq.lab.eng.bos.redhat.com/templates/Dev/rhel-x86_64-6Server-cf-se-Library-export.xml",
        "apps" : ["CFSE on 6Server - x86_64", "CFSE-6x86_64-b", "CFSE-6x86_64-c"]},

        {"name" : "rhel-x86_64-6Server-cf-ce",
        "template_url" : "https://qeblade40.rhq.lab.eng.bos.redhat.com/templates/Dev/rhel-x86_64-6Server-cf-ce-Library-export.xml",
        "apps" : ["CFCE on 6Server - x86_64", "CFCE-6x86_64-b", "CFCE-6x86_64-c"]},

        {"name" : "rhel-x86_64-6Server-cf-configserver",
        "template_url" : "https://qeblade40.rhq.lab.eng.bos.redhat.com/templates/Dev/rhel-x86_64-6Server-cf-configserver-Library-export.xml",
        "apps" : ["ConfigServer on 6Server - x86_64", "ConfigServer-6x86_64-b", "ConcifServer-6x86_64-c"]},

        {"name" : "rhel-x86_64-6Server-cf-tools",
        "template_url" : "https://qeblade40.rhq.lab.eng.bos.redhat.com/templates/Dev/rhel-x86_64-6Server-cf-tools-Library-export.xml",
        "apps" : ["CF Tools on 6Server - x86_64", "CF-tools-6x86_64-b", "CF-tools-6x86_64-c"]},

        {"name" : "rhel-x86_64-5Server-cf-tools",
        "template_url" : "https://qeblade40.rhq.lab.eng.bos.redhat.com/templates/Dev/rhel-x86_64-5Server-cf-tools-Library-export.xml",
        "apps" : ["5Sever CF tools - x86_64", "CF-tools-5x86_64-b", "CF-tools-5x86_64-c"]},

        {"name" : "rhel-i386-5Server-cf-tools",
        "template_url" : "https://qeblade40.rhq.lab.eng.bos.redhat.com/templates/Dev/rhel-i386-5Server-cf-tools-Library-export.xml",
        "apps" : ["5Sever i386", "5Sever i386-b", "5Sever i386-c"]},

        {"name" : "rhel-i386-6Server-cf-tools",
        "template_url" : "https://qeblade40.rhq.lab.eng.bos.redhat.com/templates/Dev/rhel-i386-6Server-cf-tools-Library-export.xml",
        "apps" : ["6Sever i386", "6Sever i386-b", "6Sever i386-c"]}]
        
    apps = [
        {"name" : "Katello_1.1",
        "hwp" : ['small-x86_64'],
        "catalog" : ['web services', 'operations']},
        {"name" : "Aeolus_1.1",
        "hwp" : ['small-x86_64', 'large-x86_64'],
        "catalog" : ['operations', 'IT', 'engineering tools']},
        {"name" : "Wordpress",
        "hwp" : ['medium-x86_64', 'small-x86_64'],
        "catalog" : ['engineering tools', 'development', 'web services', 'operations']},
        {"name" : "DNS Server",
        "hwp" : ['small-x86_64'],
        "catalog" : ['operations']},
        {"name" : "CloudEngine_1.1",
        "hwp" : ['large-x86_64'],
        "catalog" : ['web services', 'engineering tools']},
        {"name" : "SystemEngine_1.1",
        "hwp" : ['medium-x86_64'],
        "catalog" : ['web services']}]

