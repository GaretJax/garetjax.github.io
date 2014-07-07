<!-- 
.. title: Throttling requests using Flask and Selenium
.. slug: throttling-requests-using-flask-and-selenium
.. date: 05/12/2014 03:56:44 PM UTC
.. tags: selenium, Flask, testing, python
.. link: 
.. description: 
.. type: text
-->

While using [py.test](http://pytest.org/) and
[Selenium](http://docs.seleniumhq.org/) on a recent project of mine, I needed
to test that a spinner appears to indicate that some content is loading.
As it is often the case when testing against a local server, the content is
loaded too rapidly for the application to trigger the visual loading hint, and
the tests kept failing.

To work around the issue, I artificially delayed the server-side response using
a value stored in a cookie. Simple but effective!


Talk is cheap. Show me the code.
================================

The implementation of this techique using [Flask](http://flask.pocoo.org/) and
`Selenium` takes just a handful of lines of code.
First of all, we define a Flask
[`before_request`](http://flask.pocoo.org/docs/api/#flask.Flask.before_request)
handler to throttle requests on the server when a certain cookie is set, as
shown in lines 9 to 14 in the following snippet:

    #!python
    # app.py

    import time
    from flask import Flask, request

    app = Flask(__name__)
    app.config['TESTING'] = True

    DELAY_COOKIE = 'delay'

    if app.config['TESTING']:
        @app.before_request
        def throttle():
            time.sleep(float(request.cookies.get(DELAY_COOKIE, 0)))

    @app.route('/')
    def hello_world():
        return 'Hello World!\n'

    if __name__ == '__main__':
        app.run()

If we start the application right now, we can already test this behavior
from the command line:

    :::bash
    python app.py

In a separate session, run the following two commands, once without setting
any cookies...

    :::bash
    time curl localhost:5000
    Hello World!
    curl localhost:5000  0.00s user 0.00s system 62% cpu 0.005 total

And once by setting a delay of 5 seconds:

    :::bash
    time curl --cookie delay=5 localhost:5000
    Hello World!
    curl --cookie delay=5 localhost:5000  0.00s user 0.00s system 0% cpu 5.013 total

As you can see from the total time, the throttling code is working properly.


A context manager for Selenium
==============================

We can take the whole concept a step further by applying it to `Selenium` tests
run through `py.test` (check
[my previous post](/posts/combining-pytest-and-selenium.html) for some advice
about integrating `Selenium` with `py.test`).
The following code introduces a context manager which takes care to set and
reset the `delay` cookie in the current browsing session and shows
an example of its usage:

    #!python

    import contextlib

    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.common.by import By


    DELAY_COOKIE = 'delay'


    @contextlib.contextmanager
    def delay_responses(browser, time, cookie_name=DELAY_COOKIE):
        """
        Context manager to set the delay cookie on the given browser session
        on entering and restore its previous value on exiting.
        """
        prev = browser.get_cookie(cookie_name)
        browser.add_cookie({'name': cookie_name, 'value': str(time)})
        yield
        if prev:
            browser.add_cookie({'name': cookie_name, 'value': prev})
        else:
            browser.delete_cookie(cookie_name)


    def test_spinner(browser):
        browser.get('/')

        # Trigger the action
        with delay_responses(browser, 3):
            browser.find_element_by_css_selector('button').click()

        # Check for spinner to appear
        WebDriverWait(browser, 1).until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, '.spinner')
        ))

That's it, happy (throttled) testing!
