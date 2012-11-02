# Order Of Aeolus Tests

Example command: 

    py.test tests/aeolus2/

*Note*: Workflow assumes running configserver

Tests are collected in correct order for complete workflow. Edit `tests/aeolus2/pytest.ini` for test control.

*Note*: Comment out select clouds (build/push) or catalogs (launch) in `data/large_dataset.py` to isolate running to certain providers

## Known issues
* `tests/aeolus2/test_content.py` is _way_ too tightly coupled to `data/large_dataset.py`.
* RHEV-M requires app name of less than 50 characters

