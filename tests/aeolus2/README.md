# Order Of Aeolus Tests

Example command: 

    py.test --project=aeolus --driver=firefox --baseurl=https://FQDN/conductor -q tests/aeolus2/test_[filename].py

1. `-q test_users.py` (skip if in LDAP mode)
2. `-q test_environment.py`
3. `-q test_provider.py`
4. `-q test_content.py -k create_images`
5. `-q test_content.py -k build_images` (wait for build to complete)
6. `-q test_content.py -k create_blueprint`
7. `-q test_content.py -k push_images` (wait for push to complete)
8. `-q test_content.py -k launch_configserver`
9. Maually configure config server

        # if ec2 download key, chmod 400 key.pem
        # ssh [-i key.pem] config_server_url
        # `aeolus-configserver-setup`, 'y', default, copy values
        # nav to cloud provider account, enter values, confirm success

10. `-q test_content.py -k launch_apps` (test sleeps for 20 seconds to provide time to edit blueprint params)

*Note*: Comment out catalogs in `data/large_dataset.py` to isolate running to certain providers

## Known issues
* `tests/aeolus2/test_content.py` is _way_ too tightly coupled to `data/large_dataset.py`.
* RHEV-M requires app name of less than 50 characters

