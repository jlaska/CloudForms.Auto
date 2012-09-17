This is the automation testing framework for CloudForms, including SystemEngine, CloudEngine and upstream projects Katello, Aeolus and Headpin:  

* [Aeolus](http://aeolusproject.org/)
* [Katello](http://katello.org) Note: Headpin is a lite version of Katello

This test framework was originally written for Katello and headpin, and extended by the Red Hat CloudForms QE Integration team. Tests use Mozilla's [pytest-mozwebqa plugin](https://github.com/davehunt/pytest-mozwebqa).

## Documentation
Current documentation is [hosted here](http://eanxgeek.github.com/katello_challenge/index.html).

## Dependencies and Installation
* selenium webdriver or selenium server
* pytest==2.2.3
* pytest-xdist==1.6
* pytest-mozwebqa==0.7.1
* unittestzero

1. Clone this project and install dependencies. Dependencies may be installed by running `pip-python install -r ./requirements.txt` from the root of the project.
2. Edit `data/template_data.py` if desired.
3. Execute `./generate_dataset.py` to generate a semi-random dataset based on `data/template_data.py`.
4. Update `data/private_data.ini` file with private provider account details.
5. Run tests!

## Requirements
These tests assume a fresh install of the product(s) that are accessible from the machine running the tests.

## Executing Tests
There are two ways to run Selenium tests.

1. Use the Selenium WebDriver. Executing the tests with argument `--driver=firefox` allows for simple test runs. This is the method most commonly used during development.
2. Use the Selenium Server. Running a standalone Selenium Server supports test distribution on multiple hosts.

To start the Selenium Server for local testing:
`java -jar /path/to/your/selenium/selenium-X.Y.jar \`
`-firefoxProfileTemplate /path/to/ff_profile/.mozilla/firefox/[profile]/`

See [Selenium documentation](http://seleniumhq.org/docs/03_webdriver.html) for more details.

### Basic Usage
`py.test --driver=firefox --baseurl=https://<FQDN>/conductor|katello --project=[project] -q testdir/path/my_test_file.py`

### Options
* `--driver=firefox` Allows tests to be run without a separate Selenium server running.
* `--baseurl=...` FQDN of product under test. Include `/conductor` or `/katello`
* `--product=katello|aeolus|katello.cfse|aeolus.cfce` Specify product under test.
* `-q path/to/test_file.py` Point to dir to run all tests in dir, or single file
* `-k [test_keyword]` Test keyword to run specific tests.
* `-m <marker>` For running tests tagged with py.test markers.

See [py.test documentation](http://pytest.org/) for more information.

## Development Notes

### About the Files
`tests/` Test code goes here.  It's common to organize tests into project-specific sub-directories.  For example, katello tests reside in `tests/katello`.

`apps/__init__.py` Provides base objects for use inherited projects and convenience methods to initialize projects.  Setup methods to use throughout the page objects. By inheritance these methods are accessible in other page objects. It is important not to include locators or site specific functions in this file.  The functions in this file are common across our projects and don't change often.

`apps/locators.py` Base locator object inherited by project-specific locators.  It's rare to have locators that work across applications.  However, if any exist, they'll live here.

`apps/[project]/__init__.py` Project specific handlers.

`apps/[project]/locators.py` Project specific locators.

`pages/` Going away.  The pages/ heirarchy exists for historic purposes.  The apps/ heirarchy is intended to replace the need for pages.

`api/` API helper methods.

`api/[project]/api.py` Project-specific API helper methods.

`credentials.yaml` Not currently in use. Store the credentials to log into the site with. The mozwebqa plugin will parse this file and make the values available inside the tests.

`conftest.py` Specify custom command-line options.

`mozwebqa.cfg` The mozwebqa plugin will read the parameters in this file and automatically add them onto the py.test command line. It is handy for parameters that are constant like --browsername=firefox

`generate_dataset.py` Standalone script to generate semi-random data file. Data derived from lists in `data/template_data.py`.

`data/large_dataset.py` Dataset generated from `generate_dataset.py`.

`data/private_data.ini` Private cloud provider credentials. Update before running provider tests.

`data/manifests/` Content provider manifest.zip files.

`requirements.txt` Lists required packages. Running `sudo pip install -r requirements.txt` (Mac/Linux) will automatically download and install the packages in this file. We recommend 'pinning' the packages to a specific version, for example pytest==2.1.3. This decreases the chance that a change to py.test will affect your test suite.


### Interactive Test Development
Developing Selenium tests is tricky and requires some trial and error. Launching a whole test just to see if your last code edit works takes a long time. A quicker way is to use the interactive Python shell (or even better, [IPython](http://ipython.org/) for auto-complete) to start an interactive webdriver session.

    $ python
    >>> from selenium import webdriver
    >>> url = 'https://myUrl/aeolus'
    >>> driver = webdriver.Firefox()
    >>> driver.get(url)

A Firefox browser window should open to the URL. You can now interact with the new  browser window (login, nav to page you're working on, inspect elements). Then try a locator and see if it works.

    >>> driver.find_elements_by_css_selector('li#promotions')
    >>> [<selenium.webdriver.remote.webelement.WebElement at 0x1a42e50>] # valid

Once your selector code is valid you can add to your code and keep going!

