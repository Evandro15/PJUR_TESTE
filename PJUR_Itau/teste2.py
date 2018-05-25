from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import csv
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
import os

caminho_base = r"C:\Users\evand"
downloads = r"{0}\Downloads".format(caminho_base)

path = r"chromedriver.exe"
prefs = {"download.default_directory": downloads,
         "profile.default_content_setting_values.automatic_downloads": 1,
         "plugins.always_open_pdf_externally": True,
         "download.prompt_for_download": False,
         "profile.default_content_setting_values.notifications": 2,
         "profile.managed_default_content_settings.stylesheets": 2,
         # "profile.managed_default_content_settings.cookies": 2,
         "profile.managed_default_content_settings.javascript": 1,
         "profile.managed_default_content_settings.plugins": 1,
         "profile.managed_default_content_settings.popups": 2,
         "profile.managed_default_content_settings.geolocation": 2,
         "profile.managed_default_content_settings.media_stream": 2
         }
chromeOptions = webdriver.ChromeOptions()
chromeOptions.add_experimental_option("prefs", prefs)

chromeOptions.add_argument("--disable-web-security")
chromeOptions.add_argument("--allow-running-insecure-content")
chromeOptions.add_argument("--disable-extensions")
chromeOptions.add_argument("--disable-print-preview")

driver = webdriver.Chrome(executable_path=path,
                          chrome_options=chromeOptions)

driver.get("http://pdfy.net/convert-url-to-pdf.aspx")
WebDriverWait(driver, 5).until(EC.visibility_of_element_located(
    (By.ID, """mainContent_BtnCreatePdf""")))
with open(r"C:\Users\evand\Desktop\links.csv") as listaPjur:
    leitorCSV = csv.reader(listaPjur)

    for linha in leitorCSV:
        driver.find_element_by_xpath(
            """//*[@id="mainContent_TxtUrl"]""").clear()
        driver.find_element_by_xpath(
            """//*[@id="mainContent_TxtUrl"]""").send_keys(linha)
        driver.find_element_by_xpath(
            """//*[@id="mainContent_BtnCreatePdf"]""").click()
a = 1
