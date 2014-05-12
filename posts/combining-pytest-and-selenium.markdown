<!-- 
.. title: Combining py.test and Selenium
.. slug: combining-pytest-and-selenium
.. date: 2014/05/08 21:13:56
.. tags: selenium, py.test, testing
.. link: 
.. description: 
.. type: text
-->


I recently started using [py.test](http://pytest.org/) for the unit testing of
a couple of in-house projects. I particularly fell in love with their [concept
of fixtures](http://pytest.org/latest/fixture.html) and overall cleanliness of
the resulting test code, so wondered if I could use it alongside with
[Selenium](http://docs.seleniumhq.org/) for the functional testing part as
well.

Thanks to a custom fixture, the integration of these two libraries was
straightforward. The code below shows how to setup a `browser` fixture to
connect to a Selenium `Remote` driver for each test.

    #!python
    # conftest.py

    import pytest
    from selenium import webdriver


    BROWSERS = {
        'firefox': DesiredCapabilities.FIREFOX,
        'chrome': DesiredCapabilities.CHROME,
    }

    WEBDRIVER_ENDPOINT = 'http://localhost:4444/wd/hub'


    @pytest.yield_fixture(params=BROWSERS.keys())
    def browser(request):
        driver = webdriver.Remote(
            command_executor=WEBDRIVER_ENDPOINT,
            desired_capabilities=BROWSERS[request.param]
        )
        yield driver
        driver.quit()

Once familiar with the way `py.test` is organized, using this fixture comes
down to putting the above code in a file named `conftest.py` at the
[appropriate location](http://pytest.org/latest/plugins.html#conftest-py-local-per-directory-plugins)
and using the fixture from one or more test cases by declaring a test
function with a named `browser` argument:

    #!python
    # test_functional.py

    def test_python_org(browser):
        browser.get('http://python.org')
        assert 'Python' in browser.title


Bonus: DRY URLs
===============

As I found myself testing against a development instance of the web
application, I had plenty of calls to `browser.get(...)` with different
development URLs. These URLs, and particularly the `domain:port` portion change
depending on the environment you are testing against (dev, test, staging,...)
and I wanted an easy way to adapt my test code to it.

The solution I came up with consists in extending the [`webdriver.Remote`](http://selenium.googlecode.com/git/docs/api/py/webdriver_remote/selenium.webdriver.remote.webdriver.html#module-selenium.webdriver.remote.webdriver) class
and providing my own implementation of the `get` method, which joins the
provided URL with one defined at instantiation time by the calling code.

The resulting class and an example of its usage are shown in the next code
snippet.

    #!python
    import pytest
    from urlparse import
    from selenium import webdriver


    BROWSERS = {
        'firefox': DesiredCapabilities.FIREFOX,
        'chrome': DesiredCapabilities.CHROME,
    }

    WEBDRIVER_ENDPOINT = 'http://localhost:4444/wd/hub'

    BASE_URL = 'http://python.org'


    class BaseUrlWrapper(webdriver.Remote):
        def __init__(self, base, *args, **kwargs):
            self._base_url = base
            super(BaseUrlWrapper, self).__init__(*args, **kwargs)

        def get(self, url):
            url = urljoin(self._base_url, url)
            return super(HostMappedWrapper, self).get(url)


    @pytest.yield_fixture(params=BROWSERS.keys())
    def browser(request):
        driver = BaseUrlWrapper(
            base=BASE_URL,
            command_executor=WEBDRIVER_ENDPOINT,
            desired_capabilities=BROWSERS[request.param]
        )
        yield driver
        driver.quit()


    def test_homepage(browser):
        browser.get('/')
        assert 'Python' in browser.title


    def test_about(browser):
        browser.get('/about/')
        assert 'About Python' in browser.title


    def test_other(browser):
        # Absolute URLs still yield the expected result
        browser.get('https://www.ruby-lang.org/en/')
        pytest.fail("Ruby always fails!")


Possible optimizations
======================

The code presented above is not the most performant version, as a new instance
of each browser is spawned for each test and closed right after it.

An approach which could yield faster test execution times would be to open
each browser just [once per testing session](http://pytest.org/latest/example/simple.html?highlight=scope#package-directory-level-fixtures-setups)
and then just clear the browsing session each time. Some hints for such an
implementation can be found in the [Selenium API documentation](http://selenium.googlecode.com/git/docs/api/py/webdriver_remote/selenium.webdriver.remote.webdriver.html#selenium.webdriver.remote.webdriver.WebDriver.start_session).
Once I had the chance to try them out, I may write a follow-up post.
