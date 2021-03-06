#!/usr/bin/env python
__author__ = [' Jan Alexander Slabiak (alex@tesobe.com)']
__license__ = """
    Copyright (C) 2011-2015, TESOBE / Music Pictures Ltd

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

    Email: contact@tesobe.com
    TESOBE / Music Pictures Ltd
    Osloerstrasse 16/17
    Berlin 13359, Germany
"""

__doc__ = """
Using Selenium RC2, install it with "pip install selenium"
need also =>selenium-2.0

This tool will take control of a local Firefox and download the CSV file from PB.
TMP is in the obp_config, this is important. Not every system has a /tmp (also related
to win32 systems)

I disabled the obp_logger, because the webdriver of selenium used it as well and printed
out sensible data. I wasn't able to control this behavior of selenium.
Have to find a fix for this!
J.A.S
"""


import os
import sys

from obp_config import TMP, TMP_CSV_SUFFIX
from libs.import_helper import show_here, check_for_clean_folder
from libs.debugger import debug
from selenium import webdriver
from debugger import obp_logger


postbank_main_url_login_page = " https://banking.postbank.de/rai/login"
postbank_main_url_value_page = "https://banking.postbank.de/rai/?wicket:bookmarkablePage=:de.postbank.ucp.application.rai.fs.umsatzauskunft.UmsatzauskunftPage"
postbank_main_url_value_download = "https://banking.postbank.de/rai/?wicket:interface=:3:umsatzauskunftpanel:panel:form:umsatzanzeigeGiro:umsatzaktionen:umsatzanzeigeUndFilterungDownloadlinksPanel:csvHerunterladen::IResourceListener::"


def get_csv_with_selenium(path_to_save_csv, username, password):
    """Getting CSV file via Firefox, controlled by Selenium webdriver"""
    # TODO: When no username and password is set, use the demo login.
    # Clean up the OBP temp folder (delete all csv files there).
    # LINK: http://seleniumhq.org/docs/03_webdriver.html#getting-started-with-selenium-webdriver
    obp_logger.info("Setting csv_folder...")

    # Check for existing and empty tmp
    check_for_clean_folder(path_to_save_csv)

    csv_save_path = os.path.join(os.getcwd(), path_to_save_csv, TMP_CSV_SUFFIX)
    obp_logger.debug("csv_folder is: %s" % csv_save_path)

    check_for_clean_folder(csv_save_path)

    obp_logger.info("Start Selenium")
    obp_logger.debug("csv_save_path: %s" % csv_save_path)
    obp_logger.debug("username is set")
    obp_logger.debug("password is set")

    # Setting up a Profile for Firefox.
    # Proxy is disabled and download files without asking.
    obp_logger.info("Setup Firefox Profile")
    fp = webdriver.FirefoxProfile()
    obp_logger.debug("webdriver firefox")
    fp.set_preference("network.proxy.type", 0)
    obp_logger.debug("network.proxy.type 0")
    fp.set_preference("browser.download.folderList", 2)
    obp_logger.debug("rowser.download.fold 2")
    fp.set_preference("browser.download.manager.showWhenStarting", False)
    obp_logger.debug("rowser.download.manager.showWhenStarting False ")
    fp.set_preference("browser.download.dir", csv_save_path)
    obp_logger.debug("browser.download.dir %s" % csv_save_path)

    # Need to set CSV to saveToDisk, else it's unknown to FF and it will ask for it
    fp.set_preference("browser.helperApps.neverAsk.saveToDisk", "text/csv")
    obp_logger.debug("browser.helperApps.neverAsk.saveToDisk text/csv")

    obp_logger.info("Start Firefox")
    browser = webdriver.Firefox(firefox_profile=fp)  # Get local session of firefox

    obp_logger.debug("Open URL: %s" % postbank_main_url_login_page)
    browser.get(postbank_main_url_login_page)  # Load page
    assert "Postbank Online-Banking" in browser.title

    #selenium.set_browser_log_level("error")

    # Here we will insert the username and password:
    # find the element that's name attribute is nutzername and kennwort
    obp_logger.info("Inserting Username and Password to Login")
    obp_logger.debug("searching for login box")
    inputElement_username = browser.find_element_by_name("nutzername")
    obp_logger.debug("searching for password box")
    inputElement_password = browser.find_element_by_name("kennwort")

    # send Username and Password
    obp_logger.debug("Inserting username into login box: %s " % username)
    inputElement_username.send_keys(username)
    obp_logger.debug("Inserting password into login box")
    inputElement_password.send_keys(password)

    # submit the Username and Password to Postbank.
    obp_logger.info("submitting login_data to login")
    inputElement_password.submit()

    # This opens the main page for accounts, and checks the name.
    # Call the Transaction Page
    obp_logger.debug("Open URL: %s" % postbank_main_url_value_page)
    browser.get(postbank_main_url_value_page)
    assert "Postbank Online-Banking" in browser.title

    # Call the CSV Link.
    # Warning!
    # The Postbank uses a :page counter, and when the URL doesn't have the right page counter it will return
    # an error message.
    obp_logger.debug("Open URL: %s" % postbank_main_url_value_download)
    result = browser.get(postbank_main_url_value_download)
    obp_logger.info("closing Firefox")
    browser.close()
    return csv_save_path


def main():
    obp_logger.info("Start main")
    check_for_clean_folder()
    get_csv_with_selenium(TMP)
    obp_logger.info("Done main")


if __name__ == '__main__':
    main()
