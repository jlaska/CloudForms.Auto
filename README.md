This is the automation testing framework for CloudForms CloudEngine integration testing. There is limited support for SystemEngine and upstream projects Katello and Aeolus.

* [Aeolus](http://aeolusproject.org/)
* [Katello](http://katello.org)

This test framework was originally written for Katello and headpin, and extended by the Red Hat CloudForms QE Integration team. Tests use Mozilla's [pytest-mozwebqa plugin](https://github.com/davehunt/pytest-mozwebqa).

## Documentation
Documentation is [hosted here](http://eanxgeek.github.com/katello_challenge/index.html) but it is way out of date. We need someone generate documentation using Sphinx and host on Github. Contribute!

## Dependencies and Installation
* selenium webdriver or selenium server
* pytest==2.3.3
* pytest-xdist==1.8
* pytest-mozwebqa==1.0

1. Clone this project and install dependencies. Dependencies may be installed by running `pip install -r ./requirements.txt` from the root of the project.
2. Copy `cloudforms.template` to `cloudforms.cfg` and update as needed.
3. Copy `credentials.template` to `credentials.yml` and updated as needed.
6. Run tests from project root dir: `py.test`. Consult `py.test --help` for options.

The end-to-end test run assumes a fresh default install of the product(s) that are accessible from the machine running the tests.

## Commonly used options
* `--driver=firefox|chrome` Allows tests to be run without a separate Selenium server running.
* `--project=katello|aeolus|katello.cfse|aeolus.cfce` Specify project under test.
* `-q path/to/test_file.py` Point to dir to run all tests in dir, or single file
* `-k <test_keyword>` Test keyword to run specific tests.
* `-m <marker>` For running tests tagged with py.test markers.

Run `py.test --help` for help or refer to [py.test documentation](http://pytest.org/) for complete documentation.

## Different ways to run the tests
* End-to-end Aeolus workflow: `py.test -m "aeolus and not saucelabs"`
* If Aeolus is already set up with users, groups, clouds and providers, omit the setup tests to run complete setup of configserver(s) and apps: `py.test -m "aeolus and not setup"`
* To just launch apps run `py.test -m "aeolus and content"`
* To just verify apps are launched run `py.test -m "aeolus and verify"`
* For Saucelabs UI testing add your credentials to sauce_labs.yaml and run: `py.test -m saucelabs --browsername=iexplore|firefox|chrome --browserver=<version> --platform='WINDOWS [2003|2008|2012]'|'Linux' --saucelabs=sauce_labs.yaml`


## About the Files

`tests/` Test code goes here. These are typically simple calls to the more complex operations in `apps/`.

* `tests/conftest.py` Customize pytest for processing CloudForms.Auto tests. Includes provide custom pytest command-line arguments as well as adding pytest plugins and hooks.

`apps/`:

* `__init__.py` Provides base objects for use inherited projects and convenience methods to initialize projects.  Setup methods to use throughout the page objects. By inheritance these methods are accessible in other page objects. It is important not to include locators or site specific functions in this file.  The functions in this file are common across our projects and don't change often.

* `locators.py` Base locator object inherited by project-specific locators.  It's rare to have locators that work across applications.  However, if any exist they'll live here.

* `[project]/__init__.py` Project specific handlers.

* `[project]/locators.py` Project specific locators.

`api/` API helper methods.

* `[project]/api.py` Project-specific API helper methods.

`data/`:
* `dataset.py` Dataset that drives data-driven testing.

* `manifests/` Content provider manifest.zip files.


### Configuration
* `cloudforms.cfg` Main configuration file for product parameters and general preferences. This defines the test matrix as tests are run, looping through space-delimited lists.

* `credentials.yaml` Used to store aeolus provider credentials, and application usernames and passwords.

* `mozwebqa.cfg` (optional) The mozwebqa plugin will read the parameters in this file and automatically add them onto the py.test command line. It is handy for parameters that are constant like --browsername=firefox.

* `requirements.txt` Lists required packages. Running `sudo pip install -r requirements.txt` (Mac/Linux) will automatically download and install the packages in this file. We recommend 'pinning' the packages to a specific version, for example pytest==2.1.3. This decreases the chance that a change to py.test will affect your test suite.

* `sauce_labs.yaml` Your username, password and api-key for Saucelabs testing. If application resides on a private network you'll need to run the [Sauce Connect](https://saucelabs.com/docs/connect) tunnel.

## Working with Selenium
There are two ways to run Selenium tests.

1. Use the Selenium WebDriver. Executing the tests with argument `--driver=firefox` allows for simple test runs. This is the method most commonly used during development.
2. Use the Selenium Server. Running a standalone Selenium Server supports test distribution on multiple hosts.

To start the Selenium Server for local testing:
`java -jar /path/to/your/selenium/selenium-X.Y.jar \`
`-firefoxProfileTemplate /path/to/ff_profile/.mozilla/firefox/[profile]/`

See [Selenium webdriver documentation](http://seleniumhq.org/docs/03_webdriver.html) for more details.

