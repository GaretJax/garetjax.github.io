<!-- 
.. title: Combining py.test and Selenium
.. slug: combining-pytest-and-selenium
.. date: 2014/05/08 21:13:56
.. tags: 
.. link: 
.. description: 
.. type: text
-->

Lore Per inceptos himenaeos. Morbi laoreet. Suspendisse potenti. Donec accumsan
porta felis.

Fusce tristique leo quis pede. Cras nibh. Sed eget est vitae tortor mollis
ullamcorper. Suspendisse placerat dolor a dui. Vestibulum condimentum dui et
elit. Pellentesque porttitor ipsum at ipsum. Nam massa. Duis lorem. Donec
porta. Proin ligula. Aenean nunc massa, dapibus quis, imperdiet id, commodo a,
lacus. Cras sit amet erat et nulla varius aliquet. Aliquam erat volutpat.
Praesent feugiat vehicula pede. Suspendisse pulvinar, orci in sollicitudin
venenatis, nibh libero hendrerit sem, eu tempor nisi felis et metus. Etiam
gravida sem ut mi. Integer volutpat, enim eu varius gravida, risus urna.

    #!python
    import pytest


    BROWSERS = {
        'firefox': DesiredCapabilities.FIREFOX,
        'chrome': DesiredCapabilities.CHROME,
    }

    BASE_URL = 'http://localhost:8000'

    WEBDRIVER_ENDPOINT = 'http://localhost:4444/wd/hub'


    class BaseUrlWrapper(webdriver.Remote):
        def __init__(self, base, *args, **kwargs):
            self._base_url = base
            super(HostMappedWrapper, self).__init__(*args, **kwargs)

        def get(self, url):
            url = urljoin(self._base_url, url)
            return super(HostMappedWrapper, self).get(url)


    @pytest.yield_fixture(params=BROWSERS.keys())
    def driver(request):
        driver = BaseUrlWrapper(
            base=BASE_URL,
            command_executor=WEBDRIVER_ENDPOINT,
            desired_capabilities=BROWSERS[request.param]
        )
        yield driver
        driver.quit()

Cras sit amet mauris. Curabitur a quam. Aliquam neque. Nam nunc nunc, lacinia
sed, varius quis, iaculis eget, ante. Nulla dictum justo eu lacus. Phasellus
sit amet quam. Nullam sodales. Cras non magna eu est consectetuer faucibus.
Donec tempor lobortis turpis. Sed tellus velit, ullamcorper ac, fringilla
vitae, sodales nec, purus. Morbi aliquet risus in mi.

Lore Vitae odio lobortis tristique. Donec vestibulum mattis lectus. Donec et
lorem.

Curabitur cursus volutpat neque. Proin posuere mauris ut ipsum. Praesent
scelerisque tortor a justo. Quisque consequat libero eu erat. In eros augue,
sollicitudin sed, tempus tincidunt, pulvinar a, lectus. Vestibulum ante ipsum
primis in faucibus orci.
