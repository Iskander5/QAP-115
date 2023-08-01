import pytest
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options


@pytest.fixture(scope='session')
def driver():
    service = ChromeService(executable_path=ChromeDriverManager().install())
    options = Options()
    driver = webdriver.Chrome(service=service, options=options)

    yield driver

    driver.quit()


