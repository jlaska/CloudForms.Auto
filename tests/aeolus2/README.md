# Order Of Aeolus Tests

Example command: 

    py.test --project=aeolus --driver=firefox --baseurl=https://FQDN/conductor -q tests/aeolus2/test_[filename].py

*Note*: Workflow assumes running configserver

1. `-q test_users.py` (skip if in LDAP mode)
2. `-q test_environment.py`
3. `-q test_provider.py`
4. `-q test_content.py`

*Note*: Comment out select clouds (build/push) or catalogs (launch) in `data/large_dataset.py` to isolate running to certain providers

## Known issues
* `tests/aeolus2/test_content.py` is _way_ too tightly coupled to `data/large_dataset.py`.
* RHEV-M requires app name of less than 50 characters

