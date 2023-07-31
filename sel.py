from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.service import Service as FirefoxService
options = Options()
options.add_argument('-headless')
driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()),options=options)
driver.get()
source = driver.page_source
driver.quit()
